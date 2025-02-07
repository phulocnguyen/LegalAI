import pandas as pd
import csv
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import FAISS
from .embedding import get_openai_embedding


def get_retriever(source: str, embedding: Embeddings):
    return FAISS.load_local(
        f"./rag/faiss/{source}",
        embedding,
        allow_dangerous_deserialization=True,
    ).as_retriever()

def get_vectorstore(source: str, embedding: Embeddings):
    return FAISS.load_local(
        f"./rag/faiss/{source}",
        embedding,
        allow_dangerous_deserialization=True,
    )

def process_questions(file_path: str, vectorstore):
    df = pd.read_csv("./data_test/test.csv", header=1)
    questions = df['Câu hỏi'].head(100)  # Thay "cột câu hỏi" bằng tên chính xác của cột trong file test.xlsx
    print(df.head())
    with open("result.csv", mode="w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Question", "Relevant Documents"])

        for question in questions:
            relevant_documents = vectorstore.similarity_search_with_relevance_scores(question)
            for doc in relevant_documents:
                writer.writerow([question, doc])
            print(f"Processed question: {question}")

if __name__ == "__main__":
    embedding = get_openai_embedding()
    vectorstore = get_vectorstore("dan_su", embedding)
    relevant_documents = vectorstore.similarity_search_with_relevance_scores(
        "Trong trường hợp hai bên ký hợp đồng vay tài sản mà không có văn bản, chỉ bằng lời nói, nếu bên vay không trả tiền đúng hạn thì bên cho vay có quyền khởi kiện đòi nợ không?"
    )
    for doc in relevant_documents:
        print(doc)
        print()
