# 운영 가이드

## 모니터링/알림

- 상태 점검: `monitoring/health_checker.py`
  - 엔드포인트/응답시간/콘텐츠 최소 길이 기반 헬스 확인
  - 알림 채널: 이메일/Slack/Discord (환경변수 필요)
  - 로그: `monitoring.log` 및 콘솔

- 알림 설정: `monitoring/setup_alerts.md`
  - Gmail 앱 비밀번호/Slack Incoming Webhook/Discord Webhook 설정 절차 포함

## 크론/서비스 등록

- 크론 설정 스크립트: `monitoring/setup_cron.sh`
  - `.env` 템플릿 생성, 로그/리포트 디렉토리 생성, 크론 잡 설치, (선택) systemd 타이머 생성
  - 설치 후 유용 명령 목록 출력

실행 예시
```
bash monitoring/setup_cron.sh
```

설치되는 잡(예시)
- 15분 간격 헬스 체크(업무 시간), 시간 간격 헬스 체크(야간/주말)
- 매일 09:00 성능 리포트 실행
- 주간 로그/리포트 보관정리

## 성능 리포트

- `performance_monitor.py` (Lighthouse 필요)
  - 각 페이지 성능/접근성/SEO 점수와 핵심 지표(LCP/CLS/FID 등) 요약
  - 리포트 출력 폴더: `performance_reports/`

## 배포/운영 팁

- 정적 리소스 캐시 헤더 최적화 및 버전 쿼리스트링 사용 권장
- 이미지 WebP, JS/CSS 최소화, 폰트 preconnect
- GA/광고/파트너 코드 환경별 스위칭은 `.env`로 관리

