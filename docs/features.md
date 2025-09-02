# 기능 명세 (Feature Specs)

이 문서는 플랫폼이 제공하는 주요 기능을 “무엇을/어디서/어떻게/확장” 기준으로 정리합니다.

## 다국어 지원

- 무엇을: 한국어(ko), 일본어(ja), 영어(en) 3개 언어 페이지 제공
- 어디서: `ko/`, `ja/`, `en/` 및 각 테스트 하위 폴더(`*/ko|ja|en/*.html`)
- 어떻게: `update_index.py`가 언어별 인덱스/카운트 갱신, `assets/seo-optimizer.js`가 hreflang 링크 자동 보강
- 확장: `config.py: SUPPORTED_LANGUAGES`에 언어 추가 후, 동일 폴더 구조/파일 추가 → `python update_index.py`

## 접근성(Accessibility)

- 무엇을: 키보드 내비게이션, 명확한 포커스, aria 속성, 색 대비, 스크린리더 친화 구조 지향
- 어디서: 공통 마크업 + `assets/accessibility.js` (보강 스크립트, 필요한 경우)
- 어떻게: 시맨틱 태그 사용, 인터랙션 요소에 키보드 포커스, 포커스 스타일 유지, 이미지에 적절한 `alt`
- 확장: 컴포넌트 추가 시 키보드/스크린리더 시나리오 포함 테스트

## 성능 최적화

- 무엇을: lazy 이미지, 지연 로딩 모듈, preconnect/dns-prefetch, Lighthouse 리포트 수집(옵션)
- 어디서: `assets/module-loader.js`, `assets/seo-optimizer.js`, `performance_monitor.py`
- 어떻게: DOMContentLoaded 시 페이지 타입 감지 → 필요한 모듈만 동적 로딩, 이미지 lazy 부여
- 확장: 대형 모듈은 사용자 인터랙션/가시성 기반 로딩으로 분리

## SEO 강화

- 무엇을: 메타/OG/Twitter/JSON-LD/Canonical 자동화 및 점검/보정 파이프라인
- 어디서: 정적 메타(`*.html`), 동적 보강(`assets/seo-optimizer.js`), 점검(`seo_audit_*.py`), 보정(`seo_fixer.py`)
- 어떻게: 점검 → 보정 → `sitemap_generator.py` → `submit_sitemap.py`
- 확장: 새로운 테스트 템플릿에 기본 메타/JSON-LD 포함, 누락은 JS 보강에 맡김

## 분석(Analytics)

- 무엇을: 페이지뷰/사용자 상호작용/에러/성능/세션 기반 커스텀 이벤트 배치 전송
- 어디서: `assets/analytics-enhanced.js` + GA4 `gtag.js`
- 어떻게: 이벤트 큐 누적 → 일정/임계 시 배치 전송, Web Vitals 수집(LCP/FID/CLS)
- 확장: `window.track(eventName, properties)` 전역 API로 커스텀 이벤트 추가

## 광고(Ads)

- 무엇을: Google AdSense(자동), Coupang 파트너스(위젯) 지원
- 어디서: 정적 스니펫 + `apply_coupang_ads.py` (메인/테스트 규칙 삽입)
- 어떻게: 삽입 마커/패턴 탐지 → 중복 방지 후 주석 구간 삽입
- 확장: `config.py:get_coupang_ad_config()` 템플릿 크기/트래킹 조정

## 모니터링/알림

- 무엇을: 엔드포인트 상태/응답시간/콘텐츠 길이 기준 헬스체크, 이슈시 다중 채널 알림
- 어디서: `monitoring/health_checker.py`, 설정 `monitoring/setup_alerts.md`
- 어떻게: 결과 JSON 저장(`monitoring/reports/`), 이메일/Slack/Discord로 통지
- 확장: 임계값(`thresholds`) 조정, 엔드포인트 목록 확장

## 사이트 인덱싱/맵핑

- 무엇을: 테스트 목록 자동 갱신, 사이트맵 생성/제출
- 어디서: `update_index.py`, `sitemap_generator.py`, `submit_sitemap.py`
- 어떻게: 폴더 스캔 → `index.html` JS 배열 치환 → `sitemap.xml` 생성 → GSC 제출
- 확장: 제외 규칙(`SitemapGenerator.excluded_files/excluded_patterns`) 유지

