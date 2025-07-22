#!/usr/bin/env python3
import os
import re

def remove_footer_whitespace():
    """Definitively remove all whitespace before footer tags"""
    base_dir = "romance-test"
    languages = ["ko", "ja", "en"]

    for lang in languages:
        lang_dir = os.path.join(base_dir, lang)
        if not os.path.exists(lang_dir):
            continue

        for filename in os.listdir(lang_dir):
            if filename.endswith('.html'):
                file_path = os.path.join(lang_dir, filename)

                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Direct pattern: remove all whitespace (including newlines and spaces) before <footer>
                # This will match any combination of whitespace characters before <footer>
                content = re.sub(r'\s*\n\s*\n\s*<footer>', '\n\n<footer>', content)
                content = re.sub(r'\s*\n\s*<footer>', '\n\n<footer>', content)

                # Extra cleanup: ensure only one blank line before footer
                content = re.sub(r'</div>\s*\n+\s*<footer>', '</div>\n\n<footer>', content)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                print(f"✅ Processed {lang}/{filename}")

if __name__ == "__main__":
    remove_footer_whitespace()
    print("🎉 All footer whitespace removed!")