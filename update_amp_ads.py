
import os
import re
from pathlib import Path

def update_amp_ads_in_test_files():
    """romance-test 폴더의 모든 테스트 파일에서 AMP 광고 코드를 푸터 위로 이동"""
    
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
                try:
                    with open(test_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # AMP 광고 코드가 이미 푸터 위에 있는지 확인
                    if '<amp-ad width="100vw" height="320"' in content and content.find('<amp-ad width="100vw" height="320"') < content.find('<footer>'):
                        print(f"  ✅ {test_file.name}: Already updated")
                        continue
                    
                    # 기존 패턴 찾아서 교체
                    # 패턴 1: AdSense 광고 유닛 뒤에 바로 푸터가 오는 경우
                    pattern1 = re.compile(
                        r'(\s*</ins>\s*<script>.*?</script>\s*)</body>',
                        re.DOTALL
                    )
                    
                    if pattern1.search(content):
                        # AdSense 광고 유닛 뒤에 AMP 광고 추가
                        content = re.sub(
                            r'(\s*</ins>\s*\n)',
                            r'\1\n  <amp-ad width="100vw" height="320"\n       type="adsense"\n       data-ad-client="ca-pub-5508768187151867"\n       data-ad-slot="7298546648"\n       data-auto-format="rspv"\n       data-full-width="">\n    <div overflow=""></div>\n  </amp-ad>\n\n',
                            content
                        )
                        
                        with open(test_file, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        print(f"  ✅ {test_file.name}: Updated")
                    else:
                        print(f"  ❌ {test_file.name}: Pattern not found")
                        
                except Exception as e:
                    print(f"  ❌ {test_file.name}: Error - {e}")
            else:
                print(f"  ❌ {test_file.name}: File not found")

if __name__ == "__main__":
    print("🚀 Updating AMP ads in romance-test files...")
    update_amp_ads_in_test_files()
    print("\n✨ Done!")
