import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {checkReferences} from '../tools/check_external_skills.mjs';

test('only checks explicit skill folders and reports missing and invalid files', async t => {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), 'ara-refs-'));
  t.after(() => fs.rm(root, {recursive:true, force:true}));
  const valid = path.join(root, 'valid'), invalid = path.join(root, 'invalid');
  await fs.mkdir(valid); await fs.writeFile(path.join(valid, 'SKILL.md'), 'private content');
  await fs.mkdir(invalid); await fs.mkdir(path.join(invalid, 'SKILL.md'));
  const report = await checkReferences({version:1, skills:[
    {name:'valid',path:valid}, {name:'missing',path:path.join(root,'missing')}, {name:'invalid',path:invalid}
  ]});
  assert.deepEqual(report.results.map(x => x.status), ['readable','unavailable','invalid-skill-file']);
  assert.ok(!JSON.stringify(report).includes('private content'));
});

test('rejects relative paths, duplicate names and unbounded lists', async () => {
  await assert.rejects(checkReferences({version:1,skills:[{name:'x',path:'relative'}]}));
  await assert.rejects(checkReferences({version:1,skills:[{name:'x',path:os.tmpdir()},{name:'x',path:os.tmpdir()}]}));
  await assert.rejects(checkReferences({version:1,skills:Array(101).fill({name:'x',path:os.tmpdir()})}));
});
