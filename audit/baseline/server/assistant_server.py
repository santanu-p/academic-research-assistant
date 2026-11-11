"""Local read-only research collection MCP server; Python stdlib only.

No shell execution, network access, credential handling, or arbitrary file access.
The newline-delimited JSON-RPC transport implements the MCP methods advertised.
"""
from pathlib import Path, PurePosixPath
import hashlib
import importlib.util
import json
import math
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
PROTOCOLS = ['2025-06-18', '2025-11-25']

def load_json(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8'))

def tokens(value):
    return set(re.findall(r'[a-z0-9]+', value.lower()))

def bounded_int(value, minimum, maximum, label):
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(f'{label} must be an integer from {minimum} to {maximum}')
    return value

def text_arg(value, label, maximum=10000):
    if not isinstance(value, str) or not value.strip() or len(value)>maximum:
        raise ValueError(f'{label} must be a nonblank string of at most {maximum} characters')
    return value

def search_capabilities(query, limit=12):
    query=text_arg(query,'query')
    limit=bounded_int(limit,1,117,'limit')
    qt=tokens(query)
    ranked=[]
    for s in load_json('catalog/skills.json'):
        nt=tokens(s['name'])
        dt=tokens(s['description'])
        score=4*len(qt & nt)+len(qt & dt)
        if query.casefold()==s['name'].casefold():
            score+=100
        if query.lower() in s['name'] or query.lower() in s['description'].lower():
            score+=5
        if score:
            ranked.append((score,s))
    ranked.sort(key=lambda x:(-x[0],x[1]['name']))
    return [dict(name=s['name'],path=s['path'],description=s['description'],family=s['family'],score=n) for n,s in ranked[:limit]]

def route_task(task):
    task=text_arg(task,'task')
    lower=task.lower()
    matches=[]
    for i,r in enumerate(load_json('catalog/routes.json')):
        hits=[term for term in r['terms'] if re.search(r'(?<!\w)'+re.escape(term)+r'(?!\w)',lower)]
        if hits:
            # Specific multiword intent outranks broad single-word overlap.
            score=sum(len(t.split())*3 for t in hits)+max(len(t) for t in hits)/100
            matches.append((score,i,r))
    matches.sort(key=lambda x:(-x[0],x[1]))
    byname={s['name']:s for s in load_json('catalog/skills.json')}
    names=[]
    for _,_,r in matches:
        for name in r['skills']:
            if name not in names:
                names.append(name)
    if not names:
        names=[x['name'] for x in search_capabilities(task)]
    return {'task':task,'routes':[r['id'] for _,_,r in matches],
            'skills':[{k:byname[n][k] for k in ['name','path','description','family']} for n in names[:20]],
            'requires_reading_skill':True,
            'fallback':'Read skills/research-assistant/SKILL.md and catalog/skills.json if no route matches.',
            'contract':'docs/INTEGRATION.md',
            'execution_status':'Routing guidance only; no research or external tool has been executed.'}

def contained_path(root, relative):
    text_arg(relative,'path',1000)
    # Use portable separators and reject drive/UNC syntax on every host.
    rel=PurePosixPath(relative.replace('\\','/'))
    if rel.is_absolute() or '..' in rel.parts or ':' in relative:
        raise ValueError('path must stay inside the plugin package')
    target=(root/Path(*rel.parts)).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError('path escapes the plugin package')
    return target

def read_resource(path, offset=0, max_chars=16000):
    offset=bounded_int(offset,0,10000000,'offset')
    max_chars=bounded_int(max_chars,1,64000,'max_chars')
    target=contained_path(ROOT,path)
    if not target.is_file():
        raise ValueError('resource does not exist or is not a file')
    if target.stat().st_size>8*1024*1024:
        raise ValueError('resource exceeds the text reader size limit; use host file tools')
    try:
        value=target.read_text(encoding='utf-8-sig')
    except UnicodeError:
        raise ValueError('binary resource: use the host PDF/image/archive tools') from None
    if '\x00' in value:
        raise ValueError('binary resource: use the host file tools')
    return {'path':target.relative_to(ROOT).as_posix(),'text':value[offset:offset+max_chars],
            'total_chars':len(value),'next_offset':offset+max_chars if offset+max_chars<len(value) else None}

def verify_entries(base, entries):
    report={'verified':0,'directories_verified':0,'missing':[],'mismatched':[]}
    for e in entries:
        p=contained_path(base,e['destination'])
        if e.get('kind')=='directory':
            if p.is_dir():
                report['directories_verified']+=1
            else:
                report['missing'].append(e['destination'])
        elif not p.is_file():
            report['missing'].append(e['destination'])
        elif hashlib.sha256(p.read_bytes()).hexdigest()!=e['sha256']:
            report['mismatched'].append(e['destination'])
        else:
            report['verified']+=1
    report['passed']=not report['missing'] and not report['mismatched']
    return report

def verify_sources():
    return verify_entries(ROOT,load_json('audit/source-map.json'))

def environment_status():
    modules=['numpy','scipy','pandas','matplotlib','sklearn','PIL','fitz','pptx','yaml','jsonschema']
    commands=['latexmk','pdflatex','xelatex','lualatex','tectonic','biber','pandoc','soffice','pdftoppm','latexdiff','bash','claude','codex','node','Rscript']
    return {'python':sys.version.split()[0], 'python_executable':sys.executable,
            'modules':{name:importlib.util.find_spec(name) is not None for name in modules},
            'commands':{name:shutil.which(name) is not None for name in commands},
            'external_services':'not_configured_by_this_plugin',
            'limits':'Presence checks only; no imports, authentication, API requests or program execution.',
            'setup':'docs/DEPENDENCIES.md'}

def tool_schema(name, description, properties=None, required=None):
    return {'name':name,'description':description,'inputSchema':{'type':'object','properties':properties or {},
            'required':required or [],'additionalProperties':False},
            'annotations':{'readOnlyHint':True,'destructiveHint':False,'openWorldHint':False}}

TOOLS=[
 tool_schema('search_capabilities','Search all 117 integrated source skills, preserving overlapping capabilities.',
             {'query':{'type':'string','minLength':1},'limit':{'type':'integer','minimum':1,'maximum':117}},['query']),
 tool_schema('route_task','Select relevant research workflows and exact skill files; does not execute the task.',
             {'task':{'type':'string','minLength':1}},['task']),
 tool_schema('read_resource','Read contained UTF-8 plugin instructions, templates, source metadata or datasets with pagination.',
             {'path':{'type':'string'},'offset':{'type':'integer','minimum':0},'max_chars':{'type':'integer','minimum':1,'maximum':64000}},['path']),
 tool_schema('environment_status','Check optional runtime module and executable presence; never claims service connection.'),
 tool_schema('verify_sources','Verify every original and expanded file against its recorded SHA-256 and every mapped directory.'),
]
FUNCTIONS={f.__name__:f for f in [search_capabilities,route_task,read_resource,environment_status,verify_sources]}

def handle(request):
    if not isinstance(request,dict) or request.get('jsonrpc')!='2.0' or not isinstance(request.get('method'),str):
        candidate=request.get('id') if isinstance(request,dict) else None
        return {'jsonrpc':'2.0','id':candidate if type(candidate) in [str,int] else None,'error':{'code':-32600,'message':'Invalid Request'}}
    # MCP notifications never receive responses.
    if 'id' not in request:
        return None
    rid=request['id']
    if type(rid) not in [str,int]:
        return {'jsonrpc':'2.0','id':None,'error':{'code':-32600,'message':'Invalid request identifier'}}
    method=request['method']
    params=request.get('params',{})
    if not isinstance(params,dict):
        return {'jsonrpc':'2.0','id':rid,'error':{'code':-32602,'message':'params must be an object'}}
    if method=='initialize':
        requested=params.get('protocolVersion')
        result={'protocolVersion':requested if requested in PROTOCOLS else PROTOCOLS[-1],
                'capabilities':{'tools':{'listChanged':False}},
                'serverInfo':{'name':'academic-research-local','version':'1.0.0'},
                'instructions':'Read skills/research-assistant/SKILL.md, then route the task and read selected skills. External services are not configured.'}
    elif method=='ping':
        result={}
    elif method=='tools/list':
        result={'tools':TOOLS}
    elif method=='tools/call':
        name=params.get('name')
        arguments=params.get('arguments',{})
        if not isinstance(name,str) or name not in FUNCTIONS or not isinstance(arguments,dict):
            return {'jsonrpc':'2.0','id':rid,'error':{'code':-32602,'message':'Unknown tool or malformed tool call'}}
        try:
            value=FUNCTIONS[name](**arguments)
            result={'content':[{'type':'text','text':json.dumps(value,ensure_ascii=False,allow_nan=False)}],'isError':False}
        except (ValueError,TypeError,OSError,KeyError) as e:
            result={'content':[{'type':'text','text':str(e)}],'isError':True}
    else:
        return {'jsonrpc':'2.0','id':rid,'error':{'code':-32601,'message':'Method not found'}}
    return {'jsonrpc':'2.0','id':rid,'result':result}

def main():
    for raw in sys.stdin.buffer:
        try:
            if len(raw)>1024*1024:
                raise ValueError('message exceeds 1 MiB')
            request=json.loads(raw.decode('utf-8'))
            response=handle(request)
        except (ValueError,UnicodeError):
            response={'jsonrpc':'2.0','id':None,'error':{'code':-32700,'message':'Parse error'}}
        if response is not None:
            sys.stdout.buffer.write((json.dumps(response,ensure_ascii=False,allow_nan=False)+'\n').encode('utf-8'))
            sys.stdout.buffer.flush()

if __name__=='__main__':
    main()
