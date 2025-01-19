import os
from dotenv import load_dotenv
from pydantic import BaseModel
from rag.chain import BasicRAG
from rag.retriever import get_retriever
from rag.embedding import get_openai_embedding
from langchain_openai import ChatOpenAI
from rag.retriever import get_retriever

load_dotenv()

embedding = get_openai_embedding(api_key="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")
retrievers = get_retriever(source="dan_su", embedding=embedding)
gpt_llm = ChatOpenAI(temperature=0, openai_api_key="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")
basicrag = BasicRAG(retrievers, gpt_llm)
question = str(input("Tôi có thể giúp gì cho bạn: "))
ans = basicrag.answer(question=question)
print(ans)
