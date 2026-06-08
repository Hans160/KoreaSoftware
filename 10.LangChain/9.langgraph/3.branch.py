from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import MemorySaver

from typing import TypedDict, List, Dict, Any

import uuid

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')
graph = StateGraph(state_schema=MessagesState)
memory = MemorySaver()


# 그래프 구조:
#
#                            ->    weather
#        Start  ->    router ->    news     --->    END
#                            ->    chat
#

def get_weather():
    return "오늘 서울의 맑고, 기온이 22도 입니다."

def get_news():
    return "최신 뉴스: 오늘 삼성전자 주가는 -9% 하락중입니다"



class State(TypedDict):
    messages: List[AIMessage]
    topic: str

def topic_router(state, config):
    """사용자 질문에 따라서 경로를 라우팅 하는 함수"""
    last_message = state["messages"][-1].content.lower()   # News, news, NEWS
    if "날씨" in last_message:
        print("라우터: '날씨' 를 감지하여 weather 라우팅으로 보내는중...")
        return "weather"
    elif "뉴스" in last_message:
        print("라우터: '뉴스' 를 감지하여 news 라우팅으로 보내는중...")
        return "news"
    else:
        print("라우터: '날씨' 를 감지하지 않아서 chat 라우팅으로 보내는중...")
        return "chat"


def router_node(state: State, config: RunnableConfig) -> Dict[str, Any]:
    #특별히 할일없음 그냥 placeholder 로만의 역할을 함.
    return dict(state)

def weather_node(state: State, config: RunnableConfig) -> Dict[str, Any]:
    weather_info = get_weather()
    response = llm.invoke([
        SystemMessage(content="당신은 날씨 전문가 입니다."),
        HumanMessage(content=f"다른 뉴스 정보를 사용자에게 친절하게 설명해 주세요: {weather_info}")
    ])
    return {"messages": state["messages"] + [response], "topic": "weather"}

def news_node(state: State, config: RunnableConfig) -> Dict[str, Any]:
    news_info = get_news()
    response = llm.invoke([
        SystemMessage(content="당신은 뉴스 전문가 입니다."),
        HumanMessage(content=f"다른 뉴스 정보를 사용자에게 친절하게 설명해 주세요: {news_info}")
    ])
    return {"messages": state["messages"] + [response], "topic": "news"}

def chat_node(state: State, config: RunnableConfig) -> Dict[str, Any]:
    messages= state["messages"]
    response = llm.invoke([
        SystemMessage(content="당신은 친절한 AI비서 입니다."),
        HumanMessage(content=f"{messages}")
    ])
    return {"messages": state["messages"] + [response], "topic": "chat"}

graph =StateGraph(State)
graph.add_node("router", router_node)
graph.add_node("weather", weather_node)
graph.add_node("news", news_node)
graph.add_node("chat", chat_node)

graph.add_edge(START, "router")
graph.add_conditional_edges(
    "router",
    topic_router,
    path_map = {
        "weather": "weather",
        "news": "news",
        "chat": "chat",
    }
)
graph.add_edge("weather", END)
graph.add_edge("news", END)
graph.add_edge("chat", END)

app = graph.compile(checkpointer=memory)   
thread_id = str(uuid.uuid4())
config = {"configurable": {"thread_id": thread_id}}

while True:
    user_input = input("질문을 입력하세요: ")
    if user_input.lower() == 'exit':
        break

    result = app.invoke({"messages": [HumanMessage(content=user_input)], "topic": ""}, config=config)

    chosen_topic = result.get('topic', '알 수 없음')
    ai_response = result['messages'][-1].content
    print(f"AI 선택 토픽: {chosen_topic}, 응답: {ai_response}")