import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {ROOT,indexFiles} from '../lib/core.mjs';
export const extraKeywords={
 'research-assistant':['help','capabilities','onboarding'],
 'research-question':['research gap','topic','hypothesis','objectives','question'],
 'methodology-design':['study design','methodology','framework','survey','experiment','sampling'],
 'literature-search':['find papers','literature search','citation chaining','full text','database'],
 'source-verification':['verify citation','doi','retraction','source credibility'],
 'paper-reading':['explain paper','summarize paper','paper summary'],
 'evidence-extraction':['extract evidence','extraction table','data extraction'],
 'research-appraisal':['appraise','peer review','manuscript review','risk of bias'],
 'literature-review':['literature review','evidence synthesis','claim check','decision brief','debate'],
 'systematic-review':['systematic review','scoping review','prisma','screening'],
 'meta-analysis':['meta-analysis','meta analysis','pooled effect','heterogeneity'],
 'citations-and-bibliographies':['bibliography','references','bibtex','biber','citation style','natbib'],
 'statistical-analysis':['statistics','regression','statistical analysis','data analysis','p-value','confidence interval','credible interval','odds ratio','risk ratio','risk difference'],
 'qualitative-analysis':['qualitative','thematic analysis','coding','interview','reflexivity'],
 'research-proposals':['grant','research proposal','funding','proposal background'],
 'research-planning':['timeline','research plan','schedule','milestones','project management'],
 'research-integrity':['ethics','consent','plagiarism','data privacy','research integrity'],
 'journal-submission':['journal selection','submission','author guidelines','cover letter'],
 'reviewer-response':['reviewer response','rebuttal','response to reviewers','respond to reviewers','reviewer comments'],
 'research-communication':['plain language','public audience','policy brief','research blog','press release'],
 'manuscript-writing':['write manuscript','abstract','introduction','paper outline','paper sections'],
 'academic-editing':['edit','proofread','humanize','paraphrase','translate','shorten','word limit'],
 'humanizer':['humanize general prose','humanize my blog','humanize this email'],
 'academic-humanizer':['humanize academic prose','humanize my manuscript','humanize the manuscript','humanize my abstract'],
 'scientific-reasoning':['mechanism','scientific argument','causal reasoning','explanation'],
 'mathematical-modeling':['mathematical model','derivation','equation code','theoretical model'],
 'research-validation':['validate','verification','simulation','convergence','sensitivity','reproducibility'],
 'adversarial-revision':['review loop','adversarial review','iterative revision','manuscript versions','compare versions','compare revisions','text revision'],
 'research-pipeline':['research pipeline','end to end','orchestration'],
 'document-production':['academic document','report','manual','book','lecture notes','latex document'],
 'tex-layout':['font','layout','multilingual','macro','hyperref','cross-reference'],
 'mathematics-notation':['equation','proof','theorem','algorithm','pseudocode','units'],
 'tex-figures-tables':['tikz','pgfplots','latex table','latex figure','longtable'],
 'professional-documents':['cv','resume','recommendation letter','certificate','invitation','flyer'],
 'teaching-materials':['homework','exam','quiz','assessment','worksheet','solutions'],
 'tex-build-repair':['compile','latex error','latex build','missing package','build failure','latex cleanup'],
 'document-conversion':['convert document','pandoc','latex to word','format conversion','csv to','convert csv','spreadsheet to latex'],
 'presentations-posters':['presentation','slides','poster','talk','beamer','powerpoint','defense'],
 'thesis-preparation':['thesis','dissertation','viva','degree'],
 'scientific-visuals':['figure','chart','plot','visualization','numerical table','pareto']
};
const draftImports=JSON.parse(await fs.readFile(path.join(ROOT,'docs/independent-skill-import.json'),'utf8'));
for(const item of draftImports){
 if(extraKeywords[item.target_name])throw Error('Independent skill name collides: '+item.target_name);
 extraKeywords[item.target_name]=[item.target_name.replaceAll('-',' ')];
}
export function frontmatter(raw){
 const parts=raw.replace(/^\uFEFF/,'').split(/^---\s*$/m);
 if(parts.length<3||parts[0].trim())throw Error('Expected YAML front matter');
 const name=parts[1].match(/^name:\s*["']?([a-z0-9-]+)["']?\s*$/m)?.[1];
 let description=parts[1].match(/^description:\s*(.+)$/m)?.[1]?.trim();
 if(description?.startsWith('"'))description=JSON.parse(description);
 else if(description?.startsWith("'"))description=description.slice(1,-1).replaceAll("''","'");
 if(!name||!description||['|','>'].includes(description))throw Error('Use name and one-line description in skill front matter');
 return {name,description,body:parts.slice(2).join('---').trim()};
}
export async function build(){
const entries=[];
for(const dir of await fs.readdir(path.join(ROOT,'skills'),{withFileTypes:true})){
 if(!dir.isDirectory())continue;
 const rel='skills/'+dir.name+'/SKILL.md';const front=frontmatter(await fs.readFile(path.join(ROOT,rel),'utf8'));
 if(front.name!==dir.name)throw Error('Skill name differs from directory: '+dir.name);
 entries.push({name:front.name,description:front.description,path:rel,keywords:extraKeywords[front.name]||[],
  execution:'Instruction-based assistance; bundled tools require explicit execution and their documented prerequisites.'});
}
entries.sort((a,b)=>a.name.localeCompare(b.name));
await fs.mkdir(path.join(ROOT,'catalog'),{recursive:true});
await fs.writeFile(path.join(ROOT,'catalog/skills.json'),JSON.stringify(entries,null,2)+'\n');
await indexFiles();
console.log('Indexed '+entries.length+' canonical skills.');
}
if(process.argv[1]&&pathToFileURL(path.resolve(process.argv[1])).href===import.meta.url)await build();
