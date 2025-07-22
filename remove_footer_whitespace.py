
#!/usr/bin/env python3
import os
import re
from pathlib import Path

def completely_remove_footer_whitespace(file_path):
    """푸터 앞의 모든 빈 줄과 공백을 완전히 제거하는 강력한 함수"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        original_lines = lines[:]
        
        # 푸터 라인 찾기
        footer_line_index = -1
        for i, line in enumerate(lines):
            if '<footer>' in line:
                footer_line_index = i
                break
        
        if footer_line_index == -1:
            return False
        
        # 푸터 앞의 모든 빈 줄 제거
        new_lines = []
        skip_empty_lines = False
        
        for i, line in enumerate(lines):
            # </div> 이후부터 푸터까지 빈 줄 제거 모드 시작
            if '</div>' in line and i < footer_line_index:
                new_lines.append(line)
                skip_empty_lines = True
                continue
            
            # 푸터에 도달하면 빈 줄 제거 모드 종료
            if i == footer_line_index:
                # 푸터 앞에 정확히 한 줄 추가
                new_lines.append('\n')
                new_lines.append(line)
                skip_empty_lines = False
                continue
            
            # 빈 줄 제거 모드일 때 빈 줄은 스킵
            if skip_empty_lines and line.strip() == '':
                continue
            
            new_lines.append(line)
        
        # 변경사항이 있는 경우에만 파일 저장
        if new_lines != original_lines:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
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
