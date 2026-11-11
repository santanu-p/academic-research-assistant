"""Exercise all five tools through the real MCP stdio subprocess."""
from pathlib import Path
import json, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]
PACKAGE=ROOT/'academic-research-assistant'

def main():
    names=[('search_capabilities',{'query':'systematic review','limit':30}),
           ('route_task',{'task':'Plan a PRISMA systematic review'}),
           ('read_resource',{'path':'README.md','max_chars':200}),
           ('environment_status',{}),('verify_sources',{})]
    messages=[{'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-11-25','capabilities':{},'clientInfo':{'name':'release-smoke','version':'1'}}},
              {'jsonrpc':'2.0','method':'notifications/initialized'},
              {'jsonrpc':'2.0','id':2,'method':'tools/list'}]
    messages.extend({'jsonrpc':'2.0','id':i,'method':'tools/call','params':{'name':n,'arguments':a}} for i,(n,a) in enumerate(names,3))
    p=subprocess.run([sys.executable,'-X','utf8','-B','-u',str(PACKAGE/'server/assistant_server.py')],
                     input='\n'.join(json.dumps(m) for m in messages)+'\n',capture_output=True,text=True,encoding='utf-8',timeout=30)
    assert p.returncode==0,p.stderr
    rows=[json.loads(s) for s in p.stdout.splitlines()]
    assert len(rows)==7
    assert len(rows[1]['result']['tools'])==5
    values=[]
    for response,(name,_) in zip(rows[2:],names):
        assert not response['result'].get('isError'),response
        value=json.loads(response['result']['content'][0]['text'])
        values.append((name,value))
    assert values[-1][1]['verified']==273 and values[-1][1]['passed']
    assert 'evidence-systematic-review' in [s['name'] for s in values[1][1]['skills']]
    result={'passed':True,'transport':'actual stdio subprocess','protocol':'2025-11-25',
            'discovered_tools':[x['name'] for x in rows[1]['result']['tools']],
            'successful_calls':[name for name,_ in values],'source_preservation':values[-1][1],
            'external_services':values[3][1]['external_services'],'stderr':p.stderr,'exit_code':p.returncode}
    (PACKAGE/'audit/mcp-smoke.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
