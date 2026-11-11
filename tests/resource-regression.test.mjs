import test from 'node:test';
import assert from 'node:assert/strict';
import path from 'node:path';
import {pathToFileURL} from 'node:url';

const target=path.resolve(import.meta.dirname,'..');
const {handle}=await import(pathToFileURL(path.join(target,'server/mcp.mjs')));

// Catches a package that advertises a method but omits the supporting resource tree.
for(const file of ['skills/humanizer/README.md','skills/humanizer/LICENSE',
                  'skills/academic-humanizer/examples/before-after.md']){
 test('MCP reads the preserved support '+file,async()=>{
  const result=await handle({jsonrpc:'2.0',id:1,method:'tools/call',
    params:{name:'read_resource',arguments:{path:file,max_chars:4000}}});
  assert.equal(result.result?.isError,false,JSON.stringify(result));
  const content=JSON.parse(result.result.content[0].text);
  assert.equal(content.path,file);
  assert.ok(content.total_chars>100);
 });
}
