# 운영 Runbooks

반복되는 운영 작업을 표준화한 실무 가이드입니다. 각 단계는 순서대로 실행하세요.

## 1) 새 테스트 추가

전제: `config.py: DIRECTORIES['tests']`에 대상 루트가 포함되어 있어야 함

절차
1. 디렉토리 생성: `new-test/{ko,ja,en}/index.html`
2. 템플릿 적용: 기본 `<head>`에 Title/Description/OG/Twitter/Canonical 포함
3. 공통 스크립트 포함: `/assets/accessibility.js`, `/assets/seo-optimizer.js`, `/assets/analytics-enhanced.js`
4. 인덱스 반영: `python update_index.py`
5. 사이트맵 생성: `python sitemap_generator.py`
6. 점검: `python seo_audit_fixed.py` → 이슈 확인/보정
7. 제출(선택): `python submit_sitemap.py`

체크포인트
- 메인/언어 인덱스에 카드가 추가되었는가
- OG/Twitter 카드, JSON-LD 누락 없음
- 이미지 alt/크기, lazy 여부 확인

## 2) 기존 테스트에 언어 추가

절차
1. 대상 경로에 언어 폴더 생성: `romance-test/ja/index.html`
2. 기존 ko 버전 메타/본문을 해당 언어로 현지화
3. `python update_index.py` → 카드에 언어 링크가 추가되는지 확인
4. `python sitemap_generator.py`
5. `python seo_audit_fixed.py`로 메타/태그 점검

## 3) 릴리즈 체크리스트 기반 배포

절차
1. 인덱스/사이트맵 최신화: `python update_index.py && python sitemap_generator.py`
2. SEO 점검: `python seo_audit_fixed.py` 결과 확인, 필요 시 `seo_fixer.py`
3. 광고 스캔/삽입(선택): `python apply_coupang_ads.py`
4. 성능 스폿체크(옵션): `python performance_monitor.py` (Lighthouse 필요)
5. 검색엔진 제출: `python submit_sitemap.py`

## 4) SEO 이슈 대응

절차
1. 누락 스캔: `python find_missing_tags.py`, `python find_title_issues.py`
2. 자동 보정: `python seo_fixer.py`
3. 재검증: `python seo_audit_fixed.py`
4. 사이트맵 재생성/제출

## 5) 모니터링 알림 대응

증상: 알림 수신(응답 코드 ≠ 200, 응답 지연, 콘텐츠 부족 등)

점검 순서
1. 로그 확인: `monitoring/logs/cron.log`, `monitoring.log`
2. 최근 리포트 확인: `monitoring/reports/health_report_*.json`
3. 브라우저에서 해당 URL 직접 접속하여 재현 여부 확인
4. 네트워크/호스팅/도메인/인증서 이슈 점검
5. 임시 조치: 문제 파일의 최소 콘텐츠 보강, 링크 경로 수정
6. 재실행: `python monitoring/health_checker.py`

## 6) Coupang 광고 정책 변경 대응

절차
1. `config.py:get_coupang_ad_config()`에서 사이즈/트래킹 값을 변경
2. 기존 삽입물 폭 일괄 수정: `python fix_coupang_width.py`
3. 필요 시 `apply_coupang_ads.py` 재실행 (중복 삽입 방지 로직 있음)

