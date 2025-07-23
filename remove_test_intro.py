
import os
import re
from bs4 import BeautifulSoup

def remove_test_intro_divs():
    """모든 romance-test 페이지에서 test-intro 클래스를 가진 div 제거"""
    
    print("🔍 test-intro 클래스 div 제거 시작...")
    
    languages = ['ko', 'ja', 'en']
    
    for lang in languages:
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
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # BeautifulSoup으로 HTML 파싱
                soup = BeautifulSoup(content, 'html.parser')
                
                # test-intro 클래스를 가진 모든 div 찾기
                test_intro_divs = soup.find_all('div', class_='test-intro')
                
                if test_intro_divs:
                    print(f"  📄 {test_file}에서 {len(test_intro_divs)}개의 test-intro div 발견")
                    
                    # 모든 test-intro div 제거
                    for div in test_intro_divs:
                        div.extract()
                    
                    # 파일에 저장
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(str(soup))
                    
                    print(f"  ✅ {test_file} 수정 완료")
                else:
                    print(f"  ⚪ {test_file}에서 test-intro div 없음")
                
            except Exception as e:
                print(f"  ❌ {test_file} 처리 중 오류: {e}")
    
    print("🎉 모든 test-intro 클래스 div 제거 완료!")

if __name__ == "__main__":
    remove_test_intro_divs()
