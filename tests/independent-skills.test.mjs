import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {catalog,route} from '../lib/core.mjs';

const root=fileURLToPath(new URL('../',import.meta.url));
test('all independently written skills and both original overlapping methods are discoverable',async()=>{
 const expected=JSON.parse(await fs.readFile(path.join(root,'tests/fixtures/independent-skills.json'),'utf8'));
 assert.equal(expected.length,50);
 const entries=await catalog(), names=new Set(entries.map(entry=>entry.name));
 assert.equal(names.size,90);
 assert.ok(!names.has('latex-document-workflow'),'Retired general skill remains discoverable');
 await assert.rejects(fs.lstat(path.join(root,'skills/latex-document-workflow')),{code:'ENOENT'});
 for(const name of expected)assert.ok(names.has(name),'Missing '+name);
 for(const name of ['methodology-design','research-planning'])assert.ok(names.has(name),'Missing original '+name);
});
test('imported draft instructions match their recorded provenance hashes',async()=>{
 const imports=JSON.parse(await fs.readFile(path.join(root,'docs/independent-skill-import.json'),'utf8'));
 assert.equal(imports.length,50);
 assert.ok(!imports.some(item=>item.target_name==='latex-document-workflow'),'Retired general skill remains imported');
 for(const item of imports){
  const bytes=await fs.readFile(path.join(root,'skills',item.target_name,'SKILL.md'));
  assert.equal(createHash('sha256').update(bytes).digest('hex'),item.target_sha256,item.target_name);
  if(item.note==='Copied unchanged.')assert.equal(item.source_sha256,item.target_sha256,item.target_name);
  else assert.ok(item.note && item.source_sha256,`Missing provenance for ${item.target_name}`);
 }
});
test('explicit requests select independently written specialist methods',async()=>{
 for(const name of ['systematic-review-protocol','latex-beamer-presentations','reference-identity-verification','independent-methodology-design']){
  const result=await route(name);
  assert.equal(result.skills[0]?.name,name,'Wrong route for '+name);
 }
});
test('representative requests discover specialist draft skills',async()=>{
 for(const [request,expected] of [
  ['Create a systematic review protocol with screening decisions','systematic-review-protocol'],
  ['Prepare a LaTeX beamer presentation with overlays','latex-beamer-presentations'],
  ['Plan meta analysis pooling and sensitivity analyses','meta-analysis-planning'],
  ['Create a citation network search with backward and forward links','citation-network-search'],
  ['Debug this LaTeX build using the compiler log','latex-build-debugging'],
  ['Verify reference identity using authoritative records','reference-identity-verification'],
  ['Compare Paperpal with a local academic writing workflow','academic-writing-tool-evaluation'],
  ['Develop a field-specific evidence guide for a research question','research-field-evidence-guide']
 ]){
  const result=await route(request);
  assert.ok(result.skills.slice(0,3).some(skill=>skill.name===expected),`${expected} not in top three for ${request}`);
 }
});
