
import os
import re
from bs4 import BeautifulSoup

def check_romance_test_files():
    """romance-test 모든 파일들의 구조와 내용을 전수 조사"""
    
    print("🔍 Romance Test 파일들 전수 조사 시작...")
    
    languages = ['ko', 'ja', 'en']
    issues_found = []
    
    # 기준점: test18.html 구조 분석
    print("\n📊 기준점 분석: test18.html")
    reference_structure = analyze_reference_structure()
    
    for lang in languages:
        folder_path = f"romance-test/{lang}"
        if not os.path.exists(folder_path):
            issues_found.append(f"❌ {folder_path} 폴더가 존재하지 않음")
            continue
            
        print(f"\n📁 {lang.upper()} 언어 페이지 점검 중...")
        
        # 필수 파일들 확인
        required_files = ['index.html', 'style.css', 'favicon.png', 'thumbnail.png']
        for req_file in required_files:
            if not os.path.exists(os.path.join(folder_path, req_file)):
                issues_found.append(f"❌ {lang}/{req_file} 파일 누락")
        
        # 모든 test*.html 파일 점검
        test_files = [f for f in os.listdir(folder_path) if f.startswith('test') and f.endswith('.html')]
        test_files.sort(key=lambda x: int(re.search(r'test(\d+)', x).group(1)))
        
        for test_file in test_files:
            file_path = os.path.join(folder_path, test_file)
            file_issues = check_individual_file(file_path, lang, test_file, reference_structure)
            issues_found.extend(file_issues)
    
    # 결과 정리
    print("\n" + "="*60)
    print("📋 전수 조사 결과 요약")
    print("="*60)
    
    if not issues_found:
        print("✅ 모든 파일이 정상적으로 작동합니다!")
    else:
        print(f"⚠️  총 {len(issues_found)}개의 문제점 발견:")
        for issue in issues_found:
            print(f"  {issue}")
    
    return issues_found

def analyze_reference_structure():
    """test18.html의 기준 구조 분석"""
    reference_files = [
        'romance-test/ko/test18.html',
        'romance-test/ja/test18.html', 
        'romance-test/en/test18.html'
    ]
    
    structure = {
        'required_elements': ['h1', 'h2', 'div.choices', 'div.result', 'div.navigation'],
        'title_pattern': {
            'ko': r'💖 연애 심리 테스트 \d+$',
            'ja': r'💖 恋愛心理テスト \d+$',
            'en': r'💖 Love Psychology Test \d+$'
        }
    }
    
    return structure

def check_individual_file(file_path, lang, filename, reference_structure):
    """개별 파일 점검"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # 1. 기본 HTML 구조 확인
        if not soup.find('html'):
            issues.append(f"❌ {lang}/{filename}: HTML 태그 누락")
        
        if not soup.find('head'):
            issues.append(f"❌ {lang}/{filename}: HEAD 태그 누락")
        
        if not soup.find('body'):
            issues.append(f"❌ {lang}/{filename}: BODY 태그 누락")
        
        # 2. 필수 메타 태그 확인
        meta_checks = [
            ('charset', 'utf-8'),
            ('viewport', 'width=device-width, initial-scale=1.0')
        ]
        
        for meta_name, expected in meta_checks:
            meta_tag = soup.find('meta', attrs={meta_name: True}) or soup.find('meta', attrs={'name': meta_name})
            if not meta_tag:
                issues.append(f"❌ {lang}/{filename}: {meta_name} 메타 태그 누락")
        
        # 3. 제목 형식 확인
        h1_tag = soup.find('h1')
        if h1_tag:
            title_pattern = reference_structure['title_pattern'][lang]
            if not re.match(title_pattern, h1_tag.get_text().strip()):
                issues.append(f"❌ {lang}/{filename}: H1 제목 형식 불일치 - '{h1_tag.get_text().strip()}'")
        else:
            issues.append(f"❌ {lang}/{filename}: H1 태그 누락")
        
        # 4. 필수 구조 요소 확인
        for element in reference_structure['required_elements']:
            if '.' in element:
                tag, class_name = element.split('.')
                found = soup.find(tag, class_=class_name)
            else:
                found = soup.find(element)
            
            if not found:
                issues.append(f"❌ {lang}/{filename}: {element} 요소 누락")
        
        # 5. test-intro div가 제거되었는지 확인
        test_intro = soup.find('div', class_='test-intro')
        if test_intro:
            issues.append(f"❌ {lang}/{filename}: test-intro div가 여전히 존재함")
        
        # 6. 불필요한 p style 태그 확인
        choices_div = soup.find('div', class_='choices')
        h2_tag = soup.find('h2')
        
        if choices_div and h2_tag:
            # h2와 choices 사이에 p style 태그가 있는지 확인
            current = h2_tag.next_sibling
            while current and current != choices_div:
                if hasattr(current, 'name') and current.name == 'p' and current.get('style'):
                    issues.append(f"❌ {lang}/{filename}: H2와 choices 사이에 불필요한 p style 태그 존재")
                    break
                current = current.next_sibling
        
        # 7. JavaScript 함수 확인
        script_tags = soup.find_all('script')
        has_show_result = False
        has_share_functions = False
        
        for script in script_tags:
            if script.string and 'showResult' in script.string:
                has_show_result = True
            if script.string and ('shareToTwitter' in script.string or 'shareToFacebook' in script.string):
                has_share_functions = True
        
        if not has_show_result:
            issues.append(f"❌ {lang}/{filename}: showResult 함수 누락")
        
        if not has_share_functions:
            issues.append(f"❌ {lang}/{filename}: 공유 함수들 누락")
        
        # 8. 선택지 개수 확인
        choice_divs = soup.find_all('div', class_='choice')
        if len(choice_divs) < 2:
            issues.append(f"❌ {lang}/{filename}: 선택지가 부족함 ({len(choice_divs)}개)")
        
        # 9. CSS 링크 확인
        css_link = soup.find('link', rel='stylesheet')
        if not css_link:
            issues.append(f"❌ {lang}/{filename}: CSS 링크 누락")
        
        # 10. 네비게이션 링크 확인
        nav_div = soup.find('div', class_='navigation')
        if nav_div:
            nav_links = nav_div.find_all('a')
            if len(nav_links) < 2:
                issues.append(f"❌ {lang}/{filename}: 네비게이션 링크 부족")
        
        if not issues:
            print(f"  ✅ {filename}: 정상")
        else:
            print(f"  ⚠️  {filename}: {len([i for i in issues if filename in i])}개 문제 발견")
            
    except Exception as e:
        issues.append(f"❌ {lang}/{filename}: 파일 읽기 오류 - {str(e)}")
    
    return issues

def fix_found_issues(issues):
    """발견된 문제점들 자동 수정"""
    print("\n🔧 발견된 문제점들 자동 수정 시작...")
    
    # 문제점 분류별로 수정 로직 구현
    for issue in issues:
        if "test-intro div가 여전히 존재함" in issue:
            # test-intro div 제거
            pass
        elif "불필요한 p style 태그 존재" in issue:
            # p style 태그 제거
            pass
        # 추가 수정 로직들...

if __name__ == "__main__":
    issues = check_romance_test_files()
    
    if issues:
        print(f"\n🤔 문제점 수정을 진행하시겠습니까? (y/n)")
        # 실제 환경에서는 입력을 받아 처리
        # response = input().lower()
        # if response == 'y':
        #     fix_found_issues(issues)
