from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# 1단계 : 리서치
research_prompt = ChatPromptTemplate.from_template(
    "다음 주제에 대해 핵심 사실 5가지를 간결하게 정리해주세요"
    "\n\n주제: {topic}"
)

research_chain = research_prompt | llm | parser


# 2단계 : 게이트 검증
gate_prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 리서치 결과를 검증하는 엄격한 평가관입니다. "
               "기준을 통과하면 다른 설명 없이 오직 'PASS'만 출력하세요. "
               "실패하면 오직 한 줄로만 실패 이유를 설명하세요."),
    ("user", (
        "다음 리서치 결과가 적합한지 평가해 주세요.\n\n"
        "리서치 결과:\n{research}\n\n"
        "평가 기준:\n"
        "1. 사실 5가지가 올바르게 포함되어 있는가?\n"
        "2. 각 사실이 구체적이고 검증 가능한가?\n"
        "3. 주제와 관련이 있는가?\n\n"
        "결과:"
    ))
])
gate_chain = gate_prompt | llm | parser

# 3단계 :분석 수행
analysis_prompt = ChatPromptTemplate.from_template(
    "다음 리서치 결과를 바탕으로 심층 분석 내용을 작성해주시오.\n\n"
    "리서치 결과:\n{research}\n\n"
    "다음을 포함해주세요.\n"
    "- 핵심 트렌드 또는 패턴\n"
    "- 시사점\n"
    "- 향후 전망"
)
analysis_chain = analysis_prompt | llm | parser


# 4단계 : 보고서 생성
report_chain = ''
report_prompt = ChatPromptTemplate.from_template(
    "다음 리서치와 분석된 내용을 바탕으로 간결한 보고서를 작성하시오.\n"
    "작성 레벨: CEO에게 보고하는 레벨로 작성해주세요.\n\n"
    "리서치:\n{research}\n\n"
    "분석:\n{analysis}\n\n"
    "출력형식:\n"
    "- 제목:\n"
    "- 요약 (3줄):\n"
    "- 핵심 발견사항:\n"
    "- 결론:"
    "- 출력형식: HTML"
)
report_chain = report_prompt | llm | parser

def run_chaining_pipeline(topic):
    # 1단계 : 리서치
    print('[1단계] 리서치 수행중')
    research = research_chain.invoke({"topic": topic})

    # 2단계 : 게이트 검증
    print('[2단계] 게이트 검증 수행중')
    gate_result = gate_chain.invoke({"research": research})
    print(f" 2단계 결과: {gate_result.strip()}")
    if gate_result.strip() != "PASS":
        print(" 게이트 검증에 실패하여 해당 업무를 재 수행 합니다.")
        gate_result = gate_chain.invoke({"research": research})
        # 고도화를 할거면, 반복 횟수 정의하거나, 프롬프트를 살짝씩 고도화 한거로 시키거나, 또는 모델(gpt-4o-mini)

    # 3단계 :분석 수행
    print('[3단계] 분석 수행중')
    analysis = analysis_chain.invoke({"research": research})

    # 4단계 : 보고서 생성
    print('[4단계] 보고서 생성중')
    report = report_chain.invoke({"research": research , "analysis": analysis})

    return report

# 질문
# 1. 2026년도 생성형 AI 시장 동향 조사를 해오시오.
# topic = "2026년 생성형 AI 시장 동향 조사를 해오시오."
topic = "2025년도의 한해동안의 주요 해킹 사례와 보안기술 동향을 알려줘"
result = run_chaining_pipeline(topic)

print('-'*60)
print('최종 보고서')
print('-'*60)

# 리서치 -> 분석 -> 보고서
print(result)