
#!/usr/bin/env python3
import os
import re
from pathlib import Path

def clean_footer_whitespace(content):
    """푸터 위의 화이트스페이스를 정확하게 제거"""
    lines = content.split('\n')
    cleaned_lines = []
    
    for i, line in enumerate(lines):
        # 푸터 태그를 찾았을 때
        if '<footer>' in line:
            # 이전 라인들에서 끝의 모든 빈 줄들을 제거
            while cleaned_lines and cleaned_lines[-1].strip() == '':
                cleaned_lines.pop()
            
            # 푸터 라인 추가 (빈 줄 없이)
            cleaned_lines.append(line)
        else:
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def remove_footer_whitespace(file_path):
    """HTML 파일에서 푸터 위의 화이트스페이스 제거"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        
        # 정규식으로 푸터 위 빈 줄들 제거
        # </div> 다음에 오는 여러 빈 줄들과 <footer> 사이의 공백 제거
        pattern = r'(</div>\s*)\n\s*\n+\s*(<footer>)'
        content = re.sub(pattern, r'\1\n\2', content, flags=re.MULTILINE)
        
        # 일반적인 경우: 푸터 앞의 모든 빈 줄 제거
        pattern2 = r'\n\s*\n+\s*(<footer>)'
        content = re.sub(pattern2, r'\n\1', content)

        # 파일 저장 (변경사항이 있을 때만)
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True

        return False

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """romance-test 폴더의 모든 HTML 파일에서 푸터 위 화이트스페이스 제거"""
    base_path = Path('romance-test')
    languages = ['ko', 'ja', 'en']

    print("🧹 푸터 위 화이트스페이스 정확한 제거 중...\n")

    total_processed = 0

    for lang in languages:
        lang_path = base_path / lang
        if not lang_path.exists():
            continue

        print(f"📁 {lang.upper()} 폴더 처리 중...")

        # index.html과 모든 test 파일들 처리
        files_to_process = ['index.html'] + [f'test{i}.html' for i in range(1, 31)]

        for filename in files_to_process:
            file_path = lang_path / filename

            if file_path.exists():
                if remove_footer_whitespace(file_path):
                    print(f"  ✅ {filename}: 화이트스페이스 제거됨")
                    total_processed += 1
                else:
                    print(f"  ℹ️  {filename}: 변경사항 없음")

    print(f"\n🎉 총 {total_processed}개 파일에서 화이트스페이스가 제거되었습니다!")

if __name__ == "__main__":
    main()
