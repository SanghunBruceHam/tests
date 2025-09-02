# 유지보수 가이드

## 정기 작업

- 의존성 점검: `requirements.txt` / `pyproject.toml` 버전 업데이트 검토
- 로그/리포트 보관: `monitoring/setup_cron.sh`의 logrotate/정리 잡 유지
- 사이트맵 예외 목록 업데이트: `sitemap_generator.py: excluded_files/patterns`

## 설정 변경

- GA/AdSense/Coupang 변경 시: `config.py` 환경변수 기반 설정 → `.env` 업데이트
- 테스트 루트 추가/변경: `config.py: DIRECTORIES['tests']`에 반영 → `update_index.py`로 카드 생성 확인

## 테스트/페이지 정리

- 중단 테스트 제거: 폴더 삭제 → `python update_index.py` → `python sitemap_generator.py`
- 검색 제외 파일: `sitemap_generator.excluded_files`에 추가

## 장애 예방

- 모듈 크기 증가 시 지연 로딩 검토(`assets/module-loader.js`)
- 이미지 용량 관리(WebP, 썸네일 사이즈 표준화)

