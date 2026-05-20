import requests
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")

text = "파이썬 웹개발"
url = "https://openapi.naver.com/v1/search/news.json"

headers = {
    "X-Naver-Client-Id": client_id,
    "X-Naver-Client-Secret": client_secret
}

params = {
    "query": text
}

resp = requests.get(url, headers=headers, params=params)
# print(resp)
data = resp.json()
print(data)