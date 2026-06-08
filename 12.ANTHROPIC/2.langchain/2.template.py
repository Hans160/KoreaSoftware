from dotenv import load_dotenv

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

load_dotenv()

llm = Chat







chat_template = PromptTemplate.from_messages(
    ("system", "당신은 {role} 전문가입니다. 질문에 자세히 답변해 주세요."),
    ("human", "다음 개념에 대해서 설명해주세요: {concept}")
)

chain = chat_template | llm

response = chain.invoke({"role": "자율주행 자동차", "concept": "자율주행 자동차"})