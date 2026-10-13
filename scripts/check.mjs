import { readFile, access, stat } from 'node:fs/promises';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { join, resolve } from 'node:path';
import { parseArgs } from 'node:util';
import { spawnSync } from 'node:child_process';

const root = fileURLToPath(new URL('../', import.meta.url));

export async function validate() {
  const html = await readFile(join(root, 'index.html'), 'utf8');
  const css = await readFile(join(root, 'styles.css'), 'utf8');
  const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]);
  if (new Set(ids).size !== ids.length) throw new Error('Duplicate HTML IDs');
  if ((html.match(/<h1\b/g) || []).length !== 1) throw new Error('Expected one page H1');
  if (/href="tel:/.test(html)) throw new Error('Public telephone links are disabled');
  const emails = [...html.matchAll(/mailto:([^?"\s]+)/g)].map(match => match[1]);
  if (!emails.length || emails.some(email => email !== 'nedjma@steibu.com')) throw new Error('Unexpected public contact email');
  for (const [, id] of html.matchAll(/href="#([^"]+)"/g)) {
    if (!ids.includes(id)) throw new Error(`Broken section link: #${id}`);
  }
  const assets = new Set();
  for (const [, path] of html.matchAll(/(?:src|href)="([^"#]+)"/g)) {
    if (!/^(https?:|mailto:|tel:)/.test(path)) assets.add(path);
  }
  for (const [, path] of html.matchAll(/(?:srcset="|,\s*)(assets\/[\w./-]+)\s+\d+w/g)) assets.add(path);
  for (const [, path] of css.matchAll(/url\(['"]?([^'")]+)['"]?\)/g)) assets.add(path);
  for (const [, name] of html.matchAll(/data-image="([^"]+)"/g)) assets.add(`assets/images/${name}-1200.webp`);
  for (const path of assets) {
    await access(join(root, path));
    if (!(await stat(join(root, path))).size) throw new Error(`Empty asset: ${path}`);
  }
  const syntax = spawnSync(process.execPath, ['--check', join(root, 'script.js')], { encoding: 'utf8' });
  if (syntax.status !== 0) throw new Error(syntax.stderr);
  if (!html.includes('prefers-reduced-motion') && !css.includes('prefers-reduced-motion')) throw new Error('Reduced motion support missing');
  console.log(`Verified ${ids.length} section/control IDs and ${assets.size} local assets; JavaScript syntax OK.`);
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  parseArgs({ options: {}, strict: true });
  await validate();
}
