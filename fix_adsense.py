
#!/usr/bin/env python3
import os
import re
from pathlib import Path

def fix_adsense_in_file(file_path):
    """개별 파일의 AdSense 광고 코드 수정"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # AMP 스크립트 제거
        content = re.sub(
            r'\s*<!-- AMP Ad Script -->\s*\n\s*<script async custom-element="amp-ad" src="https://cdn\.ampproject\.org/v0/amp-ad-0\.1\.js"></script>\s*\n?',
            '',
            content
        )
        
        # AMP 광고 태그 제거
        content = re.sub(
            r'\s*<amp-ad width="100vw" height="320"[^>]*>.*?</amp-ad>\s*\n?',
            '',
            content,
            flags=re.DOTALL
        )
        
        # AdSense 광고 초기화 스크립트 추가
        adsense_pattern = r'(\s*<ins class="adsbygoogle"[^>]*></ins>)\s*\n'
        if re.search(adsense_pattern, content):
            content = re.sub(
                adsense_pattern,
                r'\1\n  <script>\n       (adsbygoogle = window.adsbygoogle || []).push({});\n  </script>\n',
                content
            )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """romance-test 폴더의 모든 테스트 파일 수정"""
    base_path = Path('romance-test')
    languages = ['ko', 'ja', 'en']
    
    for lang in languages:
        lang_path = base_path / lang
        if not lang_path.exists():
            continue
            
        print(f"\n📁 Processing {lang} files...")
        
        # test1.html부터 test30.html까지 처리
        for i in range(1, 31):
            test_file = lang_path / f'test{i}.html'
            
            if test_file.exists():
                if fix_adsense_in_file(test_file):
                    print(f"  ✅ {test_file.name}: Fixed")
                else:
                    print(f"  ❌ {test_file.name}: Failed")

if __name__ == "__main__":
    main()
