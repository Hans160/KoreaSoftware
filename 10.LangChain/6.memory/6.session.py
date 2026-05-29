from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder 
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# 💡 LangGraph의 상태(State)와 체크포인터(Memory)를 가져옵니다.
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')

prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 친절한 한국어 어시스턴트 입니다."),
    MessagesPlaceholder("history"),  # 💡 LangGraph의 MessagesState를 쓸 때는 변수명을 'history' 또는 'messages'로 매핑 가능합니다.
    ("user", "{input}")
])

# 1. 핵심이 되는 기본 체인을 구성합니다. (출력 파서 유지 가능)
chain = prompt | llm | StrOutputParser()

# 2. LangGraph가 대화를 처리할 노드(함수)를 정의합니다.
def call_model(state: MessagesState):
    # 최근 유저 입력값과 이전 대화 기록(history)을 가져옵니다.
    user_input = state["messages"][-1].content
    chat_history = state["messages"][:-1]
    
    # 체인을 실행하여 답변을 얻습니다.
    response = chain.invoke({"history": chat_history, "input": user_input})
    
    # 💡 새로운 AI 메시지를 반환하면 LangGraph가 기존 내역에 자동으로 누적(Append)합니다.
    return {"messages": [("ai", response)]}

# 3. 그래프 구조를 빌드합니다.
workflow = StateGraph(MessagesState)
workflow.add_node("model", call_model)
workflow.add_edge(START, "model")

# 4. 💡 대화 기록을 저장할 체크포인터(메모리)를 지정하여 컴파일합니다.
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)


def chat(message, session_id):
    print(f"\n[{session_id}] 질문: {message}")
    
    # 💡 LangGraph 앱을 호출합니다. thread_id가 기존의 session_id 역할을 합니다.
    config = {"configurable": {"thread_id": session_id}}
    
    # 메시지를 보내고 상태 업데이트를 받아옵니다.
    events = app.stream({"messages": [("user", message)]}, config, stream_mode="values")
    
    # 스트림의 가장 마지막 이벤트를 통해 최종 답변을 출력합니다.
    final_event = list(events)[-1]
    answer = final_event["messages"][-1].content
    print(f"[{session_id}] 답변: {answer}")


user_a = "user-A"
user_b = "user-B"

chat("제 이름은 홍길동 입니다.", user_a)
chat("제 이름은 김철수 입니다.", user_b)

chat("저는 등산을 좋아합니다.", user_a)
chat("제 취미는 낚시입니다.", user_b)

chat("제 이름과 취미가 뭐라고 했죠?", user_a)
chat("제 이름과 취미가 뭐라고 했죠?", user_b)
