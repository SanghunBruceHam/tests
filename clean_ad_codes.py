import re
from pathlib import Path

def remove_old_adsense_from_file(html_file_path):
    """HTML 파일에서 기존 autorelaxed 애드센스 코드를 제거"""
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        original_content = content

        # 기존 autorelaxed 애드센스 코드 패턴들
        old_patterns = [
            # 기본 autorelaxed 패턴
            r'<!-- AdSense Ad Unit -->\s*<script async src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js\?client=ca-pub-5508768187151867"\s*crossorigin="anonymous"></script>\s*<ins class="adsbygoogle"\s*style="display:block"\s*data-ad-format="autorelaxed"\s*data-ad-client="ca-pub-5508768187151867"\s*data-ad-slot="9345718962"></ins>\s*<script>\s*\(adsbygoogle = window\.adsbygoogle \|\| \[\]\)\.push\(\{\}\);\s*</script>',

            # 줄바꿈이 있는 패턴
            r'<!-- AdSense Ad Unit -->\s*<script async src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js\?client=ca-pub-5508768187151867"\s*crossorigin="anonymous"></script>\s*<ins class="adsbygoogle"\s*style="display:block"\s*data-ad-format="autorelaxed"\s*data-ad-client="ca-pub-5508768187151867"\s*data-ad-slot="9345718962"></ins>\s*<script>\s*\(adsbygoogle = window\.adsbygoogle \|\| \[\]\)\.push\(\{\}\);\s*</script>',

            # 개별 태그들 (fallback)
            r'<ins class="adsbygoogle"\s*style="display:block"\s*data-ad-format="autorelaxed"\s*data-ad-client="ca-pub-5508768187151867"\s*data-ad-slot="9345718962"></ins>',

            # script 태그만
            r'<script>\s*\(adsbygoogle = window\.adsbygoogle \|\| \[\]\)\.push\(\{\}\);\s*</script>'
        ]

        # 각 패턴에 대해 제거 시도
        for pattern in old_patterns:
            content = re.sub(pattern, '', content, flags=re.DOTALL)

        # 연속된 빈 줄 정리
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)

        # 변경사항이 있었다면 파일 저장
        if content != original_content:
            with open(html_file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True

        return False

    except Exception as e:
        print(f"Error processing {html_file_path}: {e}")
        return False

def main():
    """romance-test의 모든 HTML 파일에서 기존 autorelaxed 애드센스 코드 제거"""
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
                if remove_old_adsense_from_file(html_file):
                    print(f"✅ Removed old ads from: {html_file}")
                    updated_count += 1
                else:
                    print(f"📝 No old ads found in: {html_file}")

            print(f"📋 Updated {updated_count} files in {lang}")
            total_updated += updated_count

    print(f"\n🎉 Total files updated: {total_updated}")

if __name__ == "__main__":
    main()