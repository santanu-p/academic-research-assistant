import {ROOT,json,search,route,readText,verify,environment} from '../lib/core.mjs';
import {pathToFileURL} from 'node:url';
const protocols=['2025-06-18','2025-11-25'];
const definition=(name,description,properties={},required=[])=>({name,description,inputSchema:{type:'object',properties,required,additionalProperties:false},annotations:{readOnlyHint:true,destructiveHint:false,openWorldHint:false}});
const TOOLS=[
 definition('search_capabilities','Find canonical research instructions; does not execute them.',{query:{type:'string',minLength:1},limit:{type:'integer',minimum:1,maximum:250}},['query']),
 definition('route_task','Select skills for a research task and report execution boundaries.',{task:{type:'string',minLength:1}},['task']),
 definition('read_resource','Read UTF-8 public package resources with pagination measured in Unicode code points.',{path:{type:'string'},offset:{type:'integer',minimum:0},max_chars:{type:'integer',minimum:1,maximum:64000}},['path']),
 definition('environment_status','Report this runtime and declared optional requirements; no commands or network probes.'),
 definition('verify_package','Compare the public bundle with its local SHA-256 inventory; not a research or publisher attestation.'),
];
const funcs={search_capabilities:({query,limit})=>search(query,limit),route_task:({task})=>route(task),
 read_resource:({path,offset,max_chars})=>readText(path,offset,max_chars),environment_status:()=>environment(),verify_package:()=>verify()};
const object=x=>x!==null&&typeof x==='object'&&!Array.isArray(x);
const validId=x=>typeof x==='string'||Number.isSafeInteger(x);
const error=(id,code,message)=>({jsonrpc:'2.0',id:validId(id)?id:null,error:{code,message}});
export async function handle(request){
 if(!object(request)||request.jsonrpc!=='2.0'||typeof request.method!=='string'||!request.method)return error(request?.id,-32600,'Invalid Request');
 if(!Object.hasOwn(request,'id'))return null;
 const id=request.id;if(!validId(id))return error(null,-32600,'Invalid request identifier');
 const params=Object.hasOwn(request,'params')?request.params:{};if(!object(params))return error(id,-32602,'params must be an object');
 let result;
 if(request.method==='initialize'){
  if(typeof params.protocolVersion!=='string'||!params.protocolVersion||!object(params.capabilities)||!object(params.clientInfo)
     ||typeof params.clientInfo.name!=='string'||!params.clientInfo.name||typeof params.clientInfo.version!=='string'||!params.clientInfo.version)return error(id,-32602,'Missing or invalid initialize fields');
  const version=(await json('package.json')).version;
  result={protocolVersion:protocols.includes(params.protocolVersion)?params.protocolVersion:protocols.at(-1),
   capabilities:{tools:{listChanged:false}},serverInfo:{name:'academic-research-assistant',version},
   instructions:'Read the selected canonical skills and research contract. Local read-only tools do not perform research or configure external services.'};
 }else if(request.method==='ping')result={};
 else if(request.method==='tools/list')result={tools:TOOLS};
 else if(request.method==='tools/call'){
  if(!Object.hasOwn(funcs,params.name))return error(id,-32602,'Unknown tool');
  const args=Object.hasOwn(params,'arguments')?params.arguments:{};if(!object(args))return error(id,-32602,'Tool arguments must be an object');
  const schema=TOOLS.find(x=>x.name===params.name).inputSchema;
  if(Object.keys(args).some(x=>!Object.hasOwn(schema.properties,x))||schema.required.some(x=>!Object.hasOwn(args,x)))return error(id,-32602,'Invalid tool argument names');
  try{const value=await funcs[params.name](args);result={content:[{type:'text',text:JSON.stringify(value)}],isError:false};}
  catch(e){result={content:[{type:'text',text:e.message}],isError:true};}
 }else return error(id,-32601,'Method not found');
 return {jsonrpc:'2.0',id,result};
}
export async function serve(input=process.stdin,output=process.stdout){
 let buffer=Buffer.alloc(0),dropping=false;
 const max=1024*1024;
 async function line(bytes){
  let response;
  try{response=await handle(JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(bytes)));}
  catch(e){response=error(null,e instanceof SyntaxError||e instanceof TypeError?-32700:-32603,e instanceof SyntaxError||e instanceof TypeError?'Parse error':'Internal error');}
  if(response)output.write(JSON.stringify(response)+'\n');
 }
 for await(const chunk of input){
  let bytes=Buffer.isBuffer(chunk)?chunk:Buffer.from(chunk);
  while(bytes.length){
   const end=bytes.indexOf(10);const part=end<0?bytes:bytes.subarray(0,end);
   if(!dropping&&buffer.length+part.length>max){dropping=true;buffer=Buffer.alloc(0);}
   if(!dropping)buffer=Buffer.concat([buffer,part]);
   if(end<0)break;
   if(dropping)output.write(JSON.stringify(error(null,-32600,'Message exceeds 1 MiB'))+'\n');
   else await line(buffer);
   buffer=Buffer.alloc(0);dropping=false;bytes=bytes.subarray(end+1);
  }
 }
 if(dropping)output.write(JSON.stringify(error(null,-32600,'Message exceeds 1 MiB'))+'\n');
 else if(buffer.length)await line(buffer);
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
 serve().catch(error=>{console.error('MCP transport: '+error.message);process.exitCode=1;});
}
