#!/usr/bin/env python3
"""
Twitter Card와 Open Graph 태그가 누락된 파일들을 찾는 스크립트
"""

import os
import re

def find_files_missing_tags():
    """Twitter Card와 Open Graph 태그가 누락된 파일들을 찾기"""
    base_path = os.path.abspath(os.path.dirname(__file__))
    
    missing_twitter = []
    missing_og = []
    
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                relative_path = file_path.replace(base_path, '').lstrip('/')
                
                # 검증 파일들 제외
                if any(x in relative_path for x in ['google', 'yandex', 'seo_']):
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Twitter Card 태그 검사
                    twitter_tags = ['twitter:card', 'twitter:title', 'twitter:description', 'twitter:image', 'twitter:site']
                    twitter_count = 0
                    for tag in twitter_tags:
                        if re.search(f'name\s*=\s*["\']?{re.escape(tag)}["\']?', content, re.IGNORECASE):
                            twitter_count += 1
                    
                    if twitter_count < 5:
                        missing_twitter.append({
                            'file': relative_path,
                            'missing_count': 5 - twitter_count,
                            'found_tags': twitter_count
                        })
                    
                    # Open Graph 태그 검사
                    og_tags = ['og:title', 'og:description', 'og:image', 'og:url', 'og:type']
                    og_count = 0
                    for tag in og_tags:
                        if re.search(f'property\s*=\s*["\']?{re.escape(tag)}["\']?', content, re.IGNORECASE):
                            og_count += 1
                    
                    if og_count < 5:
                        missing_og.append({
                            'file': relative_path,
                            'missing_count': 5 - og_count,
                            'found_tags': og_count
                        })
                
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    return missing_twitter, missing_og

if __name__ == "__main__":
    print("🔍 Twitter Card와 Open Graph 태그 누락 파일들을 찾고 있습니다...")
    
    missing_twitter, missing_og = find_files_missing_tags()
    
    print(f"\n📱 Twitter Card 태그가 누락된 파일들 ({len(missing_twitter)}개):")
    print("-" * 50)
    for item in missing_twitter:
        print(f"📄 {item['file']} - {item['found_tags']}/5개 태그 보유 (누락: {item['missing_count']}개)")
    
    print(f"\n📈 Open Graph 태그가 누락된 파일들 ({len(missing_og)}개):")  
    print("-" * 50)
    for item in missing_og:
        print(f"📄 {item['file']} - {item['found_tags']}/5개 태그 보유 (누락: {item['missing_count']}개)")
    
    print(f"\n✅ 분석 완료!")
    print(f"📱 Twitter Card 개선 대상: {len(missing_twitter)}개 파일")
    print(f"📈 Open Graph 개선 대상: {len(missing_og)}개 파일")
