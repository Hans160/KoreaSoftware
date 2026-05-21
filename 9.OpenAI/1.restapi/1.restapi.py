import requests
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
user_input = "우리집에 새로운 강아지를 분양했어.. 강아지 이름을 뭐라고 지을까? 성병은 남 셩격은 사람말 잘듣고 특징이 사람을 좋아해"

response = requests.post(
    'https://api.openai.com/v1/chat/completions',
    json = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "너는 나를 잘 도와주는 경력 20년차 작명가야"},
            {"role": "user", "content": user_input}
        ],
        'temperature': 1.3
    },
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_api_key}' # Basic 인증 = Basic Authentication
    }
)

data = response.json()
final_response = data['choices'][0]['message']['content']
print(final_response)