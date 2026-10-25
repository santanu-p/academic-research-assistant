import {test} from 'node:test';
import assert from 'node:assert/strict';
import {route} from '../lib/core.mjs';
test('representative stage requests select their canonical method first',async()=>{
 const cases=[['respond to reviewers','reviewer-response'],['create a scientific figure','scientific-visuals'],['repair a LaTeX build error','tex-build-repair'],['plan a grant proposal','research-proposals'],['qualitative thematic analysis','qualitative-analysis'],['derive a mathematical model','mathematical-modeling'],['translate and shorten my manuscript','academic-editing']];
 for(const [task,name] of cases)assert.equal((await route(task)).skills[0].name,name,task);
});
