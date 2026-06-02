# 금융 도우미 에이전트 챗봇 만들기
from langchain.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# 랭체인들을 불러온다.

from fin_tools import TOOLS

SYSTEM="""
당신은 금융 정보 비서입니다. OOO OOO OOO을 하는...
"""

def ask(q):
    r = llm_with_tools.invoke([SystemMessage(content=SYSTEM), HumanMessage(content=q)])
    if not r.tool_calls:
        print(f" (도구 없는 결과): {r.content}")
    else:
        for call in r.tool_calls:
            print(f" -> {call['name']}({call['args']})")

            # 실제 실행을 원하면??
            name2tool = {t.name: t for t in TOOLS}
            result = name2tool[call["name"]].invoke(call["args"])
            print(f" -> 결과: {result}")

if __name__ == "__main__":
    print('=== 데모 명령어 실행 ===')
    for q in ["삼성전자 주가 알려줘", "달러 환율 얼마야?", "엔비디아 관련 최근 뉴스는 뭐가 있어?"]:
        ask(q)

    print('=== 수동 질의 응답 시작 ===')
    llm_with_tools = ChatOpenAI(model="gpt-4o-mini").bind_tools(TOOLS)
    while True:
        q = input(">>> ")
        ask(q)