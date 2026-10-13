"""Download redistributable fonts from their official distribution sources."""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urljoin
import re

out = Path(__file__).resolve().parent.parent / 'assets' / 'fonts'
out.mkdir(parents=True, exist_ok=True)
agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'

def fetch(url):
    with urlopen(Request(url, headers={'User-Agent':agent}), timeout=30) as response:
        return response.read()

pretendard_css_url = 'https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.css'
pretendard_css = fetch(pretendard_css_url).decode('utf-8')
pretendard = urljoin(pretendard_css_url, re.findall(r'url\([\'"]?([^\'"\)]+\.woff2)[\'"]?\)', pretendard_css)[0])
css = fetch('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&display=swap').decode('utf-8')
latin_url = re.findall(r'url\((https://fonts.gstatic.com/[^)]+\.woff2)\)', css)[-1]
for url, target in [(pretendard,'pretendard.woff2'),(latin_url,'manrope.woff2'),('https://raw.githubusercontent.com/orioncactus/pretendard/v1.3.9/LICENSE','Pretendard-LICENSE.txt'),('https://raw.githubusercontent.com/google/fonts/main/ofl/manrope/OFL.txt','Manrope-LICENSE.txt')]:
    data = fetch(url)
    if target.endswith('.txt'):
        data = ('\n'.join(line.rstrip() for line in data.decode('utf-8').splitlines()) + '\n').encode('utf-8')
    (out / target).write_bytes(data)
    print(f'{target}: {len(data)} bytes')
