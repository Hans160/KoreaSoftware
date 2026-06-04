# whisper(속삭임) 말을 기반으로 text로 변환 : STT(Speech to Text)

import os
import base64

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def transcribe_audio(file): # 오디오를 설명하시오.
    with open(file, "rb") as af:
       transcript = client.audio.transcriptions.create(
           file=af,
           model="whisper-1",
           response_format="text",
           language="ko"
       )

    return transcript

result = transcribe_audio("audio.mp3")
print(result)