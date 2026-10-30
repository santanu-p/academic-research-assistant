#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import {constants} from 'node:fs';
import {ROOT,RUNTIME_DIRS,catalog,search,route,readText,environment,verify,publicFiles,indexFiles,json} from '../lib/core.mjs';
const HELP='Academic Research Assistant\n\nUsage:\n  academic-research-assistant list [--json]\n  academic-research-assistant route "research task"\n  academic-research-assistant read skills/name/SKILL.md\n  academic-research-assistant doctor\n  academic-research-assistant verify\n  academic-research-assistant mcp\n  academic-research-assistant export --host codex|claude|antigravity|generic|codex-skill|claude-skill|antigravity-skill --target NEW_DIRECTORY\n  academic-research-assistant install --host HOST --target NEW_DIRECTORY\n  academic-research-assistant config --host codex|claude|antigravity|generic --root INSTALLED_BUNDLE\n\nInstall/export copy files only. They do not edit account settings, install dependencies or publish anything.\nClaude and Antigravity plugin exports contain one complete outer skill; their JSON result identifies the nested runtime bundle.\nAntigravity MCP is optional: config prints absolute paths for its mcp_config.json after the final bundle location is known.\n';
function options(args,allowed){
 const out={};for(let i=0;i<args.length;i++){
  const name=args[i];if(!allowed.includes(name)||out[name]!==undefined)throw Error('Unknown or repeated option: '+name);
  if(name==='--json'){out[name]=true;continue;}
  const value=args[++i];if(!value||value.startsWith('--'))throw Error('Missing value for '+name);out[name]=value;
 }return out;
}
function absoluteRoot(root){if(!root)throw Error('--root is required');return path.resolve(root);}
function serverConfig(root){return {command:'node',args:[path.join(root,'server/mcp.mjs')]};}
// The next-step commands target PowerShell on Windows and POSIX sh elsewhere.
function shellQuote(value){return process.platform==='win32'?"'"+value.replaceAll("'","''")+"'":"'"+value.replaceAll("'","'\\''")+"'";}
async function resolvedTarget(target){
 let parent=path.dirname(target);const missing=[path.basename(target)];
 for(;;){
  try{return path.join(await fs.realpath(parent),...missing);}
  catch(error){
   if(error.code!=='ENOENT')throw error;
   const next=path.dirname(parent);if(next===parent)throw error;
   missing.unshift(path.basename(parent));parent=next;
  }
 }
}
function pathKey(value){const normalized=path.normalize(value);return process.platform==='win32'?normalized.toLowerCase():normalized;}
function inside(target,base){const rel=path.relative(pathKey(base),pathKey(target));return rel===''||(!path.isAbsolute(rel)&&rel!=='..'&&!rel.startsWith('..'+path.sep));}
async function exportBundle(host,target){
 if(!['codex','claude','antigravity','generic','codex-skill','claude-skill','antigravity-skill'].includes(host))throw Error('Choose --host codex, claude, antigravity, generic, codex-skill, claude-skill or antigravity-skill');
 if(!target)throw Error('--target is required');
 const dest=path.resolve(target);
 const realRoot=await fs.realpath(ROOT);const realDest=await resolvedTarget(dest);
 if(pathKey(realDest)===pathKey(realRoot)||RUNTIME_DIRS.some(x=>inside(realDest,path.join(realRoot,x))))throw Error('Target overlaps package runtime files');
 const sourceCheck=await verify();if(!sourceCheck.passed)throw Error('Source verification failed; run verify for details before exporting');
 await catalog();const files=await publicFiles();
 try{await fs.lstat(dest);throw Error('Target already exists; choose a new directory');}catch(error){if(error.code!=='ENOENT')throw error;}
 await fs.mkdir(path.dirname(dest),{recursive:true});
 await fs.mkdir(dest); // exclusive: existing files are never overwritten
 const wrapper=host==='claude'||host==='antigravity';
 const instructionOnly=wrapper||host.endsWith('-skill');
 const bundle=host==='codex'?path.join(dest,'plugins/academic-research-assistant'):
  wrapper?path.join(dest,'skills/academic-research-assistant'):dest;
 await fs.mkdir(bundle,{recursive:true});
 for(const rel of files){
  // Keep archived originals intact; omit only live plugin-discovery markers.
  if(instructionOnly&&(['plugin.json','mcp.json','.mcp.json'].includes(rel)||/^(\.claude-plugin|\.codex-plugin)\//.test(rel)))continue;
  const to=path.join(bundle,rel);await fs.mkdir(path.dirname(to),{recursive:true});
  await fs.copyFile(path.join(ROOT,rel),to,constants.COPYFILE_EXCL);
 }
 const packageInfo=await json('package.json',bundle);
 delete packageInfo.scripts;await fs.writeFile(path.join(bundle,'package.json'),JSON.stringify(packageInfo,null,2)+'\n');
 if(wrapper){
  const manifest={name:packageInfo.name,description:packageInfo.description};
  if(host==='claude'){
   manifest.version=packageInfo.version;
   manifest.author={name:'Academic Research Assistant contributors'};
   const wrapperReadme=`# Academic Research Assistant\n\nThis plugin provides research planning, evidence review, academic writing, scientific communication, and document preparation instructions for compatible assistants. The bundled methods guide an assistant; external sources, research tools, credentials, and verification still depend on the host and the user's setup. Read the [complete bundle guide](skills/${packageInfo.name}/README.md) for installation, usage, and limitations.\n\nThe bundle includes third-party material with its own terms. Read [LICENSE](LICENSE) and [third-party notices](THIRD_PARTY_NOTICES.md) before redistribution. Exporting the plugin does not configure external services or perform research.\n`;
   await fs.writeFile(path.join(dest,'README.md'),wrapperReadme);
   for(const notice of ['LICENSE','THIRD_PARTY_NOTICES.md'])await fs.copyFile(path.join(bundle,notice),path.join(dest,notice),constants.COPYFILE_EXCL);
   await fs.mkdir(path.join(dest,'.claude-plugin'));
   await fs.writeFile(path.join(dest,'.claude-plugin/plugin.json'),JSON.stringify(manifest,null,2)+'\n');
   await fs.writeFile(path.join(dest,'.mcp.json'),JSON.stringify({mcpServers:{[packageInfo.name]:{command:'node',args:['${CLAUDE_PLUGIN_ROOT}/skills/academic-research-assistant/server/mcp.mjs']}}},null,2)+'\n');
  }else await fs.writeFile(path.join(dest,'plugin.json'),JSON.stringify(manifest,null,2)+'\n');
 }
 if(host==='codex'){
  const file=path.join(dest,'.agents/plugins/marketplace.json');await fs.mkdir(path.dirname(file),{recursive:true});
  await fs.writeFile(file,JSON.stringify({name:'academic-research-assistant-local',plugins:[{name:'academic-research-assistant',
   source:{source:'local',path:'./plugins/academic-research-assistant'},policy:{installation:'AVAILABLE',authentication:'ON_INSTALL'},category:'Education & Research'}]},null,2)+'\n');
 }
 await indexFiles(bundle);
 const next=host==='codex'?['codex plugin marketplace add '+shellQuote(dest),'codex plugin add academic-research-assistant@academic-research-assistant-local']:
  host==='claude'?['claude plugin validate '+shellQuote(dest),'claude --plugin-dir '+shellQuote(dest)]:
  host==='antigravity'?['agy plugin install '+shellQuote(dest),'agy plugin list --json',
   'Optional MCP: use the actual installed nested bundle path with config --host antigravity --root INSTALLED_BUNDLE, then apply the JSON through the host MCP manager. Regenerate after relocation.']:
  host.endsWith('-skill')?['Place this complete directory at the host skill path, then restart/reload that host.','The outer skill reads the nested canonical methods; MCP registration remains optional and explicit.']:
  ['Read SKILL.md or configure an MCP-capable host with:','node '+shellQuote(path.join(bundle,'cli/ara.mjs'))+' config --host generic --root '+shellQuote(bundle)];
 return {host,target:dest,bundle,next,next_shell:process.platform==='win32'?'PowerShell':'POSIX sh',host_settings_changed:false,
  ...(wrapper?{skill_entrypoint:'academic-research-assistant',wrapper_root_agents_directory_included:false}:{}),
  ...(host==='antigravity'?{mcp_bundled:false,mcp_configuration:'Optional absolute-path configuration after installation; no plugin-root interpolation assumed.'}:{})};
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
  if(!['codex','claude','antigravity','generic'].includes(host))throw Error('Choose --host codex, claude, antigravity or generic');
  await fs.access(path.join(root,'server/mcp.mjs'));
  if(host==='codex'){console.log('[mcp_servers.academic-research-assistant]\ncommand = "node"\nargs = ['+JSON.stringify(path.join(root,'server/mcp.mjs'))+']');return;}
  value={mcpServers:{'academic-research-assistant':serverConfig(root)}};
 }else throw Error('Unknown command: '+cmd+'\nUse --help');
 console.log(JSON.stringify(value,null,2));
}
main().catch(error=>{console.error('academic-research-assistant: '+error.message);process.exitCode=1;});
