- **LangChain**：Agent 框架、工具调用、记忆管理
- **ChromaDB**：向量存储，用于相似度检索
- **DeepSeek**：对话模型（API 调用）
- **HuggingFace Embeddings**：本地向量化模型（all-MiniLM-L6-v2）
- **Gradio**：Web 界面

## 🚀 快速开始

### 环境要求
- Python 3.11
- DeepSeek API 密钥（[注册地址](https://platform.deepseek.com/)）

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/你的用户名/auto-service-agent.git
cd auto-service-agent

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的 DeepSeek API 密钥