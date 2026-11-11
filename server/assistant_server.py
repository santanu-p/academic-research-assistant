"""Local read-only research collection MCP server; Python stdlib only.

No shell execution, network access, credential handling, or arbitrary file access.
The newline-delimited JSON-RPC transport implements the MCP methods advertised.
"""
from pathlib import Path, PurePosixPath
import hashlib
import importlib.util
import json
import math
import os
import re
import shutil
import sys

def filesystem_root(root):
    """Use extended-length Windows paths for filesystem operations."""
    if sys.platform != 'win32':
        return Path(root)
    path = os.path.abspath(root)
    if path.startswith('\\\\?\\'):
        return Path(path)
    if path.startswith('\\\\'):
        return Path('\\\\?\\UNC\\' + path[2:])
    return Path('\\\\?\\' + path)


ROOT = filesystem_root(Path(__file__).parent.parent).resolve()
PROTOCOLS = ['2025-06-18', '2025-11-25']
RUNTIME_DIRS = {'cli','lib','server','skills','catalog','docs','tools','workflows','examples',
                'resources','licenses','agents','audit','dev','.codex-plugin','.claude-plugin'}
RUNTIME_FILES = {'package.json','plugin.json','mcp.json','.mcp.json','SKILL.md','README.md','LICENSE',
                 'THIRD_PARTY_NOTICES.md','CHANGELOG.md','requirements-optional.txt'}
EXCLUDED_PARTS = {'.git','node_modules','__pycache__','.private-archive','.public-build','dist'}
NPM_NORMALIZED_FILES = {'resources/upstream/academic-humanizer-main/.gitignore',
                        'skills/academic-humanizer/.gitignore'}

def load_json(path):
    return json.loads((filesystem_root(ROOT)/path).read_text(encoding='utf-8'))

STOP = set('a an and are as at be by can do for from help how i in into is it me my of on or our that the these this to use using we what when which with you your'.split())

def tokens(value):
    return {word for word in re.findall(r'[a-z0-9]+', value.lower()) if len(word)>1 and word not in STOP}

def bounded_int(value, minimum, maximum, label):
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(f'{label} must be an integer from {minimum} to {maximum}')
    return value

def text_arg(value, label, maximum=10000):
    if not isinstance(value, str) or not value.strip() or len(value)>maximum:
        raise ValueError(f'{label} must be a nonblank string of at most {maximum} characters')
    return value

def search_capabilities(query, limit=12):
    query=text_arg(query,'query').strip()
    limit=bounded_int(limit,1,250,'limit')
    entries=load_json('catalog/skills.json')
    aliases=load_json('catalog/aliases.json')
    key=re.sub(r'^[$/]', '', query).lower()
    exact=next((s for s in entries if s['name']==aliases.get(key,key)),None)
    if exact:
        return [exact]
    qt=tokens(query)
    ranked=[]
    for s in entries:
        nt=tokens(s['name'])
        dt=tokens(s['description'])
        score=4*len(qt & nt)+len(qt & dt)
        score+=sum(8 for term in s.get('keywords',[]) if len(term)>3 and term.lower() in query.lower())
        if score:
            ranked.append((score,s))
    ranked.sort(key=lambda x:(-x[0],x[1]['name']))
    return [s for _,s in ranked[:limit]]

def route_task(task):
    task=text_arg(task,'task').strip()
    entries=load_json('catalog/skills.json')
    byname={s['name']:s for s in entries}
    aliases=load_json('catalog/aliases.json')
    key=re.sub(r'^[$/]', '', task).lower()
    exact=byname.get(aliases.get(key,key))
    rules=load_json('catalog/routes.json')
    def matching_rules(segments):
        matches=[]
        for rule in rules:
            matched=lambda pattern: any(re.search(pattern,s,re.I) for s in segments)
            excluded=any(matched(p) for p in rule['unless_any'])
            # These exclusions use an explicit negative constraint as a mode signal.
            if (rule['id'] in ('evidence-find-studies-2','evidence-evidence-answer-34')
                    and re.search(r"\b(?:do\s+not|don['\u2019]t|never)\s+search\b",task,re.I)):
                excluded=True
            if (any(matched(p) for p in rule['when_any']) and
                    all(matched(p) for p in rule['when_all']) and not excluded):
                matches.append(rule)
        return sorted(matches,key=lambda r:(-r['priority'],r['id']))

    matches=matching_rules([task])
    clauses=list(re.finditer(
        r"\b(?:do\s+not|don['\u2019]t|never|not\s+a)\b"
        r"(?:(?![.,;:!?\n]|\b(?:but|instead|however|rather|yet)\b).)*",
        task,re.I))
    clarify_negation=False
    if clauses and not exact:
        affirmative=[]
        cursor=0
        for clause in clauses:
            affirmative.append(task[cursor:clause.start()])
            cursor=clause.end()
        affirmative.append(task[cursor:])
        affirmative_matches=matching_rules(affirmative)
        raw_winner=matches[0] if matches else None
        affirmative_winner=affirmative_matches[0] if affirmative_matches else None
        competing_rules=[r for r in matches if r['priority']==raw_winner['priority']]
        negated_trigger=any(
            re.search(pattern,clause.group(),re.I)
            for rule in competing_rules for clause in clauses for pattern in rule['when_any'])
        action_clauses=[clause.group() for clause in clauses if re.match(
            r"\b(?:do\s+not|don['\u2019]t|never)\s+(?:create|use|generate|write|make|produce)\b",
            clause.group(),re.I)]
        selected_names=[aliases.get(name,name) for rule in competing_rules for name in rule['support']]
        negated_support=any(
            aliases.get(rule['primary'],rule['primary']) in selected_names
            and any(re.search(pattern,clause,re.I)
                    for clause in action_clauses for pattern in rule['when_any'])
            for rule in rules)
        clarify_negation=(not affirmative_winner or raw_winner != affirmative_winner
                          or negated_trigger or negated_support)
        if clarify_negation:
            matches=[]
    if exact:
        names=[exact['name']]
        selection='legacy-alias' if key in aliases else 'explicit-name'
    elif clarify_negation:
        names=['research-assistant']
        selection='clarify'
    elif re.fullmatch(r'(help|capabilities|onboarding|what can academic research assistant do)[?.!]*',task,re.I):
        names=['research-assistant']
        selection='onboarding'
    elif matches:
        names=[matches[0]['primary'],*matches[0]['support']]
        selection='rules'
    else:
        names=[s['name'] for s in search_capabilities(task,5)]
        selection='candidates' if names else 'clarify'
    if not names:
        names=['research-assistant']
    names=list(dict.fromkeys(aliases.get(name,name) for name in names))
    competing=[aliases.get(r['primary'],r['primary']) for r in matches if r['priority']==matches[0]['priority']]
    annotation_overlap=(not exact and re.search(r'annotated bibliograph|word annotations?|annotations?.{0,35}(sources?|papers?|methods)',task,re.I)
        and not re.search(r'synthesis matrix|thematic review|verified.{0,20}(reference|citation) fields|verified bibliography|gather.{0,25}fields|slides?|deck',task,re.I))
    if annotation_overlap and names[0] in ('scholar-literature-review','evidence-citations-and-references'):
        competing.extend(['scholar-literature-review','evidence-citations-and-references'])
    competing=list(dict.fromkeys(competing))
    return {'task':task,'routes':[r['id'] for r in matches],
            'skills':[byname[name] for name in names if name in byname],
            'selection':selection,'matched_rule':matches[0]['id'] if matches else None,
            'needs_clarification':selection in ('candidates','clarify') or (not exact and len(competing)>1),
            'alternatives':[name for name in competing if name!=names[0]],
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
    root=filesystem_root(root).resolve()
    target=(root/Path(*rel.parts)).resolve()
    if not target.is_relative_to(root):
        raise ValueError('path escapes the plugin package')
    return target

def read_resource(path, offset=0, max_chars=16000):
    offset=bounded_int(offset,0,10000000,'offset')
    max_chars=bounded_int(max_chars,1,64000,'max_chars')
    text_arg(path,'path',1000)
    rel=PurePosixPath(path.replace('\\','/'))
    parts=rel.parts
    # Windows treats path components as case-insensitive and strips trailing
    # dots and spaces, including when opening paths through their aliases.
    normalized=[part.rstrip('. ').casefold() for part in parts]
    if (not parts or (parts[0] not in RUNTIME_DIRS and not (len(parts)==1 and parts[0] in RUNTIME_FILES))
            or any(part in EXCLUDED_PARTS or part.startswith('.test-') or part.endswith('.pyc') for part in normalized)
            or '/'.join(normalized) in NPM_NORMALIZED_FILES):
        raise ValueError('path is not a public runtime resource')
    root=filesystem_root(ROOT).resolve()
    current=root
    for part in parts:
        current=current/part
        if current.is_symlink() or getattr(current,'is_junction',lambda:False)():
            raise ValueError('public runtime resource cannot contain symbolic links')
    target=contained_path(root,path)
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
    return {'path':target.relative_to(root).as_posix(),'text':value[offset:offset+max_chars],
            'total_chars':len(value),'next_offset':offset+max_chars if offset+max_chars<len(value) else None}

def verify_entries(base, entries):
    report={'verified':0,'directories_verified':0,'missing':[],'mismatched':[]}
    for e in entries:
        destination=e.get('preserved_at',e.get('destination'))
        p=contained_path(base,destination)
        if e.get('kind')=='directory':
            if p.is_dir():
                report['directories_verified']+=1
            else:
                report['missing'].append(destination)
        elif not p.is_file():
            report['missing'].append(destination)
        elif hashlib.sha256(p.read_bytes()).hexdigest()!=e['sha256']:
            report['mismatched'].append(destination)
        else:
            report['verified']+=1
    report['passed']=not report['missing'] and not report['mismatched']
    return report

def verify_sources():
    report=verify_entries(ROOT,load_json('audit/review-118/file-mapping.json'))
    report['scope']='Recorded original payloads only; not a publisher signature or research validation.'
    return report

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
 tool_schema('search_capabilities','Search the canonical research methods and compatibility aliases.',
             {'query':{'type':'string','minLength':1},'limit':{'type':'integer','minimum':1,'maximum':250}},['query']),
 tool_schema('route_task','Select relevant research workflows and exact skill files; does not execute the task.',
             {'task':{'type':'string','minLength':1}},['task']),
 tool_schema('read_resource','Read contained UTF-8 plugin instructions, templates, source metadata or datasets with pagination.',
             {'path':{'type':'string'},'offset':{'type':'integer','minimum':0},'max_chars':{'type':'integer','minimum':1,'maximum':64000}},['path']),
 tool_schema('environment_status','Check optional runtime module and executable presence; never claims service connection.'),
 tool_schema('verify_sources','Verify recorded original payloads against their reviewed SHA-256 mapping.'),
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
                'serverInfo':{'name':'academic-research-local','version':load_json('package.json')['version']},
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
    maximum=1024*1024
    while True:
        raw=sys.stdin.buffer.readline(maximum+2)
        if not raw:
            break
        length=len(raw)-(1 if raw.endswith(b'\n') else 0)
        if length>maximum:
            while raw and not raw.endswith(b'\n'):
                raw=sys.stdin.buffer.readline(65536)
            response={'jsonrpc':'2.0','id':None,'error':{'code':-32600,'message':'Message exceeds 1 MiB'}}
            sys.stdout.buffer.write((json.dumps(response,ensure_ascii=True,allow_nan=False)+'\n').encode('utf-8'))
            sys.stdout.buffer.flush()
            continue
        try:
            request=json.loads(raw.decode('utf-8'))
            response=handle(request)
        except (ValueError,UnicodeError,RecursionError):
            response={'jsonrpc':'2.0','id':None,'error':{'code':-32700,'message':'Parse error'}}
        if response is not None:
            sys.stdout.buffer.write((json.dumps(response,ensure_ascii=True,allow_nan=False)+'\n').encode('utf-8'))
            sys.stdout.buffer.flush()

if __name__=='__main__':
    main()
