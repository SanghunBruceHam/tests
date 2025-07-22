
#!/usr/bin/env python3
import os
import re
from pathlib import Path

def remove_footer_whitespace(file_path):
    """HTML 파일에서 풋터 위의 불필요한 화이트스페이스 제거"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 풋터 앞의 과도한 빈 줄들 제거
        # 여러 개의 연속된 빈 줄을 하나로 줄임
        content = re.sub(r'\n\s*\n\s*\n+(?=\s*<footer)', '\n\n<footer', content)
        
        # 풋터 바로 앞의 불필요한 공백 라인들 제거
        content = re.sub(r'\n\s+\n\s*<footer', '\n\n<footer', content)
        
        # </div> 다음에 오는 과도한 빈 줄들을 정리 (풋터 앞에서)
        content = re.sub(r'(</div>)\s*\n\s*\n\s*\n+(?=\s*<footer)', r'\1\n\n<footer', content)
        
        # 일반적인 과도한 빈 줄들 정리 (3개 이상의 연속 빈 줄을 2개로)
        content = re.sub(r'\n\s*\n\s*\n\s*\n+', '\n\n', content)
        
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
    """romance-test 폴더의 모든 HTML 파일에서 풋터 위 화이트스페이스 제거"""
    base_path = Path('romance-test')
    languages = ['ko', 'ja', 'en']
    
    print("🧹 풋터 위 화이트스페이스 제거 중...\n")
    
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
