import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {checkHandoff} from '../tools/external_handoff.mjs';

const record = () => ({version:1, capabilities:[
  {id:'search',kind:'mcp-tool',host:'research host',status:'available',evidence:'Observed in host tool list'},
  {id:'review',kind:'skill',host:'research host',status:'unverified'}
], steps:[
  {id:'find',action:'Search using the registered tool',dependsOn:[],requires:['search'],status:'completed',evidence:'Search log in project'},
  {id:'assess',action:'Use the separately installed review skill',dependsOn:['find'],requires:['review'],status:'pending'},
  {id:'write',action:'Synthesize checked sources',dependsOn:['assess'],requires:[],status:'pending'}
]});

test('tracks recorded prerequisites without treating unverified access as available', () => {
  const r = record();
  assert.deepEqual(checkHandoff(r).results.map(x => [x.assessment,x.issues]), [
    ['recorded-completed',[]], ['blocked',['capability:review']], ['blocked',['dependency:assess']]
  ]);
  r.capabilities[1].status = 'available'; r.capabilities[1].evidence = 'Visible in host';
  assert.equal(checkHandoff(r).results[1].assessment, 'ready-for-host');
  r.steps[1].status = 'completed'; r.steps[1].evidence = 'Appraisal notes';
  assert.equal(checkHandoff(r).results[2].assessment, 'ready-for-host');
});

test('flags inconsistent completion and rejects invented or cyclic dependencies', () => {
  const r = record(); r.steps[1].status = 'completed'; r.steps[1].evidence = 'Notes';
  assert.equal(checkHandoff(r).results[1].assessment, 'completed-needs-review');
  assert.equal(checkHandoff(r).results[2].assessment, 'blocked');
  r.steps[0].dependsOn = ['write'];
  assert.throws(() => checkHandoff(r), /cycle/);
  r.steps[0].dependsOn = ['absent'];
  assert.throws(() => checkHandoff(r), /Unknown/);
});

test('requires evidence for available capabilities and completed steps', () => {
  const r = record(); delete r.capabilities[0].evidence;
  assert.throws(() => checkHandoff(r), /Invalid capability/);
  r.capabilities[0].evidence = 'Visible'; delete r.steps[0].evidence;
  assert.throws(() => checkHandoff(r), /Invalid step/);
});

test('CLI reports inconsistent completion without running the recorded action', async t => {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), 'ara-handoff-'));
  t.after(() => fs.rm(root, {recursive:true, force:true}));
  const r = record(); r.steps[1].status = 'completed'; r.steps[1].evidence = 'Notes';
  r.steps[1].action = 'this is a description, never a command';
  const file = path.join(root, 'handoff.json');
  await fs.writeFile(file, JSON.stringify(r));
  const cli = fileURLToPath(new URL('../tools/external_handoff.mjs', import.meta.url));
  const run = spawnSync(process.execPath, [cli, file], {encoding:'utf8'});
  assert.equal(run.status, 1);
  assert.equal(JSON.parse(run.stdout).results[1].assessment, 'completed-needs-review');
  assert.equal(run.stderr, '');
});
