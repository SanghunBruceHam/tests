
import os
import re
from pathlib import Path

def clean_ad_codes_in_file(file_path):
    """Remove old ad codes and ensure only the specified AdSense code is in head"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove all <ins> ad blocks and their scripts
        content = re.sub(r'<ins class="adsbygoogle"[^>]*>.*?</ins>\s*<script>\s*\(adsbygoogle = window\.adsbygoogle \|\| \[\]\)\.push\(\{\}\);\s*</script>', '', content, flags=re.DOTALL)
        
        # Remove standalone <ins> tags
        content = re.sub(r'<ins class="adsbygoogle"[^>]*>.*?</ins>', '', content, flags=re.DOTALL)
        
        # Remove standalone adsbygoogle push scripts
        content = re.sub(r'<script>\s*\(adsbygoogle = window\.adsbygoogle \|\| \[\]\)\.push\(\{\}\);\s*</script>', '', content, flags=re.DOTALL)
        
        # Remove duplicate or incorrect AdSense scripts
        content = re.sub(r'<script async src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js\?client=ca-pub-5508768187151867"[^>]*>.*?</script>', '', content, flags=re.DOTALL)
        
        # Remove any existing AdSense blocks in head
        content = re.sub(r'<!-- Google AdSense -->.*?</script>', '', content, flags=re.DOTALL)
        
        # Remove duplicate scripts with "}); }" pattern
        content = re.sub(r'\s*\}\);\s*</script>\s*\}\);\s*</script>', '', content, flags=re.DOTALL)
        
        # Clean up extra closing script tags
        content = re.sub(r'\s*\}\);\s*</script>\s*\}\);\s*</script>', '', content, flags=re.DOTALL)
        
        # Find the head section and add the correct AdSense code if not present
        target_ad_code = '''  <!-- Google AdSense -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js" crossorigin="anonymous"></script>
  <script>
    (adsbygoogle = window.adsbygoogle || []).push({
      google_ad_client: "ca-pub-5508768187151867",
      enable_page_level_ads: true
    });
  </script>'''

        # Check if the correct AdSense code is already present
        if 'google_ad_client: "ca-pub-5508768187151867"' not in content or 'enable_page_level_ads: true' not in content:
            # Add the AdSense code before </head>
            if '</head>' in content:
                content = content.replace('</head>', f'\n{target_ad_code}\n\n</head>')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Clean ad codes in romance-test Korean and Japanese files"""
    romance_test_path = Path('romance-test')
    
    if not romance_test_path.exists():
        print("romance-test folder not found!")
        return
    
    # Process Korean and Japanese files
    for lang in ['ko', 'ja']:
        lang_path = romance_test_path / lang
        if lang_path.exists():
            print(f"\n🔄 Processing {lang} files...")
            
            # Get all HTML files in the language directory
            html_files = list(lang_path.glob('*.html'))
            
            for html_file in html_files:
                if clean_ad_codes_in_file(html_file):
                    print(f"✅ Updated: {html_file}")
                else:
                    print(f"❌ Failed: {html_file}")
            
            print(f"📋 Processed {len(html_files)} files in {lang} folder")

if __name__ == "__main__":
    main()
