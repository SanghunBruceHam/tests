#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ensure every test page links back to the main tests page.
- Detect language (ko/ja/en) from path
- Check if a link to the language home already exists
- If <footer> exists, append a small home link block into it
- Else, inject a minimal footer with the home link before </body>

Idempotent and safe: skips files that already contain a home link.
"""

from __future__ import annotations
import os
import re
from typing import Optional, Tuple

# Root-relative home paths per language
LANG_HOME = {
    'ko': '/',
    'ja': '/ja/',
    'en': '/en/',
}

# Link text per language
HOME_TEXT = {
    'ko': '🏠 메인 테스트 페이지로 이동',
    'ja': '🏠 テスト一覧へ戻る',
    'en': '🏠 Back to Main Tests',
}

EXCLUDE_DIRS = {
    '.git', '__pycache__', 'assets', 'monitoring', 'docs', 'node_modules',
}

HTML_RE = re.compile(r"\.html?$", re.IGNORECASE)
FOOTER_CLOSE_RE = re.compile(r"</footer>", re.IGNORECASE)
BODY_CLOSE_RE = re.compile(r"</body>", re.IGNORECASE)

# Consider a few common existing home paths as equivalent
EQUIV_HOME_TARGETS = {
    'ko': {"/", "/index.html", "/ko/", "/ko/index.html"},
    'ja': {"/ja/", "/ja/index.html"},
    'en': {"/en/", "/en/index.html"},
}

LINK_RE_TMPL = r"<a[^>]+href=\"{href}\"[^>]*>"


def detect_lang(path: str) -> str:
    p = path.replace('\\', '/')
    if "/ja/" in p or p.startswith('ja/') or p.endswith('/ja'):
        return 'ja'
    if "/en/" in p or p.startswith('en/') or p.endswith('/en'):
        return 'en'
    return 'ko'


def has_home_link(content: str, lang: str) -> bool:
    # direct match for any equivalent href
    for href in EQUIV_HOME_TARGETS[lang]:
        if re.search(LINK_RE_TMPL.format(href=re.escape(href)), content):
            return True
    # also check presence of known id/class markers if previously injected
    if re.search(r'id=\"home-link\"|class=\"home-link\"', content):
        return True
    return False


def build_link_block(lang: str) -> str:
    href = LANG_HOME[lang]
    text = HOME_TEXT[lang]
    return (
        f'  <div class="footer-nav" style="margin-top:12px;">\n'
        f'    <a id="home-link" href="{href}" '
        f'style="text-decoration:none;color:#2563eb;font-weight:700;">{text}</a>\n'
        f'  </div>'
    )


def build_footer(lang: str) -> str:
    href = LANG_HOME[lang]
    text = HOME_TEXT[lang]
    return (
        "<footer style=\"text-align:center; margin-top:24px; color:#64748b; font-weight:600;\">\n"
        f"  <a id=\"home-link\" href=\"{href}\" style=\"text-decoration:none; color:#2563eb; font-weight:700;\">{text}</a>\n"
        "</footer>\n"
    )


def process_html(content: str, lang: str) -> Tuple[str, bool]:
    if has_home_link(content, lang):
        return content, False

    # prefer inserting inside existing footer
    if FOOTER_CLOSE_RE.search(content):
        link_block = build_link_block(lang)
        new_content = FOOTER_CLOSE_RE.sub(link_block + "\n</footer>", content, count=1)
        return new_content, True

    # else inject a small footer before </body>
    if BODY_CLOSE_RE.search(content):
        footer = build_footer(lang)
        new_content = BODY_CLOSE_RE.sub(footer + "</body>", content, count=1)
        return new_content, True

    # as a last resort, append at end
    return content + "\n" + build_footer(lang), True


def should_skip_file(path: str) -> bool:
    base = os.path.basename(path)
    # skip verification or token files
    if base.startswith('google') and base.endswith('.html'):
        return True
    if base.startswith('yandex_') and base.endswith('.html'):
        return True
    # skip hidden
    if base.startswith('.'):
        return True
    return False


def main() -> None:
    changed = 0
    scanned = 0
    for root, dirs, files in os.walk('.'):
        # prune excluded dirs
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
        for f in files:
            if not HTML_RE.search(f):
                continue
            full = os.path.join(root, f)
            if should_skip_file(full):
                continue
            try:
                with open(full, 'r', encoding='utf-8') as fh:
                    content = fh.read()
            except Exception:
                continue
            scanned += 1
            lang = detect_lang(full)
            new_content, did = process_html(content, lang)
            if did:
                try:
                    with open(full, 'w', encoding='utf-8') as fh:
                        fh.write(new_content)
                    changed += 1
                except Exception:
                    pass
    print(f"✅ Scanned {scanned} HTML files, updated {changed} with home links.")

if __name__ == '__main__':
    main()
