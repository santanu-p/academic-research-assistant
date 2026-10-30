#!/usr/bin/env node
// Explicit, read-only preflight for separately installed skill folders.
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';

export async function checkReferences(config) {
  if (!config || config.version !== 1 || !Array.isArray(config.skills) || config.skills.length > 100)
    throw new Error('Expected version 1 and a skills array of at most 100 entries');
  const seen = new Set();
  for (const item of config.skills) {
    if (!item || typeof item.name !== 'string' || !item.name.trim() || item.name.length > 120 ||
        typeof item.path !== 'string' || !path.isAbsolute(item.path) || seen.has(item.name))
      throw new Error('Each skill needs a unique name and an absolute directory path');
    seen.add(item.name);
  }
  const results = [];
  for (const item of config.skills) {
    let status = 'unavailable';
    try {
      const dir = await fs.lstat(item.path);
      if (dir.isSymbolicLink() || !dir.isDirectory()) status = 'invalid-directory';
      else {
        const file = path.join(item.path, 'SKILL.md');
        const stat = await fs.lstat(file);
        if (stat.isSymbolicLink() || !stat.isFile()) status = 'invalid-skill-file';
        else { await fs.access(file, fs.constants.R_OK); status = 'readable'; }
      }
    } catch (error) {
      if (!['ENOENT', 'ENOTDIR', 'EACCES', 'EPERM'].includes(error.code)) throw error;
    }
    results.push({name:item.name, path:item.path, status});
  }
  return {version:1, results, note:'Filesystem preflight only; host registration, activation and permission to use are not verified.'};
}

async function main() {
  if (process.argv.length !== 3) throw new Error('Usage: node tools/check_external_skills.mjs /absolute/path/references.json');
  if (!path.isAbsolute(process.argv[2])) throw new Error('Configuration path must be absolute');
  const config = JSON.parse(await fs.readFile(process.argv[2], 'utf8'));
  const report = await checkReferences(config);
  console.log(JSON.stringify(report, null, 2));
  if (report.results.some(item => item.status !== 'readable')) process.exitCode = 1;
}
if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href)
  main().catch(error => { console.error(error.message); process.exitCode = 1; });
