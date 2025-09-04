#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Normalize and simplify footer across HTML pages.
- Replace existing <footer> blocks with a clean, minimal design
- Language-aware home link and compact language switcher
- Insert before </body> if footer is missing

Idempotent: running multiple times keeps the same result.
"""

from __future__ import annotations
import os
import re
from typing import Tuple
from datetime import datetime

EXCLUDE_DIRS = {
    '.git', '__pycache__', 'assets', 'monitoring', 'docs', 'node_modules'
}

HTML_RE = re.compile(r"\.html?$", re.IGNORECASE)
FOOTER_BLOCK_RE = re.compile(r"<footer[\s\S]*?</footer>", re.IGNORECASE)
BODY_CLOSE_RE = re.compile(r"</body>", re.IGNORECASE)

LANG_HOME = {
    'ko': '/',
    'ja': '/ja/',
    'en': '/en/',
}

HOME_LABEL = {
    'ko': '🏠 테스트 목록 보기',
    'ja': '🏠 テスト一覧',
    'en': '🏠 Browse All Tests',
}

SITE_NAME = {
    'ko': '심리테스트 모음',
    'ja': '心理テスト集',
    'en': 'Psychological Tests Collection',
}

BRAND_NAME = 'Tests Mahalohana Bruce'
SITE_URL = 'https://tests.mahalohana-bruce.com'


def detect_lang(path: str) -> str:
    p = path.replace('\\', '/')
    if '/ja/' in p or p.startswith('ja/') or p.endswith('/ja'):
        return 'ja'
    if '/en/' in p or p.startswith('en/') or p.endswith('/en'):
        return 'en'
    return 'ko'


def lang_switcher(active: str) -> str:
    def item(code: str, label: str) -> str:
        if code == active:
            return f'<span style="font-weight:700;color:#334155;">{label}</span>'
        return f'<a href="{LANG_HOME[code]}" style="color:#475569;text-decoration:none;">{label}</a>'

    return (
        '  <div class="footer-lang" style="margin-top:6px;font-size:12px;line-height:1;">\n'
        f'    {item("ko", "한국어")} · {item("ja", "日本語")} · {item("en", "English")}\n'
        '  </div>'
    )


def build_footer(lang: str) -> str:
    year = datetime.utcnow().year
    site_name = SITE_NAME.get(lang, SITE_NAME['ko'])
    return (
        '<footer class="site-footer" '
        'style="text-align:center;padding:16px 12px;color:#64748b;font-size:14px;">\n'
        f'  <a id="home-link" href="{LANG_HOME[lang]}" '
        'style="display:inline-block;text-decoration:none;color:#2563eb;font-weight:800;">'
        f'{HOME_LABEL[lang]}</a>\n'
        f'{lang_switcher(lang)}\n'
        '  <div class="footer-brand" style="margin-top:8px;font-size:12px;color:#94a3b8;">\n'
        f'    <span class="site-name">{site_name}</span> · '
        f'    <a href="{SITE_URL}" style="color:#94a3b8;text-decoration:none;">tests.mahalohana-bruce.com</a>\n'
        '  </div>\n'
        '  <div class="copyright" style="margin-top:4px;font-size:12px;color:#94a3b8;">\n'
        f'    © {year} {BRAND_NAME}. All rights reserved.\n'
        '  </div>\n'
        '</footer>'
    )


def normalize(content: str, lang: str) -> Tuple[str, bool]:
    new_footer = build_footer(lang)

    # Replace any existing footer block
    if FOOTER_BLOCK_RE.search(content):
        new_content = FOOTER_BLOCK_RE.sub(new_footer, content, count=1)
        return new_content, new_content != content

    # Else, inject before </body>
    if BODY_CLOSE_RE.search(content):
        new_content = BODY_CLOSE_RE.sub(new_footer + '\n</body>', content, count=1)
        return new_content, True

    # Fallback: append
    return content + '\n' + new_footer + '\n', True


def main() -> None:
    changed = 0
    scanned = 0
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
        for f in files:
            if not HTML_RE.search(f):
                continue
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as fh:
                    content = fh.read()
            except Exception:
                continue
            scanned += 1
            lang = detect_lang(path)
            new_content, did = normalize(content, lang)
            if did:
                try:
                    with open(path, 'w', encoding='utf-8') as fh:
                        fh.write(new_content)
                    changed += 1
                except Exception:
                    pass
    print(f"✅ Footer normalization complete. Scanned: {scanned}, Updated: {changed}")


if __name__ == '__main__':
    main()
