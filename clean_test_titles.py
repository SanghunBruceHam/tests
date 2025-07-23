
import os
import re
from bs4 import BeautifulSoup

def clean_test_titles():
    """모든 romance-test 페이지에서 타이틀을 '💖 연애 심리 테스트 X'만 남기고 콜론 뒤 내용 제거"""
    
    print("🔍 테스트 타이틀 정리 시작...")
    
    languages = {
        'ko': '💖 연애 심리 테스트',
        'ja': '💖 恋愛心理テスト',
        'en': '💖 Love Psychology Test'
    }
    
    for lang, title_prefix in languages.items():
        folder_path = f"romance-test/{lang}"
        if not os.path.exists(folder_path):
            print(f"❌ {folder_path} 폴더가 존재하지 않습니다.")
            continue
            
        print(f"📁 {lang} 페이지 처리 중...")
        
        # 모든 test*.html 파일 찾기
        test_files = [f for f in os.listdir(folder_path) if f.startswith('test') and f.endswith('.html')]
        
        for test_file in test_files:
            file_path = os.path.join(folder_path, test_file)
            
            try:
                # 파일명에서 테스트 번호 추출
                test_number = re.search(r'test(\d+)', test_file)
                if not test_number:
                    continue
                
                test_num = test_number.group(1)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # BeautifulSoup으로 HTML 파싱
                soup = BeautifulSoup(content, 'html.parser')
                
                # h1 태그 찾기 및 수정
                h1_tags = soup.find_all('h1')
                modified = False
                
                for h1 in h1_tags:
                    if h1.get_text().strip().startswith(title_prefix):
                        # 새로운 타이틀로 변경
                        new_title = f"{title_prefix} {test_num}"
                        h1.string = new_title
                        modified = True
                        print(f"  📝 {test_file}: h1 태그 수정 - '{new_title}'")
                
                # 파일에 저장
                if modified:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(str(soup))
                    print(f"  ✅ {test_file} 수정 완료")
                else:
                    print(f"  ⚪ {test_file}에서 수정할 h1 태그 없음")
                
            except Exception as e:
                print(f"  ❌ {test_file} 처리 중 오류: {e}")
    
    print("🎉 모든 테스트 타이틀 정리 완료!")

if __name__ == "__main__":
    clean_test_titles()
