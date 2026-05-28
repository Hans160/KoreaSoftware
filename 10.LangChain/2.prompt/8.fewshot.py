from dotenv import load_dotenv

from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    FewShotPromptTemplate
)

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
llm = ChatOpenAI(model='gpt-4o-mini')
parser = StrOutputParser()

examples = [
    {"sentence": "오늘 정말 최고의 하루였어!", "result": "감정: 긍정 / 점수: 9"},
    {"sentence": "이거 진짜 별로네요. 시간 낭비였어요.", "result": "감정: 부정 / 점수: 2"},
    {"sentence": "그냥 평범했어요. 특별히 좋지도 나쁘지도 않았네요.", "result": "감정: 중립 / 점수: 5"},
    {"sentence": "와 진짜 감동이예요. 눈물이 날 정도였어요!", "result": "감정: 긍정 / 점수: 10"},
    {"sentence": "기대했던 것보다는 별로지만, 그래도 쓸만했어요.", "result": "감정: 중립 / 점수: 6"}
]

example_prompt = PromptTemplate(
    input_variables=["sentence", "result"],
    template="문장: {sentence}\n분석: {result}\n"
)

fewshot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="다음은 문장의 감정을 분석한 예시입니다. \n같은 형식으로 다음 문장을 분석하세요. \n\n=== 예시 :",
    suffix="=== 예시 끝 === \n\n새로 분석할 문장 :\n문장: {sentence}\n분석: ",
    input_variables=["sentence"],
    example_separator="\n~~~~~\n"
)

# 🛠️ [수정 포인트 1] 중괄호 {}를 소괄호 () 형태로 변경하여 튜플로 구성합니다.
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 한국어 감정 분석가 입니다. 예시와 같은 형태로 답변하세요."),
    ("user", "{fewshot_text}")
])

llm = ChatOpenAI(model='gpt-4o-mini')
chain = chat_prompt | llm | StrOutputParser()

# 최종 분석할 문장
target = "오랫만에 만난 친구랑 좋은 시간을 보냈어요. 다음에 또 보고 싶네요."
fewshot_text = fewshot_prompt.format(sentence=target)

# 🛠️ [수정 포인트 2] 조립된 fewshot_text를 체인에 입력하여 실행(invoke)하고 결과를 출력합니다.
result = chain.invoke({"fewshot_text": fewshot_text})

print("=== [LLM 분석 결과] ===")
print("문장 :", target, "\n분석 : ", result)


#########################
# 만약 우리가 퓨샷을 안했다면? 그냥 질문했다면?

plain_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "당신은 한국어 감정 분석가 입니다."),
        ("user", "다음 문장의 감정을 분석하시오: {sentence}"),
    ]) | llm | StrOutputParser
)
print(plain_chain.invoke({"sentence": target}))
