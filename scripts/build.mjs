import { cp, mkdir, rm } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { join } from 'node:path';
import { validate } from './check.mjs';

const root = fileURLToPath(new URL('../', import.meta.url));
const dist = join(root, 'dist');
await validate();
await rm(dist, { recursive: true, force: true });
await mkdir(dist, { recursive: true });
for (const entry of ['index.html', 'styles.css', 'script.js', 'favicon.svg', 'robots.txt', 'sitemap.xml', 'assets']) {
  await cp(join(root, entry), join(dist, entry), { recursive: true });
}
await cp(join(root, '.nojekyll'), join(dist, '.nojekyll'));
console.log('Built static site → dist/');
