# 아키텍처

## 개요

- 정적(MPA) 기반 다국어 웹사이트 구조에 Python 자동화 스크립트를 결합해 SEO/운영을 강화한 형태입니다.
- 핵심 폴더
  - 정적 페이지: `index.html`, `ko/`, `ja/`, `en/`, 각 테스트 디렉토리(예: `romance-test/`, `egen-teto/`, `anime-personality/`)
  - 자산: `assets/` (공통 JS/CSS 모듈)
  - 자동화/운영: Python 스크립트 루트 및 `monitoring/`
  - 설정/유틸: `config.py`, `utils.py`

## 디렉토리 구조 요약

```
tests/
├── index.html                      # 메인(ko) 인덱스
├── ko/ ja/ en/                     # 언어별 인덱스(선택)
├── romance-test/                   # 연애 심리 테스트 (ko/ja/en 하위 포함)
├── egen-teto/                      # 에겐테토 테스트 (ko/ja/en 하위 포함)
├── anime-personality/              # 애니 성격 진단 (ko/ja/en 및 유틸)
├── assets/                         # 공통 JS/CSS
├── monitoring/                     # 헬스체크/크론/대시보드
├── config.py                       # 전역 설정 + 환경변수 바인딩
├── utils.py                        # 파일/보안/콘텐츠 유틸 + 로거 설정
└── *.py                            # SEO/인덱스/광고/성능/제출 스크립트
```

## 페이지 유형

- 메인 페이지: `index.html` (ko 기준, 다국어 링크 및 테스트 목록 제공)
- 언어 인덱스: `ko/index.html`, `ja/index.html`, `en/index.html`
- 테스트 페이지: `romance-test/<lang>/testN.html`, `egen-teto/<lang>/index.html` 등
- 유틸/관리 페이지: 일부 생성/썸네일 유틸 HTML (`anime-personality/*`)

## 프론트엔드 모듈 개요 (`assets/`)

- `module-loader.js`: 페이지 유형 감지 후 필요한 모듈을 동적/지연 로딩
- `seo-optimizer.js`: 메타/OG/Twitter/구조화 데이터/브레드크럼/다국어 hreflang 자동 보강
- `analytics-enhanced.js`: 사용자 이벤트/성능/에러/세션 기반 배치 전송 추적
- `accessibility.js`, `common-components.js`: 접근성 강화를 위한 스크립트와 공통 UI
- `result-analysis.js`, `chart-visualization.js`, `enhanced-features.js`: 테스트 결과/차트/부가기능
- 스타일: `common-theme.css`, `enhanced-animations.css`

모듈 로딩 흐름
1) DOMContentLoaded → `window.moduleLoader.loadPageModules()`
2) 페이지 타입(test/index/기타)에 맞는 모듈 묶음 로딩
3) Intersection/Interaction 기반 추가 지연 로딩

## 백엔드/자동화 구성

- 설정: `config.py`
  - `BASE_URL`, `SUPPORTED_LANGUAGES`, 광고/애널리틱스 ID, 디렉토리/SEO/로그 구성
- 유틸: `utils.py`
  - 파일 입출력 안전화, HTML 메타 추출, 경로 검증, 로깅 초기화
- 주요 자동화 스크립트
  - `sitemap_generator.py`: HTML 스캔 → 우선순위/변경주기/최종수정 반영 XML 생성
  - `update_index.py`: 테스트 디렉토리 스캔 → `index.html` 내부 tests 배열/언어 인덱스 카운트 갱신
  - `apply_coupang_ads.py`: 규칙 기반 광고 삽입(메인/테스트 페이지)
  - `seo_audit_*.py`: 정규식/BeautifulSoup 기반 SEO 점검 리포트 및 JSON 출력
  - `seo_fixer.py`: 메타/제목/트위터카드/유틸 HTML 보정 일괄 처리
  - `performance_monitor.py`: Lighthouse CLI 기반 성능 리포트 수집(옵션)
  - `monitoring/health_checker.py`: 엔드포인트 상태/응답시간/콘텐츠 길이 주기 점검 + 알림

## SEO/분석/광고

- SEO: 정적 메타 + `seo-optimizer.js`로 동적 보강, 구조화 데이터(JSON-LD) 자동 삽입
- 분석: GA4(`gtag.js`) + `analytics-enhanced.js` 사용자/성능 이벤트 배치 전송
- 광고: Google AdSense(자동 광고), Coupang 파트너스(자동 삽입 스크립트)

