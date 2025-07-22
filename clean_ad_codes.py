
import re
from pathlib import Path

def add_adsense_before_footer(html_file_path):
    """풋터 위에 애드센스 코드를 추가하는 함수"""
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        original_content = content
        
        # 이미 애드센스 코드가 풋터 위에 있는지 확인
        adsense_pattern = r'<!-- AdSense Ad Unit -->.*?data-ad-slot="7298546648".*?</script>'
        if re.search(adsense_pattern, content, re.DOTALL):
            return False  # 이미 있으면 수정하지 않음
        
        # 풋터 위에 애드센스 코드 추가
        footer_pattern = r'(\s*<footer>)'
        adsense_code = '''
  <!-- AdSense Ad Unit -->
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

\\1'''
        
        content = re.sub(footer_pattern, adsense_code, content)
        
        # 내용이 변경되었으면 파일에 저장
        if content != original_content:
            with open(html_file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {html_file_path}: {e}")
        return False

def clean_ad_codes_in_file(html_file_path):
    """Clean and replace ad codes in a single HTML file"""
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        original_content = content
        
        # Remove existing AdSense scripts in head section
        adsense_patterns = [
            r'<!-- Google AdSense -->.*?</script>',
            r'<script async src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js[^>]*>.*?</script>',
            r'<script>\s*\(adsbygoogle = window\.adsbygoogle \|\| \[\]\)\.push\({[^}]*}\);\s*</script>',
        ]
        
        for pattern in adsense_patterns:
            content = re.sub(pattern, '', content, flags=re.DOTALL | re.MULTILINE)
        
        # Add AMP Ad Script in head section if not already present
        if 'amp-ad-0.1.js' not in content:
            head_end = content.find('</head>')
            if head_end != -1:
                amp_script = '  <!-- AMP Ad Script -->\n  <script async custom-element="amp-ad" src="https://cdn.ampproject.org/v0/amp-ad-0.1.js"></script>\n\n'
                content = content[:head_end] + amp_script + content[head_end:]
        
        # Add AMP ad at the beginning of body if not already present
        if 'data-ad-client="ca-pub-5508768187151867"' not in content:
            body_start = content.find('<body>')
            if body_start != -1:
                body_end = content.find('>', body_start) + 1
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
                content = content[:body_end] + amp_ad + content[body_end:]
        
        # Clean up extra whitespace
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        # Write back to file only if content changed
        if content != original_content:
            with open(html_file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {html_file_path}: {e}")
        return False

def main():
    """romance-test의 모든 HTML 파일에 풋터 위 애드센스 코드 추가"""
    romance_test_path = Path('romance-test')
    
    if not romance_test_path.exists():
        print("romance-test folder not found!")
        return
    
    total_updated = 0
    
    # Process all language folders
    for lang in ['ko', 'ja', 'en']:
        lang_path = romance_test_path / lang
        if lang_path.exists():
            print(f"\n🔄 Processing {lang} files...")
            
            # Get all HTML files in the language directory
            html_files = list(lang_path.glob('*.html'))
            updated_count = 0
            
            for html_file in html_files:
                if add_adsense_before_footer(html_file):
                    print(f"✅ Updated: {html_file}")
                    updated_count += 1
                else:
                    print(f"📝 Already up-to-date: {html_file}")
            
            print(f"📋 Updated {updated_count}/{len(html_files)} files in {lang} folder")
            total_updated += updated_count
    
    print(f"\n🎉 Total files updated: {total_updated}")

if __name__ == "__main__":
    main()
