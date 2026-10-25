#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import {constants} from 'node:fs';
import {ROOT,RUNTIME_DIRS,catalog,search,route,readText,environment,verify,publicFiles,indexFiles,json} from '../lib/core.mjs';
const HELP='Academic Research Assistant\n\nUsage:\n  academic-research-assistant list [--json]\n  academic-research-assistant route "research task"\n  academic-research-assistant read skills/name/SKILL.md\n  academic-research-assistant doctor\n  academic-research-assistant verify\n  academic-research-assistant mcp\n  academic-research-assistant export --host codex|claude|generic|codex-skill|claude-skill --target NEW_DIRECTORY\n  academic-research-assistant install --host HOST --target NEW_DIRECTORY\n  academic-research-assistant config --host codex|claude|generic --root INSTALLED_BUNDLE\n\nInstall/export copy files only. They do not edit account settings, install dependencies or publish anything.\n';
function options(args,allowed){
 const out={};for(let i=0;i<args.length;i++){
  const name=args[i];if(!allowed.includes(name)||out[name]!==undefined)throw Error('Unknown or repeated option: '+name);
  if(name==='--json'){out[name]=true;continue;}
  const value=args[++i];if(!value||value.startsWith('--'))throw Error('Missing value for '+name);out[name]=value;
 }return out;
}
function absoluteRoot(root){if(!root)throw Error('--root is required');return path.resolve(root);}
function serverConfig(root){return {command:'node',args:[path.join(root,'server/mcp.mjs')]};}
async function exportBundle(host,target){
 if(!['codex','claude','generic','codex-skill','claude-skill'].includes(host))throw Error('Choose --host codex, claude, generic, codex-skill or claude-skill');
 if(!target)throw Error('--target is required');
 const dest=path.resolve(target);
 if(dest===ROOT||RUNTIME_DIRS.some(x=>dest===path.join(ROOT,x)||dest.startsWith(path.join(ROOT,x)+path.sep)))throw Error('Target overlaps package runtime files');
 await catalog();const files=await publicFiles();
 try{await fs.lstat(dest);throw Error('Target already exists; choose a new directory');}catch(error){if(error.code!=='ENOENT')throw error;}
 await fs.mkdir(path.dirname(dest),{recursive:true});
 await fs.mkdir(dest); // exclusive: existing files are never overwritten
 const bundle=host==='codex'?path.join(dest,'plugins/academic-research-assistant'):dest;
 await fs.mkdir(bundle,{recursive:true});
 for(const rel of files){
  const to=path.join(bundle,rel);await fs.mkdir(path.dirname(to),{recursive:true});
  await fs.copyFile(path.join(ROOT,rel),to,constants.COPYFILE_EXCL);
 }
 const packageInfo=await json('package.json',bundle);
 delete packageInfo.scripts;await fs.writeFile(path.join(bundle,'package.json'),JSON.stringify(packageInfo,null,2)+'\n');
 if(host==='codex'){
  const file=path.join(dest,'.agents/plugins/marketplace.json');await fs.mkdir(path.dirname(file),{recursive:true});
  await fs.writeFile(file,JSON.stringify({name:'academic-research-assistant-local',plugins:[{name:'academic-research-assistant',
   source:{source:'local',path:'./plugins/academic-research-assistant'},policy:{installation:'AVAILABLE',authentication:'ON_INSTALL'},category:'Education & Research'}]},null,2)+'\n');
 }
 await indexFiles(bundle);
 const next=host==='codex'?['codex plugin marketplace add '+JSON.stringify(dest),'codex plugin add academic-research-assistant@academic-research-assistant-local']:
  host==='claude'?['claude --plugin-dir '+JSON.stringify(bundle)]:
  host.endsWith('-skill')?['Place this complete directory at the host skill path, then restart/reload that host.','The outer skill reads the nested canonical methods; MCP registration remains optional and explicit.']:
  ['Read SKILL.md or configure an MCP-capable host with:','node '+JSON.stringify(path.join(bundle,'cli/ara.mjs'))+' config --host generic --root '+JSON.stringify(bundle)];
 return {host,target:dest,bundle,next,host_settings_changed:false};
}
async function main(){
 const [cmd,...args]=process.argv.slice(2);let value;
 if(!cmd||cmd==='--help'||cmd==='help'){process.stdout.write(HELP);return;}
 if(cmd==='--version'){console.log((await json('package.json')).version);return;}
 if(cmd==='mcp'){
  if(args.length)throw Error('mcp takes no arguments');const {serve}=await import('../server/mcp.mjs');await serve();return;
 }
 if(cmd==='list'){
  options(args,['--json']);value=await catalog();
  if(!args.includes('--json')){console.log(value.map(x=>x.name+' — '+x.description).join('\n'));return;}
 }else if(cmd==='route'){
  if(!args.length||args.some(x=>x.startsWith('--')))throw Error('Provide a task as text');value=await route(args.join(' '));
 }else if(cmd==='read'){
  if(args.length!==1)throw Error('read requires one public relative path');value=await readText(args[0],0,64000);
 }else if(cmd==='doctor'){
  if(args.length)throw Error('doctor takes no arguments');value={...environment(),skills:(await catalog()).length};
 }else if(cmd==='verify'){
  if(args.length)throw Error('verify takes no arguments');value=await verify();if(!value.passed)process.exitCode=1;
 }else if(cmd==='install'||cmd==='export'){
  const opts=options(args,['--host','--target']);value=await exportBundle(opts['--host'],opts['--target']);
 }else if(cmd==='config'){
  const opts=options(args,['--host','--root']);const host=opts['--host'];const root=absoluteRoot(opts['--root']);
  if(!['codex','claude','generic'].includes(host))throw Error('Choose --host codex, claude or generic');
  await fs.access(path.join(root,'server/mcp.mjs'));
  if(host==='codex'){console.log('[mcp_servers.academic-research-assistant]\ncommand = "node"\nargs = ['+JSON.stringify(path.join(root,'server/mcp.mjs'))+']');return;}
  value={mcpServers:{'academic-research-assistant':serverConfig(root)}};
 }else throw Error('Unknown command: '+cmd+'\nUse --help');
 console.log(JSON.stringify(value,null,2));
}
main().catch(error=>{console.error('academic-research-assistant: '+error.message);process.exitCode=1;});
