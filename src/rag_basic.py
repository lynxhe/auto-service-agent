# src/rag_basic.py
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings  # 本地 embedding

load_dotenv()

def build_rag_pipeline():
    """构建RAG基础流程"""
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
    # 使用 HuggingFace 本地 embedding 模型（首次运行会自动下载）
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    vectorstore = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory="./chroma_db",
        collection_name="car_manual"
    )
    vectorstore.persist()
    
    print("Step 4: 创建检索QA链...")
    # 仍使用 DeepSeek 在线模型（需要余额）
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