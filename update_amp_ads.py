
#!/usr/bin/env python3
import os
import re
from pathlib import Path

def update_romance_test_ads():
    """romance-test 폴더의 모든 페이지에 올바른 광고 구조 적용"""
    
    base_path = Path('romance-test')
    languages = ['ko', 'ja', 'en']
    
    for lang in languages:
        lang_path = base_path / lang
        if not lang_path.exists():
            continue
            
        print(f"\n📁 Processing {lang} files...")
        
        # index.html 및 test1.html부터 test30.html까지 처리
        files_to_process = ['index.html'] + [f'test{i}.html' for i in range(1, 31)]
        
        for filename in files_to_process:
            file_path = lang_path / filename
            
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 1. AMP 스크립트가 헤드에 있는지 확인하고 추가
                    amp_script = '<script async custom-element="amp-ad" src="https://cdn.ampproject.org/v0/amp-ad-0.1.js"></script>'
                    
                    if amp_script not in content:
                        # </head> 바로 앞에 AMP 스크립트 추가
                        content = content.replace('</head>', f'  {amp_script}\n</head>')
                    
                    # 2. AdSense 자동광고 스크립트가 헤드에 있는지 확인
                    adsense_auto_script = 'src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5508768187151867"'
                    
                    if adsense_auto_script not in content:
                        # </head> 바로 앞에 AdSense 자동광고 스크립트 추가
                        adsense_script_full = '''  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5508768187151867"
       crossorigin="anonymous"></script>'''
                        content = content.replace('</head>', f'{adsense_script_full}\n</head>')
                    
                    # 3. 바디 시작 부분에 AMP 광고 추가 (없는 경우만)
                    amp_ad = '''<amp-ad width="100vw" height="320"
     type="adsense"
     data-ad-client="ca-pub-5508768187151867"
     data-ad-slot="7298546648"
     data-auto-format="rspv"
     data-full-width="">
  <div overflow=""></div>
</amp-ad>'''
                    
                    if 'amp-ad width="100vw" height="320"' not in content:
                        # <body> 태그 다음에 AMP 광고 추가
                        content = re.sub(
                            r'(<body[^>]*>)\s*',
                            r'\1\n\n  ' + amp_ad + '\n\n',
                            content
                        )
                    
                    # 4. 푸터 위에 기존 AdSense 광고가 있는지 확인하고 정리
                    # 기존 AdSense 광고 패턴들 정리
                    existing_adsense_patterns = [
                        r'<!-- AdSense Ad Unit -->.*?</script>',
                        r'<script async src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js\?client=ca-pub-5508768187151867"[^>]*></script>\s*<!-- 디스플레이 가로 -->.*?</script>',
                        r'<ins class="adsbygoogle"[^>]*data-ad-slot="7298546648"[^>]*></ins>\s*<script>\s*\(adsbygoogle = window\.adsbygoogle \|\| \[\]\)\.push\(\{\}\);\s*</script>'
                    ]
                    
                    # 기존 AdSense 광고 제거
                    for pattern in existing_adsense_patterns:
                        content = re.sub(pattern, '', content, flags=re.DOTALL)
                    
                    # 5. 푸터 바로 위에 새로운 AdSense 광고 추가
                    adsense_ad = '''
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
                    
                    # 푸터 바로 앞에 AdSense 광고 삽입
                    if '<footer>' in content:
                        content = content.replace('<footer>', adsense_ad + '<footer>')
                    else:
                        # 푸터가 없으면 </body> 앞에 삽입
                        content = content.replace('</body>', adsense_ad + '</body>')
                    
                    # 파일 저장
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"  ✅ {filename}: Updated with complete ad structure")
                    
                except Exception as e:
                    print(f"  ❌ {filename}: Error - {e}")
            else:
                print(f"  ⚠️ {filename}: File not found")

if __name__ == "__main__":
    print("🚀 Updating all romance-test pages with complete ad structure...")
    update_romance_test_ads()
    print("\n✨ All files updated with:")
    print("   📍 Head: AMP script + AdSense auto ads script")
    print("   📍 Body top: AMP ad unit")
    print("   📍 Body bottom: AdSense fixed ad unit")
    print("✅ Done!")
