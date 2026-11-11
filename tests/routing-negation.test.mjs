import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import {route} from '../lib/core.mjs';

const cases=JSON.parse(await fs.readFile(new URL('./fixtures/routing-negation-cases.json',import.meta.url),'utf8'));
for(const c of cases)test(c.request,async()=>{
 const result=await route(c.request);
 const names=result.skills.map(skill=>skill.name);
 if(c.kind==='control')assert.equal(names[0],c.expected);
 else {
  for(const name of c.prohibited){
   assert.ok(!names.includes(name),`prohibited skill ${name} selected: ${names}`);
   assert.ok(!result.alternatives.includes(name),`prohibited alternative ${name}`);
  }
  if(c.clarification)assert.equal(result.needs_clarification,true);
  if(c.preferred && names[0]!==c.preferred){
   assert.equal(names[0],'research-assistant');
   assert.equal(result.needs_clarification,true);
  }
 }
});
