#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from utils import FileManager, logger

MOBILE_META = '<meta name="mobile-web-app-capable" content="yes">'

def ensure_mobile_meta(content: str) -> tuple[str, bool]:
    # Already present?
    if re.search(r'<meta[^>]+name=["\']mobile-web-app-capable["\']', content, re.IGNORECASE):
        return content, False

    # Prefer to insert after any apple-mobile-web-app-capable if found
    pattern_apple = re.compile(r'(<meta[^>]+name=["\']apple-mobile-web-app-capable["\'][^>]*>)', re.IGNORECASE)
    if pattern_apple.search(content):
        new_content = pattern_apple.sub(r"\1\n  " + MOBILE_META, content, count=1)
        return new_content, True

    # Else, insert before </head>
    pattern_head = re.compile(r'</head>', re.IGNORECASE)
    if pattern_head.search(content):
        new_content = pattern_head.sub('  ' + MOBILE_META + '\n\n</head>', content, count=1)
        return new_content, True

    # Fallback append
    return content + "\n  " + MOBILE_META + "\n", True

def main():
    updated = 0
    scanned = 0
    for root, _, files in os.walk(os.getcwd()):
        for f in files:
            if not f.endswith('.html'):
                continue
            path = os.path.join(root, f)
            scanned += 1
            content = FileManager.read_file_safely(path)
            if content is None:
                continue
            new_content, changed = ensure_mobile_meta(content)
            if changed:
                if FileManager.write_file_safely(path, new_content):
                    updated += 1
    logger.info(f"mobile-web-app-capable ensured. Scanned: {scanned}, Updated: {updated}")
    print(f"✅ mobile-web-app-capable ensured. Scanned: {scanned}, Updated: {updated}")

if __name__ == '__main__':
    main()

