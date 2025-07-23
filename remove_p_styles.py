
import os
import re
from bs4 import BeautifulSoup

def remove_p_styles_above_choices():
    """모든 romance-test 페이지에서 choices div 위에 있는 p style 태그 제거"""
    
    print("🔍 choices div 위의 p style 태그 제거 시작...")
    
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
                
                # choices div 찾기
                choices_div = soup.find('div', class_='choices')
                
                if choices_div:
                    # choices div의 이전 형제 요소들 확인
                    previous_siblings = list(choices_div.previous_siblings)
                    removed_count = 0
                    
                    for sibling in reversed(previous_siblings):  # 역순으로 처리
                        if hasattr(sibling, 'name') and sibling.name == 'p' and sibling.get('style'):
                            print(f"  📄 {test_file}에서 p style 태그 발견: {str(sibling)[:100]}...")
                            sibling.extract()
                            removed_count += 1
                        elif hasattr(sibling, 'name') and sibling.name:  # 다른 태그를 만나면 중단
                            break
                    
                    if removed_count > 0:
                        # 파일에 저장
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(str(soup))
                        print(f"  ✅ {test_file}에서 {removed_count}개의 p style 태그 제거 완료")
                    else:
                        print(f"  ⚪ {test_file}에서 제거할 p style 태그 없음")
                else:
                    print(f"  ❓ {test_file}에서 choices div를 찾을 수 없음")
                
            except Exception as e:
                print(f"  ❌ {test_file} 처리 중 오류: {e}")
    
    print("🎉 모든 p style 태그 제거 완료!")

if __name__ == "__main__":
    remove_p_styles_above_choices()
