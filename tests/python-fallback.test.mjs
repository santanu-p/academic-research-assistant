import test from 'node:test';
import assert from 'node:assert/strict';
import * as dependencies from '../lib/dependencies.mjs';

test('Python module probing falls back when an earlier candidate is unusable',async t=>{
 const current=await dependencies.dependencyStatus();
 if(current.python_probe.status!=='ok')return t.skip('No usable local Python interpreter');
 assert.equal(typeof dependencies.probePython,'function','fallback probing is implemented');
 // Node cannot run the fixed Python script, but the next candidate is the real
 // locally detected Python. This exercises two real child processes.
 const result=await dependencies.probePython([process.execPath,current.python_probe.executable]);
 assert.equal(result.python_probe.status,'ok');
 assert.equal(result.python_probe.executable,current.python_probe.executable);
 assert.equal(result.modules.json,true);
});
