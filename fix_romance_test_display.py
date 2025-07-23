
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from bs4 import BeautifulSoup

def fix_romance_test_pages():
    """romance-test 폴더의 모든 테스트 페이지에서 불필요한 표시 텍스트 제거"""
    
    print("🔍 romance-test 페이지 불필요한 텍스트 제거 시작...")
    
    languages = ['ko', 'ja', 'en']
    
    for lang in languages:
        folder_path = f"romance-test/{lang}"
        if not os.path.exists(folder_path):
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
                
                # 문제가 되는 텍스트 패턴들 제거
                patterns_to_remove = [
                    "The code has been modified to enhance SEO",
                    "```html",
                    "```",
                    # 한국어 페이지의 잘못된 텍스트
                    r"💖 연애 심리 테스트 \d+: 당신의 .*?\n이 테스트는.*?분석해드립니다\.",
                    # 일본어 페이지의 잘못된 텍스트  
                    r"💖 恋愛心理テスト \d+: あなたの.*?\nこのテストは.*?分析します\.",
                    # 영어 페이지의 잘못된 텍스트
                    r"💖 Love Psychology Test \d+: Your.*?\nThis test is.*?analyze\."
                ]
                
                # body 태그 내에서 직접적으로 표시되는 텍스트 노드 찾기 및 제거
                body = soup.find('body')
                if body:
                    # body의 직접 텍스트 노드에서 문제 텍스트 제거
                    for text_node in body.find_all(text=True, recursive=False):
                        if any(pattern in str(text_node) for pattern in [
                            "The code has been modified",
                            "```html",
                            "```"
                        ]):
                            text_node.extract()
                    
                    # container div 앞의 텍스트 노드 제거
                    container = body.find('div', class_='container')
                    if container:
                        # container 앞에 있는 모든 텍스트 노드 확인
                        for sibling in container.previous_siblings:
                            if hasattr(sibling, 'string') and sibling.string:
                                if any(pattern in sibling.string for pattern in [
                                    "The code has been modified",
                                    "html",
                                    "💖 연애 심리 테스트",
                                    "이 테스트는",
                                    "⏰ 소요시간",
                                    "📊 결과"
                                ]):
                                    sibling.extract()
                
                # test-info div가 중복되어 있는지 확인하고 정리
                test_info_divs = soup.find_all('div', class_='test-info')
                if len(test_info_divs) > 1:
                    # 첫 번째를 제외하고 모두 제거
                    for div in test_info_divs[1:]:
                        div.extract()
                
                # HTML 구조 정리
                cleaned_content = str(soup)
                
                # 정규식으로 추가 정리
                cleaned_content = re.sub(r'The code has been modified.*?```\s*html\s*', '', cleaned_content, flags=re.DOTALL)
                cleaned_content = re.sub(r'```\s*html\s*', '', cleaned_content)
                cleaned_content = re.sub(r'```', '', cleaned_content)
                
                # 중복된 빈 줄 제거
                cleaned_content = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned_content)
                
                # 파일에 다시 쓰기
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)
                
                print(f"✅ {test_file} 수정 완료")
                
            except Exception as e:
                print(f"❌ {test_file} 처리 중 오류: {e}")
                continue
    
    print("🎉 모든 romance-test 페이지 정리 완료!")

if __name__ == "__main__":
    fix_romance_test_pages()
