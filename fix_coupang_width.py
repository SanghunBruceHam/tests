
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

def fix_coupang_width():
    """쿠팡 광고 폭이 600px인 것을 750px로 수정"""
    
    # 한국어 HTML 파일들 찾기
    korean_files = []
    
    # 루트 디렉토리의 한국어 파일
    if os.path.exists('index.html'):
        korean_files.append('index.html')
    if os.path.exists('ko/index.html'):
        korean_files.append('ko/index.html')
    
    # romance-test 한국어 파일들
    romance_ko_dir = 'romance-test/ko'
    if os.path.exists(romance_ko_dir):
        for file in os.listdir(romance_ko_dir):
            if file.endswith('.html'):
                korean_files.append(os.path.join(romance_ko_dir, file))
    
    # egen-teto 한국어 파일들
    egen_ko_dir = 'egen-teto/ko'
    if os.path.exists(egen_ko_dir):
        for file in os.listdir(egen_ko_dir):
            if file.endswith('.html'):
                korean_files.append(os.path.join(egen_ko_dir, file))
    
    print(f"🔍 한국어 HTML 파일 검색 중... 발견된 파일: {len(korean_files)}개")
    
    updated_count = 0
    unchanged_count = 0
    
    for file_path in korean_files:
        try:
            print(f"\n처리 중: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 쿠팡 광고가 있는지 확인
            if 'PartnersCoupang.G' not in content:
                print(f"⚠️  {file_path}: 쿠팡 광고 없음")
                unchanged_count += 1
                continue
            
            # width가 600인 경우를 찾아서 750으로 변경
            original_content = content
            
            # 패턴 1: "width":"600"
            content = re.sub(r'"width":"600"', '"width":"750"', content)
            
            # 패턴 2: "width":600
            content = re.sub(r'"width":600', '"width":"750"', content)
            
            # 패턴 3: width="600"
            content = re.sub(r'width="600"', 'width="750"', content)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ {file_path}: 광고 폭 600px → 750px 수정 완료")
                updated_count += 1
            else:
                print(f"⚠️  {file_path}: 이미 750px 또는 수정이 필요 없음")
                unchanged_count += 1
                
        except Exception as e:
            print(f"❌ {file_path}: 오류 발생 - {e}")
            unchanged_count += 1
    
    print(f"\n🎉 작업 완료!")
    print(f"✅ 수정됨: {updated_count}개 파일")
    print(f"⚠️  변경 없음: {unchanged_count}개 파일")

if __name__ == "__main__":
    fix_coupang_width()
