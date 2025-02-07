from dotenv import load_dotenv
import os
from typing import List
from rag.prepare_data import load_data
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import numpy as np
import faiss
from rag.embedding import get_openai_embedding

def save_vector_db(
    documents: List[Document],
    embedding: Embeddings,
    path=os.environ["VECTOR_DATABASE_PATH"],
) -> FAISS:
    vector_store = FAISS.from_documents(
        documents=documents, 
        embedding=embedding
    )
    vector_store.save_local(path)
    return vector_store

if __name__ == "__main__":
    embedding = get_openai_embedding(api_key="")
    document4 = load_data("./datapickle/dan_su.pkl")
    print(document4[0])    
    save_vector_db(document4, embedding, path="./faiss/dan_su")

