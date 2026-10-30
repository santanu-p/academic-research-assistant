#!/usr/bin/env node
// Check a user-maintained coordination record. No host discovery or execution.
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';

export function checkHandoff(record) {
  if (!record || record.version !== 1 || !Array.isArray(record.capabilities) ||
      !Array.isArray(record.steps) || record.capabilities.length > 100 || record.steps.length > 100)
    throw new Error('Expected version 1 with capabilities and steps arrays of at most 100 entries');
  const validId = value => typeof value === 'string' && /^[a-zA-Z0-9][a-zA-Z0-9._-]{0,79}$/.test(value);
  const meaningful = value => typeof value === 'string' && value.trim().length > 0 && value.length <= 1000;
  const capabilities = new Map();
  for (const cap of record.capabilities) {
    if (!cap || !validId(cap.id) || capabilities.has(cap.id) ||
        !['skill', 'mcp-tool'].includes(cap.kind) || !meaningful(cap.host) ||
        !['unverified', 'available', 'unavailable'].includes(cap.status) ||
        (cap.status === 'available' && !meaningful(cap.evidence)))
      throw new Error('Invalid capability: unique id, kind, host, status and evidence for available are required');
    capabilities.set(cap.id, cap);
  }
  const steps = new Map();
  for (const step of record.steps) {
    if (!step || !validId(step.id) || steps.has(step.id) || !meaningful(step.action) ||
        !Array.isArray(step.dependsOn) || !Array.isArray(step.requires) ||
        new Set(step.dependsOn).size !== step.dependsOn.length || new Set(step.requires).size !== step.requires.length ||
        !['pending', 'completed'].includes(step.status) ||
        (step.status === 'completed' && !meaningful(step.evidence)))
      throw new Error('Invalid step: unique id, action, dependency arrays, status and evidence for completed are required');
    steps.set(step.id, step);
  }
  for (const step of steps.values()) {
    if (step.dependsOn.some(id => !steps.has(id)) || step.requires.some(id => !capabilities.has(id)))
      throw new Error(`Unknown dependency or capability in step ${step.id}`);
  }
  const visited = new Set(), visiting = new Set();
  function visit(id) {
    if (visiting.has(id)) throw new Error('Step dependency cycle');
    if (visited.has(id)) return;
    visiting.add(id);
    for (const dep of steps.get(id).dependsOn) visit(dep);
    visiting.delete(id); visited.add(id);
  }
  for (const id of steps.keys()) visit(id);
  const assessments = new Map();
  function assess(step) {
    if (assessments.has(step.id)) return assessments.get(step.id);
    const incomplete = step.dependsOn.filter(id => assess(steps.get(id)).assessment !== 'recorded-completed');
    const unavailable = step.requires.filter(id => capabilities.get(id).status !== 'available');
    const issues = [...incomplete.map(id => `dependency:${id}`), ...unavailable.map(id => `capability:${id}`)];
    const result = {id:step.id, status:step.status, assessment:step.status === 'completed'
      ? (issues.length ? 'completed-needs-review' : 'recorded-completed')
      : (issues.length ? 'blocked' : 'ready-for-host'), issues};
    assessments.set(step.id, result);
    return result;
  }
  const results = [...steps.values()].map(assess);
  return {version:1, results, note:'Based only on user-supplied claims; does not discover, invoke, or verify a host, capability, evidence, or outcome.'};
}

async function main() {
  if (process.argv.length !== 3 || !path.isAbsolute(process.argv[2]))
    throw new Error('Usage: node tools/external_handoff.mjs /absolute/path/to/handoff.json');
  const report = checkHandoff(JSON.parse(await fs.readFile(process.argv[2], 'utf8')));
  console.log(JSON.stringify(report, null, 2));
  if (report.results.some(step => step.assessment === 'completed-needs-review')) process.exitCode = 1;
}
if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href)
  main().catch(error => { console.error(error.message); process.exitCode = 1; });
