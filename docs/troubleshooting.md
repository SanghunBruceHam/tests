# 트러블슈팅

## SEO 스크립트가 경로를 못 찾음

- 증상: `seo_audit_*`/`find_*` 실행 시 파일 0개 분석
- 원인: 스크립트 내부 베이스 경로가 로컬 환경과 불일치
- 해결: 스크립트 상단의 `base_path`(절대경로)를 환경에 맞게 수정

## Google Search Console 제출 실패

- 증상: `submit_sitemap.py` 401/403/권한 오류
- 확인: `GSC_CREDENTIALS_BASE64` 환경변수 유효성, 서비스 계정에 사이트 소유권 위임 여부
- 해결: 올바른 서비스 계정 JSON을 base64로 인코딩 후 환경변수 재설정

## Lighthouse 사용 불가

- 증상: `performance_monitor.py`에서 `Lighthouse CLI not available`
- 해결: `npm i -g lighthouse` 설치 후 PATH 확인

## Coupang 광고 미삽입

- 증상: `apply_coupang_ads.py` 실행해도 변동 없음
- 원인: 지정 삽입 패턴이 페이지 구조와 불일치 또는 이미 삽입됨
- 해결: 스크립트의 `insertion_patterns`/`footer_pattern` 확장 또는 수동 삽입, 로그 확인

## 인코딩 문제(한글 깨짐)

- 현상: 파일 읽기/쓰기 시 UnicodeDecodeError
- 해결: `utils.FileManager` 사용(UTF-8 강제), 외부 편집기 인코딩 UTF-8 유지

## 헬스체크 타임아웃/오탐

- 증상: 특정 시간대 잦은 타임아웃 알림
- 해결: `monitoring/health_checker.py: thresholds.response_time` 상향, 야간/주말 크론 빈도 조정

