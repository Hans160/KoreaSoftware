from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = PyPDFLoader("./Javascript_Secure_Coding.pdf")
pages = loader.load()

print(f"PDF 페이지수: {len(pages)}")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,         # 최대 500개가 되면 일단 짜름
    chunk_overlap=100          # 문장이 중가에 짤리면 의미가 사라지니
)

chunks = splitter.split_documents(pages)
print(f"분할된 글자수: {len(chunks)}")
print(f"첫 정크 글자수: {len(chunks[0].page_content)}")

first = chunks[0]
print(first.metadata)
print(first.page_content)
print('-'*30)