import os
from dotenv import load_dotenv
from rag.chain import BasicRAG
from rag.retriever import get_retriever
from rag.embedding import get_openai_embedding
from langchain_openai import ChatOpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# Khởi tạo các đối tượng cần thiết cho AI
embedding = get_openai_embedding()
retrievers = get_retriever(source="dan_su", embedding=embedding)
gpt_llm = ChatOpenAI(temperature=0, openai_api_key=api_key)
basicrag = BasicRAG(retrievers, gpt_llm)