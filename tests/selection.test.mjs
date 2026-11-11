import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import {route,search} from '../lib/core.mjs';
const read=async p=>JSON.parse(await fs.readFile(new URL(p,import.meta.url),'utf8'));
const cases=await read('./fixtures/routing.json');
const ids=await read('./fixtures/original-ids.json');
const aliases={'scholar-research-gaps':'evidence-research-gaps','scholar-systematic-review':'evidence-systematic-review'};
test('all 118 source identifiers still select their complete canonical method',async()=>{
 for(const id of ids)assert.equal((await search(id))[0]?.name,aliases[id]||id,id);
});
for(const c of cases)test(c.request,async()=>{
 const result=await route(c.request);
 assert.equal(result.skills[0]?.name,c.primary,JSON.stringify({expected:c.primary,actual:result.skills[0]?.name,rule:result.matched_rule}));
 for(const excluded of [c.not_primary].flat().filter(Boolean))assert.notEqual(result.skills[0]?.name,aliases[excluded]||excluded);
});
test('standalone source annotations expose the genuine overlapping mode',async()=>{
 const result=await route('Write annotated bibliography annotations for these papers.');
 assert.equal(result.skills[0]?.name,'scholar-literature-review');
 assert.equal(result.needs_clarification,true);
 assert.ok(result.alternatives.includes('evidence-citations-and-references'));
});
