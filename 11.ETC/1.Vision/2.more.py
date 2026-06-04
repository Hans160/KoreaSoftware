# 방법
# 1. 사진을 직접 올린다 (base64인코딩)
# 2. 이미지 URL을 주고 읽어가라고 한다.

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

image_URL = ""

response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {
            'role':'user', 
            'content': 
        }
    ]
)

client = 

question = [
    '이미지에 있는 한글 글자를 다 읽어줘',
    '해당 이미지 사용된 주요 색상을 알려줘',
    '이미지'
]