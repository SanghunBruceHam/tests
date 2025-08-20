#!/usr/bin/env python3
"""
Simple SEO Audit Script - 기본 라이브러리만 사용하는 SEO 점검
"""

import os
import re
import json

def analyze_seo_simple(html_content, file_path):
    """간단한 SEO 분석 - 정규식 기반"""
    issues = []
    score = 0
    max_score = 100
    
    # 파일 경로에서 URL 생성
    relative_path = file_path.replace('/Users/sanghunbruceham/Documents/GitHub/tests', '')
    if relative_path.startswith('/'):
        relative_path = relative_path[1:]
    
    # 1. DOCTYPE 검사 (5점)
    if re.search(r'<!DOCTYPE\s+html>', html_content, re.IGNORECASE):
        score += 5
    else:
        issues.append("❌ DOCTYPE 선언 누락")
    
    # 2. HTML lang 속성 (5점)
    if re.search(r'<html[^>]+lang\s*=', html_content, re.IGNORECASE):
        score += 5
    else:
        issues.append("❌ HTML lang 속성 누락")
    
    # 3. Title 태그 (15점)
    title_match = re.search(r'<title[^>]*>([^<]*)</title>', html_content, re.IGNORECASE)
    if title_match:
        title_text = title_match.group(1).strip()
        title_length = len(title_text)
        if 30 <= title_length <= 60:
            score += 15
        elif title_length > 0:
            score += 10
            if title_length < 30:
                issues.append(f"⚠️ 제목이 너무 짧음 ({title_length}자)")
            else:
                issues.append(f"⚠️ 제목이 너무 길음 ({title_length}자)")
    else:
        issues.append("❌ 제목 태그 누락")
    
    # 4. Meta description (15점)
    meta_desc_match = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)["\']', html_content, re.IGNORECASE)
    if meta_desc_match:
        desc_text = meta_desc_match.group(1).strip()
        desc_length = len(desc_text)
        if 120 <= desc_length <= 160:
            score += 15
        elif desc_length > 0:
            score += 10
            if desc_length < 120:
                issues.append(f"⚠️ 메타 설명이 너무 짧음 ({desc_length}자)")
            else:
                issues.append(f"⚠️ 메타 설명이 너무 길음 ({desc_length}자)")
    else:
        issues.append("❌ 메타 설명 누락")
    
    # 5. Meta keywords (5점)
    if re.search(r'<meta[^>]+name=["\']keywords["\']', html_content, re.IGNORECASE):
        score += 5
    else:
        issues.append("⚠️ 메타 키워드 누락")
    
    # 6. Viewport meta (5점)
    if re.search(r'<meta[^>]+name=["\']viewport["\']', html_content, re.IGNORECASE):
        score += 5
    else:
        issues.append("❌ 모바일 뷰포트 태그 누락")
    
    # 7. Charset (5점)
    if re.search(r'<meta[^>]+charset\s*=', html_content, re.IGNORECASE):
        score += 5
    else:
        issues.append("❌ 문자 인코딩 설정 누락")
    
    # 8. Open Graph 태그 (15점)
    og_tags = ['og:title', 'og:description', 'og:image', 'og:url', 'og:type']
    og_score = 0
    for tag in og_tags:
        if re.search(f'<meta[^>]+property=["\']{tag}["\']', html_content, re.IGNORECASE):
            og_score += 3
        else:
            issues.append(f"⚠️ {tag} 누락")
    score += og_score
    
    # 9. Twitter Card 태그 (15점)
    twitter_tags = ['twitter:card', 'twitter:title', 'twitter:description', 'twitter:image', 'twitter:site']
    twitter_score = 0
    for tag in twitter_tags:
        if re.search(f'<meta[^>]+name=["\']{tag}["\']', html_content, re.IGNORECASE):
            twitter_score += 3
        else:
            issues.append(f"⚠️ {tag} 누락")
    score += twitter_score
    
    # 10. JSON-LD 구조화 데이터 (15점)
    json_ld_matches = re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html_content, re.DOTALL | re.IGNORECASE)
    if json_ld_matches:
        valid_schemas = 0
        for match in json_ld_matches:
            try:
                json_data = json.loads(match.strip())
                if '@context' in json_data and '@type' in json_data:
                    valid_schemas += 1
            except:
                pass
        if valid_schemas >= 2:
            score += 15
        elif valid_schemas >= 1:
            score += 10
        else:
            score += 5
    else:
        issues.append("❌ JSON-LD 구조화 데이터 누락")
    
    # 11. Canonical URL (5점)
    if re.search(r'<link[^>]+rel=["\']canonical["\']', html_content, re.IGNORECASE):
        score += 5
    else:
        issues.append("⚠️ Canonical URL 누락")
    
    # 12. 이미지 alt 속성 (10점)
    img_tags = re.findall(r'<img[^>]*>', html_content, re.IGNORECASE)
    if img_tags:
        imgs_with_alt = [img for img in img_tags if re.search(r'alt\s*=', img, re.IGNORECASE)]
        alt_ratio = len(imgs_with_alt) / len(img_tags) if img_tags else 0
        score += int(alt_ratio * 10)
        if alt_ratio < 1.0:
            missing_alt = len(img_tags) - len(imgs_with_alt)
            issues.append(f"⚠️ {missing_alt}개 이미지의 alt 속성 누락")
    
    return {
        'score': min(score, max_score),  # 최대 100점 제한
        'issues': issues,
        'raw_score': score,
        'max_score': max_score,
        'details': {
            'title_length': len(title_match.group(1).strip()) if title_match else 0,
            'meta_desc_length': len(meta_desc_match.group(1).strip()) if meta_desc_match else 0,
            'images_count': len(img_tags) if 'img_tags' in locals() else 0,
            'images_with_alt': len(imgs_with_alt) if 'imgs_with_alt' in locals() else 0,
            'json_ld_count': len(json_ld_matches) if 'json_ld_matches' in locals() else 0,
        }
    }

def scan_all_html_files():
    """모든 HTML 파일을 스캔하여 SEO 분석"""
    base_path = '/Users/sanghunbruceham/Documents/GitHub/tests'
    
    results = []
    
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    analysis = analyze_seo_simple(content, file_path)
                    analysis['file'] = file_path.replace(base_path, '').lstrip('/')
                    results.append(analysis)
                    
                except Exception as e:
                    print(f"Error analyzing {file_path}: {e}")
    
    return results

def generate_report(results):
    """SEO 리포트 생성"""
    results.sort(key=lambda x: x['score'])
    
    total_files = len(results)
    avg_score = sum(r['score'] for r in results) / total_files if total_files > 0 else 0
    
    print("=" * 60)
    print("🔍 UPDATED SEO AUDIT REPORT")
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
    
    # 카테고리별 분석
    categories = {
        'romance-test': [r for r in results if 'romance-test' in r['file']],
        'egen-teto': [r for r in results if 'egen-teto' in r['file']],
        'anime-personality': [r for r in results if 'anime-personality' in r['file']],
        'main': [r for r in results if r['file'].count('/') <= 1 and 'index.html' in r['file']],
        'utility': [r for r in results if any(x in r['file'] for x in ['create_', 'generate_', 'google', 'yandex', 'sandbox', 'monitoring'])],
    }
    
    print("📂 카테고리별 점수:")
    print("-" * 30)
    for cat_name, cat_results in categories.items():
        if cat_results:
            cat_avg = sum(r['score'] for r in cat_results) / len(cat_results)
            print(f"📁 {cat_name}: {len(cat_results)}개 파일, 평균 {cat_avg:.1f}점")
    
    print()
    print("🔧 개선이 가장 필요한 파일들:")
    print("-" * 40)
    for result in results[:10]:  # 점수가 낮은 상위 10개
        print(f"📄 {result['file']}")
        print(f"   점수: {result['score']}/100")
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
        # 이슈의 핵심 키워드 추출
        if '메타 설명' in issue:
            key = '메타 설명 관련'
        elif 'Twitter' in issue or 'twitter' in issue:
            key = 'Twitter Card 관련'
        elif 'og:' in issue:
            key = 'Open Graph 관련'
        elif 'alt' in issue:
            key = '이미지 alt 속성'
        elif 'JSON-LD' in issue:
            key = '구조화 데이터'
        elif '키워드' in issue:
            key = '메타 키워드'
        elif 'Canonical' in issue:
            key = 'Canonical URL'
        else:
            key = issue.split(' ')[1] if ' ' in issue else issue
        
        issue_counts[key] = issue_counts.get(key, 0) + 1
    
    print("📊 가장 흔한 SEO 문제들:")
    print("-" * 30)
    sorted_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    for issue, count in sorted_issues:
        percentage = (count / total_files) * 100
        print(f"• {issue}: {count}개 파일 ({percentage:.1f}%)")
    
    return results

if __name__ == "__main__":
    print("🔍 현재 SEO 상태를 재분석합니다...")
    results = scan_all_html_files()
    generate_report(results)
    
    # 결과를 JSON으로 저장
    with open('/Users/sanghunbruceham/Documents/GitHub/tests/seo_current_status.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n✅ 분석 완료! 결과가 'seo_current_status.json'에 저장되었습니다.")