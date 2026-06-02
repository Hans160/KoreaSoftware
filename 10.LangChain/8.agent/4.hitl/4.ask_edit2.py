from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
load_dotenv()

checkpoint = MemorySaver()

@tool
def send_payment(recipient: str, amount: int) -> str:
    """수신자에게 지정 금액을 송금한다."""
    return f"{recipient}에 {amount}원을 송금완료."

@tool
def get_balance(account: str) -> int:
    """ 계좌 잔액 조회"""
llm = ChatOpenAI(model="gpt-4o-mini")
agent = create_agent(llm, [send_payment], checkpointer=checkpoint, interrupt_before=["tools"])

config = {"configurable": {"thread_id":"t001"}}

question = "Alice의 잔액이 얼마야?" , "홍길동에게 10000원 송금해줘"

print(f"[유저] {question}")
result = agent.invoke({"messages": [("user", question)]}, config=config)
print(result['messages'][-1].content)

call = result["messages"][-1].tool_calls[0]   # 정지 시점 (도구를 부르기 직전)
print(f"[일시정지] {call['name']}({call['args']})")

human_result = input("\n이대로 실행할까요? (y/n)").strip().lower()
if human_result == "y":
    result = agent.invoke(None, config=config) # 할일을 계속 이어서 하시오.
else:
    print(f"\n[중단] 사용자 요청에 의해 중단되었습니다.") 