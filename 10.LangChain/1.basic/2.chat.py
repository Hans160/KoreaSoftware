import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')


llm = OpenAI(model='gpt-3.5-turbo-instruct')
prompt = '다음 문장을 한국말로 번역해줘: Good Morning, how are you?'
print(llm.invoke(prompt))
print('-'*50)

llm2 = ChatOpenAI(model='gpt-4o')
prompt = '다음 문장을 한국말로 번역해줘: Good Morning, how are you?'
print(llm2.invoke(prompt))
print('-'*50)






llm2 = ChatOpenAI(model='gpt-4o-mini')
prom