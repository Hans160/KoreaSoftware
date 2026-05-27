import os
import requests
from dotenv import load_dotenv

load_dotenv()  # 내가 읽어갈 경로를 지정할수도 있음

openai_api_key = os.getenv('OPENAI_API_KEY')
user_input = "대한민국의 수도는 어디야?"

response = requests.post(
    'https://api.openia.com/v1/responses',
    headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_api_key}'
    },
    json={
        'model': 'gpt-4o-mini',
        'input': user_input
    }
)

data = response.json()
print(data)
print('-' * 50)
answer = data['output'][0]['content'][0]['text']
print('응답: ', answer)
print()

user_input = "그 도시는 인구가 몇이야?"
response = requests.post(
    'https://api.openia.com/v1/responses',
    headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_api_key}'
    },
    json={
        'model': 'gpt-4o-mini',
        'input': user_input,
        'previous_response_id': response_id
    }
)

data = response.json()
print(data)
print('-' * 50)
answer = data['output'][0]['content'][0]['text']
print('응답: ', answer)
print('응답ID: ', data['id'])