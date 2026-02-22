\# 🚗 汽车售后知识库智能问答助手



\[!\[GitHub stars](https://img.shields.io/github/stars/lynxhe/auto-service-agent)](https://github.com/lynxhe/auto-service-agent/stargazers)

\[!\[Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3119/)

\[!\[Gradio](https://img.shields.io/badge/Gradio-4.29.0-orange)](https://gradio.app)



\## 📌 项目简介



本项目是为汽车行业设计的\*\*智能售后问答助手\*\*，基于 \*\*RAG（检索增强生成）\*\* 和 \*\*Agent 智能体\*\*架构，能够回答故障码查询、保养建议、维修步骤等售后问题。系统采用 ReAct 模式的 Agent，实现“思考-行动-观察”的推理循环，并支持多轮对话记忆。



\*\*核心价值\*\*：解决传统汽车售后中用户查阅手册耗时、客服培训周期长的问题。



\### ✨ 核心功能

\- 🔍 \*\*故障码解析\*\*：输入 P0300 等故障码，返回含义和排查步骤

\- 📚 \*\*维修手册检索\*\*：基于 RAG 技术从手册中查找答案

\- 🔧 \*\*保养建议\*\*：根据里程提供保养周期建议

\- 📊 \*\*车型参数查询\*\*：查询深蓝 SL03、赛力斯 SF5 等参数

\- 💬 \*\*多轮对话\*\*：支持上下文记忆，连续提问



\## 🏗️ 技术架构



```



用户输入 → Agent(ReAct模式) → 工具调用决策 → 知识检索/API调用 → LLM生成 → 答案溯源

↓                            ↑

┌──────┴──────┐                     │

↓              ↓                     │

故障码API       向量数据库 ──────────────────┘

(ChromaDB)



```



\- \*\*LangChain\*\*：Agent 框架、工具调用、记忆管理

\- \*\*ChromaDB\*\*：向量存储，用于相似度检索

\- \*\*DeepSeek\*\*：对话模型（API 调用）

\- \*\*HuggingFace Embeddings\*\*：本地向量化模型（all-MiniLM-L6-v2）

\- \*\*Gradio\*\*：Web 界面



\## 🚀 快速开始



\### 环境要求

\- Python 3.11

\- DeepSeek API 密钥（\[注册地址](https://platform.deepseek.com/)）



\### 安装步骤



```bash

\# 克隆仓库

git clone https://github.com/你的用户名/auto-service-agent.git

cd auto-service-agent



\# 创建虚拟环境

python -m venv venv

source venv/bin/activate  # Linux/Mac

venv\\Scripts\\activate      # Windows



\# 安装依赖

pip install -r requirements.txt



\# 配置环境变量

cp .env.example .env

\# 编辑 .env 文件，填入你的 DeepSeek API 密钥

```



运行项目



```bash

python src/app.py

```



访问 http://localhost:7860 即可使用。



🧪 使用示例



问题 回答示例

"P0300故障码是什么意思？" 发动机缺火，可能原因：火花塞老化、点火线圈故障...

"5000公里该做什么保养？" 更换机油、机滤，检查轮胎气压...

"深蓝SL03的续航是多少？" 515km（CLTC工况）



🛠️ 核心技术实现



1\. RAG 检索增强生成



· 文档切片：chunk\_size=400, chunk\_overlap=40

· 向量检索：返回 Top-3 最相关文档

· 答案溯源：每个回答都标注信息来源



2\. Agent 智能体设计



采用 ReAct 模式，实现推理循环：



```

Thought: 用户问故障码，需要查工具

Action: 故障码查询

Observation: P0300表示发动机缺火

Thought: 还需要排查步骤，查知识库

...

```



3\. 多工具协同



· 故障码查询工具：解析 OBD 故障码

· 知识库检索工具：访问维修手册

· 保养建议工具：基于里程给出建议



📊 项目亮点



1\. 汽车行业适配：针对售后场景优化，支持故障码、保养等专业查询

2\. 答案可溯源：每个回答都引用知识库来源，增强可信度

3\. 多轮对话：使用 ConversationBufferMemory 保持上下文

4\. 工程落地：完整的错误处理、API 封装、Web 界面



🎯 岗位匹配



本项目针对赛力斯 AI 智能体开发工程师岗位要求设计，展示了：



JD要求 项目体现

智能 Agent 架构设计 ReAct 模式 Agent，多智能体协同

基于大模型构建业务级 Agent 汽车售后场景的完整实现

工具调用 故障码查询、保养建议等工具

知识库接入 RAG 技术接入维修手册

系统实现 Gradio Web 界面，可部署访问



📄 许可证



MIT License



🙏 致谢



· LangChain 社区提供的优秀框架

· DeepSeek 提供的 API 服务

· 赛力斯招聘 JD 提供的岗位需求参考

