from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader("./hbm.txt", encoding="utf-8")
documents = loader.load()

contents = documents[0].page_content
print(f"원본 글자수: {len(contents)}")

# 일반적으로, 1000:200 / 1500:300 / 2000:500 정도 내외로, 실제 짤린 내용을 보고 판단함.
char_splitter = CharacterTextSplitter(
    separator="\n\n",     # 이것을 목표로 하는데, 이게 안될 수 있으니...
    chunk_size=500,         # 최대 500개가 되면 일단 짜름
    chunk_overlap=100)          # 문장이 중가에 짤리면 의미가 사라지니

chunks_char = char_splitter.split_text(contents)
print(f"분할된 글자수: {len(chunks_char)}")
print(f"첫 정크 글자수: {len(chunks_char[0].page_content)}")

##############################

recur_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,         # 최대 500개가 되면 일단 짜름
    chunk_overlap=100          # 문장이 중가에 짤리면 의미가 사라지니
)

chunks_recur = recur_splitter.split_text(contents)
print(f"분할된 글자수: {len(chunks_recur)}")
print(f"첫 정크 글자수: {len(chunks_recur[0].page_content)}")