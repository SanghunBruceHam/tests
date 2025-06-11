import base64
import json
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# GitHub Secret에서 base64로 받은 JSON 인증서 디코딩
creds_json = base64.b64decode(os.environ["GSC_CREDENTIALS_BASE64"]).decode("utf-8")
creds_dict = json.loads(creds_json)

SCOPES = ['https://www.googleapis.com/auth/webmasters']
credentials = service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
service = build('webmasters', 'v3', credentials=credentials)

# 제출할 사이트와 sitemap 경로
SITE_URL = "https://tests.mahalohana-bruce.com/"
SITEMAP_URL = "https://tests.mahalohana-bruce.com/sitemap.xml"

# 제출 실행
service.sitemaps().submit(siteUrl=SITE_URL, feedpath=SITEMAP_URL).execute()
print(f"✅ sitemap 제출 완료: {SITEMAP_URL}")
