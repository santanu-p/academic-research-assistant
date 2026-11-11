import test from 'node:test';
import assert from 'node:assert/strict';
import path from 'node:path';
import {pathToFileURL} from 'node:url';

const target=path.resolve(import.meta.dirname,'..');
const {search,route}=await import(pathToFileURL(path.join(target,'lib/core.mjs')));

// Catches absent skill discovery and the old blanket general/academic editing route.
for(const name of ['humanizer','academic-humanizer']){
 test('exact discovery retains '+name,async()=>{
  const matches=await search(name);
  assert.equal(matches[0]?.name,name);
 });
}
for(const [request,primary,neighbor] of [
 ['Make this personal blog post sound like me and remove AI writing patterns.','humanizer','academic-humanizer'],
 ['Humanize this manuscript abstract while preserving equations, citation keys and calibrated uncertainty.','academic-humanizer','humanizer'],
 ['Edit my NIH Specific Aims for natural scholarly voice and preserve proposal ambition and feasibility.','academic-humanizer','humanizer'],
 ['Rewrite this casual email in my own voice.','humanizer','academic-humanizer'],
 ['Using only these six supplied studies, weigh the evidence and explain disagreements; do not search.','scholar-evidence-synthesis','evidence-evidence-answer'],
 ['Find and verify current studies, then answer my research question with verified citations.','evidence-evidence-answer','scholar-evidence-synthesis'],
 ['Create a 120-word annotated bibliography entry for each provided source.','scholar-literature-review','evidence-literature-review'],
 ['Run the frozen validated method on the final held-out evaluation; reconcile equations and code and log anomalies.','arms-paper-modeler','arms-methodology-architect']
]){
 test(request,async()=>{
  const result=await route(request);
  assert.equal(result.skills[0]?.name,primary);
  assert.notEqual(result.skills[0]?.name,neighbor);
  assert.match(result.execution_status,/no research|not.*execut/i);
 });
}

test('scatter plots select scientific visuals without taking over narrative plots',async()=>{
 for(const request of [
  'Create a scatter plot of my experimental data',
  'Make a scatterplot comparing the measured variables'
 ]){
  const result=await route(request);
  assert.equal(result.skills[0]?.name,'visuals-scientific-visual-table-style',request);
  assert.equal(result.needs_clarification,false,request);
 }
 for(const request of [
  'Help me develop the plot of my short story',
  'Summarize the plot of this novel'
 ])assert.notEqual((await route(request)).skills[0]?.name,'visuals-scientific-visual-table-style',request);
 const latex=await route('Create a scatter plot in pgfplots from the experimental data');
 assert.equal(latex.skills[0]?.name,'latex-pgfplots-charts');
});

test('editable PowerPoint research posters select the presentation workflow',async()=>{
 for(const request of [
  'Design a research poster as an editable PowerPoint slide',
  'Create a conference poster in PPTX'
 ]){
  const result=await route(request);
  assert.equal(result.skills[0]?.name,'academic-pptx',request);
  assert.equal(result.needs_clarification,false,request);
 }
});

test('editable is not a scientific table and real scientific tables still route correctly',async()=>{
 const poster=await route('Design a research poster as an editable file');
 assert.notEqual(poster.matched_rule,'artifact-artifact-scientific-visuals');
 const table=await route('Make a scientific table of these results');
 assert.equal(table.skills[0]?.name,'visuals-scientific-visual-table-style');
 const latex=await route('Build a conference poster using LaTeX');
 assert.equal(latex.skills[0]?.name,'latex-academic-poster');
});
