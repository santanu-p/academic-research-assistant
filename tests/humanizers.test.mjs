import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {route} from '../lib/core.mjs';
const root=fileURLToPath(new URL('../',import.meta.url));

test('both MIT humanizers and their complete recorded source payloads are retained',async()=>{
 const mapping=JSON.parse(await fs.readFile(path.join(root,'docs/humanizer-source-map.json'),'utf8'));
 assert.ok(mapping.length>=20);
 for(const item of mapping){
  const bytes=await fs.readFile(path.join(root,item.destination));
  assert.equal(createHash('sha256').update(bytes).digest('hex'),item.sha256,item.destination);
 }
 for(const name of ['humanizer','academic-humanizer']){
  const original=await fs.readFile(path.join(root,'resources/upstream',name+'-main/SKILL.md'),'utf8');
  const active=await fs.readFile(path.join(root,'skills',name,'SKILL.md'),'utf8');
  const body=original.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/,'');
  assert.ok(active.includes(body),'Complete upstream instructions missing: '+name);
  assert.match(await fs.readFile(path.join(root,'skills',name,'LICENSE'),'utf8'),/MIT License/);
  assert.equal((await route(name)).skills[0].name,name);
 }
});

test('general and scholarly humanization requests select the appropriate distinct skill',async()=>{
 for(const [request,name] of [
  ['Humanize my manuscript abstract while preserving citations and uncertainty','academic-humanizer'],
  ['Humanize my email to my colleague','humanizer'],
  ['Humanise my personal blog about academic research','humanizer'],
  ['Humanize this abstract but do not change citations','academic-humanizer'],
  ['Humanize the grant proposal without strengthening the claims','academic-humanizer']
 ])assert.equal((await route(request)).skills[0].name,name,request);
});

test('explicit Humanizer exclusions remove both skills while routing the remaining task',async()=>{
 for(const request of [
  'Do not humanize my manuscript; check citations',
  'Use no humanizer: summarize the paper',
  'Summarize the paper without using an academic humanizer',
  'Avoid humanising the abstract; check references'
 ]){
  const result=await route(request);
  assert.ok(result.skills.length,request);
  assert.ok(result.skills.every(x=>!['humanizer','academic-humanizer'].includes(x.name)),request);
  assert.ok(result.skills.some(x=>/citation|bibliograph|paper|reference/.test(x.name)),request);
 }
});

test('an exclusion alone or a conflicting humanization request asks for clarification',async()=>{
 for(const request of ['Do not humanize','No humanizer','Do not use a humanizer','Humanize my manuscript, but do not use a humanizer']){
  const result=await route(request);
  assert.ok(result.skills.every(x=>!['humanizer','academic-humanizer'].includes(x.name)),request);
  assert.match(result.clarification,/clarif/i,request);
 }
});
