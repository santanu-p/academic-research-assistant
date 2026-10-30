import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

const ROOT=fileURLToPath(new URL('../',import.meta.url));
const run=(cli,args)=>spawnSync(process.execPath,[cli,...args],{encoding:'utf8',timeout:60000});

test('export rejects corrupted sources and overlapping resolved targets',async t=>{
 const base=await fs.mkdtemp(path.join(ROOT,'tests','.export-integrity-'));
 try{
  const source=path.join(base,'source');
  const initial=run(path.join(ROOT,'cli/ara.mjs'),['export','--host','generic','--target',source]);
  assert.equal(initial.status,0,initial.stderr);
  const cli=path.join(source,'cli/ara.mjs');
  await t.test('rejects a source whose indexed file changed',async()=>{
   const skill=path.join(source,'SKILL.md');const original=await fs.readFile(skill);
   try{
    await fs.appendFile(skill,'\ncorrupt source\n');
    const target=path.join(base,'corrupt-export');
    const r=run(cli,['export','--host','generic','--target',target]);
    assert.notEqual(r.status,0);assert.match(r.stderr,/source.*verif/i);
    await assert.rejects(fs.lstat(target),{code:'ENOENT'});
   }finally{await fs.writeFile(skill,original);}
  });
  await t.test('rejects alternate casing of an existing runtime path',async t=>{
   if(process.platform!=='win32')return t.skip('Windows path casing behavior');
   const target=path.join(source,'SKILLS','overlap-case');
   const r=run(cli,['export','--host','generic','--target',target]);
   assert.notEqual(r.status,0);assert.match(r.stderr,/overlaps package runtime files/i);
   await assert.rejects(fs.lstat(target),{code:'ENOENT'});
  });
  await t.test('rejects a junction or symlink to a runtime directory',async t=>{
   const link=path.join(base,'linked-skills');
   try{await fs.symlink(path.join(source,'skills'),link,process.platform==='win32'?'junction':'dir');}
   catch(error){if(['EPERM','EACCES','ENOSYS'].includes(error.code))return t.skip('symlink creation unavailable: '+error.code);throw error;}
   const target=path.join(link,'new-parent','overlap-link');
   const r=run(cli,['export','--host','generic','--target',target]);
   assert.notEqual(r.status,0);assert.match(r.stderr,/overlaps package runtime files/i);
   await assert.rejects(fs.lstat(path.join(link,'new-parent')),{code:'ENOENT'});
  });
 }finally{await fs.rm(base,{recursive:true,force:true});}
});
