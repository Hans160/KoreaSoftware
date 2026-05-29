# 목적 - 여행계획 
# 도시입력  -> 음식추천                
#         -> 관광지 추천
#         -> 호텔 추천
# 사용자 입력의 OO을 보고, 시간표/동선/교통수단 vs 음식/관광지/
# RunnableParallel, RunnableBranch

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnableLambda, RunnableParallel

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.3)