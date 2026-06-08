from dotenv import load_dotenv

# pip install langchain-openai
# from langchain_openai import ChatOpenAI

# pip install langchain-anthropic
from langchain_anthropic import ChatAnthropic

load_dotenv()

llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=1.0)

response = llm.invoke("인공지능에 대해서 설명해 주시오")
print(response.content)