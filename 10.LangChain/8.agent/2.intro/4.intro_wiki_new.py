# pip install langchain-wikipedia
import wikipedia

from dotenv import load_dotenv

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

load_dotenv()

wikipedia.wikipedia.USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

wiki_ko = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(language="ko", top_k_results=3, doc_content_chars_max=200, ),
    name="wiki_ko",
    description="한국어 위키피디어. 한국에서 일어난 사건 또는 인물,개념 등"
)

wiki_en = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(language="en",name="wiki_en", top_k_results=3, doc_content_chars_max=200),
    name="wiki_en",
    description="English Wikipedia. Global events or concepts"
)


llm = ChatOpenAI(model="gpt-4o-mini")

system_prompt = """
당신은 위키피디아를 활용해 정보를 조회하고 답변하는 챗봇입니다.
도구 사용 가이드:
- 한국 또는 한국어 관련 주제는 한국어 위키피디어에서 검색
- 글로벌/영어권 주제는 영어 위키피디어에서 검색
- 검색 결과가 한번에 안나올 경우, 유사어(유의어)등으로 변경해서 재시도 할수 있음.

영어 검색한 결과인 경우, 한국어로 번역해서 답변하세요."""

agent = create_agent(
    model=llm,
    tools=[wiki_ko, wiki_en],
    system_prompt=system_prompt
)

questions = ["what is artificial intelligence?", "세종대왕은 누구인가요?"]
import time
for q in questions:
    time.sleep(2)  # API 호출 간에 잠시 대기
    try:
        result = agent.invoke({"messages": [("user", q)]})
    except Exception as e:
        print(f"Error: {type(e).__name__} - {e}")
        continue

    for m in result["messages"]:
        if hasattr(m, "tool_calls") and m.tool_calls:
            for c in m.tool_calls:
                print(f"[도구 호출] {c['name']}({c['args']})")
        if m.type == "tool":
            print(f"[도구 결과] {m.content[:100]}...")

    print(f"\n\n최종답변: {result['messages'][-1].content}")