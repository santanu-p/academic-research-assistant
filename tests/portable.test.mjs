import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const ROOT=fileURLToPath(new URL('../',import.meta.url));
const cli=path.join(ROOT,'cli/ara.mjs');
function run(args,input=''){return spawnSync(process.execPath,[cli,...args],{input,encoding:'utf8',timeout:20000});}
test('CLI shebang remains byte-stable during npm installation',async()=>{
 const source=await fs.readFile(cli);assert.ok(source.subarray(0,20).equals(Buffer.from('#!/usr/bin/env node\n')),'CLI shebang must end in LF');
});
test('help is useful without modifying a host',()=>{
 const r=run(['--help']);assert.equal(r.status,0,r.stderr);assert.match(r.stdout,/export/);assert.match(r.stdout,/mcp/);
});
test('unknown arguments fail without a stack trace',()=>{
 const r=run(['install','--bogus']);assert.notEqual(r.status,0);assert.match(r.stderr,/Unknown/);assert.doesNotMatch(r.stderr,/at file:/);
});
test('printed marketplace command preserves a path containing shell substitutions and apostrophes',async()=>{
 const base=await fs.mkdtemp(path.join(ROOT,'tests','.shell-path-'));
 try{
  const windows=process.platform==='win32';
  const target=path.join(base,windows?"bundle ' $(Write-Output altered)":"bundle ' $(printf altered) \\ end");
  const r=run(['export','--host','codex','--target',target]);assert.equal(r.status,0,r.stderr);
  const command=JSON.parse(r.stdout).next[0];
  const shell=windows?'powershell.exe':'/bin/sh';
  const script=windows?`function codex { [Console]::Out.Write(($args | ConvertTo-Json -Compress)) }; ${command}`:
   `codex() { printf '%s\\n' "$@"; }; ${command}`;
  const executed=spawnSync(shell,windows?['-NoProfile','-Command',script]:['-c',script],{encoding:'utf8',env:{...process.env,ARA_TEST_VALUE:'altered'}});
  assert.equal(executed.status,0,executed.stderr);
  const args=windows?JSON.parse(executed.stdout):executed.stdout.trimEnd().split('\n');
  assert.deepEqual(args,['plugin','marketplace','add',target]);
 }finally{await fs.rm(base,{recursive:true,force:true});}
});
test('local catalogs and traversal rejection use real public methods',async()=>{
 const r=run(['list','--json']);assert.equal(r.status,0,r.stderr);const entries=JSON.parse(r.stdout);
 assert.ok(entries.some(x=>x.name==='research-assistant'));assert.equal(new Set(entries.map(x=>x.name)).size,entries.length);
 const bad=run(['read','../package.json']);assert.notEqual(bad.status,0);assert.match(bad.stderr,/inside|relative|path/i);
});
test('export copies a self-contained bundle and never overwrites an existing target',async()=>{
 const base=await fs.mkdtemp(path.join(ROOT,'tests','.install-'));
 try{
 const target=path.join(base,'bundle with spaces');let r=run(['export','--host','generic','--target',target]);
 assert.equal(r.status,0,r.stderr);assert.ok((await fs.stat(path.join(target,'skills/research-assistant/SKILL.md'))).isFile());
 assert.ok((await fs.stat(path.join(target,'docs/RESEARCH-CONTRACT.md'))).isFile());
 assert.equal(await fs.readFile(path.join(target,'LICENSE'),'utf8'),await fs.readFile(path.join(ROOT,'LICENSE'),'utf8'));
 await fs.writeFile(path.join(target,'keep.txt'),'user content');r=run(['export','--host','generic','--target',target]);
 assert.notEqual(r.status,0);assert.equal(await fs.readFile(path.join(target,'keep.txt'),'utf8'),'user content');
 }finally{await fs.rm(base,{recursive:true,force:true});}
});
test('Codex marketplace and Claude root formats are actually exported',async()=>{
 const base=await fs.mkdtemp(path.join(ROOT,'tests','.hosts-'));
 try{
 for(const host of ['codex','claude','codex-skill','claude-skill']){
 const dest=path.join(base,host);const r=run(['install','--host',host,'--target',dest]);assert.equal(r.status,0,r.stderr);
 const bundle=host==='codex'?path.join(dest,'plugins/academic-research-assistant'):
  host==='claude'?path.join(dest,'skills/academic-research-assistant'):dest;
 if(host==='codex'){
 const manifest=JSON.parse(await fs.readFile(path.join(bundle,'plugin.json'),'utf8'));assert.equal(manifest.name,'academic-research-assistant');
 const m=JSON.parse(await fs.readFile(path.join(dest,'.agents/plugins/marketplace.json'),'utf8'));
 assert.equal(m.plugins[0].source.path,'./plugins/academic-research-assistant');
 }else if(host==='claude'){
 const manifest=JSON.parse(await fs.readFile(path.join(dest,'.claude-plugin/plugin.json'),'utf8'));assert.equal(manifest.name,'academic-research-assistant');
 assert.match(await fs.readFile(path.join(dest,'README.md'),'utf8'),/research planning/i);
 assert.deepEqual(await fs.readFile(path.join(dest,'LICENSE')),await fs.readFile(path.join(ROOT,'LICENSE')));
 assert.deepEqual(await fs.readFile(path.join(dest,'THIRD_PARTY_NOTICES.md')),await fs.readFile(path.join(ROOT,'THIRD_PARTY_NOTICES.md')));
 const m=JSON.parse(await fs.readFile(path.join(dest,'.mcp.json'),'utf8'));
 assert.ok(m.mcpServers['academic-research-assistant'].args[0].includes('CLAUDE_PLUGIN_ROOT'));
 }else assert.match(await fs.readFile(path.join(dest,'SKILL.md'),'utf8'),/skills\/research-assistant\/SKILL.md/);
 }
 }finally{await fs.rm(base,{recursive:true,force:true});}
});
test('stdio speaks MCP, rejects malformed initialize, and recovers after bad JSON',()=>{
 const messages=[
 '{bad json}\n',
 JSON.stringify({jsonrpc:'2.0',id:1,method:'initialize',params:{}})+'\n',
 JSON.stringify({jsonrpc:'2.0',id:2,method:'initialize',params:{protocolVersion:'2025-11-25',capabilities:{},clientInfo:{name:'test',version:'1'}}})+'\n',
 JSON.stringify({jsonrpc:'2.0',id:3,method:'tools/list'})+'\n',
 JSON.stringify({jsonrpc:'2.0',id:4,method:'tools/call',params:{name:'route_task',arguments:{task:'what can Academic Research Assistant do'}}})+'\n',
 JSON.stringify({jsonrpc:'2.0',id:5,method:'tools/call',params:{name:'read_resource',arguments:{path:'../../secrets'}}})+'\n'];
 const r=run(['mcp'],messages.join(''));assert.equal(r.status,0,r.stderr);
 const rows=r.stdout.trim().split('\n').map(JSON.parse);assert.equal(rows.length,6);
 assert.equal(rows[0].error.code,-32700);assert.equal(rows[1].error.code,-32602);assert.equal(rows[2].result.serverInfo.version,'3.1.0');
 assert.ok(rows[3].result.tools.some(x=>x.name==='read_resource'));assert.equal(rows[4].result.isError,false);
 assert.match(rows[4].result.content[0].text,/research-assistant/);assert.equal(rows[5].result.isError,true);
});
test('a host can launch the server directly without the CLI',()=>{
 const message=JSON.stringify({jsonrpc:'2.0',id:1,method:'ping'})+'\n';
 const r=spawnSync(process.execPath,[path.join(ROOT,'server/mcp.mjs')],{input:message,encoding:'utf8',timeout:10000});
 assert.equal(r.status,0,r.stderr);assert.deepEqual(JSON.parse(r.stdout),{jsonrpc:'2.0',id:1,result:{}});
});
