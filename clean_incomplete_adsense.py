
#!/usr/bin/env python3
import os
import re
from pathlib import Path

def clean_incomplete_adsense_from_file(file_path):
    """파일에서 불완전한 AdSense 코드를 정리"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 불완전한 AdSense 스크립트 패턴들 제거
        patterns_to_remove = [
            # 불완전한 스크립트 태그 (닫는 태그가 없는 것)
            r'\s*<script async src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js\?client=ca-pub-5508768187151867"\s*\n',
            r'\s*<script async src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js\?client=ca-pub-5508768187151867"$',
            
            # 잘못된 닫는 태그들
            r'\s*crossorigin="anonymous"></script>\s*\n',
            r'^\s*crossorigin="anonymous"></script>\s*$',
            
            # Google AdSense 주석만 남은 것들
            r'\s*<!-- Google AdSense -->\s*\n',
            r'^\s*<!-- Google AdSense -->\s*$',
            
            # 빈 줄들과 함께 있는 패턴들
            r'\n\s*\n\s*crossorigin="anonymous"></script>',
        ]
        
        for pattern in patterns_to_remove:
            content = re.sub(pattern, '', content, flags=re.MULTILINE)
        
        # 연속된 빈 줄들 정리 (3개 이상의 연속 빈줄을 2개로)
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        
        # 파일이 변경되었으면 저장
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """romance-test 폴더의 모든 HTML 파일에서 불완전한 AdSense 코드 제거"""
    base_path = Path('romance-test')
    languages = ['ko', 'ja', 'en']
    
    print("🧹 불완전한 AdSense 코드 정리 중...\n")
    
    total_cleaned = 0
    
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
                if clean_incomplete_adsense_from_file(file_path):
                    print(f"  ✅ {filename}: 불완전한 코드 정리됨")
                    total_cleaned += 1
                else:
                    print(f"  📝 {filename}: 정리할 코드 없음")
            else:
                print(f"  ❌ {filename}: 파일 없음")
    
    print(f"\n🎉 총 {total_cleaned}개 파일이 정리되었습니다!")

if __name__ == "__main__":
    main()
