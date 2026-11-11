import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import {handle} from '../server/mcp.mjs';

test('MCP resource pagination counts Unicode code points and never splits a supplementary character', async () => {
 const path = 'audit/baseline/skills/humanizer/README.md';
 const original = await fs.readFile(new URL('../' + path, import.meta.url), 'utf8');
 const characters = Array.from(original);
 const offset = characters.indexOf('🚀');
 assert.ok(offset > 0, 'the bundled resource contains the supplementary character');
 const read = async (offset, max_chars) => {
  const response = await handle({jsonrpc:'2.0',id:1,method:'tools/call',params:{name:'read_resource',arguments:{path,offset,max_chars}}});
  assert.equal(response.result.isError, false);
  return JSON.parse(response.result.content[0].text);
 };
 const before = await read(offset - 1, 1);
 const emoji = await read(before.next_offset, 1);
 const after = await read(emoji.next_offset, 1);
 assert.equal(emoji.text, '🚀');
 assert.equal(before.text + emoji.text + after.text, characters.slice(offset - 1, offset + 2).join(''));
 assert.equal(emoji.next_offset, offset + 1);
 assert.equal(emoji.total_chars, characters.length);
 const last = await read(characters.length - 1, 1);
 assert.equal(last.text, characters.at(-1));
 assert.equal(last.next_offset, null);
});
