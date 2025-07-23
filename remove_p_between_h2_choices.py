
import os
import re
from bs4 import BeautifulSoup

def remove_p_between_h2_and_choices():
    """모든 romance-test 페이지에서 </h2>와 <div class="choices"> 사이의 p style 태그 제거"""
    
    print("🔍 h2와 choices div 사이의 p style 태그 제거 시작...")
    
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
                
                # h2 태그들 찾기
                h2_tags = soup.find_all('h2')
                removed_count = 0
                
                for h2_tag in h2_tags:
                    # h2 태그 다음 형제 요소들 확인
                    next_siblings = []
                    current = h2_tag.next_sibling
                    
                    while current:
                        if hasattr(current, 'name'):
                            if current.name == 'div' and 'choices' in current.get('class', []):
                                # choices div를 만나면 중단
                                break
                            elif current.name == 'p' and current.get('style'):
                                # p style 태그 발견
                                print(f"  📄 {test_file}에서 p style 태그 발견: {str(current)[:100]}...")
                                next_siblings.append(current)
                        
                        current = current.next_sibling
                    
                    # 발견된 p style 태그들 제거
                    for p_tag in next_siblings:
                        p_tag.extract()
                        removed_count += 1
                
                if removed_count > 0:
                    # 파일에 저장
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(str(soup))
                    print(f"  ✅ {test_file}에서 {removed_count}개의 p style 태그 제거 완료")
                else:
                    print(f"  ⚪ {test_file}에서 제거할 p style 태그 없음")
                
            except Exception as e:
                print(f"  ❌ {test_file} 처리 중 오류: {e}")
    
    print("🎉 모든 h2와 choices div 사이의 p style 태그 제거 완료!")

if __name__ == "__main__":
    remove_p_between_h2_and_choices()
