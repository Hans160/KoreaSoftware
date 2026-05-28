
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JSONOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')

parser = JSONOutputParser()

prompt = ChatPromptTemplate.from_messages(
     """아듬 영화 리뷰를 분석해 주시오.

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
     print(result)