
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document   
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
llm = ChatOpenAI(model='gpt-4o-mini')

docs = [
    Document(page_content="NVMe 는 SSD 의 인터페이스 규격으로 PCIe를 사용한다."),
    Document(page_content="SATA SSD 는 NVMe 보다 속도가 느리다."),
    Document(page_content="HDD는 회전 디스크 기반이라 IO가 느린 편이다."),
    Document(page_content="파이썬은 인기 있는 프로그래밍 언어다."),
    Document(page_content="자바스크립트는 브라우저에서 동작하는 언어이다."),
    Document(page_content="Rust는 메모리 안정성과 성능을 동시에 추구한다.")
]

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
store = InMemoryVectorStore.from_documents(docs,embedding = embeddings)
retriever = store.as_retriever(search_kwargs={"k": 2})

prompt = ChatPromptTemplate.from_template(
    """
아래 문서를 참고하여 질문에 답하시오.\n\n
문서:\n
{content}\n\n
질문: {question}
"""
)

def format_docs(docs):
    """검색된 Document 리스트를 => 하나ㅡ의 문자열로 변환한다."""
    return "\n\n".join([doc.page_content for doc in docs])

chain = (
    {
        "context": retriever | 결과는 document포멧이라서_이포멧을_일반 자연어로 변화해주는 함수짜기
        "question": RunnablePassthrough()  # 질문을 다음 파이프라인으로도 그대로 전달함.
    }
    | prompt
    | llm
    | StrOutputParser()
)

question = "NVMe 와 SATA의 차이는 무엇인가?"
question = "파이썬은