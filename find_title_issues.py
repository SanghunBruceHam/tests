#!/usr/bin/env python3
"""
제목 길이 문제가 있는 파일들을 찾는 스크립트
"""

import os
import re

def find_title_length_issues():
    """제목 길이가 30-60자 범위를 벗어나는 파일들을 찾기"""
    base_path = '/Users/sanghunbruceham/Documents/GitHub/tests'
    
    title_issues = []
    
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
                    
                    # 제목 태그 찾기
                    title_match = re.search(r'<title[^>]*>([^<]*)</title>', content, re.IGNORECASE)
                    if title_match:
                        title_text = title_match.group(1).strip()
                        title_length = len(title_text)
                        
                        if title_length < 30 or title_length > 60:
                            issue_type = "너무 짧음" if title_length < 30 else "너무 길음"
                            title_issues.append({
                                'file': relative_path,
                                'title': title_text,
                                'length': title_length,
                                'issue': issue_type,
                                'full_path': file_path
                            })
                
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    return title_issues

if __name__ == "__main__":
    print("🔍 제목 길이 문제가 있는 파일들을 찾고 있습니다...")
    
    title_issues = find_title_length_issues()
    
    # 문제별로 분류
    too_short = [item for item in title_issues if item['issue'] == '너무 짧음']
    too_long = [item for item in title_issues if item['issue'] == '너무 길음']
    
    print(f"\n📏 제목 길이 문제가 있는 파일들 ({len(title_issues)}개):")
    print("=" * 70)
    
    print(f"\n⚠️ 제목이 너무 짧은 파일들 ({len(too_short)}개) - 30자 미만:")
    print("-" * 50)
    for item in too_short:
        print(f"📄 {item['file']}")
        print(f"   제목: \"{item['title']}\" ({item['length']}자)")
        print()
    
    print(f"⚠️ 제목이 너무 긴 파일들 ({len(too_long)}개) - 60자 초과:")
    print("-" * 50)
    for item in too_long:
        print(f"📄 {item['file']}")
        print(f"   제목: \"{item['title']}\" ({item['length']}자)")
        print()
    
    print(f"✅ 분석 완료!")
    print(f"📏 제목 길이 개선 대상: {len(title_issues)}개 파일")
    
    # 긴 제목들 중에서 최적화 후보들을 출력
    if too_long:
        print(f"\n🎯 최적화 우선순위 (길이순):")
        print("-" * 40)
        too_long_sorted = sorted(too_long, key=lambda x: x['length'], reverse=True)
        for item in too_long_sorted[:10]:  # 상위 10개만
            print(f"{item['length']}자: {item['file']}")