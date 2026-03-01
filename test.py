import sys
sys.path.insert(0, '.')

from src.agent_implementation import create_agent, chat_with_agent

print("正在初始化Agent...")
agent, _ = create_agent(verbose=True)
print("Agent初始化完成。")

print("\n测试提问：P0300故障码是什么意思？")
response = chat_with_agent(agent, "P0300故障码是什么意思？")
print("\n回答：", response)