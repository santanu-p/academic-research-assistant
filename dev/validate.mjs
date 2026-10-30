import fs from 'node:fs/promises';
import path from 'node:path';
import {ROOT,catalog,publicFiles,verify} from '../lib/core.mjs';
import {frontmatter,extraKeywords} from './build-catalog.mjs';
const failures=[];let checks=0,links=0;
function check(ok,message){checks++;if(!ok)failures.push(message);}
const read=rel=>fs.readFile(path.join(ROOT,rel),'utf8');
const pkg=JSON.parse(await read('package.json'));
check(pkg.version==='3.1.0'&&pkg.license==='MIT'&&pkg.private===false,'Expected publishable MIT package metadata');
check(Object.keys(pkg.dependencies||{}).length===0,'Runtime must have no Node dependencies');
check(!Object.keys(pkg.scripts||{}).some(x=>['install','postinstall','preinstall'].includes(x)),'Unexpected install hook');
const entries=await catalog();
const imported=JSON.parse(await read('docs/independent-skill-import.json'));
const draftNames=new Set(imported.map(item=>item.target_name));
check(imported.length===50&&entries.length===90,'Expected 38 existing skills, 50 independent drafts and two MIT humanizers');
check(!draftNames.has('latex-document-workflow')&&!entries.some(x=>x.name==='latex-document-workflow'),'Retired general skill remains in the draft');
check(!await fs.stat(path.join(ROOT,'skills/latex-document-workflow')).then(()=>true,()=>false),'Retired general skill directory remains in the draft');
check(JSON.stringify(entries.map(x=>x.name).sort())===JSON.stringify(Object.keys(extraKeywords).sort()),'Skill coverage differs from release plan');
for(const entry of entries){
 const f=frontmatter(await read(entry.path));
 check(f.name===entry.name&&f.description===entry.description,'Catalog metadata differs: '+entry.name);
 check(f.body.split(/\s+/).length>=(draftNames.has(entry.name)?150:250),'Skill is too brief: '+entry.name);
}
const files=await publicFiles();
for(const rel of files){
 if(rel.endsWith('.json')){try{JSON.parse(await read(rel));check(true,'');}catch{check(false,'Invalid JSON: '+rel);}}
 const originalHumanizerImage=/^resources\/upstream\/academic-humanizer-main\/assets\/(rednote-zh|x-en)\.png$/.test(rel);
 check(originalHumanizerImage||!/\.(zip|tgz|tar|gz|pyc|pdf|png|jpe?g)$/i.test(rel),'Generated or historical binary in runtime: '+rel);
 if(!rel.endsWith('.md'))continue;
 const raw=await read(rel);
 check(!/plugins_6adda4eb33a88191935589dfe7d8a506|D:[\\/]PLUGIN|C:[\\/]Users[\\/]psant|resources\/originals/i.test(raw),'Historical or machine-specific reference: '+rel);
 for(const match of raw.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)){
  let target=match[1].replace(/^<|>$/g,'').split('#')[0];
  if(!target||/^[a-z][a-z0-9+.-]*:/i.test(target))continue;
  target=target.split(/\s+["']/)[0];
  const dest=path.resolve(path.dirname(path.join(ROOT,rel)),decodeURIComponent(target));
  links++;
  check(dest.startsWith(ROOT)&&await fs.stat(dest).then(()=>true,()=>false),'Broken or escaping link in '+rel+': '+target);
 }
}
for(const rel of ['plugin.json','.codex-plugin/plugin.json','.claude-plugin/plugin.json']){
 const manifest=JSON.parse(await read(rel));check(manifest.name===pkg.name&&manifest.version===pkg.version,'Manifest disagreement: '+rel);
}
const codex=JSON.parse(await read('mcp.json')),claude=JSON.parse(await read('.mcp.json'));
check(codex.mcpServers[pkg.name].args[0]==='${PLUGIN_ROOT}/server/mcp.mjs','Codex MCP root placeholder');
check(claude.mcpServers[pkg.name].args[0]==='${CLAUDE_PLUGIN_ROOT}/server/mcp.mjs','Claude MCP root placeholder');
const integrity=await verify();check(integrity.passed,'Runtime integrity: '+JSON.stringify(integrity));
const report={version:pkg.version,skills:entries.length,runtimeFiles:files.length,localLinks:links,checks,failures};
await fs.mkdir(path.join(ROOT,'build'),{recursive:true});
await fs.writeFile(path.join(ROOT,'build/validation.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));if(failures.length)process.exitCode=1;
