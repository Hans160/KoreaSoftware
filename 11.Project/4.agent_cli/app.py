# app.py
import os
from dotenv import load_dotenv

# 1. 분리해둔 금융 툴셋 모듈로부터 4대 TOOLS 리스트 로드
# (get_naver_news_api, get_exchange_rate, get_stock_price, get_company_info가 포함됨)
from fin_tools import TOOLS

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

# 환경 변수(.env) 로드
load_dotenv()

# 2. 4가지 도구의 특성에 맞게 시스템 지침(System Prompt) 고도화
SYSTEM_PROMPT = """당신은 금융 및 경제 정보 분석 전문 개인 비서입니다.
주가 조회, 실시간 환율 체크, 뉴스 브리핑, 기업 조회를 정확하게 처리하는 역할을 수행합니다.
- 환율/주가 같은 수치 데이터는 반드시 도구를 통해서 확인하시오 ( 추측 또는 과거데이터 이용 금지)
- 출처 링크가 있으면 함께 제시하시오.

[도구 사용 가이드 가이드라인]
1. 주가 관련 질문(예: 시세, 종가, 고가 등) -> 'get_stock_price' 툴 사용
2. 환율 관련 질문(예: 달러 가격, 엔화 환율 등) -> 'get_exchange_rate' 툴 사용
3. 실시간 뉴스 및 언론사 동향 브리핑 -> 'get_naver_news_api' 툴 사용
4. 기업의 개요, 창립 정보, 비즈니스 모델 및 백과사전식 최근 정보 요약 -> 'get_company_info' 툴 사용

각 도구들로부터 전달받은 가공되지 않은 러프한 데이터를 수집한 뒤, 
사용자가 한눈에 읽기 편하도록 항목별로 단락을 나누어 깔끔한 한국어 브리핑 리포트 형태로 답변하세요."""

# 3. LLM 모델 및 랭체인 에이전트 빌드 (가장 정확한 도구 선택을 위해 temperature=0 설정)
llm = ChatOpenAI(model="gpt-4o-mini")
agent = create_agent(
    model=llm,
    tools=TOOLS,
    system_prompt=SYSTEM_PROMPT
)

def ask(q: str):
    """LangChain 에이전트를 통해서 질문을 호출하고 최종 답변을 반환합니다."""
    print(f"\n[질문] {q}")
    try:
        # 최신 에이전트 실행 표준 포맷 (대화 메시지 리스트 형태로 래핑)
        result = agent.invoke({"messages": [("user", q)]})
        # AI가 도구를 거쳐 내놓은 최종 메시지 콘텐츠 추출
        tool_used = [c["name"] for c in result["messages"][-1].tool_calls]
        answer = result["messages"][-1].content
        return answer
    except Exception as e:
        return f"에이전트 실행 중 오류가 발생했습니다: {str(e)}"


if __name__ == "__main__":
    print('==================================================')
    print('   금융 정보 AI 비서 CLI 시스템 가동 (데모 시작)  ')
    print('==================================================')
    
    demo_questions = [
        "삼성전자 주가 알려줘", 
        "달러 환율 얼마야?", 
        "엔비디아 관련 최근 뉴스는 뭐가 있어?"
    ]
    
    for q in demo_questions:
        response = ask(q)
        print(f"[답변] {response}")
        print("-" * 60)

    print('\n==================================================')
    print('   수동 실시간 질의 응답 시스템 터미널 가동       ')
    print('==================================================')
    
    while True:
        try:
            # 사용자로부터 콘솔창 입력을 받음
            user_input = input("\n금융 비서에게 질문을 입력하세요 (종료: q, quit, exit): ").strip()
        except (KeyboardInterrupt, EOFError):
            # Ctrl+C 등을 눌렀을 때 비정상 종료되는 현상 방지 안전장치
            print("\n프로그램을 종료합니다.")
            break

        # 사용자가 아무것도 입력하지 않은 경우 스킵 후 다음 루프 진행
        if not user_input:
            continue

        # 종료 명령어 조건 검증 탈출
        if user_input.lower() in ("q", "quit", "exit"):
            print("==================================================")
            print(" 금융 정보 비서 프로그램을 종료합니다. 감사합니다! ")
            print("==================================================")
            break
            
        # 정상 질문인 경우 ask 함수 호출 후 결과 출력
        response = ask(user_input)
        print(f"[답변] {response}")
