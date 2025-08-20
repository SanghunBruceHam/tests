#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Website Health Monitoring System
웹사이트 상태 모니터링 및 알림 시스템
"""

import requests
import time
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from typing import List, Dict, Optional
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('monitoring.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AlertSystem:
    """다중 채널 알림 시스템"""
    
    def __init__(self):
        # 환경변수에서 설정 로드
        self.email_config = {
            'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
            'smtp_port': int(os.getenv('SMTP_PORT', '587')),
            'email_user': os.getenv('EMAIL_USER'),
            'email_password': os.getenv('EMAIL_PASSWORD'),
            'to_email': os.getenv('TO_EMAIL')
        }
        
        self.slack_webhook = os.getenv('SLACK_WEBHOOK_URL')
        self.discord_webhook = os.getenv('DISCORD_WEBHOOK_URL')
        
    def send_email_alert(self, subject: str, message: str):
        """이메일 알림 발송"""
        if not all([self.email_config['email_user'], 
                   self.email_config['email_password'], 
                   self.email_config['to_email']]):
            logger.warning("Email configuration incomplete")
            return False
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_config['email_user']
            msg['To'] = self.email_config['to_email']
            msg['Subject'] = f"🚨 {subject}"
            
            body = f"""
            <html>
            <body>
                <h2 style="color: #e74c3c;">{subject}</h2>
                <p><strong>시간:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <div style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #e74c3c; margin: 10px 0;">
                    {message.replace('\n', '<br>')}
                </div>
                <p><small>이 메시지는 자동 모니터링 시스템에서 발송되었습니다.</small></p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.starttls()
                server.login(self.email_config['email_user'], self.email_config['email_password'])
                server.send_message(msg)
                
            logger.info("Email alert sent successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")
            return False
    
    def send_slack_alert(self, message: str, severity: str = "warning"):
        """Slack 알림 발송"""
        if not self.slack_webhook:
            logger.warning("Slack webhook URL not configured")
            return False
            
        color_map = {
            "good": "#36a64f",
            "warning": "#ff9500", 
            "danger": "#e74c3c",
            "info": "#3498db"
        }
        
        payload = {
            "text": "🚨 시스템 알림",
            "attachments": [{
                "color": color_map.get(severity, "#ff9500"),
                "title": "Health Check Alert",
                "text": message,
                "footer": "Website Monitoring",
                "ts": int(time.time())
            }]
        }
        
        try:
            response = requests.post(self.slack_webhook, json=payload, timeout=10)
            response.raise_for_status()
            logger.info("Slack alert sent successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to send Slack alert: {e}")
            return False
    
    def send_discord_alert(self, message: str, severity: str = "warning"):
        """Discord 알림 발송"""
        if not self.discord_webhook:
            logger.warning("Discord webhook URL not configured")
            return False
            
        color_map = {
            "good": 0x36a64f,
            "warning": 0xff9500,
            "danger": 0xe74c3c,
            "info": 0x3498db
        }
        
        embed = {
            "title": "🚨 Website Health Alert",
            "description": message,
            "color": color_map.get(severity, 0xff9500),
            "timestamp": datetime.now().isoformat(),
            "footer": {
                "text": "Website Monitoring System"
            }
        }
        
        payload = {
            "embeds": [embed]
        }
        
        try:
            response = requests.post(self.discord_webhook, json=payload, timeout=10)
            response.raise_for_status()
            logger.info("Discord alert sent successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to send Discord alert: {e}")
            return False
    
    def send_alert(self, subject: str, message: str, severity: str = "warning"):
        """모든 구성된 채널로 알림 발송"""
        results = []
        
        # 이메일 알림
        results.append(self.send_email_alert(subject, message))
        
        # Slack 알림
        results.append(self.send_slack_alert(f"**{subject}**\n{message}", severity))
        
        # Discord 알림
        results.append(self.send_discord_alert(f"**{subject}**\n{message}", severity))
        
        return any(results)  # 하나라도 성공하면 True

class HealthChecker:
    """웹사이트 상태 모니터링"""
    
    def __init__(self):
        self.base_url = "https://tests.mahalohana-bruce.com"
        self.alert_system = AlertSystem()
        
        # 모니터링할 엔드포인트
        self.endpoints = [
            "/",
            "/ko/index.html",
            "/ja/index.html", 
            "/en/index.html",
            "/romance-test/ko/",
            "/romance-test/ko/test1.html",
            "/anime-personality/ko/index.html",
            "/sitemap.xml",
            "/robots.txt"
        ]
        
        # 성능 임계값
        self.thresholds = {
            'response_time': 5.0,  # 5초
            'status_code': 200,
            'content_length': 1000  # 최소 콘텐츠 길이
        }
    
    def check_endpoint(self, endpoint: str) -> Dict:
        """단일 엔드포인트 상태 확인"""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'HealthChecker/1.0'
            })
            
            response_time = time.time() - start_time
            
            result = {
                'url': url,
                'status_code': response.status_code,
                'response_time': response_time,
                'content_length': len(response.content),
                'is_healthy': True,
                'issues': []
            }
            
            # 상태 코드 확인
            if response.status_code != 200:
                result['is_healthy'] = False
                result['issues'].append(f"HTTP {response.status_code}")
            
            # 응답 시간 확인
            if response_time > self.thresholds['response_time']:
                result['is_healthy'] = False
                result['issues'].append(f"Slow response: {response_time:.2f}s")
            
            # 콘텐츠 길이 확인
            if len(response.content) < self.thresholds['content_length']:
                result['is_healthy'] = False
                result['issues'].append(f"Content too short: {len(response.content)} bytes")
                
            return result
            
        except requests.exceptions.Timeout:
            return {
                'url': url,
                'status_code': 0,
                'response_time': 10.0,
                'content_length': 0,
                'is_healthy': False,
                'issues': ['Timeout']
            }
        except Exception as e:
            return {
                'url': url,
                'status_code': 0,
                'response_time': 0,
                'content_length': 0,
                'is_healthy': False,
                'issues': [f"Error: {str(e)}"]
            }
    
    def run_health_check(self) -> Dict:
        """전체 건강 상태 확인"""
        results = []
        
        logger.info("Starting health check...")
        
        for endpoint in self.endpoints:
            result = self.check_endpoint(endpoint)
            results.append(result)
            
            if not result['is_healthy']:
                logger.warning(f"Issue detected on {result['url']}: {result['issues']}")
        
        # 전체 상태 분석
        healthy_count = sum(1 for r in results if r['is_healthy'])
        total_count = len(results)
        overall_healthy = healthy_count == total_count
        
        summary = {
            'timestamp': datetime.now().isoformat(),
            'overall_healthy': overall_healthy,
            'healthy_endpoints': healthy_count,
            'total_endpoints': total_count,
            'avg_response_time': sum(r['response_time'] for r in results) / len(results),
            'results': results
        }
        
        # 문제가 있을 때 알림 발송
        if not overall_healthy:
            unhealthy_endpoints = [r for r in results if not r['is_healthy']]
            self.send_alert_for_issues(unhealthy_endpoints)
        
        logger.info(f"Health check completed: {healthy_count}/{total_count} endpoints healthy")
        return summary
    
    def send_alert_for_issues(self, unhealthy_endpoints: List[Dict]):
        """문제가 있는 엔드포인트에 대한 알림 발송"""
        if not unhealthy_endpoints:
            return
        
        issues_text = "\n".join([
            f"• {endpoint['url']}: {', '.join(endpoint['issues'])}"
            for endpoint in unhealthy_endpoints
        ])
        
        subject = f"Website Health Issues Detected ({len(unhealthy_endpoints)} endpoints)"
        message = f"""
다음 엔드포인트에서 문제가 감지되었습니다:

{issues_text}

자세한 내용을 확인하고 필요한 조치를 취해주세요.

모니터링 대시보드: {self.base_url}
        """
        
        severity = "danger" if len(unhealthy_endpoints) > len(self.endpoints) // 2 else "warning"
        self.alert_system.send_alert(subject, message, severity)
    
    def save_report(self, summary: Dict, filename: Optional[str] = None):
        """결과를 JSON 파일로 저장"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"health_report_{timestamp}.json"
        
        os.makedirs("monitoring/reports", exist_ok=True)
        filepath = f"monitoring/reports/{filename}"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Report saved to {filepath}")

def main():
    """메인 실행 함수"""
    checker = HealthChecker()
    
    # 건강 상태 확인
    summary = checker.run_health_check()
    
    # 보고서 저장
    checker.save_report(summary)
    
    # 결과 출력
    print(f"\n{'='*50}")
    print(f"HEALTH CHECK SUMMARY")
    print(f"{'='*50}")
    print(f"Time: {summary['timestamp']}")
    print(f"Status: {'✅ HEALTHY' if summary['overall_healthy'] else '🚨 ISSUES DETECTED'}")
    print(f"Endpoints: {summary['healthy_endpoints']}/{summary['total_endpoints']}")
    print(f"Average Response Time: {summary['avg_response_time']:.2f}s")
    
    if not summary['overall_healthy']:
        print(f"\n🚨 Issues detected:")
        for result in summary['results']:
            if not result['is_healthy']:
                print(f"  • {result['url']}: {', '.join(result['issues'])}")

if __name__ == "__main__":
    main()