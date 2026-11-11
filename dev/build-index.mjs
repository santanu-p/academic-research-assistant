import {catalog,indexFiles,json} from '../lib/core.mjs';
const skills=await catalog();const names=new Set(skills.map(x=>x.name));
for(const rule of await json('catalog/routes.json')){
 if(!names.has(rule.primary)||rule.support.some(x=>!names.has(x)))throw Error('Unresolved routing destination: '+rule.id);
 for(const p of [...rule.when_any,...rule.when_all,...rule.unless_any])new RegExp(p,'i');
}
const files=await indexFiles();
console.log('Indexed '+skills.length+' canonical methods, two compatibility entries and '+files.length+' package files.');
