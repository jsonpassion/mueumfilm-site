# mueumfilm-site

무음필름(MUEUMFILM) — 셔터음 없는 iOS 되감기 카메라의 공식 사이트.

**Live**: https://jsonpassion.github.io/mueumfilm-site/ (GitHub Pages, main 루트 배포)

## 구성

- `index.html` — 랜딩 (다크 시네마틱: 글로우+그레인, 스크롤 리빌, 떠 있는 필름 카드, 되감기 인터랙티브 데모)
- `privacy.html` / `terms.html` — 법률 문서 (다크 테마)
- `lottie/` — 자체 제작 로티 6종: rewind·silent·film-tone·level·stamp·lens
- `tools/make_lottie.py` — 로티 재생성기 (`python3 tools/make_lottie.py`)

## 규칙

- 푸터 5요소 고정: 개인정보 처리방침 · 이용약관 · ✉️ 문의하기 버튼(이메일 텍스트 비노출) · © 2026 ForgeLab · ForgeLab · 대표 Jason Lee
- 외부 의존성은 lottie-player CDN 하나. 나머지는 단일 HTML 자급자족

© 2026 ForgeLab · Jason Lee
