from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_openai_embedding(model_name="text-embedding-3-small", api_key=None):
    # Lấy API key từ biến môi trường nếu không được truyền trực tiếp
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("API key không được cung cấp và không tìm thấy biến môi trường OPENAI_API_KEY.")
    
    return OpenAIEmbeddings(model=model_name, api_key=api_key)

if __name__ == "__main__":
    # Bạn có thể truyền API key trực tiếp ở đây nếu cần
    model = get_openai_embedding(api_key="")
    print(model)
