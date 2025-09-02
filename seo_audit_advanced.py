#!/usr/bin/env python3
"""
Advanced SEO Audit Script - 고급 SEO 점검 및 최적화 분석
"""

import os
import re
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import sys

def analyze_seo_advanced(html_content, file_path):
    """고급 SEO 분석 - 더 세밀한 점수 계산"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    issues = []
    score = 0
    max_score = 200  # 더 세밀한 점수 체계
    
    # 파일 경로에서 URL 생성
    base_dir = os.path.abspath(os.path.dirname(__file__))
    try:
        relative_path = os.path.relpath(file_path, start=base_dir)
    except Exception:
        relative_path = file_path
    expected_url = f"https://tests.mahalohana-bruce.com/{relative_path}"
    
    # 1. 기본 HTML 구조 (20점)
    doctype = str(soup).strip().startswith('<!DOCTYPE html>')
    if doctype:
        score += 10
    else:
        issues.append("❌ DOCTYPE 선언 누락")
    
    html_tag = soup.find('html')
    if html_tag and html_tag.get('lang'):
        score += 10
    else:
        issues.append("❌ HTML lang 속성 누락")
    
    # 2. 메타 태그 검사 (50점)
    title = soup.find('title')
    if title and title.string:
        title_text = title.string.strip()
        if 30 <= len(title_text) <= 60:
            score += 15
        elif len(title_text) < 30:
            score += 8
            issues.append(f"⚠️ 제목이 너무 짧음 ({len(title_text)}자)")
        else:
            score += 8
            issues.append(f"⚠️ 제목이 너무 길음 ({len(title_text)}자)")
    else:
        issues.append("❌ 제목 태그 누락")
    
    meta_description = soup.find('meta', attrs={'name': 'description'})
    if meta_description and meta_description.get('content'):
        desc_text = meta_description.get('content').strip()
        if 120 <= len(desc_text) <= 160:
            score += 15
        elif len(desc_text) < 120:
            score += 10
            issues.append(f"⚠️ 메타 설명이 너무 짧음 ({len(desc_text)}자)")
        else:
            score += 10
            issues.append(f"⚠️ 메타 설명이 너무 길음 ({len(desc_text)}자)")
    else:
        issues.append("❌ 메타 설명 누락")
    
    meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
    if meta_keywords and meta_keywords.get('content'):
        score += 5
    else:
        issues.append("⚠️ 메타 키워드 누락")
    
    viewport = soup.find('meta', attrs={'name': 'viewport'})
    if viewport:
        score += 10
    else:
        issues.append("❌ 모바일 뷰포트 태그 누락")
    
    charset = soup.find('meta', attrs={'charset': True})
    if charset:
        score += 5
    else:
        issues.append("❌ 문자 인코딩 설정 누락")
    
    # 3. Open Graph 태그 (25점)
    og_tags = ['og:title', 'og:description', 'og:image', 'og:url', 'og:type']
    og_score = 0
    for tag in og_tags:
        if soup.find('meta', attrs={'property': tag}):
            og_score += 5
        else:
            issues.append(f"⚠️ {tag} 누락")
    score += og_score
    
    # 4. Twitter Card 태그 (25점)
    twitter_tags = ['twitter:card', 'twitter:title', 'twitter:description', 'twitter:image', 'twitter:site']
    twitter_score = 0
    for tag in twitter_tags:
        if soup.find('meta', attrs={'name': tag}):
            twitter_score += 5
        else:
            issues.append(f"⚠️ {tag} 누락")
    score += twitter_score
    
    # 5. 구조화 데이터 (30점)
    json_ld_scripts = soup.find_all('script', {'type': 'application/ld+json'})
    if json_ld_scripts:
        score += 20
        # JSON-LD 구조 검증
        valid_schemas = 0
        for script in json_ld_scripts:
            try:
                json_data = json.loads(script.string)
                if '@context' in json_data and '@type' in json_data:
                    valid_schemas += 1
            except:
                pass
        if valid_schemas >= 2:
            score += 10
        elif valid_schemas >= 1:
            score += 5
    else:
        issues.append("❌ JSON-LD 구조화 데이터 누락")
    
    # 6. Canonical URL (10점)
    canonical = soup.find('link', attrs={'rel': 'canonical'})
    if canonical and canonical.get('href'):
        score += 10
    else:
        issues.append("⚠️ Canonical URL 누락")
    
    # 7. 이미지 최적화 (20점)
    images = soup.find_all('img')
    if images:
        images_with_alt = [img for img in images if img.get('alt')]
        alt_ratio = len(images_with_alt) / len(images)
        score += int(alt_ratio * 10)
        if alt_ratio < 1.0:
            missing_alt = len(images) - len(images_with_alt)
            issues.append(f"⚠️ {missing_alt}개 이미지의 alt 속성 누락")
        
        # 이미지 loading 속성 검사
        lazy_images = [img for img in images if img.get('loading') == 'lazy']
        if lazy_images:
            score += 5
        
        # 이미지 크기 속성 검사
        sized_images = [img for img in images if img.get('width') and img.get('height')]
        if len(sized_images) == len(images):
            score += 5
    
    # 8. 성능 관련 태그 (10점)
    if soup.find('link', attrs={'rel': 'preconnect'}):
        score += 3
    if soup.find('link', attrs={'rel': 'dns-prefetch'}):
        score += 2
    if soup.find('script', attrs={'async': True}):
        score += 3
    if soup.find('script', attrs={'defer': True}):
        score += 2
    
    # 9. 보안 태그 (10점)
    if soup.find('meta', attrs={'http-equiv': 'Content-Security-Policy'}):
        score += 5
    if soup.find('meta', attrs={'name': 'robots'}):
        score += 5
    
    # 최종 점수를 100점 만점으로 변환
    final_score = (score / max_score) * 100
    
    return {
        'score': round(final_score, 1),
        'issues': issues,
        'raw_score': score,
        'max_score': max_score,
        'details': {
            'title_length': len(title.string.strip()) if title and title.string else 0,
            'meta_desc_length': len(meta_description.get('content').strip()) if meta_description and meta_description.get('content') else 0,
            'images_count': len(images) if 'images' in locals() else 0,
            'images_with_alt': len(images_with_alt) if 'images_with_alt' in locals() else 0,
            'json_ld_count': len(json_ld_scripts),
            'has_canonical': canonical is not None,
        }
    }

def scan_all_html_files():
    """모든 HTML 파일을 스캔하여 고급 SEO 분석"""
    base_path = os.path.abspath(os.path.dirname(__file__))
    
    results = []
    
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    analysis = analyze_seo_advanced(content, file_path)
                    analysis['file'] = file_path.replace(base_path, '').lstrip('/')
                    results.append(analysis)
                    
                except Exception as e:
                    print(f"Error analyzing {file_path}: {e}")
    
    return results

def generate_advanced_report(results):
    """고급 SEO 리포트 생성"""
    results.sort(key=lambda x: x['score'])
    
    total_files = len(results)
    avg_score = sum(r['score'] for r in results) / total_files if total_files > 0 else 0
    
    print("=" * 60)
    print("🚀 ADVANCED SEO AUDIT REPORT")
    print("=" * 60)
    print(f"📊 총 분석 파일: {total_files}개")
    print(f"📈 평균 SEO 점수: {avg_score:.1f}/100")
    print()
    
    # 점수별 분류
    excellent = [r for r in results if r['score'] >= 90]
    good = [r for r in results if 80 <= r['score'] < 90]
    needs_improvement = [r for r in results if r['score'] < 80]
    
    print(f"🏆 우수 (90+): {len(excellent)}개 파일")
    print(f"✅ 양호 (80-89): {len(good)}개 파일")
    print(f"⚠️ 개선 필요 (<80): {len(needs_improvement)}개 파일")
    print()
    
    # 가장 개선이 필요한 파일들
    print("🔧 개선이 가장 필요한 파일들:")
    print("-" * 40)
    for result in results[:10]:  # 점수가 낮은 상위 10개
        print(f"📄 {result['file']}")
        print(f"   점수: {result['score']}/100")
        print(f"   주요 문제: {len(result['issues'])}개")
        if result['issues'][:3]:  # 상위 3개 문제만 표시
            for issue in result['issues'][:3]:
                print(f"   • {issue}")
        print()
    
    # 공통 문제점 분석
    all_issues = []
    for result in results:
        all_issues.extend(result['issues'])
    
    # 문제점 빈도 계산
    issue_counts = {}
    for issue in all_issues:
        issue_type = issue.split(' ')[1] if ' ' in issue else issue
        issue_counts[issue_type] = issue_counts.get(issue_type, 0) + 1
    
    print("📊 가장 흔한 SEO 문제들:")
    print("-" * 30)
    sorted_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    for issue, count in sorted_issues:
        percentage = (count / total_files) * 100
        print(f"• {issue}: {count}개 파일 ({percentage:.1f}%)")
    
    return results

if __name__ == "__main__":
    print("🔍 고급 SEO 분석을 시작합니다...")
    results = scan_all_html_files()
    generate_advanced_report(results)
    
    # 결과를 JSON으로 저장
    output_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'seo_audit_advanced_results.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n✅ 분석 완료! 결과가 'seo_audit_advanced_results.json'에 저장되었습니다.")
