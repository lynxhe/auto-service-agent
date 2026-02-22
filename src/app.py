import sys
import os
sys.path.append(os.path.dirname(__file__))
import gradio as gr
from agent_implementation import create_agent, chat_with_agent
import time

# 初始化Agent（全局单例）
agent, _ = create_agent(verbose=False)

def respond(message, history):
    """处理聊天消息"""
    response = chat_with_agent(agent, message)
    
    # 模拟打字效果
    full_response = ""
    for char in response:
        full_response += char
        time.sleep(0.01)
        yield full_response

def clear_chat():
    """清空对话历史"""
    agent.memory.clear()
    return []

# 创建Gradio界面
with gr.Blocks(title="汽车售后智能助手", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🚗 汽车售后智能助手
    
    ### 基于RAG + Agent的智能问答系统
    
    支持功能：
    - 🔍 **故障码查询**：输入P0300、P0171等故障码
    - 📚 **维修手册检索**：查询保养步骤、维修方法
    - 🔧 **保养建议**：输入里程获取保养项目
    - 📊 **车型参数**：查询深蓝SL03、赛力斯SF5等参数
    
    *本项目针对赛力斯AI智能体开发工程师岗位设计*
    """)
    
    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(label="对话历史", height=500)
            msg = gr.Textbox(
                label="输入您的问题",
                placeholder="例如：P0300故障码是什么意思？",
                lines=2
            )
            with gr.Row():
                clear = gr.Button("🗑️ 清空对话")
                submit = gr.Button("🚀 发送", variant="primary")
        
        with gr.Column(scale=1):
            gr.Markdown("### 📝 示例问题")
            gr.Examples(
                examples=[
                    ["P0300故障码是什么意思？"],
                    ["5000公里该做什么保养？"],
                    ["深蓝SL03的续航是多少？"],
                    ["怎么更换机油？"],
                    ["发动机故障灯亮了怎么办？"],
                    ["赛力斯SF5的参数"]
                ],
                inputs=msg
            )
            
            gr.Markdown("### 🔧 技术栈")
            gr.Markdown("""
            - **LangChain**: Agent框架
            - **ChromaDB**: 向量检索
            - **OpenAI**: LLM + Embeddings
            - **Gradio**: Web界面
            - **ReAct模式**: 思考-行动-观察
            """)
    
    # 绑定事件
    msg.submit(respond, [msg, chatbot], chatbot).then(
        lambda: "", None, msg
    )
    submit.click(respond, [msg, chatbot], chatbot).then(
        lambda: "", None, msg
    )
    clear.click(clear_chat, None, chatbot)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=False
    )