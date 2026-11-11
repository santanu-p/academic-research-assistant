import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {createHash} from 'node:crypto';
import * as core from '../lib/core.mjs';
import {handle} from '../server/mcp.mjs';

const digest=value=>createHash('sha256').update(value).digest('hex');
const call=(name)=>handle({jsonrpc:'2.0',id:1,method:'tools/call',params:{name,arguments:{}}});
async function fixture(entries, run){
 const root=await fs.mkdtemp(path.join(os.tmpdir(),'ara-source-ledger-'));
 try{
  await fs.mkdir(path.join(root,'audit/review-118'),{recursive:true});
  await fs.writeFile(path.join(root,'audit/review-118/file-mapping.json'),JSON.stringify(entries));
  await run(root);
 }finally{await fs.rm(root,{recursive:true,force:true});}
}

test('configured MCP exposes a passing reviewed source check separately from package verification',async()=>{
 const response=await call('verify_sources');
 assert.equal(response.result.isError,false);
 const report=JSON.parse(response.result.content[0].text);
 assert.equal(report.passed,true);assert.equal(report.verified,600);
 assert.deepEqual(report.missing,[]);assert.deepEqual(report.mismatched,[]);
 assert.equal((await call('verify_package')).result.isError,false);
});

test('source check identifies missing and changed originals without modifying the ledger or payload',async()=>{
 const entries=['present.txt','missing.txt','good.txt'].map(preserved_at=>({preserved_at,sha256:digest('original')}));
 await fixture(entries,async root=>{
  await fs.writeFile(path.join(root,'present.txt'),'changed');
  await fs.writeFile(path.join(root,'good.txt'),'original');
  const before=await fs.readFile(path.join(root,'audit/review-118/file-mapping.json'));
  const result=await core.verifySources(root);
  assert.equal(result.passed,false);assert.equal(result.verified,1);
  assert.deepEqual(result.missing,['missing.txt']);assert.deepEqual(result.mismatched,['present.txt']);
  assert.deepEqual(await fs.readFile(path.join(root,'audit/review-118/file-mapping.json')),before);
  assert.equal(await fs.readFile(path.join(root,'present.txt'),'utf8'),'changed');
 });
});

test('source check rejects unsafe paths and invalid expected hashes',async()=>{
 for(const entry of [
  {preserved_at:'../outside.txt',sha256:digest('original')},
  {preserved_at:'present.txt',sha256:'not-a-sha256'}
 ])await fixture([entry],async root=>assert.rejects(core.verifySources(root)));
});

test('source check rejects a path through a link outside the bundle',async t=>{
 const outside=await fs.mkdtemp(path.join(os.tmpdir(),'ara-source-outside-'));
 try{
  await fs.writeFile(path.join(outside,'original.txt'),'original');
  await fixture([{preserved_at:'linked/original.txt',sha256:digest('original')}],async root=>{
   try{await fs.symlink(outside,path.join(root,'linked'),process.platform==='win32'?'junction':'dir');}
   catch(error){if(['EPERM','EACCES','ENOTSUP'].includes(error.code)){t.skip('Link creation is unavailable in this environment');return;}throw error;}
   await assert.rejects(core.verifySources(root),/outside the package/);
  });
 }finally{await fs.rm(outside,{recursive:true,force:true});}
});
