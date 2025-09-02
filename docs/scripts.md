# 스크립트 가이드

각 스크립트는 루트에서 실행합니다. 일부는 환경변수나 외부 도구가 필요합니다.

## 인덱스/사이트맵

- `update_index.py`
  - 테스트 디렉토리 스캔 → `index.html` 내부 `const tests = [...]` 배열 갱신
  - 언어별 인덱스(`ko/ja/en/index.html`)의 통계 수치도 함께 업데이트
  - 사용: `python update_index.py`

- `sitemap_generator.py`
  - 모든 HTML 파일을 크롤링해 `sitemap.xml` 생성, 우선순위/변경주기/최종수정 반영
  - 사용: `python sitemap_generator.py`
  - 생성 후 내부 유효성 체크: 자동 실행(`validate_sitemap()`)

- `submit_sitemap.py`
  - Google Search Console에 사이트맵 제출
  - 필요: `GSC_CREDENTIALS_BASE64` 환경변수(서비스 계정 JSON base64)
  - 사용: `python submit_sitemap.py`

## SEO 점검/수정

- `seo_audit_simple.py`
  - 정규식 기반 기본 점검(Title/Description/OG/Twitter/JSON-LD/Canonical/이미지 alt)
  - 콘솔 리포트 + `seo_current_status.json` 저장
  - 사용: `python seo_audit_simple.py`

- `seo_audit_fixed.py`
  - 정규식 개선판(메타 설명 탐지 강화, 태그 검출 정확도 개선)
  - 콘솔 리포트 + `seo_fixed_results.json` 저장
  - 사용: `python seo_audit_fixed.py`

- `seo_audit_advanced.py`
  - BeautifulSoup 기반 고급 점검(세분화된 가중치/세부 통계)
  - 콘솔 리포트 + `seo_audit_advanced_results.json` 저장
  - 사용: `python seo_audit_advanced.py`

- `find_missing_tags.py`
  - Twitter Card/OG 누락 파일 탐지 요약 리포트
  - 사용: `python find_missing_tags.py`

- `find_title_issues.py`
  - 제목 길이(30–60자 권장) 벗어난 파일 탐지
  - 사용: `python find_title_issues.py`

- `seo_fixer.py`
  - 일괄 보정 도구: 로맨스 테스트 메타 설명, 제목 길이, Twitter 카드 추가, 유틸 HTML 보정 등
  - 사용: `python seo_fixer.py`

## 광고/분석 보정

- `apply_coupang_ads.py`
  - 메인/테스트 페이지에 Coupang 파트너스 블록 자동 삽입 (중복 삽입 방지)
  - 위치: AMP 광고/푸터/내비 아래 등 규칙 기반
  - 사용: `python apply_coupang_ads.py`

- `fix_coupang_width.py`
  - 기존 삽입 광고 중 width 600 → 750으로 일괄 수정(ko 기준)
  - 사용: `python fix_coupang_width.py`

- `fix_ga_romance_test.py`
  - `romance-test/*/test*.html` 내 GA 코드가 불완전한 경우 정규 패턴으로 교체
  - 사용: `python fix_ga_romance_test.py`

## 성능/헬스체크

- `performance_monitor.py`
  - Lighthouse CLI 기반 주요 페이지 성능 리포트 수집(json/html)
  - 필요: `npm i -g lighthouse`
  - 사용: `python performance_monitor.py`

- `monitoring/health_checker.py`
  - 지정 엔드포인트(루트/언어 인덱스/테스트/robots/sitemap) 가용성/응답시간/콘텐츠 길이 점검
  - 이슈 발생 시 이메일/Slack/Discord 알림 발송(구성된 채널만)
  - 리포트 저장: `monitoring/reports/health_report_*.json`
  - 사용: `python monitoring/health_checker.py`

## 운영 보조

- `update_files.py`
  - `robots.txt`, `ads.txt` 최신화(시간 스탬프 포함)
  - 사용: `python update_files.py`

## 주의사항

- 대량 수정 스크립트 실행 전에는 Git 커밋으로 스냅샷을 남기는 것을 권장합니다.
- 일부 스크립트는 루트 절대경로를 가정합니다. 다른 환경에서 실행 시 경로를 조정하세요.

