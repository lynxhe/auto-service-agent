# src/app.py
import gradio as gr
from src.agent_implementation import create_agent, chat_with_agent

# 初始化Agent（全局单例）
agent, _ = create_agent(verbose=False)

def respond(message):
    print(f"收到用户消息: {message}")
    try:
        response = chat_with_agent(agent, message)
        print(f"助手回复: {response}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        response = f"错误: {str(e)}"
    return response

# 创建简单界面
iface = gr.Interface(
    fn=respond,
    inputs=gr.Textbox(label="输入您的问题", placeholder="例如：P0300故障码是什么意思？"),
    outputs=gr.Textbox(label="回答"),
    title="汽车售后智能助手",
    description="基于RAG + Agent的智能问答系统。支持故障码查询、保养建议、车型参数等。",
    examples=[
        "P0300故障码是什么意思？",
        "5000公里该做什么保养？",
        "深蓝SL03的续航是多少？",
        "怎么更换机油？",
        "发动机故障灯亮了怎么办？",
        "赛力斯SF5的参数"
    ]
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860, share=False)