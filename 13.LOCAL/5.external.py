# 외부에 ollama 서버가 있는 경우... 나의 req를 api 에 요청하듯이 하면 됨...

import requests


OLLAMA_HOST = "http://123.123.123.123:11434"
OLLAMA_ENDPONT = f"{OLLAMA_HOST}/api/generate"      

payload = {
    "model": "exaone3.5:2.4b",  # 필요한 모델 선택
    "prompt": "Hello, how are you?"
}                                        

response = requests.post(OLLAMA_ENDPONT, json=payload)
data = response.json()

print("모델응답", data)

