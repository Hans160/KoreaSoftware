# 목적 - 뉴스 입력 -> 요약
#                 -> 감정분석
#                 -> 카테고리 분석  
#RunnableParallel

# 목적 - 뉴스 입력 -> 요약
#                 -> 감정분석
#                 -> 카테고리 분석  
# RunnableParallel 활용 구조 완성

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
# 💡 핵심 컴포넌트인 RunnableParallel을 임포트합니다.
from langchain_core.runnables import RunnableParallel

load_dotenv()
llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.5)  

# =====================================================================
# 1. 각 목적별 프롬프트 템플릿 정의 (가독성이 좋은 최신 튜플 스타일 활용)
# =====================================================================

# 1-1. 요약 프롬프트
summary_prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 전문 문장 요약가 입니다."),
    ("human", "다음의 긴 내용을 1개의 문장으로 핵심만 요약하시오:\n\n{article}")
])

# 1-2. 감정 분석 프롬프트
sentiment_prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 냉철한 금융·부동산 뉴스 감정 분석가입니다."),
    ("human", "다음 뉴스 기사의 전반적인 어조를 분석하여 [긍정, 부정, 중립] 중 하나로 답변하고, 그렇게 판단한 이유를 1문장으로 덧붙이세요:\n\n{article}")
])

# 1-3. 카테고리 분석 프롬프트
category_prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 뉴스를 정확히 분류하는 에디터입니다."),
    ("human", "다음 뉴스 기사에 가장 적합한 카테고리(예: 부동산, 정치, 경제, 사회, 테크 등)를 단어 하나로 지정하고 관련 키워드 3개를 뽑아주세요:\n\n{article}")
])


# =====================================================================
# 2. 각 목적별 서브 체인 정의
# =====================================================================
summary_chain = summary_prompt | llm | StrOutputParser()
sentiment_chain = sentiment_prompt | llm | StrOutputParser()
category_chain = category_prompt | llm | StrOutputParser()


# =====================================================================
# 3. RunnableParallel을 사용하여 서브 체인들을 병렬로 묶기
# =====================================================================
# 이렇게 묶어두면 단 한 번의 invoke 호출로 3개의 체인에 {article}이 동시에 전달되어 처리됩니다.
total_analysis_chain = RunnableParallel(
    summary=summary_chain,
    sentiment=sentiment_chain,
    category=category_chain
)


# =====================================================================
# 4. 데이터 입력 및 통합 실행
# =====================================================================
input_text = {
    "article": "서울 전세시장의 불안이 아파트를 넘어 빌라·다세대·연립 등 비아파트 시장 전반으로 확산되고 있다. "
                "전세 물건 부족과 임대료 상승이 장기화되는 가운데, 서민과 청년층의 주거 진입 통로 역할을 해온 비아파트 공급마저 급감하면서 주거 시장 불안이 비아파트 시장까지 빠르게 번지고 있다는 우려가 커지고 있다. "
                "이에 정부는 비아파트 주택 공급 촉진 대책을 발표했지만, 업계에서는 세제·금융 등 추가 규제 완화 방안이 빠진 만큼 단기간 내 공급 확대 효과를 기대하기 어렵다는 지적이 나온다."
}

# 병렬 체인 실행
result = total_analysis_chain.invoke(input_text)

# 결과 출력
print("=" * 60)
print("🔍 [1. 뉴스 요약 결과]")
print(result["summary"])
print("-" * 60)
print("📊 [2. 감정 분석 결과]")
print(result["sentiment"])
print("-" * 60)
print("🏷️ [3. 카테고리 분석 결과]")
print(result["category"])
print("=" * 60)


