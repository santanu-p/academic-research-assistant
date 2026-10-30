import {test} from 'node:test';
import assert from 'node:assert/strict';
import {route,search} from '../lib/core.mjs';
test('keyword matches do not route unrelated words containing the keyword',async()=>{
 assert.ok(!(await search('credit')).some(skill=>skill.name==='academic-editing'));
 assert.ok(!(await search('editorship')).some(skill=>skill.name==='academic-editing'));
 assert.ok((await search('edit this manuscript')).some(skill=>skill.name==='academic-editing'));
});
test('common connective words alone do not create spurious search matches',async()=>{
 assert.deepEqual(await search('the and a'),[]);
 assert.equal((await route('the and a')).skills[0].name,'research-assistant');
});
test('statistical interpretation requests discover the statistics method',async()=>{
 for(const task of ['Explain a confidence interval and odds ratio','Interpret an absolute risk difference'])
  assert.equal((await route(task)).skills[0].name,'statistical-analysis',task);
});
test('conversion and version comparison discover their actionable workflows',async()=>{
 assert.ok((await route('Convert this CSV to a LaTeX table')).skills.slice(0,3).some(s=>s.name==='document-conversion'));
 assert.ok((await route('Compare these two manuscript versions')).skills.slice(0,3).some(s=>s.name==='adversarial-revision'));
});
test('representative stage requests select their canonical method first',async()=>{
 const cases=[['respond to reviewers','reviewer-response'],['create a scientific figure','scientific-visuals'],['repair a LaTeX build error','tex-build-repair'],['plan a grant proposal','research-proposals'],['qualitative thematic analysis','qualitative-analysis'],['derive a mathematical model','mathematical-modeling'],['translate and shorten my manuscript','academic-editing']];
 for(const [task,name] of cases)assert.equal((await route(task)).skills[0].name,name,task);
});
