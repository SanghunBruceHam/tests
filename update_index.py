
import os
import re
import json
from pathlib import Path

def scan_test_directories():
    """테스트 디렉토리들을 스캔하여 테스트 정보를 수집"""
    tests = []
    
    # 루트 디렉토리에서 테스트 폴더들을 찾기
    for item in os.listdir('.'):
        if os.path.isdir(item) and not item.startswith('.') and item != '__pycache__':
            test_path = Path(item)
            
            # 언어별 폴더 확인
            languages = {}
            for lang in ['ko', 'ja', 'en']:
                lang_path = test_path / lang
                if lang_path.exists():
                    index_file = lang_path / 'index.html'
                    if index_file.exists():
                        # HTML 파일에서 제목과 설명 추출
                        title, desc = extract_test_info(index_file, lang)
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
    
    return tests

def extract_test_info(html_file, lang):
    """HTML 파일에서 테스트 제목과 설명을 추출"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # title 태그에서 제목 추출
        title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else f"테스트"
        
        # description 메타 태그에서 설명 추출
        desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', content, re.IGNORECASE)
        desc = desc_match.group(1).strip() if desc_match else "심리테스트"
        
        # 제목에서 불필요한 부분 제거
        title = re.sub(r'[|｜].*$', '', title).strip()
        
        return title, desc
        
    except Exception as e:
        print(f"Error reading {html_file}: {e}")
        return "테스트", "심리테스트"

def update_index_html(tests):
    """index.html 파일의 테스트 정보를 업데이트"""
    index_file = 'index.html'
    
    try:
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # JavaScript의 tests 배열 부분을 찾아서 교체
        tests_js = generate_tests_js(tests)
        
        # tests 배열 패턴 찾기
        pattern = r'(const tests = \[)(.*?)(\];)'
        replacement = f'\\1\n{tests_js}\n    \\3'
        
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        if new_content != content:
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ index.html 업데이트 완료 - {len(tests)}개 테스트")
            return True
        else:
            print("⚠️ 업데이트할 내용이 없습니다.")
            return False
            
    except Exception as e:
        print(f"❌ index.html 업데이트 실패: {e}")
        return False

def generate_tests_js(tests):
    """테스트 데이터를 JavaScript 배열 형식으로 생성"""
    js_items = []
    
    for test in tests:
        js_item = f'      {{\n        id: "{test["id"]}",'
        
        for lang in ['ko', 'ja', 'en']:
            if lang in test:
                data = test[lang]
                js_item += f'\n        {lang}: {{ url: "{data["url"]}", title: "{data["title"]}", desc: "{data["desc"]}" }},'
        
        js_item = js_item.rstrip(',') + '\n      }'
        js_items.append(js_item)
    
    return ',\n'.join(js_items)

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
        
        if success:
            print("✨ 업데이트 완료!")
        else:
            print("💡 변경사항이 없습니다.")
    else:
        print("⚠️ 테스트를 찾을 수 없습니다.")

if __name__ == "__main__":
    main()
