from dotenv import load_dotenv

from langchain_core.prompts import (ChatPromptTemplate,MessagesPlaceholder) 
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI


load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.3)

prompt = ChatPromptTemplate.from_messages([
   ("system", "당신은 친절한 챗봇입니다."),      # 나의 페르소나
   ("user", "{input}")                      # 나의 질문      # 챗봇 답변("ai","assistant")

])

chain = prompt | llm | StrOutputParser()
print(chain.invoke({"input":"안녕하세요, 나는 홍길동입니다."}))
print(chain.invoke({"input":"그래서, 내가 누구라구요?"}))
print(chain.invoke({"input":"아니! 내가 방금 말했잖아!! 왜 넌 그것도 몰라??"}))

print('-'*50)

prompt_with_history = ChatPromptTemplate.from_messages([
   ("system", "당신은 친절한 챗봇입니다."),     
   MessagesPlaceholder("history"), 
   ("user", "{input}")

])

chain2 = prompt_with_history | llm | StrOutputParser()
print(chain2.invoke({"input":"안녕하세요, 나는 홍길동입니다."}))
print(chain2.invoke({"input":"그래서, 내가 누구라구요?"}))
print(chain2.invoke({"input":"아니! 내가 방금 말했잖아!! 왜 넌 그것도 몰라??"}))
print(chain2.invoke({"input":"그래서, 누구라구요?"}))

chain2 = prompt_with_history | llm | StrOutputParser()

history_example = [
    HumanMessage(content="안녕하세요, 나는 홍길동입니다."),
    AIMessage(content="네, 홍길동님 반갑습니다."),
]

answer = chain2.invoke({
    "history": history_example,
    "input":"그래서, 누구라구요?" 
    })
print(answer)