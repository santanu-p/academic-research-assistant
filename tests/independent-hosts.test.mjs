import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const root=fileURLToPath(new URL('../',import.meta.url));
const cli=path.join(root,'cli/ara.mjs');
const run=(args)=>spawnSync(process.execPath,[cli,...args],{encoding:'utf8',timeout:60000});
async function allSkillsPresent(bundle){
 const skills=JSON.parse(await fs.readFile(path.join(bundle,'catalog/skills.json'),'utf8'));
 assert.equal(skills.length,90);
 assert.ok(!skills.some(skill=>skill.name==='latex-document-workflow'));
 await assert.rejects(fs.lstat(path.join(bundle,'skills/latex-document-workflow')),{code:'ENOENT'});
 for(const skill of skills)assert.ok((await fs.stat(path.join(bundle,skill.path))).isFile(),skill.path);
}

test('Antigravity wrapper retains the complete draft and emits an absolute optional MCP config',async()=>{
 const base=await fs.mkdtemp(path.join(root,'tests','.draft-host-'));
 try{
  const target=path.join(base,'plugin with spaces');
  const result=run(['export','--host','antigravity','--target',target]);
  assert.equal(result.status,0,result.stderr);
  const details=JSON.parse(result.stdout), bundle=path.join(target,'skills/academic-research-assistant');
  assert.equal(details.bundle,bundle);
  const manifest=JSON.parse(await fs.readFile(path.join(target,'plugin.json'),'utf8'));
  assert.deepEqual(Object.keys(manifest).sort(),['description','name']);
  assert.equal(manifest.name,'academic-research-assistant');
  assert.ok((await fs.stat(path.join(bundle,'skills/systematic-review-protocol/SKILL.md'))).isFile());
  await allSkillsPresent(bundle);
  await assert.rejects(fs.lstat(path.join(target,'agents')),{code:'ENOENT'});
  const config=run(['config','--host','antigravity','--root',bundle]);
  assert.equal(config.status,0,config.stderr);
  assert.equal(JSON.parse(config.stdout).mcpServers['academic-research-assistant'].args[0],path.join(bundle,'server/mcp.mjs'));
 }finally{await fs.rm(base,{recursive:true,force:true});}
});

test('skill-only exports omit plugin markers and retain specialist skills',async()=>{
 const base=await fs.mkdtemp(path.join(root,'tests','.draft-skill-'));
 try{
  const target=path.join(base,'skill');const result=run(['export','--host','claude-skill','--target',target]);
  assert.equal(result.status,0,result.stderr);
  for(const marker of ['plugin.json','.claude-plugin','.mcp.json','mcp.json'])await assert.rejects(fs.lstat(path.join(target,marker)),{code:'ENOENT'});
  assert.ok((await fs.stat(path.join(target,'skills/latex-beamer-presentations/SKILL.md'))).isFile());
  await allSkillsPresent(target);
 }finally{await fs.rm(base,{recursive:true,force:true});}
});
