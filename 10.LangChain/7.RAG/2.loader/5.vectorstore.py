# pip install chromadb
# pip install langchain-chroma

import os 
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

from langchain_chroma import Chroma

load_dotenv()

DB_DIR = "./chroma_db"
COLLECTION_NAME ="memory"


embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

def bulid_store():
    docs = TextLoader("./hbm.txt", encoding="utf-8").load()
    chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100).split_documents(docs)

    store = Chroma.from_documents(
        chunks, 
        embeddings, 
        persist_directory=DB_DIR, 
        collection_name=COLLECTION_NAME
        )
    return store

def load_store():
    store = Chroma(
        persist_directory=DB_DIR, 
        collection_name=COLLECTION_NAME, 
        embedding_function=embeddings
        )
    print(f"기존 DB 로딩 성공 - {store._collection.count()} 청크 로딩됨")
    return store

if os.path.exists(DB_DIR) and os.listdir(DB_DIR):
    store = load_store()
else:
    store = bulid_store()

results = store.similarity_search("HBM이란 무엇인가요?", k=2)
for i,d in enumerate(results, start=1):
    print(f"{i} -> {d.page_content}")