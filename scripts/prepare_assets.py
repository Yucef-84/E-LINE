"""Prepare supplied photographs without altering their content.

Usage: python scripts/prepare_assets.py "path/to/키즈모델"
Requires Pillow. No original files are changed.
"""
import json
import sys
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont

SOURCE = Path(sys.argv[1])
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets' / 'images'
DOCS = ROOT / 'assets' / 'documents'
OUT.mkdir(parents=True, exist_ok=True)
DOCS.mkdir(parents=True, exist_ok=True)

photos = {
    'studio': ('3돌 샘플', '정면.JPG'),
    'portrait': ('키즈노트 샘플', 'img - 2026-06-09T205956.665.jpg'),
    'guitar': ('3돌 샘플', '광고2.JPG'),
    'outdoor': ('키즈노트 샘플', 'img - 2026-06-09T205338.275.jpg'),
    'tambourine': ('키즈노트 샘플', 'img - 2026-06-09T205631.505.jpg'),
    'playful': ('키즈노트 샘플', 'img - 2026-06-09T205835.330.jpg'),
    'balloon': ('모델링 샘플', 'img - 2026-06-09T203852.758.jpg'),
    'guitar-wide': ('3돌 샘플', 'CB3I3731.JPG'),
    'focus': ('키즈노트 샘플', 'img - 2026-06-11T103815.489.jpg'),
    'closeup': ('모델링 샘플', 'img - 2026-06-09T203634.747.jpg'),
    'studio-full': ('3돌 샘플', 'CB3I3719.JPG'),
    'cake': ('키즈노트 샘플', 'img - 2026-06-09T204244.559.jpg'),
}
manifest = []
for name, (folder, filename) in photos.items():
    original = ImageOps.exif_transpose(Image.open(SOURCE / folder / filename)).convert('RGB')
    for width in (640, 1200):
        height = round(original.height * width / original.width)
        resized = original.resize((width, height), Image.Resampling.LANCZOS)
        target = OUT / f'{name}-{width}.webp'
        resized.save(target, 'WEBP', quality=83, method=6)
        manifest.append({'file':target.name,'source':f'{folder}/{filename}','width':width,'height':height,'bytes':target.stat().st_size})

# A sharing image, composed from the original photos and native typography.
social = Image.new('RGB', (1200, 630), '#e9efdf')
portrait = ImageOps.exif_transpose(Image.open(SOURCE / photos['studio'][0] / photos['studio'][1])).convert('RGB')
portrait = ImageOps.fit(portrait, (400, 530), centering=(.5, .48))
social.paste(portrait, (750, 50))
draw = ImageDraw.Draw(social)
font_path = Path('C:/Windows/Fonts/malgun.ttf')
latin_path = Path('C:/Windows/Fonts/arial.ttf')
big = ImageFont.truetype(str(font_path), 77)
small = ImageFont.truetype(str(font_path), 22)
logo = ImageFont.truetype(str(latin_path), 26)
draw.text((70, 53), 'E-LINE', font=logo, fill='#20231f')
draw.text((68, 174), '작은 순간,', font=big, fill='#20231f')
draw.text((68, 281), '큰 가능성.', font=big, fill='#4c6544')
draw.text((73, 467), '김일린 · KIM E-LINE', font=small, fill='#56674a')
draw.text((73, 504), '키즈 모델 · 아동 연기', font=small, fill='#859377')
social.save(OUT / 'social.jpg', quality=89, optimize=True)
(OUT / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Prepared {len(photos)} photographs / {len(manifest)} WebP assets and social sharing image.')
print('Download documents are generated separately with create_public_documents.py; original contact documents are never copied.')
print(f'Image payload: {sum(item["bytes"] for item in manifest)/1024:.0f} KB')
