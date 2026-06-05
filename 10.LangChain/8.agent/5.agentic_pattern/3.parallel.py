from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

load_dotenv()

# AI 심사위원에게 '오직 숫자 점수만' 출력하라고 지시하는 프롬프트
vote_prompt = ChatPromptTemplate.from_template(
"""
당신은 번역 품질 평가자 입니다. 다음 번역의 품질을 평가해 주세요.

원문(영어): {original}
번역(한국어): {translation}

[주의] 다른 설명이나 문장은 절대 출력하지 마세요. 
오직 리커트 척도 점수(1, 2, 3, 4, 5 중 하나)에 해당되는 숫자 1글자만 출력하세요.
"""
)

# 3명의 AI 심사위원 설정
llm1 = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
llm2 = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
llm3 = ChatOpenAI(model="gpt-4o-mini", temperature=1.0)

parser = StrOutputParser()

# 각 심사위원의 체인 생성
voter1 = vote_prompt | llm1 | parser
voter2 = vote_prompt | llm2 | parser
voter3 = vote_prompt | llm3 | parser

# 병렬 처리 설정
parallel_vote = RunnableParallel(
    judge_strict=voter1,
    judge_balance=voter2,
    judge_creative=voter3
)

#  테스트할 문장 (원문과 번역문)
input_data = {
    "original": "Even a sheet of blank paper is better if lifted together.",
    "translation": "백지장도 맞들면 낫다"
}

print("---  3명의 AI 심사위원이 점수를 매기는 중입니다 --- \n")

# 동시에 채점 시작
results = parallel_vote.invoke(input_data)

#  결과 출력 및 숫자 변환
score1 = int(results['judge_strict'].strip())
score2 = int(results['judge_balance'].strip())
score3 = int(results['judge_creative'].strip())

print(f" 심사위원 1 (엄격) 점수: {score1} / 5")
print(f" 심사위원 2 (밸런스) 점수: {score2} / 5")
print(f" 심사위원 3 (창의적) 점수: {score3} / 5")
print("-" * 40)

#  파이썬으로 평균 점수 계산하기
average_score = (score1 + score2 + score3) / 3
print(f" 최종 평균 점수: {average_score:.2f} / 5")
