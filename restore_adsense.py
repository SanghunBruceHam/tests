#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Restore Google AdSense loader across HTML pages by ensuring the correct
adsbygoogle.js client is present in <head>. Updates wrong/masked IDs
and inserts the script before </head> when missing.
"""

import os
import re
from utils import FileManager, logger
from config import Config


ADSENSE_SRC_PATTERN = re.compile(
    r"https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js\?client=([^\"'\s>]+)",
    re.IGNORECASE,
)


EXCLUDE_NAMES = {
    'googlee53980ef2acb81e6.html',
    'yandex_1010c8523eee2722.html',
}

EXCLUDE_PARTS = {
    '/monitoring/', '/assets/', '/.git/', '/node_modules/', '/compat-pick/'
}


def should_skip(path: str) -> bool:
    base = os.path.basename(path)
    if base in EXCLUDE_NAMES:
        return True
    for p in EXCLUDE_PARTS:
        if p in path.replace('\\', '/'):
            return True
    return False


def ensure_adsense(content: str, client_id: str) -> tuple[str, bool]:
    """Return (new_content, changed) ensuring correct AdSense loader exists."""
    changed = False

    # Update existing wrong client IDs
    def _repl(m: re.Match) -> str:
        nonlocal changed
        current = m.group(1)
        if current != client_id:
            changed = True
        return f"https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={client_id}"

    new_content, count = ADSENSE_SRC_PATTERN.subn(_repl, content)
    if count > 0:
        # Ensure crossorigin attribute exists on same tag if not already present
        new_content = re.sub(
            r'(\<script[^>]*src=\"https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js\?client=' + re.escape(client_id) + r'\"(?![^>]*crossorigin)[^>]*)(>)',
            r"\1 crossorigin=\"anonymous\"\2",
            new_content,
            flags=re.IGNORECASE,
        )
        # If loader only appears inside HTML comments, still insert a live one
        content_no_comments = re.sub(r'<!--.*?-->', '', new_content, flags=re.DOTALL)
        if ADSENSE_SRC_PATTERN.search(content_no_comments):
            return new_content, changed
        else:
            # Insert a live loader before </head>
            script_tag = (
                f'  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={client_id}" '
                f'crossorigin="anonymous"></script>'
            )
            closing_head_pattern = re.compile(r'</head>', re.IGNORECASE)
            inserted, n = closing_head_pattern.subn(script_tag + "\n\n</head>", new_content, count=1)
            if n:
                return inserted, True
            return new_content, changed

    # If not present at all, insert before </head>
    script_tag = (
        f'  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={client_id}" '
        f'crossorigin="anonymous"></script>'
    )
    if '</head>' in content.lower():
        # Case-insensitive replacement; capture original closing tag
        closing_head_pattern = re.compile(r'</head>', re.IGNORECASE)
        new_content, n = closing_head_pattern.subn(script_tag + "\n\n</head>", content, count=1)
        if n:
            return new_content, True

    # As a fallback, append at the end if no </head> found
    return content + "\n" + script_tag + "\n", True


def main() -> None:
    client_id = Config.ADSENSE_CLIENT_ID
    if not client_id:
        logger.error("ADSENSE_CLIENT_ID is empty. Set environment var or config.")
        return

    updated = 0
    scanned = 0

    for root, _, files in os.walk(os.getcwd()):
        for fname in files:
            if not fname.endswith('.html'):
                continue
            full = os.path.join(root, fname)
            if should_skip(full):
                continue
            scanned += 1
            content = FileManager.read_file_safely(full)
            if not content:
                continue
            new_content, changed = ensure_adsense(content, client_id)
            if changed and new_content != content:
                if FileManager.write_file_safely(full, new_content):
                    updated += 1

    logger.info(f"AdSense restore scan completed. Scanned: {scanned}, Updated: {updated}")
    print(f"✅ AdSense restore done. Scanned: {scanned}, Updated: {updated}")


if __name__ == "__main__":
    main()
