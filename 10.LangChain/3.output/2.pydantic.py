from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

load_dotenv()


class MovieReview(BaseModel):
    """영화 리뷰 분석 결과"""
    title: str = Field(description="영화 제목")
    sentiment: str = Field(description="감성 분류: 긍정, 부정, 중립")
    score: int = Field(description="1~10점수")
    summary: str = Field(description="리뷰 요약 (1~2문장)")
    keywords: list[str] = Field(description="핵심 키워드 3개")

llm = ChatOpenAI(model='gpt-4o-mini')

parser = PydanticOutputParser(pydantic_object=MovieReview)
# print("포멧 명령문:")
# print(parser.get_format_instructions())

prompt = ChatPromptTemplate.from_template(
    """아듬 영화 리뷰를 분석해 주세요.

   리뷰: {review}

   {format_instructions}
   """
)

chain = prompt | llm | parser

reviews = [
    "",
    "",
    ""
]

for review in reviews:
    result = chain.invoke({
        "review": review,
        "format_instructions": parser.get_format_instructions()
        })
    
    print(f"제목: result.title")
    print(f"감성: result.sentiment")
    print(f"점수: result.score")
    print(f"리뷰 요약: result.summary")
    print(f"핵심 키워드: result.keywords")

