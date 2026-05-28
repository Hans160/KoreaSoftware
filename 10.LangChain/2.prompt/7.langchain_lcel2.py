
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from langchain_openai import ChatOpenAI

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda


load_dotenv()
llm = ChatOpenAI(model='gpt-4o-mini')

template = " "

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("당신은 브랜드 컨텐츠 기획자 입니다."),
    HumanMessagePromptTemplate.from_template("회사를 홍보하기 위한 {company}  회사의 {product} 상품을 " \
    "기반으로 캐치프레이즈를 만들어 주세요"),
])

llm = ChatOpenAI(model='gpt-4o-mini')
parser = StrOutputParser()

# 아래 체이닝 문법을 LCEL ( LangChain Expression Language)라고 부름
chain = prompt | llm | RunnableLambda(lambda x: {"response": x})

# inputs = {"company":"삼성전자", "product":"메모리"}
inputs = {"company":"하이닉스", "product":"HBM"}

result = chain.invoke(inputs)  # <--여기가 핵심, 모든건 체인을 호출(invoke) 하면서 실행됨.

# 아래 부분 조차도 체인에 포함한것 (RunnableLambda)를 차가시다.
final_result = {"response": result}
print(final_result)