# 설정

## 환경변수

필수/선택 환경변수는 운영(분석/광고/알림) 기능과 자동화 스크립트에서 사용됩니다. 루트에 `.env`를 두거나 셸 환경에 설정하세요.

예시 (`.env`):
```
# Analytics / Ads
GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX
ADSENSE_CLIENT_ID=ca-pub-XXXXXXXXXXXXXXX

# Coupang Partners
COUPANG_PARTNER_ID=867629
COUPANG_TRACKING_CODE=AF6959276

# Alerts (monitoring/health_checker.py)
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
TO_EMAIL=alert-recipient@gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXX/YYY/ZZZ
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/AAA/BBB

# Google Search Console submit (submit_sitemap.py)
GSC_CREDENTIALS_BASE64=base64-encoded-service-account-json
```

참고 파일: `monitoring/setup_alerts.md`, `monitoring/setup_cron.sh`

## 코드 기반 설정

- `config.py`
  - `BASE_URL`, `SITEMAP_FILE`
  - `GOOGLE_ANALYTICS_ID`, `ADSENSE_CLIENT_ID` (환경변수 기본값 바인딩)
  - `COUPANG_PARTNER_ID`, `COUPANG_TRACKING_CODE`
  - `SUPPORTED_LANGUAGES = ['ko','ja','en']`
  - `DIRECTORIES['tests'] = ['romance-test','egen-teto']`
  - `SEO_CONFIG`(사이트명/기본 설명/키워드), `LOGGING_CONFIG`(레벨/포맷/파일)

- `utils.py`
  - 파일 읽기/쓰기 안전화, 언어별 HTML 탐색, 제목/설명 추출, 입력 새니타이징, 경로 검증, 로깅 초기화 헬퍼 제공

## 파이썬 의존성

- `requirements.txt` 또는 `pyproject.toml` 사용
```
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```

