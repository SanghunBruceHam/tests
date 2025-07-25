
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

def fix_google_analytics():
    """romance-test 테스트 페이지들의 Google Analytics 코드 수정"""
    
    # romance-test 디렉토리의 모든 언어별 테스트 파일들 찾기
    test_files = []
    
    romance_test_dir = Path('romance-test')
    if romance_test_dir.exists():
        for lang in ['ko', 'en', 'ja']:
            lang_dir = romance_test_dir / lang
            if lang_dir.exists():
                # test*.html 파일들 찾기
                for file in lang_dir.glob('test*.html'):
                    test_files.append(str(file))
    
    print(f"🔍 romance-test 테스트 파일 검색 중... 발견된 파일: {len(test_files)}개")
    
    if not test_files:
        print("❌ romance-test 테스트 파일을 찾을 수 없습니다.")
        return
    
    updated_count = 0
    unchanged_count = 0
    
    for file_path in test_files:
        try:
            print(f"\n처리 중: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 이미 올바른 Google Analytics 코드가 있는지 확인
            if 'https://www.googletagmanager.com/gtag/js?id=G-45VSGEM7EZ' in content:
                print(f"✅ {file_path}: 이미 올바른 Google Analytics 코드가 있음")
                unchanged_count += 1
                continue
            
            # 기존의 불완전한 Google Analytics 코드 패턴 찾기
            incomplete_pattern = r'<!-- Google tag \(gtag\.js\) -->\s*<script>\s*window\.dataLayer = window\.dataLayer \|\| \[\];\s*function gtag\(\)\{dataLayer\.push\(arguments\);\}\s*gtag\(\'js\', new Date\(\)\);\s*gtag\(\'config\', \'G-45VSGEM7EZ\'\);\s*</script>'
            
            # 올바른 Google Analytics 코드
            correct_ga_code = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-45VSGEM7EZ"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-45VSGEM7EZ');
</script>'''
            
            # 패턴 매칭 및 교체
            if re.search(incomplete_pattern, content, re.DOTALL):
                new_content = re.sub(incomplete_pattern, correct_ga_code, content, flags=re.DOTALL)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"✅ {file_path}: Google Analytics 코드 수정 완료")
                updated_count += 1
            else:
                # 다른 패턴으로 시도
                # 더 유연한 패턴 (공백, 줄바꿈 등을 고려)
                flexible_pattern = r'<!-- Google tag \(gtag\.js\) -->\s*<script>[^<]*window\.dataLayer[^<]*</script>'
                
                if re.search(flexible_pattern, content, re.DOTALL):
                    new_content = re.sub(flexible_pattern, correct_ga_code, content, flags=re.DOTALL)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    print(f"✅ {file_path}: Google Analytics 코드 수정 완료 (유연한 패턴)")
                    updated_count += 1
                else:
                    print(f"⚠️  {file_path}: Google Analytics 패턴을 찾을 수 없음")
                    unchanged_count += 1
                
        except Exception as e:
            print(f"❌ {file_path}: 오류 발생 - {e}")
            unchanged_count += 1
    
    print(f"\n🎉 작업 완료!")
    print(f"✅ 수정됨: {updated_count}개 파일")
    print(f"⚠️  변경 없음: {unchanged_count}개 파일")

def check_ga_status():
    """Google Analytics 코드 상태 확인"""
    print("📊 Google Analytics 코드 상태 확인")
    print("=" * 50)
    
    romance_test_dir = Path('romance-test')
    if not romance_test_dir.exists():
        print("❌ romance-test 디렉토리를 찾을 수 없습니다.")
        return
    
    total_files = 0
    correct_files = 0
    incorrect_files = 0
    
    for lang in ['ko', 'en', 'ja']:
        lang_dir = romance_test_dir / lang
        if lang_dir.exists():
            test_files = list(lang_dir.glob('test*.html'))
            total_files += len(test_files)
            
            print(f"\n📁 {lang}/ 디렉토리: {len(test_files)}개 파일")
            
            for file in test_files:
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if 'https://www.googletagmanager.com/gtag/js?id=G-45VSGEM7EZ' in content:
                        print(f"  ✅ {file.name}: 올바른 GA 코드")
                        correct_files += 1
                    else:
                        print(f"  ❌ {file.name}: GA 코드 누락 또는 불완전")
                        incorrect_files += 1
                        
                except Exception as e:
                    print(f"  ⚠️  {file.name}: 읽기 오류 - {e}")
                    incorrect_files += 1
    
    print(f"\n📊 전체 요약:")
    print(f"총 파일 수: {total_files}개")
    print(f"올바른 GA 코드: {correct_files}개")
    print(f"수정 필요: {incorrect_files}개")

def main():
    """메인 실행 함수"""
    print("🔧 romance-test Google Analytics 코드 수정 도구")
    print("=" * 50)
    
    # 현재 상태 확인
    check_ga_status()
    
    print("\n🔧 Google Analytics 코드 수정 시작...")
    fix_google_analytics()
    
    print("\n📊 수정 후 상태 확인...")
    check_ga_status()

if __name__ == "__main__":
    main()
