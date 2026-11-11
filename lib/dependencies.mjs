import fs from 'node:fs/promises';
import {constants} from 'node:fs';
import path from 'node:path';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';

const execute=promisify(execFile);
const commands=['latexmk','pdflatex','xelatex','lualatex','tectonic','biber','pandoc','soffice','pdftoppm','latexdiff','bash','claude','codex','node','Rscript'];
const modules=['json','numpy','scipy','pandas','matplotlib','sklearn','PIL','fitz','pptx','yaml','jsonschema'];
const pythonCode='import importlib.util,json\nnames='+JSON.stringify(modules)+'\nr={}\nfor n in names:\n try: r[n]=importlib.util.find_spec(n) is not None\n except Exception: r[n]=None\nprint(json.dumps(r))';

async function findExecutable(name,env=process.env,{python=false}={}){
 const folders=(env.PATH||'').split(path.delimiter).filter(Boolean).map(x=>x.replace(/^"|"$/g,''));
 const extensions=process.platform==='win32'?(python?['.EXE','.COM']:(env.PATHEXT||'.COM;.EXE;.BAT;.CMD').split(';')):[''];
 for(const dir of folders){
  for(const ext of extensions){
   const candidate=path.resolve(dir,name+ext);
   try{
    await fs.access(candidate,process.platform==='win32'?constants.F_OK:constants.X_OK);
    if((await fs.stat(candidate)).isFile())return candidate;
   }catch{}
  }
 }
 return null;
}

export async function probePython(candidates,env=process.env){
 const unknown=Object.fromEntries(modules.map(name=>[name,null]));
 const unique=[...new Set(candidates.filter(Boolean))];
 if(!unique.length)return {modules:unknown,python_probe:{status:'unavailable',executable:null}};
 const deadline=Date.now()+5000;
 for(let i=0;i<unique.length;i++){
  const python=unique[i],remaining=deadline-Date.now();
  if(remaining<=0)break;
  try{
   const timeout=Math.max(1,Math.floor(remaining/(unique.length-i)));
   const {stdout}=await execute(python,['-B','-c',pythonCode],{env,timeout,maxBuffer:65536,windowsHide:true});
   const values=JSON.parse(stdout);
   if(!values||typeof values!=='object'||modules.some(name=>![true,false,null].includes(values[name])))throw Error('Unexpected module report');
   return {modules:Object.fromEntries(modules.map(name=>[name,values[name]])),python_probe:{status:'ok',executable:python}};
  }catch{}
 }
 return {modules:unknown,python_probe:{status:'error',executable:null}};
}

export async function dependencyStatus(env=process.env){
 const found=await Promise.all(commands.map(name=>findExecutable(name,env)));
 const commandStatus=Object.fromEntries(commands.map((name,index)=>[name,Boolean(found[index])]));
 const candidates=await Promise.all(['python','python3'].map(name=>findExecutable(name,env,{python:true})));
 const result=await probePython(candidates,env);
 return {commands:commandStatus,...result,
  scope:'Executable and module presence only; does not establish compatibility, successful execution, licenses or authentication.'};
}
