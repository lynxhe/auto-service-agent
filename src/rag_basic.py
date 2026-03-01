# src/rag_basic.py
import os
# 强制离线模式，必须在导入任何 HuggingFace 相关库之前设置
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_DATASETS_OFFLINE"] = "1"

from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings

# 加载 .env 文件
load_dotenv()

# 调试：打印环境变量，确认读取成功（可删除）
print("DEEPSEEK_API_KEY from env:", os.getenv("DEEPSEEK_API_KEY"))

# 将 DeepSeek 密钥设置为 OpenAI 密钥环境变量（兼容性处理）
os.environ["OPENAI_API_KEY"] = os.getenv("DEEPSEEK_API_KEY", "")

def build_rag_pipeline():
    print("Step 1: 加载文档...")
    loader = TextLoader("data/manual_sample.txt", encoding='utf-8')
    documents = loader.load()
    
    print("Step 2: 文档切片...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=40,
        separators=["\n\n", "\n", " ", ""]
    )
    texts = text_splitter.split_documents(documents)
    print(f"生成 {len(texts)} 个文本块")
    
    print("Step 3: 创建向量库（使用本地 embedding）...")
    # 使用本地 embedding 模型（从缓存加载，不会联网）
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    vectorstore = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory="./chroma_db",
        collection_name="car_manual"
    )
    # 新版 Chroma 自动持久化，无需手动调用 persist()
    
    print("Step 4: 创建检索QA链...")
    llm = ChatOpenAI(
        model="deepseek-chat",
        temperature=0,
        openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
        openai_api_base="https://api.deepseek.com/v1"
    )
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        ),
        return_source_documents=True
    )
    
    return qa_chain, vectorstore

def ask_question(qa_chain, question):
    result = qa_chain({"query": question})
    return {
        "answer": result['result'],
        "sources": [doc.page_content[:100] + "..." for doc in result['source_documents']]
    }

if __name__ == "__main__":
    qa_chain, _ = build_rag_pipeline()
    result = ask_question(qa_chain, "P0300故障码是什么意思？")
    print(f"答案: {result['answer']}")
    print("来源:", result['sources'])