name: Generate sitemap

on:
  schedule:
    - cron: '0 0 * * *'   # 매일 오전 9시 KST (UTC 0시)
    - cron: '0 12 * * *'  # 매일 오후 9시 KST (UTC 12시)
  workflow_dispatch:

permissions:
  contents: write

jobs:
  generate:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Pull latest main
        run: git pull --rebase origin main

      - name: Generate sitemap.xml
        run: python sitemap_generator.py

      - name: Commit and push sitemap
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add sitemap.xml
          git commit -m "Auto-generate sitemap.xml" || echo "No changes to commit"
          git push
