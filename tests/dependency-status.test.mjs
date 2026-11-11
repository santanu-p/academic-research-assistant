import test from 'node:test';
import assert from 'node:assert/strict';
import {handle} from '../server/mcp.mjs';

async function status(){
 const response=await handle({jsonrpc:'2.0',id:1,method:'tools/call',params:{name:'environment_status',arguments:{}}});
 assert.equal(response.result?.isError,false,JSON.stringify(response));
 return JSON.parse(response.result.content[0].text);
}
test('environment status reports dependency presence and unknown Python modules when no interpreter is on PATH',async()=>{
 const old=process.env.PATH;process.env.PATH='';
 try{
  const result=await status();
  assert.ok(result.commands, "dependency commands are reported");
  assert.equal(result.commands.node,false);
  assert.equal(result.python_probe.status,'unavailable');
  assert.equal(result.modules.json,null);
  assert.match(result.scope,/presence/i);
 }finally{if(old===undefined)delete process.env.PATH;else process.env.PATH=old;}
});
test('environment status reports actual local runtime metadata and Python module probe',async()=>{
 const result=await status();
 assert.ok(result.commands, 'dependency commands are reported');
 assert.equal(typeof result.commands.node,'boolean');
 if(result.python_probe.status==='ok')assert.equal(result.modules.json,true);
 else assert.ok(['unavailable','error'].includes(result.python_probe.status));
 assert.match(result.scope,/authentication/i);
});
