import {test} from 'node:test';
import assert from 'node:assert/strict';
import {handle,serve} from '../server/mcp.mjs';
import {Readable,Writable} from 'node:stream';
test('reject invalid identifiers, null arguments and null params',async()=>{
 for(const id of [null,true,1.5])assert.equal((await handle({jsonrpc:'2.0',id,method:'ping'})).error.code,-32600);
 assert.equal((await handle({jsonrpc:'2.0',id:1,method:'ping',params:null})).error.code,-32602);
 assert.equal((await handle({jsonrpc:'2.0',id:2,method:'tools/call',params:{name:'environment_status',arguments:null}})).error.code,-32602);
});
test('oversize message is bounded and next message still works',async()=>{
 const messages='x'.repeat(1024*1024+1)+'\n'+JSON.stringify({jsonrpc:'2.0',id:2,method:'ping'})+'\n';
 let output='';const sink=new Writable({write(chunk,encoding,done){output+=chunk.toString();done();}});
 await serve(Readable.from([messages.slice(0,5000),messages.slice(5000)]),sink);
 const rows=output.trim().split('\n').map(JSON.parse);
 assert.equal(rows[0].error.code,-32600);assert.deepEqual(rows[1],{jsonrpc:'2.0',id:2,result:{}});
});
test('resource reads paginate without exposing developer files',async()=>{
 const request=(args,id)=>handle({jsonrpc:'2.0',id,method:'tools/call',params:{name:'read_resource',arguments:args}});
 const first=JSON.parse((await request({path:'README.md',max_chars:10},1)).result.content[0].text);
 const next=JSON.parse((await request({path:'README.md',offset:first.next_offset,max_chars:10},2)).result.content[0].text);
 assert.equal(first.text.length,10);assert.equal(next.text.length,10);assert.equal(next.total_chars,first.total_chars);
 for(const file of ['dev/PLAN.md','package.json:secret','C:/Windows/win.ini','../README.md'])assert.equal((await request({path:file},3)).result.isError,true);
});
