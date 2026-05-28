# pip install langchain langchain-openai
import os
from dotenv import load_dotenv

# from langchain.llms import OpenAI # 구 버전
from langchain_openai import OpenAI # 최신 버전

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

llm = OpenAI(model="gpt-4o-mini", temperature=1.0)

prompt = "오늘 저녁은 무엇을 먹을까요?"
result = llm.invoke(prompt)
print(result)