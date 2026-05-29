
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document   

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

query = "NVMe와 SATA의 차이는 무엇인가요?"
results = store.similarity_search(query, k=3) # 위 질문

print(f"질문: {query}\n")
print(f"가장 가까운 {len(results)} 개의 문서:\n")
for i, doc in enumerate(results):
    print(f"{i}. {doc.page_content}")


# 검색 결과 합치기
content = "\n".join([doc.page_content for doc in results])

prompt = ChatPromptTemplate.from_template(
    """
아래 문서를 참고하여 질문에 답하시오.

문서:
{content}

질문: {question}
"""
)

chain = prompt | llm

answer = chain.invoke({
    "question": query,
    "content": content
})

print(f"답변: {answer.content}")