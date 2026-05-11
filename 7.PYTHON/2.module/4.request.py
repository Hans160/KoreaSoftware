# 외부 모듈은 pip install requests로 설치한다
# 그러면, pypi.org로 부터 다운로드 받아서 나의 "가상환경"에 설치가 됨
import requests

# # 외부에 HTTP 요청을 대신 해주는 라이브러리
# resp = requests.get("https://www.example.com")
# print(resp.text)

resp = requests.get('https://api.github.com')
print(resp.text)