import os
from operator import itemgetter
from dotenv import load_dotenv
from rag.retriever import get_retriever
from typing import List, Literal
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import LLM
from langchain_community.vectorstores import FAISS

load_dotenv()

def format_docs(docs: Document):
    def get_content(doc: Document):
        res = doc.page_content
        
        return res
    return "\n\n".join(
        get_content(doc) if isinstance(doc, Document) else get_content(doc[0])
        for doc in docs
    )

class BasicRAG:
    def __init__(self, retriever: VectorStoreRetriever, llm):
        self.retriever = retriever
        self.llm = llm
        template = """Giả sử bạn là chuyên gia tư vấn về pháp luật Việt Nam có tên là EasyLaw, bạn là 1 người nhiệt huyết, tận tình, mong muốn giải đáp những thắc mắc, câu hỏi về pháp lý. Bạn có nhiệm vụ tư vấn, trả lời câu hỏi pháp luật chỉ dựa trên những tài liệu mà bạn được cung cấp bên dưới đây.
        Đây là tài liệu được cung cấp: {context}

        Đây là câu hỏi, nội dung tư vấn bạn cần trả lời: {question}
        
        Hãy trả lời câu hỏi trên bằng 1 đoạn văn trả lời không quá dài theo định dạng sau:
        "Căn cứ vào điều ..., bộ luật ... có hiệu lực từ ngày ... thì ....". Đoạn cuối văn bản có thể cung cấp thêm đường link dẫn đến nội dung chứa bộ luật đó. Đương nhiên, nếu tài liệu không liên quan đến câu hỏi, hoặc không giải quyết được vấn đề câu hỏi đưa ra thì xin lỗi người dùng và trả lời họ theo định dạng: "Hiện tại, với kho dữ liệu đang được hoàn thiện, EasyLaw rất tiếc chưa thể cung cấp câu trả lời thoả đáng cho câu hỏi của bạn. Chúng tôi đang nỗ lực nghiên cứu và phát triển để mở rộng phạm vi hỗ trợ của EasyLaw trong tương lai gần. Bạn cũng có thể truy cập website LuatVietnam.vn để tìm kiếm thêm thông tin về những thắc mắc của mình! Cảm ơn bạn đã kiên nhẫn. Hy vọng những thông tin trên sẽ hữu ích cho bạn.
        """
        self.prompt = ChatPromptTemplate.from_template(template)
        self.chain = (
            {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def answer(self, question: str) -> str:
        return self.chain.invoke(question)
if __name__ == "__main__":
    pass