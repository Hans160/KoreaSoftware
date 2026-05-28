from dotenv import load_dotenv

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,    
    AIMessagePromptTemplate
) 

from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableBranch, RunnableLambda

load_dotenv()

template = "다음의 긴 내용을 3개의 문장으로 요약하시오:\n\n{article}"
chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("당신은 전문 문장 요약가 입니다."),
    HumanMessagePromptTemplate.from_template(template)
])

llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.5)  # 이런 경우 0.3~0.5

chain = chat_prompt | llm | RunnableLambda(lambda x: {"summary":x.content.strip()})

input_text = {
    "article": "서울 전세시장의 불안이 아파트를 넘어 빌라·다세대·연립 등 비아파트 시장 전반으로 확산되고 있다."
                "전세 물건 부족과 임대료 상승이 장기화되는 가운데, 서민과 청년층의 주거 진입 통로 역할을 해온 비아파트 공급마저 급감하면서 주거 시장 불안이 비아파트 시장까지 빠르게 번지고 있다는 우려가 커지고 있다."
                "이에 정부는 비아파트 주택 공급 촉진 대책을 발표했지만, 업계에서는 세제·금융 등 추가 규제 완화 방안이 빠진 만큼 단기간 내 공급 확대 효과를 기대하기 어렵다는 지적이 나온다."
}

result = chain.invoke(input_text)
print("요약 결과 :", result["summary"])
