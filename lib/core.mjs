import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
export const ROOT=fileURLToPath(new URL('../',import.meta.url));
export const RUNTIME_DIRS=['cli','lib','server','skills','catalog','docs','tools','workflows','examples','resources','licenses','agents','audit','dev','.codex-plugin','.claude-plugin'];
export const RUNTIME_FILES=['package.json','plugin.json','mcp.json','.mcp.json','SKILL.md','README.md','LICENSE','THIRD_PARTY_NOTICES.md','CHANGELOG.md','requirements-optional.txt'];
const badParts=new Set(['.git','node_modules','__pycache__','.private-archive','.public-build','dist']);
// npm normalizes .gitignore while extracting packages. Byte-exact originals
// are mapped under audit/review-118/preserved-ignore-files instead.
const npmNormalizedFiles=new Set(['resources/upstream/academic-humanizer-main/.gitignore','skills/academic-humanizer/.gitignore']);
export const json=async(file,root=ROOT)=>JSON.parse(await fs.readFile(path.join(root,file),'utf8'));
export function text(value,label='value',max=10000){
 if(typeof value!=='string'||!value.trim()||value.length>max)throw Error(label+' must be nonempty text of at most '+max+' characters');
 return value.trim();
}
export function integer(value,min,max,label){
 if(!Number.isSafeInteger(value)||value<min||value>max)throw Error(label+' must be an integer between '+min+' and '+max);
 return value;
}
export async function contained(relative,root=ROOT){
 text(relative,'path',1000);
 if(path.isAbsolute(relative)||/^[a-z]:|^[\\/]{2}/i.test(relative)||relative.includes('\0'))throw Error('Use a relative path inside the package');
 const parts=relative.replaceAll('\\','/').split('/');
 if(parts.includes('..')||parts.some(x=>badParts.has(x))||relative.includes(':'))throw Error('Path must stay inside the public package');
 const target=await fs.realpath(path.resolve(root,...parts));
 const base=await fs.realpath(root);const rel=path.relative(base,target);
 if(rel.startsWith('..'+path.sep)||rel==='..'||path.isAbsolute(rel))throw Error('Path resolves outside the package');
 return target;
}
export async function publicFiles(root=ROOT){
 const result=[];
 async function visit(rel){
  if(npmNormalizedFiles.has(rel))return;
  const target=path.join(root,rel);let stat;
  try{stat=await fs.lstat(target);}catch(e){if(e.code==='ENOENT')return;throw e;}
  if(stat.isSymbolicLink())throw Error('Public bundle cannot contain symbolic links: '+rel);
  if(stat.isDirectory()){
   for(const name of (await fs.readdir(target)).sort()){
    if(badParts.has(name)||name.startsWith('.test-')||name.endsWith('.pyc'))continue;
    await visit(rel?rel+'/'+name:name);
   }
  }else if(stat.isFile())result.push(rel.replaceAll('\\','/'));
 }
 for(const name of [...RUNTIME_FILES,...RUNTIME_DIRS])await visit(name);
 return [...new Set(result)].sort();
}
export async function catalog(root=ROOT){
 const entries=await json('catalog/skills.json',root);
 if(!Array.isArray(entries)||!entries.length)throw Error('Capability catalog is unavailable');
 const names=new Set();
 for(const entry of entries){
  if(!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(entry.name)||names.has(entry.name))throw Error('Invalid or duplicated skill name');
  names.add(entry.name);text(entry.description,'description');
  if(entry.path!=='skills/'+entry.name+'/SKILL.md')throw Error('Invalid skill path');
  await contained(entry.path,root);
 }
 const aliases=await json('catalog/aliases.json',root);
 for(const [alias,target] of Object.entries(aliases)){
  if(names.has(alias)||!names.has(target))throw Error('Invalid compatibility alias');
  await contained('skills/'+alias+'/SKILL.md',root);
 }
 const actual=(await fs.readdir(path.join(root,'skills'),{withFileTypes:true})).filter(x=>x.isDirectory()&&!Object.hasOwn(aliases,x.name)).map(x=>x.name).sort();
 if(JSON.stringify(actual)!==JSON.stringify([...names].sort()))throw Error('Catalog and skill directories differ');
 return entries;
}
const stop=new Set('a an and are as at be by can do for from help how i in into is it me my of on or our that the these this to use using we what when which with you your'.split(' '));
const words=s=>new Set((s.toLowerCase().match(/[a-z0-9]+/g)||[]).filter(x=>!stop.has(x)&&x.length>1));
export async function search(query,limit=12){
 query=text(query,'query');integer(limit,1,250,'limit');const entries=await catalog();
 const key=query.replace(/^[$/]/,'').toLowerCase();const aliases=await json('catalog/aliases.json');
 const exact=entries.find(x=>x.name===(aliases[key]||key));
 if(exact)return [exact];
 const terms=words(query);
 return entries.map(entry=>{
  let score=0;for(const word of words(entry.name))if(terms.has(word))score+=4;
  for(const word of words(entry.description))if(terms.has(word))score++;
  for(const term of entry.keywords||[])if(term.length>3&&query.toLowerCase().includes(term.toLowerCase()))score+=8;
  return {entry,score};
 }).filter(x=>x.score>0).sort((a,b)=>b.score-a.score||a.entry.name.localeCompare(b.entry.name)).slice(0,limit).map(x=>x.entry);
}
// A bounded safeguard, not a general natural-language negation parser.
function prohibitionSegments(task){
 const start=/\b(?:do\s+not|don['’]t|never|not\s+a)\b/ig;
 const boundary=/[.,;:!?\n]|\b(?:but|instead|however|yet|rather)\b/i;
 const positive=[],negative=[];let cursor=0,match;
 while((match=start.exec(task))){
  const tail=task.slice(start.lastIndex),endMatch=boundary.exec(tail);
  const end=endMatch?start.lastIndex+endMatch.index:task.length;
  positive.push(task.slice(cursor,match.index));
  negative.push(task.slice(match.index,end));
  cursor=end;start.lastIndex=end;
 }
 positive.push(task.slice(cursor));
 return {positive,negative};
}
function matchingRules(rules,segments,rawTask){
 const matches=(pattern)=>segments.some(segment=>new RegExp(pattern,'i').test(segment));
 return rules.filter(r=>r.when_any.some(matches)&&r.when_all.every(matches)
  &&!r.unless_any.some(matches)
  // These two exclusions intentionally use a negative constraint as a mode signal.
  &&!(['evidence-find-studies-2','evidence-evidence-answer-34'].includes(r.id)
   &&/\b(?:do\s+not|don['’]t|never)\s+search\b/i.test(rawTask)))
  .sort((a,b)=>b.priority-a.priority||a.id.localeCompare(b.id));
}
export async function route(task){
 task=text(task,'task');const entries=await catalog();const aliases=await json('catalog/aliases.json');
 const key=task.replace(/^[$/]/,'').toLowerCase();const exact=entries.find(x=>x.name===(aliases[key]||key));
 const rules=await json('catalog/routes.json');
 const matches=matchingRules(rules,[task],task);
 const {positive,negative}=prohibitionSegments(task);
 if(!exact&&negative.length){
  const affirmative=matchingRules(rules,positive,task);
  const competing=matches.filter(r=>r.priority===matches[0]?.priority);
  const negatedTrigger=competing.some(r=>r.when_any.some(p=>negative.some(s=>new RegExp(p,'i').test(s))));
  const supporting=new Set(competing.flatMap(r=>r.support).map(name=>aliases[name]||name));
  const excludedSupport=rules.some(r=>supporting.has(aliases[r.primary]||r.primary)
   &&r.when_any.some(p=>negative.some(s=>/^\b(?:do\s+not|don['’]t|never)\s+(?:create|use|generate|write|make|produce)\b/i.test(s)
    &&new RegExp(p,'i').test(s))));
  if(!matches.length||!affirmative.length||matches[0].id!==affirmative[0].id||negatedTrigger||excludedSupport){
   return {task,skills:[entries.find(x=>x.name==='research-assistant')],selection:'clarify',matched_rule:null,
    needs_clarification:true,alternatives:[],contract:'docs/INTEGRATION.md',
    execution_status:'Instruction routing only; no research, external service or model has been executed.'};
  }
 }
 let names=[],selection='rules';
 if(exact){names=[exact.name];selection=aliases[key]?'legacy-alias':'explicit-name';}
 else if(/^(help|capabilities|onboarding|what can academic research assistant do)[?.!]*$/i.test(task)){names=['research-assistant'];selection='onboarding';}
 else if(matches.length)names=[matches[0].primary,...matches[0].support];
 else {names=(await search(task,5)).map(x=>x.name);selection=names.length?'candidates':'clarify';}
 if(!names.length)names=['research-assistant'];
 const skills=[...new Set(names.map(x=>aliases[x]||x))].map(name=>entries.find(x=>x.name===name)).filter(Boolean);
 const competing=matches.filter(x=>x.priority===matches[0]?.priority).map(x=>aliases[x.primary]||x.primary);
 const annotationOverlap=!exact&&/annotated bibliograph|word annotations?|annotations?.{0,35}(sources?|papers?|methods)/i.test(task)
  &&!(/synthesis matrix|thematic review|verified.{0,20}(reference|citation) fields|verified bibliography|gather.{0,25}fields|slides?|deck/i.test(task));
 if(annotationOverlap&&['scholar-literature-review','evidence-citations-and-references'].includes(skills[0]?.name)){
  competing.push('scholar-literature-review','evidence-citations-and-references');
 }
 return {task,skills,selection,matched_rule:matches[0]?.id||null,
  needs_clarification:selection==='candidates'||selection==='clarify'||(!exact&&new Set(competing).size>1),
  alternatives:[...new Set(competing)].filter(x=>x!==skills[0]?.name),
  contract:'docs/INTEGRATION.md',execution_status:'Instruction routing only; no research, external service or model has been executed.'};
}
export async function readText(relative,offset=0,max_chars=16000){
 integer(offset,0,10000000,'offset');integer(max_chars,1,64000,'max_chars');
 const allowed=new Set(await publicFiles());
 const normalized=text(relative,'path',1000).replaceAll('\\','/').replace(/^\.\//,'');
 const target=await contained(normalized);
 if(!allowed.has(normalized))throw Error('Path is not a public runtime resource');
 const stat=await fs.stat(target);if(!stat.isFile()||stat.size>8*1024*1024)throw Error('Resource is not a readable text file or exceeds 8 MiB');
 const bytes=await fs.readFile(target);let value;
 try{value=new TextDecoder('utf-8',{fatal:true}).decode(bytes);}catch{throw Error('Binary resource; use an appropriate local viewer');}
 if(value.includes('\0'))throw Error('Binary resource; use an appropriate local viewer');
 const page=[];let total_chars=0;
 for(const character of value){
  if(total_chars>=offset&&total_chars<offset+max_chars)page.push(character);
  total_chars++;
 }
 return {path:normalized,text:page.join(''),total_chars,next_offset:offset+max_chars<total_chars?offset+max_chars:null};
}
export const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
export async function verifySources(root=ROOT){
 const ledger=await contained('audit/review-118/file-mapping.json',root);
 const entries=JSON.parse(await fs.readFile(ledger,'utf8'));
 if(!Array.isArray(entries)||!entries.length)throw Error('Source preservation ledger is unavailable or empty');
 const report={verified:0,directories_verified:0,missing:[],mismatched:[]};
 for(const entry of entries){
  if(!entry||typeof entry!=='object'||typeof entry.preserved_at!=='string'||
     typeof entry.sha256!=='string'||!/^[a-f0-9]{64}$/i.test(entry.sha256))throw Error('Invalid source preservation ledger entry');
  let target;
  try{target=await contained(entry.preserved_at,root);}
  catch(error){if(error.code==='ENOENT'){report.missing.push(entry.preserved_at);continue;}throw error;}
  if(!(await fs.stat(target)).isFile()){report.missing.push(entry.preserved_at);continue;}
  if(hash(await fs.readFile(target))!==entry.sha256.toLowerCase())report.mismatched.push(entry.preserved_at);
  else report.verified++;
 }
 return {...report,passed:!report.missing.length&&!report.mismatched.length,
  scope:'Recorded original payloads only; not a publisher signature or research validation.'};
}
export async function indexFiles(root=ROOT){
 const entries=[];
 for(const rel of await publicFiles(root)){
  if(rel==='catalog/files.json')continue;
  const bytes=await fs.readFile(path.join(root,rel));entries.push({path:rel,bytes:bytes.length,sha256:hash(bytes)});
 }
 await fs.writeFile(path.join(root,'catalog/files.json'),JSON.stringify(entries,null,2)+'\n');
 return entries;
}
export async function verify(){
 const expected=await json('catalog/files.json');const failures=[];
 for(const entry of expected){
  try{const target=await contained(entry.path);if(hash(await fs.readFile(target))!==entry.sha256)failures.push({path:entry.path,reason:'hash differs'});}
  catch(error){failures.push({path:entry.path,reason:error.message});}
 }
 const known=new Set(expected.map(x=>x.path));const extra=(await publicFiles()).filter(x=>x!=='catalog/files.json'&&!known.has(x));
 return {passed:!failures.length&&!extra.length,verified:expected.length-failures.length,failures,unindexed:extra,
  scope:'Local consistency only, not a cryptographic publisher signature or research validation.'};
}
export function environment(){
 return {node:process.version,platform:process.platform,architecture:process.arch,executable:process.execPath,
  optional_python:'Python 3.10+ and component-specific libraries; not probed or installed by this call',
  external_services:'No credentials, research databases or paid model connection are configured by this package.'};
}
