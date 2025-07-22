
#!/usr/bin/env python3
import os
import re
from pathlib import Path

def clean_and_fix_ads(file_path):
    """파일의 광고 코드를 정리하고 올바른 구조로 수정"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 기존 광고 관련 코드들 모두 제거
        patterns_to_remove = [
            r'<script async src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js\?client=ca-pub-5508768187151867"[^>]*></script>',
            r'<script async custom-element="amp-ad" src="https://cdn\.ampproject\.org/v0/amp-ad-0\.1\.js"></script>',
            r'<ins class="adsbygoogle"[^>]*>.*?</ins>',
            r'<script>\s*\(adsbygoogle = window\.adsbygoogle \|\| \[\]\)\.push\(\{\}\);\s*</script>',
            r'<amp-ad[^>]*>.*?</amp-ad>',
            r'<!-- AdSense.*?-->',
            r'<!-- 디스플레이.*?-->',
            r'<!-- AMP Ad.*?-->',
        ]
        
        for pattern in patterns_to_remove:
            content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
        
        # 2. 불필요한 빈 줄들 정리
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        # 3. 헤드에 필요한 스크립트 추가 (</head> 바로 앞에)
        head_scripts = '''  <!-- Google AdSense Auto Ads -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5508768187151867"
       crossorigin="anonymous"></script>
  <script async custom-element="amp-ad" src="https://cdn.ampproject.org/v0/amp-ad-0.1.js"></script>
'''
        
        if '</head>' in content:
            content = content.replace('</head>', head_scripts + '</head>')
        
        # 4. 바디 시작 직후에 AMP 광고 추가
        amp_ad = '''
  <amp-ad width="100vw" height="320"
     type="adsense"
     data-ad-client="ca-pub-5508768187151867"
     data-ad-slot="7298546648"
     data-auto-format="rspv"
     data-full-width="">
  <div overflow=""></div>
</amp-ad>

'''
        
        # <body> 태그 뒤에 AMP 광고 삽입
        if '<body>' in content:
            content = content.replace('<body>', '<body>' + amp_ad)
        
        # 5. 푸터 앞에 일반 AdSense 광고 추가
        footer_ad = '''
  <!-- AdSense Fixed Ad Unit -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5508768187151867"
       crossorigin="anonymous"></script>
  <!-- 디스플레이 가로 -->
  <ins class="adsbygoogle"
       style="display:block"
       data-ad-client="ca-pub-5508768187151867"
       data-ad-slot="7298546648"
       data-ad-format="auto"
       data-full-width-responsive="true"></ins>
  <script>
       (adsbygoogle = window.adsbygoogle || []).push({});
  </script>

'''
        
        if '<footer>' in content:
            content = content.replace('<footer>', footer_ad + '<footer>')
        else:
            # 푸터가 없으면 </body> 앞에 삽입
            content = content.replace('</body>', footer_ad + '</body>')
        
        # 6. 파일 저장 (변경사항이 있을 때만)
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """romance-test 폴더의 모든 HTML 파일 처리"""
    base_path = Path('romance-test')
    languages = ['ko', 'ja', 'en']
    
    total_processed = 0
    
    for lang in languages:
        lang_path = base_path / lang
        if not lang_path.exists():
            continue
            
        print(f"\n📁 Processing {lang} files...")
        
        # index.html과 모든 test 파일들 처리
        files_to_process = ['index.html'] + [f'test{i}.html' for i in range(1, 31)]
        
        for filename in files_to_process:
            file_path = lang_path / filename
            
            if file_path.exists():
                if clean_and_fix_ads(file_path):
                    print(f"  ✅ {filename}: Updated with correct ad structure")
                    total_processed += 1
                else:
                    print(f"  📄 {filename}: No changes needed")
            else:
                print(f"  ❌ {filename}: File not found")
    
    print(f"\n🎉 Total files processed: {total_processed}")
    print("✨ All romance-test pages now have the correct ad structure!")

if __name__ == "__main__":
    main()
