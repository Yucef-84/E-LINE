import http from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { resolve, extname, sep } from 'node:path';

const root = fileURLToPath(new URL('../', import.meta.url));
const port = Number(process.env.PORT || 4173);
const mime = { '.html':'text/html; charset=utf-8', '.css':'text/css; charset=utf-8', '.js':'text/javascript; charset=utf-8', '.svg':'image/svg+xml', '.webp':'image/webp', '.jpg':'image/jpeg', '.png':'image/png', '.pdf':'application/pdf', '.woff2':'font/woff2', '.xml':'application/xml', '.txt':'text/plain; charset=utf-8' };
const server = http.createServer(async (request, response) => {
  try {
    if (!['GET','HEAD'].includes(request.method)) { response.writeHead(405); response.end(); return; }
    let pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
    if (pathname === '/E-LINE' || pathname.startsWith('/E-LINE/')) pathname = pathname.slice(7) || '/';
    const target = resolve(root, `.${pathname === '/' ? '/index.html' : pathname}`);
    const relative = target.slice(root.length).split(/[\\/]/).filter(Boolean);
    if (!target.startsWith(root) || relative.some(part => part.startsWith('.')) || relative[0] === 'scripts' || !['index.html','styles.css','script.js','favicon.svg','robots.txt','sitemap.xml','assets'].includes(relative[0])) {
      response.writeHead(403); response.end('Forbidden'); return;
    }
    const info = await stat(target);
    if (!info.isFile()) throw new Error('Not a file');
    response.writeHead(200, { 'Content-Type':mime[extname(target)] || 'application/octet-stream', 'Cache-Control':'no-cache', 'X-Content-Type-Options':'nosniff' });
    response.end(request.method === 'HEAD' ? undefined : await readFile(target));
  } catch { response.writeHead(404); response.end('Not found'); }
});
server.listen(port, '127.0.0.1', () => console.log(`E-LINE preview: http://127.0.0.1:${port}/E-LINE/`));
for (const signal of ['SIGINT','SIGTERM']) process.on(signal, () => server.close(() => process.exit(0)));
