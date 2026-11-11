import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import {route} from '../lib/core.mjs';
const cases=JSON.parse(await fs.readFile(new URL('./fixtures/holdout.json',import.meta.url),'utf8'));
for(const c of cases)test('holdout: '+c.request,async()=>{
 const result=await route(c.request);
 assert.equal(result.skills[0]?.name,c.expected_primary);
 assert.equal(result.needs_clarification,c.expected_clarification);
});
for(const [request,expected] of [
 ['Design candidate research methodologies from the brief, compare adjacent-field combinations, and choose what should be validated later.','arms-methodology-architect'],
 ['Turn this evidence-review question into searchable PICO concepts and synonym blocks.','evidence-research-question']
])test('neighbor: '+request,async()=>{
 const result=await route(request);
 assert.equal(result.skills[0]?.name,expected);
 assert.equal(result.needs_clarification,false);
});
