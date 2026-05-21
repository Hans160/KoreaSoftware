import requests
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

message = []
message.append({"role": "system", "content": "너는 나를 잘 도와주는 모든 분야 전문가야"})

def ask_chatbot(user_input):
    global message
    message.append({"role": "user", "content": user_input})
    try:
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            json = {
                "model": "gpt-3.5-turbo",
                "messages": message,
                'temperature': 1.0,
                'max_tokens': 10000,
            },
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {openai_api_key}' # Basic 인증 = Basic Authentication
            }
        )

        data = response.json()
        final_response = data['choices'][0]['message']['content']
        message.append({"role": "assistant", "content": final_response})

        # 예시 : 히스토리 10개 (5개의 오고간 대화) 로 제한
        message = [message[0]] + message[-10:]
    except Exception as e:
        print('오류: ', e)
    return final_response

while True:
    user_input = input("\n당신의 질문: ").strip()
    if user_input.lower() in ['quit', 'exit', '종료', '끝']: 
        print("대화를 종료합니다. 안녕히 가세요.")
        break
    else:
        print("대화를 생성중입니다. 잠시만 기다려 주세요...")
        print("챗봇응답: ", ask_chatbot(user_input))
        print("-"*50)