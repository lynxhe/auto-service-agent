# src/agent_implementation.py
import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from rag_basic import build_rag_pipeline
from tools import FaultCodeTool, MaintenanceTool, VehicleInfoTool

load_dotenv()

def create_agent(verbose=True):
    """创建ReAct模式的Agent"""
    
    # 构建RAG问答链
    qa_chain, vectorstore = build_rag_pipeline()
    
    # 初始化工具
    fault_tool = FaultCodeTool()
    maintenance_tool = MaintenanceTool()
    vehicle_tool = VehicleInfoTool()
    
    # 知识库检索工具（包装RAG链）
    retrieval_tool = Tool(
        name="知识库检索",
        func=lambda q: qa_chain.run(q),
        description="查询汽车维修手册、保养指南、故障码解释等知识。输入应该是具体的自然语言问题。"
    )
    
    tools = [retrieval_tool, fault_tool, maintenance_tool, vehicle_tool]
    
    # 创建记忆组件
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    # 系统提示词
    system_message = """你是一位专业的汽车售后顾问。你的职责是：
1. 基于检索到的知识回答问题，不要编造信息
2. 如果不确定，请说明不知道
3. 涉及安全操作时，建议前往专业维修店
4. 回答要简洁、专业、有用
5. 对于故障码问题，先查故障码工具，再查知识库获取详细步骤"""
    
    # 初始化DeepSeek LLM
    llm = ChatOpenAI(
        model="deepseek-chat",
        temperature=0,
        openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
        openai_api_base="https://api.deepseek.com/v1"
    )
    
    # 初始化Agent - 使用ReAct模式
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=verbose,
        handle_parsing_errors=True,
        agent_kwargs={
            "system_message": system_message
        }
    )
    
    return agent, vectorstore

def chat_with_agent(agent, message):
    """与Agent对话"""
    try:
        response = agent.run(message)
        return response
    except Exception as e:
        return f"抱歉，处理出错：{str(e)}"

if __name__ == "__main__":
    agent, _ = create_agent()
    print("汽车售后智能助手已启动（输入exit退出）")
    print("-" * 50)
    
    while True:
        user_input = input("\n您: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        
        response = chat_with_agent(agent, user_input)
        print(f"\n助手: {response}")