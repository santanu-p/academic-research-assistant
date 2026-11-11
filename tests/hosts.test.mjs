import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
const ROOT=fileURLToPath(new URL('../',import.meta.url));
const cli=path.join(ROOT,'cli/ara.mjs');
const run=(args)=>spawnSync(process.execPath,[cli,...args],{encoding:'utf8',timeout:30000});
async function assertOriginals(bundle){
 const mapping=JSON.parse(await fs.readFile(path.join(bundle,'audit/review-118/file-mapping.json'),'utf8'));assert.equal(mapping.length,600);
 for(const row of mapping)assert.equal(createHash('sha256').update(await fs.readFile(path.join(bundle,row.preserved_at))).digest('hex'),row.sha256,row.preserved_at);
}

test('Codex export refuses instruction-only bundles before creating a target',async()=>{
 const base=await fs.mkdtemp(path.join(ROOT,'tests','.host-reexport-'));
 try{
  for(const host of ['codex-skill','claude']){
   const source=path.join(base,host);const first=run(['export','--host',host,'--target',source]);
   assert.equal(first.status,0,first.stderr);
   const bundle=JSON.parse(first.stdout).bundle;
   const target=path.join(base,host+'-codex');
   const second=spawnSync(process.execPath,[path.join(bundle,'cli/ara.mjs'),'export','--host','codex','--target',target],{encoding:'utf8',timeout:30000});
   assert.notEqual(second.status,0,'incomplete source must not produce a Codex plugin');
   assert.match(second.stderr,/original.*(full|complete).*bundle/i);
   await assert.rejects(fs.lstat(target),{code:'ENOENT'});
  }
 }finally{await fs.rm(base,{recursive:true,force:true});}
});

test('instruction-only exports retain methods without live plugin markers',async()=>{
 const base=await fs.mkdtemp(path.join(ROOT,'tests','.host-skills-'));
 try{
  for(const host of ['codex-skill','claude-skill','antigravity-skill']){
   const target=path.join(base,host);const r=run(['export','--host',host,'--target',target]);assert.equal(r.status,0,r.stderr);
   for(const rel of ['plugin.json','mcp.json','.mcp.json','.claude-plugin','.codex-plugin']){
    await assert.rejects(fs.lstat(path.join(target,rel)),{code:'ENOENT'});
   }
   for(const rel of ['SKILL.md','skills/research-assistant/SKILL.md','agents/evidence-librarian.md','audit/source-map.json']){
    assert.deepEqual(await fs.readFile(path.join(target,rel)),await fs.readFile(path.join(ROOT,rel)));
   }
   const verified=spawnSync(process.execPath,[path.join(target,'cli/ara.mjs'),'verify'],{encoding:'utf8'});
   assert.equal(verified.status,0,verified.stderr);assert.equal(JSON.parse(verified.stdout).passed,true);
   await assertOriginals(target);
  }
 }finally{await fs.rm(base,{recursive:true,force:true});}
});

test('Antigravity export isolates role documents inside a complete outer skill',async()=>{
 const base=await fs.mkdtemp(path.join(ROOT,'tests','.host-antigravity-'));
 try{
  const target=path.join(base,'plugin with spaces');const r=run(['export','--host','antigravity','--target',target]);assert.equal(r.status,0,r.stderr);
  const result=JSON.parse(r.stdout);const bundle=path.join(target,'skills/academic-research-assistant-full');assert.equal(result.bundle,bundle);
  assert.equal(result.wrapper_root_agents_directory_included,false);assert.equal('native_agents_registered' in result,false);
  const manifest=JSON.parse(await fs.readFile(path.join(target,'plugin.json'),'utf8'));
  assert.equal(manifest.name,'academic-research-assistant-full');assert.deepEqual(Object.keys(manifest).sort(),['description','name']);
  await assert.rejects(fs.lstat(path.join(target,'agents')),{code:'ENOENT'});
  await assert.rejects(fs.lstat(path.join(target,'mcp_config.json')),{code:'ENOENT'});
  assert.deepEqual(await fs.readFile(path.join(bundle,'skills/research-assistant/SKILL.md')),await fs.readFile(path.join(ROOT,'skills/research-assistant/SKILL.md')));
  await assertOriginals(bundle);
  const config=run(['config','--host','antigravity','--root',bundle]);assert.equal(config.status,0,config.stderr);
  const server=JSON.parse(config.stdout).mcpServers['academic-research-assistant-full'];
  assert.equal(server.command,'node');assert.equal(server.args[0],path.join(bundle,'server/mcp.mjs'));
  const launched=spawnSync(server.command,server.args,{input:'{"jsonrpc":"2.0","id":1,"method":"ping"}\n',encoding:'utf8',timeout:10000});
  assert.equal(launched.status,0,launched.stderr);assert.deepEqual(JSON.parse(launched.stdout),{jsonrpc:'2.0',id:1,result:{}});
  assert.equal(JSON.parse(run(['export','--host','antigravity','--target',path.join(base,'second')]).stdout).host_settings_changed,false);
 }finally{await fs.rm(base,{recursive:true,force:true});}
});

test('Claude export isolates portable roles from native agent discovery',async()=>{
 const base=await fs.mkdtemp(path.join(ROOT,'tests','.host-claude-'));
 try{
  const target=path.join(base,'plugin');const r=run(['export','--host','claude','--target',target]);assert.equal(r.status,0,r.stderr);
  const result=JSON.parse(r.stdout);assert.equal(result.bundle,path.join(target,'skills/academic-research-assistant-full'));
  assert.equal(result.wrapper_root_agents_directory_included,false);assert.equal('native_agents_registered' in result,false);
  await assert.rejects(fs.lstat(path.join(target,'agents')),{code:'ENOENT'});
  assert.ok(await fs.access(path.join(target,'README.md')).then(()=>true,()=>false),'wrapper README exists');
  assert.ok(await fs.access(path.join(target,'LICENSE')).then(()=>true,()=>false),'wrapper license exists');
  assert.deepEqual(await fs.readFile(path.join(target,'LICENSE')),await fs.readFile(path.join(ROOT,'LICENSE')));
  assert.deepEqual(await fs.readFile(path.join(target,'THIRD_PARTY_NOTICES.md')),await fs.readFile(path.join(ROOT,'THIRD_PARTY_NOTICES.md')));
  assert.deepEqual(await fs.readFile(path.join(result.bundle,'agents/README.md')),await fs.readFile(path.join(ROOT,'agents/README.md')));
  await assertOriginals(result.bundle);
  assert.deepEqual(JSON.parse(await fs.readFile(path.join(target,'.mcp.json'),'utf8')).mcpServers['academic-research-assistant-full'].args,['${CLAUDE_PLUGIN_ROOT}/skills/academic-research-assistant-full/server/mcp.mjs']);
 }finally{await fs.rm(base,{recursive:true,force:true});}
});
