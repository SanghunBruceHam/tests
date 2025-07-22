
#!/usr/bin/env python3
import os
import re
from pathlib import Path

def remove_adsense_from_file(file_path):
    """파일에서 모든 AdSense 관련 코드 제거"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # AdSense 관련 모든 패턴들 제거
        patterns_to_remove = [
            # AdSense 스크립트들
            r'<script async src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js[^>]*>.*?</script>',
            r'<script async custom-element="amp-ad" src="https://cdn\.ampproject\.org/v0/amp-ad-0\.1\.js"></script>',
            
            # AMP 광고
            r'<amp-ad[^>]*>.*?</amp-ad>',
            
            # AdSense ins 태그
            r'<ins class="adsbygoogle"[^>]*>.*?</ins>',
            
            # AdSense 초기화 스크립트
            r'<script>\s*\(adsbygoogle = window\.adsbygoogle \|\| \[\]\)\.push\(\{\}\);\s*</script>',
            
            # AdSense 주석들
            r'<!-- Google AdSense.*?-->',
            r'<!-- AdSense.*?-->',
            r'<!-- 디스플레이.*?-->',
            r'<!-- AMP Ad.*?-->',
            
            # 빈 줄이 있는 패턴들
            r'\s*<!-- Google AdSense Auto Ads -->\s*\n',
            r'\s*<!-- Google AdSense Auto Ads -->\s*',
        ]
        
        for pattern in patterns_to_remove:
            content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
        
        # 연속된 빈 줄들 정리
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        
        # 변경사항이 있으면 파일 저장
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """romance-test 폴더의 모든 HTML 파일에서 AdSense 코드 제거"""
    base_path = Path('romance-test')
    languages = ['ko', 'ja', 'en']
    
    print("🧹 Romance-test에서 모든 AdSense 코드 제거 중...\n")
    
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
                if remove_adsense_from_file(file_path):
                    print(f"  ✅ {filename}: AdSense 코드 제거됨")
                    total_processed += 1
                else:
                    print(f"  📝 {filename}: AdSense 코드 없음")
            else:
                print(f"  ❌ {filename}: 파일 없음")
        
        print()
    
    print(f"🎉 완료! 총 {total_processed}개 파일에서 AdSense 코드가 제거되었습니다.")

if __name__ == "__main__":
    main()
