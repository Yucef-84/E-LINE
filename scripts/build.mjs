import { cp, mkdir, readdir, rm, stat } from 'node:fs/promises';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { join, relative, resolve } from 'node:path';
import { validate } from './check.mjs';

const root = fileURLToPath(new URL('../', import.meta.url));
const dist = join(root, 'dist');
const maxAssetBytes = 25 * 1024 * 1024;
const publicEntries = ['index.html', 'styles.css', 'script.js', 'favicon.svg', 'robots.txt', 'sitemap.xml', 'assets', '.nojekyll'];

export async function validateDeploymentAssets(directory) {
  let files = 0;
  let bytes = 0;
  let largest = 0;

  async function visit(folder) {
    for (const entry of await readdir(folder, { withFileTypes: true })) {
      const path = join(folder, entry.name);
      if (entry.isDirectory()) {
        await visit(path);
      } else if (entry.isFile()) {
        const { size } = await stat(path);
        if (size > maxAssetBytes) {
          throw new Error(`Deployment asset exceeds Cloudflare's 25 MiB limit: ${relative(directory, path)} (${size} bytes)`);
        }
        files += 1;
        bytes += size;
        largest = Math.max(largest, size);
      } else {
        throw new Error(`Unsupported deployment asset: ${relative(directory, path)}`);
      }
    }
  }

  await visit(directory);
  return { files, bytes, largest };
}

export async function build() {
  await validate();
  await rm(dist, { recursive: true, force: true });
  await mkdir(dist, { recursive: true });
  for (const entry of publicEntries) {
    await cp(join(root, entry), join(dist, entry), { recursive: true });
  }
  const { files, bytes, largest } = await validateDeploymentAssets(dist);
  console.log(`Built static site → dist/; verified ${files} files, ${(bytes / 1024 / 1024).toFixed(2)} MiB total, ${(largest / 1024 / 1024).toFixed(2)} MiB largest.`);
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  await build();
}
