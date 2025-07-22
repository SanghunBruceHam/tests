
#!/usr/bin/env python3
import os
import re
from pathlib import Path

def completely_remove_footer_whitespace(file_path):
    """푸터 앞의 모든 빈 줄과 공백을 완전히 제거"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. </div> 다음부터 <footer> 사이의 모든 빈 줄과 공백 제거
        pattern = r'(</div>\s*)\n+\s*(<footer>)'
        content = re.sub(pattern, r'\1\n\2', content)
        
        # 2. </body> 앞의 빈 줄들도 제거
        pattern = r'\n+\s*\n+\s*(</body>)'
        content = re.sub(pattern, r'\n\1', content)
        
        # 3. 연속된 빈 줄들을 하나로 통합
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        
        # 4. 탭이나 스페이스로만 이루어진 줄들 제거
        lines = content.split('\n')
        cleaned_lines = []
        
        for i, line in enumerate(lines):
            # 푸터 바로 앞의 빈 줄들을 찾아서 제거
            if i < len(lines) - 1 and '<footer>' in lines[i + 1]:
                if line.strip() == '':
                    continue
            cleaned_lines.append(line)
        
        content = '\n'.join(cleaned_lines)
        
        # 5. 마지막으로 </div>와 <footer> 사이에 정확히 한 줄만 남기기
        content = re.sub(r'(</div>)\s*\n\s*\n+\s*(<footer>)', r'\1\n\n\2', content)
        content = re.sub(r'(</div>)\s*\n\s*(<footer>)', r'\1\n\n\2', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """모든 HTML 파일에서 푸터 앞 빈 줄들을 완전히 제거"""
    base_path = Path('romance-test')
    languages = ['ko', 'ja', 'en']
    
    print("🧹 푸터 앞 모든 빈 줄을 완전히 제거 중...\n")
    
    total_processed = 0
    
    for lang in languages:
        lang_path = base_path / lang
        if not lang_path.exists():
            continue
            
        print(f"📁 {lang.upper()} 폴더 처리 중...")
        
        # 모든 HTML 파일 처리
        html_files = list(lang_path.glob('*.html'))
        
        for file_path in html_files:
            if completely_remove_footer_whitespace(file_path):
                print(f"  ✅ {file_path.name}: 빈 줄 완전히 제거됨")
                total_processed += 1
            else:
                print(f"  ℹ️  {file_path.name}: 변경사항 없음")
    
    print(f"\n🎉 총 {total_processed}개 파일이 완전히 정리되었습니다!")

if __name__ == "__main__":
    main()
