
import os
import re

def fix_favicon_paths():
    # romance-test 폴더의 모든 언어 폴더
    languages = ['ko', 'ja', 'en']
    
    for lang in languages:
        lang_dir = f'romance-test/{lang}'
        if not os.path.exists(lang_dir):
            continue
            
        # 각 언어 폴더의 모든 HTML 파일 찾기
        for file_name in os.listdir(lang_dir):
            if file_name.endswith('.html') and file_name.startswith('test'):
                file_path = os.path.join(lang_dir, file_name)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 잘못된 파비콘 경로 패턴 찾기 및 수정
                    # /favicon.ico 를 ./favicon.png 로 변경
                    updated_content = re.sub(
                        r'<link rel="icon" href="/favicon\.ico" type="image/x-icon" />',
                        '<link rel="icon" href="./favicon.png" type="image/png" />',
                        content
                    )
                    
                    # 변경사항이 있으면 파일 저장
                    if updated_content != content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(updated_content)
                        print(f"Updated: {file_path}")
                    
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    fix_favicon_paths()
    print("Favicon paths fixed!")
