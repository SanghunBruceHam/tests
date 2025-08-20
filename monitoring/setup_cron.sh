#!/bin/bash

# 🕐 Cron 작업 설정 스크립트
# Website Health Monitoring Cron Setup

set -e  # 오류 시 스크립트 중단

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 Setting up Website Health Monitoring Cron Jobs${NC}"

# 현재 디렉토리 저장
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo -e "${YELLOW}📍 Project Directory: $PROJECT_DIR${NC}"

# Python 가상환경 확인
if [ -d "$PROJECT_DIR/venv" ]; then
    PYTHON_PATH="$PROJECT_DIR/venv/bin/python"
    echo -e "${GREEN}✅ Virtual environment found${NC}"
elif command -v python3 &> /dev/null; then
    PYTHON_PATH=$(which python3)
    echo -e "${YELLOW}⚠️  Using system Python3: $PYTHON_PATH${NC}"
else
    echo -e "${RED}❌ Python3 not found. Please install Python3.${NC}"
    exit 1
fi

# 환경변수 파일 확인
ENV_FILE="$PROJECT_DIR/.env"
if [ ! -f "$ENV_FILE" ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating template...${NC}"
    cat > "$ENV_FILE" << 'EOL'
# Email Configuration
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
TO_EMAIL=alert-recipient@gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Slack Configuration
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Discord Configuration  
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR/WEBHOOK/URL
EOL
    echo -e "${YELLOW}📝 Please edit $ENV_FILE with your actual credentials${NC}"
fi

# 로그 디렉토리 생성
mkdir -p "$PROJECT_DIR/monitoring/logs"
mkdir -p "$PROJECT_DIR/monitoring/reports"

# Cron 스크립트 생성
CRON_SCRIPT="$PROJECT_DIR/monitoring/run_health_check.sh"

cat > "$CRON_SCRIPT" << EOL
#!/bin/bash

# Set environment variables from .env file
if [ -f "$PROJECT_DIR/.env" ]; then
    export \$(cat "$PROJECT_DIR/.env" | grep -v '^#' | xargs)
fi

# Change to project directory
cd "$PROJECT_DIR"

# Run health check with logging
echo "\$(date '+%Y-%m-%d %H:%M:%S') - Starting health check" >> monitoring/logs/cron.log

$PYTHON_PATH monitoring/health_checker.py >> monitoring/logs/cron.log 2>&1

if [ \$? -eq 0 ]; then
    echo "\$(date '+%Y-%m-%d %H:%M:%S') - Health check completed successfully" >> monitoring/logs/cron.log
else
    echo "\$(date '+%Y-%m-%d %H:%M:%S') - Health check failed with exit code \$?" >> monitoring/logs/cron.log
fi
EOL

chmod +x "$CRON_SCRIPT"

# Cron 작업 설정
echo -e "${BLUE}📅 Setting up cron jobs...${NC}"

# 현재 crontab 백업
crontab -l > /tmp/crontab_backup_$(date +%Y%m%d_%H%M%S) 2>/dev/null || true

# 새로운 cron 작업 추가
(crontab -l 2>/dev/null | grep -v "health_check"; cat << EOL

# Website Health Monitoring Jobs
# 매 15분마다 헬스 체크 (업무시간: 9-18시)
*/15 9-18 * * 1-5 $CRON_SCRIPT

# 매 시간마다 헬스 체크 (업무시간 외)
0 0-8,19-23 * * * $CRON_SCRIPT
0 * * * 0,6 $CRON_SCRIPT

# 매일 오전 9시에 상세 리포트 생성
0 9 * * * $PYTHON_PATH $PROJECT_DIR/performance_monitor.py >> $PROJECT_DIR/monitoring/logs/performance.log 2>&1

# 주간 정리 작업 (일요일 새벽 2시)
0 2 * * 0 find $PROJECT_DIR/monitoring/logs -name "*.log" -mtime +30 -delete
0 2 * * 0 find $PROJECT_DIR/monitoring/reports -name "*.json" -mtime +90 -delete

EOL
) | crontab -

echo -e "${GREEN}✅ Cron jobs installed successfully!${NC}"

# 설치된 cron 작업 표시
echo -e "${BLUE}📋 Installed cron jobs:${NC}"
crontab -l | grep -A 10 "Website Health Monitoring"

# 로그 로테이션 설정 (선택사항)
LOGROTATE_CONF="/etc/logrotate.d/website-monitoring"
if [ -w /etc/logrotate.d ]; then
    echo -e "${BLUE}🔄 Setting up log rotation...${NC}"
    sudo tee "$LOGROTATE_CONF" > /dev/null << EOL
$PROJECT_DIR/monitoring/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    copytruncate
}
EOL
    echo -e "${GREEN}✅ Log rotation configured${NC}"
fi

# 시스템 서비스 설정 (선택사항)
if command -v systemctl &> /dev/null; then
    echo -e "${BLUE}🔧 Would you like to create a systemd service? (y/n)${NC}"
    read -r create_service
    
    if [[ $create_service =~ ^[Yy]$ ]]; then
        SERVICE_FILE="/etc/systemd/system/website-monitoring.service"
        sudo tee "$SERVICE_FILE" > /dev/null << EOL
[Unit]
Description=Website Health Monitoring
After=network.target

[Service]
Type=oneshot
User=$(whoami)
WorkingDirectory=$PROJECT_DIR
EnvironmentFile=$PROJECT_DIR/.env
ExecStart=$PYTHON_PATH $PROJECT_DIR/monitoring/health_checker.py
StandardOutput=append:$PROJECT_DIR/monitoring/logs/service.log
StandardError=append:$PROJECT_DIR/monitoring/logs/service.log

[Install]
WantedBy=multi-user.target
EOL

        # 타이머 설정
        TIMER_FILE="/etc/systemd/system/website-monitoring.timer"
        sudo tee "$TIMER_FILE" > /dev/null << EOL
[Unit]
Description=Website Health Monitoring Timer
Requires=website-monitoring.service

[Timer]
OnCalendar=*:0/15  # 매 15분마다
Persistent=true

[Install]
WantedBy=timers.target
EOL

        sudo systemctl daemon-reload
        sudo systemctl enable website-monitoring.timer
        sudo systemctl start website-monitoring.timer
        
        echo -e "${GREEN}✅ Systemd service and timer created${NC}"
    fi
fi

# 테스트 실행
echo -e "${BLUE}🧪 Running test health check...${NC}"
if "$PYTHON_PATH" "$PROJECT_DIR/monitoring/health_checker.py"; then
    echo -e "${GREEN}✅ Test successful! Monitoring is now active.${NC}"
else
    echo -e "${RED}❌ Test failed. Please check your configuration.${NC}"
    exit 1
fi

echo -e "${GREEN}🎉 Setup complete! Your website is now being monitored.${NC}"
echo -e "${BLUE}📊 Check logs at: $PROJECT_DIR/monitoring/logs/${NC}"
echo -e "${BLUE}📈 View reports at: $PROJECT_DIR/monitoring/reports/${NC}"

# 유용한 명령어 안내
cat << 'EOL'

📚 Useful commands:
  # View cron jobs
  crontab -l

  # Edit cron jobs  
  crontab -e

  # View monitoring logs
  tail -f monitoring/logs/cron.log

  # Manual health check
  ./monitoring/run_health_check.sh

  # Remove cron jobs
  crontab -l | grep -v "health_check" | crontab -

EOL