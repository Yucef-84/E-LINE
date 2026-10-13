# E-LINE · 김일린

김일린 키즈 모델·아동 연기 포트폴리오 홈페이지. 제공된 프로필과 실제 촬영 사진을 바탕으로 만들었습니다.

공식 사이트: https://e-line.steibu.com/

GitHub Pages 미러: https://yucef-84.github.io/E-LINE/

## 구성

- Lightspark 레퍼런스의 중앙 타이포그래피, 떠 있는 이미지, 부드러운 색 번짐을 모델 포트폴리오에 적용
- 소개, 실제 사진 12장, 캐스팅 분야, 신체·활동 프로필, 보호자 문의
- 사진 분야 필터, 확대 보기, 방향키·터치 사진 이동, Esc 닫기
- 공개용 프로필 PDF·컴카드 PDF/JPG 다운로드
- 이메일·Instagram 연결, 이메일 복사
- 모바일 메뉴, 반응형 배치, 동작 줄이기 설정 지원
- 로컬 폰트·WebP 이미지, 이미지 지연 로딩, 공유용 OG 이미지, 검색 메타데이터

기획 및 설계 내용은 [docs/DESIGN.md](docs/DESIGN.md)에 있습니다.

## 실행

Node.js 22 이상. 런타임 패키지 설치가 필요하지 않습니다.

```sh
node scripts/serve.mjs
```

http://127.0.0.1:4173/E-LINE/ 에서 확인할 수 있습니다. `PORT` 환경 변수로 포트를 변경할 수 있습니다.

```sh
node scripts/check.mjs
node scripts/build.mjs
```

검증은 내부 앵커, 중복 ID, 로컬 리소스와 확대 사진 파일, JavaScript 문법을 확인합니다. 빌드는 공개 파일만 `dist/`로 복사합니다. npm 사용 환경에서는 `npm run dev`, `npm run check`, `npm run build`도 동일하게 동작합니다.

## Cloudflare Workers 배포

Cloudflare의 `e-line` Worker는 `main` 브랜치를 연결하고 아래 빌드 설정을 사용합니다.

| 항목 | 설정 |
|---|---|
| 루트 디렉터리 | `/` |
| 빌드 명령 | `npm run build` |
| 배포 명령 | `npx wrangler deploy --config wrangler.jsonc` |

`wrangler.jsonc`의 `assets.directory`는 `./dist`입니다. 빌드가 홈페이지 HTML/CSS/JavaScript, 이미지, 폰트, 공개 다운로드 자료만 이 폴더에 복사하며, 모든 배포 파일이 Cloudflare의 파일당 25 MiB 제한 이내인지 확인합니다. 검증 또는 용량 검사에 실패하면 배포 전에 빌드가 중단됩니다.

`routes`에는 `e-line.steibu.com`을 `custom_domain: true`로 지정하여 공식 도메인 연결도 배포 설정과 함께 관리합니다. Cloudflare가 해당 호스트의 DNS와 HTTPS 인증서를 관리합니다.

저장소 루트와 `node_modules`, 개발 스크립트, 기획 문서는 업로드하지 않습니다. `dist/`와 `.wrangler/`는 생성 파일이므로 Git에 포함하지 않습니다. 공식 도메인은 `https://e-line.steibu.com/`이며 canonical, OG, 구조화 데이터, robots.txt와 sitemap.xml도 이 주소를 사용합니다. Cloudflare 기본 주소는 `https://e-line.jijimmi.workers.dev/`입니다.

## GitHub Pages 배포

`main`에 푸시하면 `.github/workflows/pages.yml`이 검증·빌드 후 GitHub Pages에 배포합니다. 저장소의 **Settings → Pages → Source**는 **GitHub Actions**를 사용합니다. 상대 경로를 사용해 `/E-LINE/` 하위 경로에서도 모든 리소스가 동작합니다.

## 콘텐츠 수정

- 문구·신체 정보·연락처: `index.html`
- 색감·레이아웃·반응형 설정: `styles.css`
- 갤러리·메뉴·클립보드 동작: `script.js`
- 사진 출처와 출력 크기: `assets/images/manifest.json`
- 다운로드 자료: `assets/documents/`

신체 정보는 제공 프로필 기준이며 캐스팅 시 현재 정보를 확인합니다. 경력·협업 브랜드·추천사는 제공 자료에서 확인되지 않아 추가하지 않았습니다.

## 이미지와 폰트

선별 사진을 다시 생성하려면 Python과 Pillow가 필요합니다. 제공 자료 폴더를 인자로 지정합니다.

```sh
python scripts/prepare_assets.py "사진 자료 폴더"
```

EXIF 방향을 반영하고 640px/1200px WebP로 변환합니다. 원본 파일은 수정하지 않으며 웹용 사진에는 EXIF 정보가 포함되지 않습니다. 다운로드 자료는 새로 만든 공개용 버전이며, 개인 전화번호와 이전 이메일은 포함하지 않습니다. `gpt 이미지` 폴더의 사진은 사용하지 않았습니다. 공유 이미지는 실제 사진과 텍스트로 구성합니다.

폰트는 로컬로 제공하며, 재다운로드가 필요할 때만 `python scripts/fetch_fonts.py`를 실행합니다. Pretendard와 Manrope의 라이선스는 `assets/fonts/`에 보관되어 있습니다. 사진·모델 자료의 권리는 해당 권리자에게 있습니다.

공개용 PDF는 `python scripts/create_public_documents.py`로 생성합니다. ReportLab과 Pillow, 한국어 TTF 폰트가 필요합니다. Windows에서는 맑은 고딕을 사용하며 다른 환경에서는 `ELINE_KOREAN_FONT`를 지정합니다. 컴카드 JPG는 공개용 PDF를 렌더링한 이미지입니다.
