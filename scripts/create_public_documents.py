"""Generate public model documents without private telephone contact details.

Requires ReportLab and Pillow. Default Korean font: Windows Malgun Gothic.
Override with ELINE_KOREAN_FONT for another embeddable Korean TTF.
"""
from pathlib import Path
from io import BytesIO
import os
from PIL import Image, ImageOps
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / 'assets' / 'documents'
IMAGES = ROOT / 'assets' / 'images'
DOCS.mkdir(parents=True, exist_ok=True)
font_path = os.environ.get('ELINE_KOREAN_FONT', 'C:/Windows/Fonts/malgun.ttf')
pdfmetrics.registerFont(TTFont('Korean', font_path))
PAPER = '#f8f9f6'
INK = '#20231f'
GREEN = '#60784d'
MUTED = '#77856a'
LINE = '#d6decc'
EMAIL = 'nedjma@steibu.com'
INSTAGRAM = '@gimcarrot23'

def text(c, x, y, value, size=10, color=INK, font='Korean', align='left'):
    c.setFillColor(HexColor(color))
    c.setFont(font, size)
    if align == 'right': c.drawRightString(x, y, value)
    else: c.drawString(x, y, value)

def line(c, x1, y1, x2, y2):
    c.setStrokeColor(HexColor(LINE))
    c.setLineWidth(.5)
    c.line(x1, y1, x2, y2)

def photo(c, name, x, y, width, height):
    source = Image.open(IMAGES / f'{name}-1200.webp').convert('RGB')
    fitted = ImageOps.fit(source, (round(width*3), round(height*3)), centering=(.5,.42))
    buffer = BytesIO()
    fitted.save(buffer, format='JPEG', quality=94)
    c.drawImage(ImageReader(buffer), x, y, width, height)

def base(path, size, title):
    c = canvas.Canvas(str(path), pagesize=size, pageCompression=1)
    c.setTitle(title)
    c.setAuthor('KIM E-LINE')
    c.setSubject('Public kids model profile and casting contact')
    c.setFillColor(HexColor(PAPER))
    c.rect(0, 0, *size, fill=1, stroke=0)
    return c

def logo(c, x, y):
    text(c, x, y, 'E-LINE', 17, font='Helvetica-Bold')
    c.setStrokeColor(HexColor(GREEN))
    c.setLineWidth(1.4)
    center_x = x-13
    for dx,dy in [(0,6),(6,0),(4.2,4.2),(4.2,-4.2)]:
        c.line(center_x-dx,y+5-dy,center_x+dx,y+5+dy)

def compcard():
    size = landscape(A4)
    w,h = size
    c = base(DOCS / 'e-line-compcard.pdf', size, 'KIM E-LINE - Public Comp Card')
    logo(c, 49, h-42)
    text(c, w-36, h-39, 'KIDS MODEL / COMP CARD', 8, MUTED, 'Helvetica', 'right')
    photo(c, 'studio', 36, 135, 245, 366)
    for i,name in enumerate(['portrait','guitar','outdoor','guitar-wide','playful','balloon']):
        col = i%3
        row = i//3
        photo(c, name, 299+col*174, 318 if row==0 else 135, 158, 183 if row==0 else 167)
    line(c,36,116,w-36,116)
    text(c,36,77,'김일린',26)
    text(c,37,58,'KIM E-LINE',9,MUTED,'Helvetica')
    line(c,235,52,235,103)
    for x,label,value in [(279,'HEIGHT','97 cm'),(411,'WEIGHT','15 kg'),(543,'CLOTHING','100'),(675,'SHOES','150 mm')]:
        text(c,x,96,label,7,MUTED,'Helvetica')
        text(c,x,71,value,23,INK,'Helvetica')
    text(c,279,51,'2023년생 / 여아  ·  서울·경기  ·  주말 중심',8,MUTED)
    text(c,36,27,EMAIL,11,GREEN,'Helvetica')
    text(c,w-36,27,INSTAGRAM+'  /  보호자 관리',9,MUTED,align='right')
    text(c,w-36,12,'신체 정보는 제공 프로필 기준이며 섭외 시 확인해 주세요.',6.5,MUTED,align='right')
    c.save()

def profile():
    w,h=A4
    c=base(DOCS / 'e-line-profile.pdf', A4, 'KIM E-LINE - Public Model Profile')
    logo(c,53,h-47)
    text(c,w-40,h-44,'MODEL PROFILE / 2026',8,MUTED,'Helvetica','right')
    text(c,40,706,'김일린',42)
    text(c,42,678,'KIM E-LINE',12,GREEN,'Helvetica')
    text(c,42,654,'키즈 모델 · 아동 연기',11,MUTED)
    photo(c,'portrait',354,531,201,226)
    for x,y,label,value in [(43,597,'HEIGHT','97 cm'),(193,597,'WEIGHT','15 kg'),(43,535,'CLOTHING','100'),(193,535,'SHOES','150 mm')]:
        text(c,x,y+21,label,7,MUTED,'Helvetica')
        text(c,x,y-3,value,25,font='Helvetica')
    line(c,40,510,w-40,510)
    text(c,40,479,'한눈에 만나는 일린',17)
    rows=[('출생 / 성별','2023년생 / 여아'),('활동 지역 / 일정','서울·경기 / 주말 중심'),('언어·배경','Korean-Algerian background'),('언어 수준','알제리 아랍어 듣기 · 간단한 단어 말하기 가능')]
    for i,(label,value) in enumerate(rows):
        y=449-i*33
        text(c,40,y,label,9,MUTED)
        text(c,160,y,value,10)
        line(c,40,y-13,w-40,y-13)
    text(c,40,301,'자연스러운 표정, 일린만의 작은 빛.',17)
    for y,value in [(274,'낯가림이 적고 새로운 사람과 자연스럽게 대화합니다.'),(251,'일상 대화와 촬영 지시 수행이 가능하며 표정 변화가 풍부합니다.'),(228,'근접 촬영에서 안정적인 시선, 생활형 콘텐츠의 자연스러운 반응.')]:
        text(c,40,y,value,10,MUTED)
    text(c,40,191,'함께 그려갈 다음 장면',15)
    text(c,40,166,'키즈 패션 · 피팅 · 라이프스타일 · 식품 · 완구·교육',10,MUTED)
    text(c,40,146,'영상 광고 · 아동 연기',10,MUTED)
    c.setFillColor(HexColor('#e1ead7'))
    c.rect(40,44,w-80,82,fill=1,stroke=0)
    text(c,56,108,'CASTING CONTACT / 보호자',7,GREEN)
    text(c,56,83,EMAIL,18,INK,'Helvetica')
    text(c,56,61,'Instagram '+INSTAGRAM+'  ·  모든 문의 및 계정은 보호자가 관리합니다.',8,MUTED)
    text(c,40,22,'신체 정보와 활동 일정, 언어 수준은 섭외 시 보호자와 확인해 주세요.',7.5,MUTED)
    text(c,w-40,22,'E-LINE / 01',7,MUTED,'Helvetica','right')
    c.save()

compcard()
profile()
print('Generated public comp card and profile PDFs with approved email and Instagram only.')
