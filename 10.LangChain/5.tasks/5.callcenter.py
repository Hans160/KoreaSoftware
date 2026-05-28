# 목적 - 질문 유형에 따라 적합한 항목으로 답변한다. 
# 질문 유형  -> 배송조회 상담원                
#           -> 결제관련 상담원
#           -> 기술지원 상담원
#RunnableBranch
# 목적 - 질문 유형에 따라 적합한 항목으로 답변한다. 
# 질문 유형  -> 배송조회 상담원                
#           -> 결제관련 상담원
#           -> 기술지원 상담원
# RunnableBranch 라우팅 구조 완성

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnableLambda

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.3)

# 🛠️ [수정] 체인을 생성하는 팩토리 함수 정의
def make_chain(role, debug_msg):
    return (
        # 디버깅 메시지 출력을 위한 RunnableLambda 연결
        RunnableLambda(lambda x: print(f"\n[라우팅 성공] >>> {debug_msg}") or x)

        | ChatPromptTemplate.from_messages([
            ("system", role),
            ("user", "{question}") # {question}을 문자열로 선언해야 합니다.
        ])
        | llm
        | StrOutputParser() # 괄호()를 붙여 인스턴스화해야 합니다.
    )

# 1. 각 질문 유형에 맞는 전문 상담원 체인 생성
delivery_chain = make_chain(
    "당신은 친절한 배송조회 상담원입니다. 배송 상태, 운송장 번호, 배송지 변경 관련 안내를 전문적이고 정중하게 답하시오.",
    "배송조회 상담원 체인 실행"
)

billing_chain = make_chain(
    "당신은 결제 및 환불 담당 상담원입니다. 결제 취소, 영수증 발행, 환불 처리 절차를 정확하게 답하시오.",
    "결제관련 상담원 체인 실행"
)

tech_chain = make_chain(
    "당신은 IT 기기 및 기술지원 담당 전문가입니다. 프로그램 설치 오류, 하드웨어 고장 진단 해결책을 단계별로 알기 쉽게 설명하시오.",
    "기술지원 상담원 체인 실행"
)

general_chain = make_chain(
    "당신은 일반 고객 센터 상담원입니다. 안내하기 어려운 질문에 대해 정중하게 양해를 구하는 답변을 작성하시오.",
    "일반 상담원 체인 실행"
)

# 2. RunnableBranch를 이용한 라우팅 조건 설정
# (조건 람다 함수, 실행할 체인) 구조로 매핑합니다.
branch = RunnableBranch(
    (
        lambda x: "배송" in x["question"] or "택배" in x["question"] or "위치" in x["question"],
        delivery_chain
    ),
    (
        lambda x: "결제" in x["question"] or "환불" in x["question"] or "카드" in x["question"],
        billing_chain
    ),
    (
        lambda x: "설치" in x["question"] or "오류" in x["question"] or "에러" in x["question"] or "고장" in x["question"],
        tech_chain
    ),
    # 위의 세 조건에 모두 해당하지 않는 경우 실행될 기본(Default) 체인
    general_chain
)

# 3. 테스트 질문 세트
questions = [
    "어제 주문한 노트북 배송 조회는 어디서 하나요?",
    "신용카드로 결제했는데 환불받고 싶어요. 절차가 어떻게 되나요?",
    "프로그램을 설치하는데 에러 코드가 뜨면서 자꾸 튕깁니다. 도와주세요.",
    "오늘 저녁 메뉴 추천해줘"
]

# 4. 반복문을 통한 라우팅 테스트 실행
print("🚀 고객 센터 AI 라우팅 시스템 구동 시작...")
for q in questions:
    print(f"\n고객 질문: '{q}'")
    # 최신 랭체인은 .run() 대신 .invoke()를 사용합니다.
    result = branch.invoke({"question": q})
    print(f"상담원 답변: {result}")
    print("-" * 50)
