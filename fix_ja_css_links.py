
import os
import glob

def fix_japanese_css_links():
    # 일본어 폴더의 모든 HTML 파일 찾기
    ja_files = glob.glob('romance-test/ja/*.html')
    
    for file_path in ja_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # CSS 링크 수정
            if 'href="style.css"' in content:
                content = content.replace('href="style.css"', 'href="./style.css"')
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed CSS link in: {file_path}")
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    fix_japanese_css_links()
    print("Japanese CSS link fixing complete!")
