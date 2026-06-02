import wikipedia
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent     # 이 함수가 3번이상 바뀌없음..
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun

# 위키피디아 API 래퍼 설정
api_wrapper = WikipediaAPIWrapper()

# 에이전트가 사용할 도구 객체 직접 생성
wikipedia_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

# 에이전트 생성 함수에 전달할 도구 리스트 구성
tools = [wikipedia_tool]

load_dotenv()


llm = ChatOpenAI(model="gpt-4o-mini")
agent = create_agent(llm, tools)

result = agent.invoke({"messages": [("user", "파이썬 프로그래밍 언어는 누가 만들었어?")]})
  