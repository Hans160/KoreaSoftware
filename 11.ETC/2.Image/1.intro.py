# 텍스트를 기반으로 이미지를 생성 ... (GAN)

# 구버전 모델이 dall-e => dall-e-2 = > ??
# gpt-image-1.5 또는 gpt-image-2

import os
import base64

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

Prompt = "노을 지는 해변, 잔잔한 파도, 수채화 스타일 . 해변위를 걷는 3명의 가족 . 14개월의 아자아장 걷는 여자아기와 아내와 남편"

result = client.images.generate(
    model="gpt-image-1.5",
    prompt=Prompt,
    size="1024x1024",     # 256x256, 512x512, 1024x1024(정사각형), 1024x1536(직사각형)
    quality="high"      # low, medium, high , auto
)

b64 = result.data[0].b64_json
with open("output.png", "wb") as f:
    f.write(base64.b64decode(b64))

print('저장 완료')