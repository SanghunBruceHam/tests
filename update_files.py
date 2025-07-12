from datetime import datetime

# 1. robots.txt
robots_txt = """User-agent: *
Allow: /

Sitemap: https://tests.mahalohana-bruce.com/sitemap.xml

#DaumWebMasterTool:9add863220c94ce5ce0e5e7ff689b22964cfdbd2b97303e6ad356185fffba89e:NnJbOlYdct0Jzm/G1OzHmA==
#naver-site-verification:9623a2fff5ba40ea03991297345b560b39f1c4b1

"""

with open("robots.txt", "w", encoding="utf-8") as f:
    f.write(robots_txt)

# 2. ads.txt
ads_txt = """google.com, pub-5508768187151867, DIRECT, f08c47fec0942fa0
# Last updated: {}
""".format(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'))

with open("ads.txt", "w", encoding="utf-8") as f:
    f.write(ads_txt)
