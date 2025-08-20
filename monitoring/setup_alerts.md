# 🚨 알림 시스템 설정 가이드

## 📧 1. 이메일 알림 설정

### Gmail 사용 시 (권장)
```bash
# 환경변수 설정 (Linux/Mac)
export EMAIL_USER="your-email@gmail.com"
export EMAIL_PASSWORD="your-app-password"  # Gmail 앱 비밀번호 필요
export TO_EMAIL="alert-recipient@gmail.com"
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
```

### Gmail 앱 비밀번호 생성 방법:
1. Google 계정 → 보안 → 2단계 인증 활성화
2. 앱 비밀번호 생성: [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. "메일" → "기타" → "모니터링 시스템" 이름으로 생성
4. 생성된 16자리 비밀번호를 `EMAIL_PASSWORD`로 사용

### 다른 이메일 서비스:
```bash
# Naver
export SMTP_SERVER="smtp.naver.com"
export SMTP_PORT="587"

# Daum
export SMTP_SERVER="smtp.daum.net" 
export SMTP_PORT="587"

# Outlook
export SMTP_SERVER="smtp.live.com"
export SMTP_PORT="587"
```

## 💬 2. Slack 알림 설정

### Webhook URL 생성:
1. [api.slack.com/apps](https://api.slack.com/apps) → "Create New App"
2. "From scratch" → 앱 이름 & 워크스페이스 선택
3. "Incoming Webhooks" → 활성화
4. "Add New Webhook to Workspace" → 채널 선택
5. Webhook URL 복사

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

### Slack 앱 권한 설정:
- `channels:read` - 채널 정보 읽기
- `chat:write` - 메시지 전송

## 🎮 3. Discord 알림 설정

### Webhook URL 생성:
1. Discord 서버 → 채널 설정 → 연동
2. "웹후크" → "새 웹후크"
3. 웹후크 이름 설정 (예: "모니터링 봇")
4. 웹후크 URL 복사

```bash
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/YOUR/WEBHOOK/URL"
```

## 🔄 4. 환경변수 영구 설정

### Linux/Mac (.bashrc 또는 .zshrc):
```bash
echo 'export EMAIL_USER="your-email@gmail.com"' >> ~/.bashrc
echo 'export EMAIL_PASSWORD="your-app-password"' >> ~/.bashrc
echo 'export TO_EMAIL="alert-recipient@gmail.com"' >> ~/.bashrc
echo 'export SLACK_WEBHOOK_URL="your-slack-webhook"' >> ~/.bashrc
echo 'export DISCORD_WEBHOOK_URL="your-discord-webhook"' >> ~/.bashrc
source ~/.bashrc
```

### Python .env 파일 (프로젝트 루트):
```env
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
TO_EMAIL=alert-recipient@gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR/WEBHOOK/URL
```

## 🧪 5. 테스트 실행

```bash
# 기본 헬스 체크 실행
python monitoring/health_checker.py

# 환경변수 확인
python -c "
import os
print('EMAIL_USER:', os.getenv('EMAIL_USER'))
print('SLACK_WEBHOOK:', 'Configured' if os.getenv('SLACK_WEBHOOK_URL') else 'Not configured')
print('DISCORD_WEBHOOK:', 'Configured' if os.getenv('DISCORD_WEBHOOK_URL') else 'Not configured')
"
```

## 📱 6. 모바일 알림 (추가 옵션)

### Telegram 봇:
```python
# 추가 설정으로 Telegram 봇 알림도 가능
TELEGRAM_BOT_TOKEN="your-bot-token"
TELEGRAM_CHAT_ID="your-chat-id"
```

### KakaoTalk 알림:
- KakaoWork API 활용
- 카카오톡 비즈니스 채널 API

## 🎯 7. 알림 우선순위 설정

```python
# severity 레벨별 알림 설정
"info"    - 정보성 (모든 채널)
"warning" - 경고 (Slack + Discord)  
"danger"  - 위험 (모든 채널 + 전화/SMS)
```

## 🔧 8. 고급 설정

### 알림 빈도 제한:
```python
# 같은 이슈에 대해 1시간마다 최대 1회 알림
ALERT_COOLDOWN = 3600  # seconds
```

### 업무시간 설정:
```python
# 업무시간에만 알림 (9-18시)
BUSINESS_HOURS = {"start": 9, "end": 18}
```

### 알림 그룹화:
```python
# 5분간 발생한 알림들을 하나로 묶어서 전송
BATCH_ALERT_INTERVAL = 300  # seconds
```

## ⚡ 9. 빠른 시작 (올인원)

```bash
# 1. 필요한 패키지 설치
pip install requests python-dotenv

# 2. .env 파일 생성 (위의 예시 참고)

# 3. 첫 테스트 실행
python monitoring/health_checker.py

# 4. 성공시 아래 메시지 확인:
# "Email alert sent successfully"
# "Slack alert sent successfully" 
# "Discord alert sent successfully"
```

설정이 완료되면 웹사이트에 문제가 발생할 때마다 즉시 알림을 받을 수 있습니다! 🎉