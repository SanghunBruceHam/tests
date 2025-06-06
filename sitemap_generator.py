import os
from datetime import datetime

BASE_URL = "https://tests.mahalohana-bruce.com"

def get_html_files(root_dir="."):
    html_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith(".html"):
                rel_dir = os.path.relpath(dirpath, root_dir)
                rel_file = os.path.join(rel_dir, f) if rel_dir != "." else f
                html_files.append(rel_file.replace("\\", "/"))
    return html_files

def make_url(path):
    # 깃허브 Pages의 index.html은 URL에서 생략
    if path.endswith("/index.html"):
        url = f"{BASE_URL}/{path[:-10]}"
    else:
        url = f"{BASE_URL}/{path}"
    # 맨 뒤에 // 생기는 것 방지
    return url.replace("//", "/").replace(":/", "://")

def main():
    files = get_html_files(".")
    now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for file in files:
        url = make_url(file)
        sitemap.append(f"  <url><loc>{url}</loc><lastmod>{now}</lastmod></url>")
    sitemap.append("</urlset>")
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(sitemap))
    print(f"총 {len(files)}개의 페이지가 sitemap.xml에 추가되었습니다.")

if __name__ == "__main__":
    main()
