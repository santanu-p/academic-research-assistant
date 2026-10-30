import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
export const ROOT=fileURLToPath(new URL('../',import.meta.url));
export const RUNTIME_DIRS=['cli','lib','server','skills','catalog','docs','tools','workflows','examples','resources','.codex-plugin','.claude-plugin'];
export const RUNTIME_FILES=['package.json','plugin.json','mcp.json','.mcp.json','SKILL.md','README.md','LICENSE','THIRD_PARTY_NOTICES.md','CHANGELOG.md'];
const badParts=new Set(['.git','node_modules','__pycache__','.private-archive','.public-build','dist']);
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
 const actual=(await fs.readdir(path.join(root,'skills'),{withFileTypes:true})).filter(x=>x.isDirectory()).map(x=>x.name).sort();
 if(JSON.stringify(actual)!==JSON.stringify([...names].sort()))throw Error('Catalog and skill directories differ');
 return entries;
}
const stopWords=new Set(['a','an','and','are','as','at','be','by','for','from','in','is','it','me','my','of','on','or','our','that','the','these','this','those','to','was','were','with','your']);
const words=s=>new Set((s.toLowerCase().match(/[a-z0-9]+/g)||[]).filter(word=>!stopWords.has(word)));
const matchesKeyword=(query,term)=>new RegExp('(?<![\\p{L}\\p{N}_])'+term.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'(?![\\p{L}\\p{N}_])','iu').test(query);
export async function search(query,limit=12){
 query=text(query,'query');integer(limit,1,250,'limit');const entries=await catalog();
 const exact=entries.find(x=>x.name===query.replace(/^[$/]/,'').toLowerCase());
 if(exact)return [exact];
 const terms=words(query);
 return entries.map(entry=>{
  let score=0;for(const word of words(entry.name))if(terms.has(word))score+=4;
  for(const word of words(entry.description))if(terms.has(word))score++;
  for(const term of entry.keywords||[])if(matchesKeyword(query,term))score+=8;
  return {entry,score};
 }).filter(x=>x.score>0).sort((a,b)=>b.score-a.score||a.entry.name.localeCompare(b.entry.name)).slice(0,limit).map(x=>x.entry);
}
export async function route(task){
 task=text(task,'task');let skills;const entries=await catalog();
 const exclusion=/\b(?:do\s+not|don't|dont|never|avoid|without|no|use\s+no)\s+(?:(?:use|using)\s+)?(?:(?:a|an|the)\s+)?(?:academic\s+)?humani[sz](?:e|ing|ation|er)\b/gi;
 const remaining=task.replace(exclusion,' ');
 const excluded=remaining!==task;
 let clarification;
 if(excluded){
  const conflict=/\bhumani[sz](?:e|ing|ation|er)\b/i.test(remaining);
  const substantive=remaining.replace(/[^a-z0-9]+/gi,' ').trim();
  if(conflict||!substantive){
   skills=[];
   clarification='Please clarify the requested task while preserving the Humanizer exclusion.';
  }else{
   skills=(await search(substantive,12)).filter(x=>!['humanizer','academic-humanizer'].includes(x.name));
   if(!skills.length)skills=entries.filter(x=>x.name==='research-assistant');
  }
 }
 const exact=entries.find(x=>x.name===task.replace(/^[$/]/,'').toLowerCase());
 if(excluded){}else if(exact)skills=[exact];
 else if(/^(help|capabilities|onboarding|what can academic research assistant do)[?.!]*$/i.test(task)){
  skills=entries.filter(x=>x.name==='research-assistant');
 }else if(/\bhumani[sz](?:e|ing|ation)\b/i.test(task)){
  const general=/\b(email|blog|personal essay|social media post|letter)\b/i.test(task);
  const academic=/\b(manuscript|thesis|dissertation|abstract|rebuttal|proposal|grant|journal|paper|citations?|academic prose)\b/i.test(task);
  const primary=general||!academic?'humanizer':'academic-humanizer';
  const alternatives=await search(task,12);
  skills=[entries.find(x=>x.name===primary),...alternatives.filter(x=>x.name!==primary)];
 }else skills=await search(task,12);
 if(!skills.length)skills=entries.filter(x=>x.name==='research-assistant');
 return {task,skills,...(clarification?{clarification}:{}),contract:'docs/RESEARCH-CONTRACT.md',execution_status:'Instruction routing only; no research, external service or model has been executed.'};
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
 const characters=Array.from(value);
 return {path:normalized,text:characters.slice(offset,offset+max_chars).join(''),total_chars:characters.length,next_offset:offset+max_chars<characters.length?offset+max_chars:null};
}
export const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
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
