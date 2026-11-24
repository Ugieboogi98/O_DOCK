
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app_id = os.getenv("META_APP_ID")
app_secret = os.getenv("META_APP_SECRET")
access_token = os.getenv("META_ACCESS_TOKEN")

if not all([app_id, app_secret, access_token]):
    raise ValueError("Meta API 환경변수가 누락되었습니다.")

url = "https://graph.facebook.com/v27.0/oauth/access_token"

params = {
    "grant_type": "fb_exchange_token",
    "client_id": app_id,
    "client_secret": app_secret,
    "fb_exchange_token": access_token,
}

response = requests.get(url, params=params, timeout=30)
response.raise_for_status()

data = response.json()

# 토큰은 화면이나 로그에 출력하지 않음
new_token = data["access_token"]

print("장기 액세스 토큰 발급 성공")
print("유효기간(초):", data.get("expires_in"))

# .env에 수동으로 복사할 수 있도록 별도 파일로 저장

from pathlib import Path

token_file = Path("meta_long_lived_token.txt")
token_file.write_text(new_token, encoding="utf-8")

print("저장 경로:", token_file.resolve())
print("파일 존재:", token_file.exists())
print("파일 크기:", token_file.stat().st_size if token_file.exists() else 0)
