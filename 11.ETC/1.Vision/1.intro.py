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

question = 