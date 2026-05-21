#pip uninstall openai;    # 현재 최신은 4.x
import openai

from dotenv import load_dotenv
import os
import base64
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=openai_api_key)

# 이런 변환함수를 일일이 다 암기할 필요는 XX. 인코딩 알아야함. 애 해야하는지도 ..
def encode_image_to_base64(image_path):
    #이미지를 읽어서 base64로 변환
    with open(image_path, "rb") as file:
        base64_bytes = base64.b64encode(file.read()).decode("utf-8")
    return f"data:image/png;base64,{base64_bytes}" #base64_bytes

def ask_chatbot(image_path, user_input):
    image_base64 = encode_image_to_base64(image_path)   

    final_message = [
        {"role": "system", "content": "당신은 스포츠 트레이너 입니다."},
        {"role": "user", "content": [
            {
                "type": "text",
                "text": user_input
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": image_base64  # OpenAI API 규격에 맞게 딕셔너리 구조 수정
                }
            }
        ]}
    ]
    
    # 들여쓰기 오류 수정 및 미완성된 messages 매개변수 완성
    response = client.chat.completions.create(
        model="gpt-4o",   # gpt-4 시리즈부터 이미지를 지원함 (멀티모달)
        messages=final_message
    )
    
    final_response = response.choices[0].message.content
    return final_response

image_path = "squats-good.png"
question = "나의 운동자세가 어떤지 전문가의 입장으로 10점 만점에 몇점인지 알려주세요 "
print(ask_chatbot(image_path, question))

print("-"*50)

image_path = "squats-bad.png"
question = "나의 운동자세가 어떤지 전문가의 입장으로 10점 만점에 몇점인지 알려주세요 "
print(ask_chatbot(image_path, question))
