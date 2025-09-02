
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Any
from utils import FileManager, ContentProcessor, logger
from config import Config

def scan_test_directories() -> List[Dict[str, Any]]:
    """테스트 디렉토리들을 스캔하여 테스트 정보를 수집"""
    tests = []
    
    try:
        # 루트 디렉토리에서 테스트 폴더들을 찾기
        for item in os.listdir('.'):
            if (os.path.isdir(item) and 
                not item.startswith('.') and 
                item not in ['__pycache__', '.git', 'node_modules']):
                
                test_path = Path(item)
                
                # 언어별 폴더 확인
                languages = {}
                for lang in Config.SUPPORTED_LANGUAGES:
                    lang_path = test_path / lang
                    if lang_path.exists():
                        index_file = lang_path / 'index.html'
                        if index_file.exists():
                            title, desc = ContentProcessor.extract_test_info(str(index_file), lang)
                            languages[lang] = {
                                'url': f'/{item}/{lang}/index.html',
                                'title': title,
                                'desc': desc
                            }
                
                if languages:
                    tests.append({
                        'id': item,
                        **languages
                    })
        
        logger.info(f"스캔 완료: {len(tests)}개 테스트 발견")
        return tests
        
    except OSError as e:
        logger.error(f"디렉토리 스캔 오류: {e}")
        return []
    except Exception as e:
        logger.error(f"예상치 못한 오류: {e}")
        return []

def update_index_html(tests: List[Dict[str, Any]]) -> bool:
    """index.html 파일의 테스트 정보를 업데이트"""
    index_file = 'index.html'
    
    content = FileManager.read_file_safely(index_file)
    if not content:
        return False
    
    try:
        # JavaScript의 tests 배열 부분을 찾아서 교체
        tests_js = generate_tests_js(tests)
        
        # tests 배열 패턴 찾기
        pattern = r'(const tests = \[)(.*?)(\];)'
        replacement = f'\\1\n{tests_js}\n    \\3'
        
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        if new_content != content:
            if FileManager.write_file_safely(index_file, new_content):
                logger.info(f"index.html 업데이트 완료 - {len(tests)}개 테스트")
                return True
        else:
            logger.warning("업데이트할 내용이 없습니다.")
            return False
            
    except re.error as e:
        logger.error(f"정규식 오류: {e}")
        return False
    except Exception as e:
        logger.error(f"index.html 업데이트 실패: {e}")
        return False

def generate_tests_js(tests: List[Dict[str, Any]]) -> str:
    """테스트 데이터를 JavaScript 배열 형식으로 생성"""
    js_items = []
    
    for test in tests:
        js_item = f'      {{\n        id: "{test["id"]}",'
        
        for lang in Config.SUPPORTED_LANGUAGES:
            if lang in test:
                data = test[lang]
                # XSS 방지를 위한 이스케이핑
                safe_title = data["title"].replace('"', '\\"').replace("'", "\\'")
                safe_desc = data["desc"].replace('"', '\\"').replace("'", "\\'")
                safe_url = data["url"].replace('"', '\\"')
                
                js_item += f'\n        {lang}: {{ url: "{safe_url}", title: "{safe_title}", desc: "{safe_desc}" }},'
        
        js_item = js_item.rstrip(',') + '\n      }'
        js_items.append(js_item)
    
    return ',\n'.join(js_items)

def update_language_index_files(tests):
    """각 언어별 index 파일 업데이트"""
    success_count = 0
    
    for lang in ['ko', 'ja', 'en']:
        lang_file = f'{lang}/index.html'
        if os.path.exists(lang_file):
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 테스트 개수 업데이트
                test_count = len(tests)
                # 라벨 텍스트(테스트/Tests/テスト) 대안 그룹을 정확히 매칭
                content = re.sub(
                    r'(<div class="stat-number"[^>]*>)\d+(</div>\s*<div class="stat-label"[^>]*>(?:테스트|Tests|テスト))',
                    f'\\g<1>{test_count}\\g<2>',
                    content
                )
                
                with open(lang_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                success_count += 1
                print(f"✅ {lang_file} 업데이트 완료")
                
            except Exception as e:
                print(f"❌ {lang_file} 업데이트 실패: {e}")
    
    return success_count

def main():
    """메인 실행 함수"""
    print("🔍 테스트 디렉토리 스캔 중...")
    tests = scan_test_directories()
    
    if tests:
        print(f"📋 발견된 테스트: {len(tests)}개")
        for test in tests:
            print(f"  - {test['id']}: {list(test.keys())[1:]} 언어 지원")
        
        print("\n📝 index.html 업데이트 중...")
        success = update_index_html(tests)
        
        print("\n📝 언어별 index 파일 업데이트 중...")
        lang_success = update_language_index_files(tests)
        
        if success or lang_success > 0:
            print("✨ 업데이트 완료!")
        else:
            print("💡 변경사항이 없습니다.")
    else:
        print("⚠️ 테스트를 찾을 수 없습니다.")

if __name__ == "__main__":
    main()
