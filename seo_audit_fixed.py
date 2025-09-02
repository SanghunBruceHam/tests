#!/usr/bin/env python3
"""
Fixed SEO Audit Script - 정확한 정규식으로 SEO 점검
"""

import os
import re
import json

def analyze_seo_fixed(html_content, file_path):
    """개선된 SEO 분석 - 정확한 정규식 사용"""
    issues = []
    score = 0
    max_score = 100
    
    # 파일 경로에서 URL 생성
    base_dir = os.path.abspath(os.path.dirname(__file__))
    try:
        relative_path = os.path.relpath(file_path, start=base_dir)
    except Exception:
        relative_path = file_path
    
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
    
    # 4. Meta description (15점) - 수정된 정규식
    # 다양한 메타 설명 형식을 모두 캐치
    meta_desc_patterns = [
        r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']',
        r'<meta\s+content=["\']([^"\']*?)["\']\s+name=["\']description["\']',
        r'<meta[^>]*name\s*=\s*["\']description["\'][^>]*content\s*=\s*["\']([^"\']*)["\']',
        r'<meta[^>]*content\s*=\s*["\']([^"\']*?)["\']\s*name\s*=\s*["\']description["\']'
    ]
    
    desc_text = ""
    for pattern in meta_desc_patterns:
        meta_desc_match = re.search(pattern, html_content, re.IGNORECASE)
        if meta_desc_match:
            desc_text = meta_desc_match.group(1).strip()
            break
    
    if desc_text:
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
    if re.search(r'<meta[^>]+name\s*=\s*["\']keywords["\']', html_content, re.IGNORECASE):
        score += 5
    else:
        issues.append("⚠️ 메타 키워드 누락")
    
    # 6. Viewport meta (5점)
    if re.search(r'<meta[^>]+name\s*=\s*["\']viewport["\']', html_content, re.IGNORECASE):
        score += 5
    else:
        issues.append("❌ 모바일 뷰포트 태그 누락")
    
    # 7. Charset (5점)
    if re.search(r'<meta[^>]+charset\s*=', html_content, re.IGNORECASE):
        score += 5
    else:
        issues.append("❌ 문자 인코딩 설정 누락")
    
    # 8. Open Graph 태그 (15점) - 더 정확한 검사
    og_tags = ['og:title', 'og:description', 'og:image', 'og:url', 'og:type']
    og_found = []
    for tag in og_tags:
        if re.search(f'<meta[^>]+property\s*=\s*["\']?{re.escape(tag)}["\']?', html_content, re.IGNORECASE):
            og_found.append(tag)
        else:
            issues.append(f"⚠️ {tag} 누락")
    score += len(og_found) * 3
    
    # 9. Twitter Card 태그 (15점) - 더 정확한 검사  
    twitter_tags = ['twitter:card', 'twitter:title', 'twitter:description', 'twitter:image', 'twitter:site']
    twitter_found = []
    for tag in twitter_tags:
        if re.search(f'<meta[^>]+name\s*=\s*["\']?{re.escape(tag)}["\']?', html_content, re.IGNORECASE):
            twitter_found.append(tag)
        else:
            issues.append(f"⚠️ {tag} 누락")
    score += len(twitter_found) * 3
    
    # 10. JSON-LD 구조화 데이터 (15점)
    json_ld_matches = re.findall(r'<script[^>]+type\s*=\s*["\']application/ld\+json["\'][^>]*>(.*?)</script>', html_content, re.DOTALL | re.IGNORECASE)
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
    if re.search(r'<link[^>]+rel\s*=\s*["\']canonical["\']', html_content, re.IGNORECASE):
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
            'meta_desc_length': len(desc_text) if desc_text else 0,
            'meta_desc_found': bool(desc_text),
            'images_count': len(img_tags) if 'img_tags' in locals() else 0,
            'images_with_alt': len(imgs_with_alt) if 'imgs_with_alt' in locals() else 0,
            'json_ld_count': len(json_ld_matches) if 'json_ld_matches' in locals() else 0,
            'og_tags_found': len(og_found),
            'twitter_tags_found': len(twitter_found),
        }
    }

def scan_all_html_files():
    """모든 HTML 파일을 스캔하여 정확한 SEO 분석"""
    base_path = os.path.abspath(os.path.dirname(__file__))
    
    results = []
    
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    analysis = analyze_seo_fixed(content, file_path)
                    analysis['file'] = file_path.replace(base_path, '').lstrip('/')
                    results.append(analysis)
                    
                except Exception as e:
                    print(f"Error analyzing {file_path}: {e}")
    
    return results

def generate_detailed_report(results):
    """상세한 SEO 리포트 생성"""
    results.sort(key=lambda x: x['score'])
    
    total_files = len(results)
    avg_score = sum(r['score'] for r in results) / total_files if total_files > 0 else 0
    
    print("=" * 70)
    print("🔍 FIXED & DETAILED SEO AUDIT REPORT")
    print("=" * 70)
    print(f"📊 총 분석 파일: {total_files}개")
    print(f"📈 평균 SEO 점수: {avg_score:.1f}/100")
    print()
    
    # 점수별 분류
    excellent = [r for r in results if r['score'] >= 90]
    good = [r for r in results if 80 <= r['score'] < 90]
    needs_improvement = [r for r in results if r['score'] < 80]
    
    print(f"🏆 우수 (90+): {len(excellent)}개 파일 ({len(excellent)/total_files*100:.1f}%)")
    print(f"✅ 양호 (80-89): {len(good)}개 파일 ({len(good)/total_files*100:.1f}%)")
    print(f"⚠️ 개선 필요 (<80): {len(needs_improvement)}개 파일 ({len(needs_improvement)/total_files*100:.1f}%)")
    print()
    
    # 메타 설명 통계
    files_with_meta_desc = [r for r in results if r['details']['meta_desc_found']]
    print(f"📝 메타 설명 보유 파일: {len(files_with_meta_desc)}개 ({len(files_with_meta_desc)/total_files*100:.1f}%)")
    print()
    
    # 카테고리별 분석
    categories = {
        'romance-test': [r for r in results if 'romance-test' in r['file']],
        'egen-teto': [r for r in results if 'egen-teto' in r['file']],
        'anime-personality': [r for r in results if 'anime-personality' in r['file']],
        'main': [r for r in results if r['file'].count('/') <= 1 and 'index.html' in r['file']],
        'utility': [r for r in results if any(x in r['file'] for x in ['create_', 'generate_', 'google', 'yandex', 'sandbox', 'monitoring'])],
    }
    
    print("📂 카테고리별 상세 점수:")
    print("-" * 50)
    for cat_name, cat_results in categories.items():
        if cat_results:
            cat_avg = sum(r['score'] for r in cat_results) / len(cat_results)
            files_with_desc = sum(1 for r in cat_results if r['details']['meta_desc_found'])
            print(f"📁 {cat_name}:")
            print(f"   평균 점수: {cat_avg:.1f}점 ({len(cat_results)}개 파일)")  
            print(f"   메타 설명: {files_with_desc}개 파일 보유")
            
            # 소셜 미디어 태그 통계
            avg_og = sum(r['details']['og_tags_found'] for r in cat_results) / len(cat_results)
            avg_twitter = sum(r['details']['twitter_tags_found'] for r in cat_results) / len(cat_results)
            print(f"   Open Graph: 평균 {avg_og:.1f}/5개 태그")
            print(f"   Twitter Card: 평균 {avg_twitter:.1f}/5개 태그")
            print()
    
    # 개선이 필요한 파일들 상세 분석
    print("🔧 즉시 개선 필요 파일들:")
    print("-" * 40)
    
    # Twitter Card 누락 파일들
    twitter_missing = [r for r in results if r['details']['twitter_tags_found'] < 5]
    print(f"📱 Twitter Card 태그 누락: {len(twitter_missing)}개 파일")
    
    # Open Graph 누락 파일들  
    og_missing = [r for r in results if r['details']['og_tags_found'] < 5]
    print(f"📈 Open Graph 태그 누락: {len(og_missing)}개 파일")
    
    # 제목 길이 문제 파일들
    title_issues = [r for r in results if r['details']['title_length'] < 30 or r['details']['title_length'] > 60]
    print(f"📏 제목 길이 문제: {len(title_issues)}개 파일")
    
    return results

if __name__ == "__main__":
    print("🔍 수정된 SEO 스크립트로 정확한 분석을 시작합니다...")
    results = scan_all_html_files()
    generate_detailed_report(results)
    
    # 결과를 JSON으로 저장
    output_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'seo_fixed_results.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n✅ 정확한 분석 완료! 결과가 'seo_fixed_results.json'에 저장되었습니다.")
