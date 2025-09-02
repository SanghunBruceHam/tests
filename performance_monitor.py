#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Performance Monitoring Script
정기적인 사이트 성능 체크를 위한 도구
"""

import subprocess
import json
import time
from datetime import datetime
import os

class PerformanceMonitor:
    def __init__(self):
        self.base_url = "https://tests.mahalohana-bruce.com"
        self.test_pages = [
            "/",
            "/ko/index.html",
            "/ja/index.html", 
            "/en/index.html",
            "/romance-test/ko/",
            "/romance-test/ko/test1.html"
        ]
        
    def check_lighthouse_availability(self):
        """Lighthouse CLI 설치 확인"""
        try:
            result = subprocess.run(['lighthouse', '--version'], 
                                 capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def run_lighthouse_audit(self, url, output_dir="performance_reports"):
        """Lighthouse 감사 실행"""
        if not self.check_lighthouse_availability():
            print("⚠️  Lighthouse CLI not available. Install with:")
            print("   npm install -g lighthouse")
            return None
            
        os.makedirs(output_dir, exist_ok=True)
        
        # 파일명에 타임스탬프 추가
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        page_name = url.replace('/', '_').replace(':', '').replace('.html', '')
        filename = f"lighthouse_{page_name}_{timestamp}"
        
        cmd = [
            'lighthouse',
            f"{self.base_url}{url}",
            '--output=json',
            '--output=html',
            f'--output-path={output_dir}/{filename}',
            '--chrome-flags=--headless',
            '--quiet'
        ]
        
        try:
            print(f"🔍 Auditing: {self.base_url}{url}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print(f"✅ Report saved: {output_dir}/{filename}")
                return f"{output_dir}/{filename}.json"
            else:
                print(f"❌ Error auditing {url}: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print(f"⏱️  Timeout auditing {url}")
            return None
        except Exception as e:
            print(f"❌ Exception auditing {url}: {e}")
            return None
    
    def analyze_report(self, json_file):
        """Lighthouse 결과 분석"""
        if not json_file or not os.path.exists(json_file):
            return None
            
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            categories = data.get('categories', {})
            audits = data.get('audits', {})
            
            # Core Web Vitals 추출
            metrics = {
                'performance_score': categories.get('performance', {}).get('score', 0) * 100,
                'accessibility_score': categories.get('accessibility', {}).get('score', 0) * 100,
                'best_practices_score': categories.get('best-practices', {}).get('score', 0) * 100,
                'seo_score': categories.get('seo', {}).get('score', 0) * 100,
                'first_contentful_paint': audits.get('first-contentful-paint', {}).get('displayValue', 'N/A'),
                'largest_contentful_paint': audits.get('largest-contentful-paint', {}).get('displayValue', 'N/A'),
                'cumulative_layout_shift': audits.get('cumulative-layout-shift', {}).get('displayValue', 'N/A'),
                'first_input_delay': audits.get('max-potential-fid', {}).get('displayValue', 'N/A')
            }
            
            return metrics
            
        except Exception as e:
            print(f"❌ Error analyzing report {json_file}: {e}")
            return None
    
    def generate_summary_report(self, reports_dir="performance_reports"):
        """성능 보고서 요약 생성"""
        print("\n" + "="*60)
        print("📊 PERFORMANCE MONITORING SUMMARY")
        print("="*60)
        
        if not self.check_lighthouse_availability():
            print("\n⚠️  Lighthouse CLI not available for detailed audit.")
            print("Manual checks you can perform:")
            print("1. Visit https://pagespeed.web.dev/")
            print(f"2. Test key pages: {self.base_url}")
            print("3. Check Core Web Vitals in Google Search Console")
            print("4. Monitor loading times in browser DevTools")
            return
        
        all_results = []
        
        for page in self.test_pages:
            print(f"\n🔍 Testing: {page}")
            report_file = self.run_lighthouse_audit(page)
            
            if report_file:
                metrics = self.analyze_report(report_file)
                if metrics:
                    metrics['page'] = page
                    all_results.append(metrics)
                    
                    print(f"   Performance: {metrics['performance_score']:.0f}")
                    print(f"   Accessibility: {metrics['accessibility_score']:.0f}")
                    print(f"   SEO: {metrics['seo_score']:.0f}")
            
            time.sleep(2)  # Rate limiting
        
        # 요약 통계
        if all_results:
            avg_performance = sum(r['performance_score'] for r in all_results) / len(all_results)
            avg_accessibility = sum(r['accessibility_score'] for r in all_results) / len(all_results)
            avg_seo = sum(r['seo_score'] for r in all_results) / len(all_results)
            
            print(f"\n📈 AVERAGE SCORES:")
            print(f"   Performance: {avg_performance:.1f}/100")
            print(f"   Accessibility: {avg_accessibility:.1f}/100")
            print(f"   SEO: {avg_seo:.1f}/100")
            
            # 개선 권장사항
            if avg_performance < 90:
                print(f"\n🎯 RECOMMENDATIONS:")
                print("   - Consider image optimization (WebP format)")
                print("   - Minimize JavaScript and CSS")
                print("   - Enable compression (gzip/brotli)")
                
        print(f"\n📁 Reports saved in: {reports_dir}/")
        print("="*60)

if __name__ == "__main__":
    monitor = PerformanceMonitor()
    monitor.generate_summary_report()
