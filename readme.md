这是一个基于 **LangChain**、**FastAPI** 和 **React Agent** 架构的商业数据库管理智能体项目。该项目结合了 RAG（检索增强生成）技术，能够理解自然语言指令，执行数据库查询、数据分析及可视化操作，并通过流式接口向前端提供实时响应。

以下是为您生成的 `README.md` 内容：

---

# 🍀 AI Database Agent (商业数据库智能管理助手)

一个基于 ReAct (Reasoning + Acting) 模式的智能体系统，旨在通过自然语言交互实现商业数据库的自动化管理、数据查询、RAG 知识问答及数据可视化。

## ✨ 核心功能

- **🗣️ 自然语言交互**：用户可通过聊天界面直接询问数据库内容，无需编写 SQL。
- **📊 智能数据可视化**：支持根据查询结果自动生成折线图、直方图等图表，并在前端实时展示。
- **🧠 RAG 知识库问答**：集成 ChromaDB 向量数据库，支持对上传的 PDF/TXT 文档进行语义检索和总结。
- **⚡ 流式响应 (SSE)**：后端采用 Server-Sent Events 技术，实现打字机效果的实时消息推送。
- **🛡️ 安全与监控**：内置中间件监控工具调用过程，支持权限控制配置。

## 🏗️ 技术栈

- **后端框架**: FastAPI, Uvicorn
- **AI 框架**: LangChain, LangGraph
- **大模型**: OpenAI 兼容接口 (默认配置为 Qwen3-14B via RinkoAI)
- **向量数据库**: ChromaDB
- **关系型数据库**: MySQL (PyMySQL driver)
- **前端**: HTML5, CSS3, JavaScript (Vanilla JS), Marked.js (Markdown 渲染)
- **可视化**: Matplotlib (后端绘图)

## 📂 项目结构

```text
.
├── agent/                  # 智能体核心逻辑
│   ├── tools/              # 工具集
│   │   ├── agent_tools.py  # 数据库查询、RAG调用等工具
│   │   ├── visualize_tools.py # Matplotlib 绘图工具
│   │   └── middleware.py   # 工具调用监控与动态 Prompt 切换
│   ├── react_agent.py      # 主 React Agent 实现
│   └── visualize_agent.py  # 专用可视化 Agent
├── api/                    # API 接口层
│   └── agent_api_handler.py # SSE 流式处理逻辑
├── app/                    # Web 应用入口
│   ├── static/             # 前端静态资源 (HTML/CSS/JS)
│   └── main.py             # FastAPI 启动文件
├── config/                 # 配置文件 (YAML)
│   ├── database.yml        # 数据库连接配置
│   ├── rag.yml             # LLM 与 Embedding 模型配置
│   └── prompts.yml         # Prompt 模板路径配置
├── data/                   # RAG 知识库源文件目录
├── img/                    # 生成的可视化图片存储目录
├── logs/                   # 日志文件目录
├── model/                  # 模型工厂 (Model Factory)
├── rag/                    # RAG 服务实现
│   ├── rag_service.py      # 检索与总结链
│   └── vector_store.py     # ChromaDB 向量存储管理
├── utils/                  # 通用工具类
│   ├── config_hander.py    # 配置加载器
│   ├── file_handler.py     # 文件处理 (MD5计算, 加载器)
│   ├── logger_hander.py    # 日志记录器
│   └── path_tool.py        # 路径处理工具
└── requirements.txt        # (建议补充) 依赖列表
```

## 🚀 快速开始

### 1. 环境准备

确保已安装 Python 3.9+ 和 MySQL 数据库。

### 2. 安装依赖

```bash
pip install fastapi uvicorn langchain langchain-openai langchain-chroma pymysql pyyaml matplotlib python-dotenv
# 其他可能需要的依赖根据实际运行情况补充
```

### 3. 配置环境变量

在项目根目录创建 `.env` 文件，配置 API Key：

```env
OPENAI_API_KEY=your_api_key_here
```

### 4. 修改配置文件

编辑 `config/database.yml` 以匹配你的 MySQL 数据库信息：

```yaml
driver: "mysql+pymysql"
username: "root"
password: "your_password"
host: "localhost"
port: 3306
database_name: "trade_db"
```

编辑 `config/rag.yml` 确认模型服务商地址：

```yaml
base_url: https://rinkoai.com/v1
chat_model_name: Qwen/Qwen3-14B
```

### 5. 初始化知识库 (可选)

将需要检索的 [.txt](file://e:\github\ai\md5_hex.txt) 或 `.pdf` 文件放入 `data/` 目录，然后运行以下命令初始化向量库：

```bash
python rag/vector_store.py
```

### 6. 启动服务

```bash
python app/main.py
```

服务将在 `http://127.0.0.1:8000` 启动。
访问 `http://127.0.0.1:8000/static/index.html` 即可使用聊天界面。

## 💡 使用示例

### 1. 数据库查询
> **用户**: "交易表里有哪些数据？"
> **Agent**: 自动调用 [get_all_table_names](file://e:\github\ai\database.py#L30-L31) -> [query_database_tool](file://e:\github\ai\agent\tools\agent_tools.py#L67-L68)，返回前几条交易记录。

### 2. 数据可视化
> **用户**: "帮我画出鼠标和键盘最近5天的销量对比图。"
> **Agent**:
> 1. 查询相关销量数据。
> 2. 调用 [plot_two_list](file://e:\github\ai\agent\tools\visualize_tools.py#L39-L105) 生成折线图并保存至 `img/`。
> 3. 调用 [call_data_visualize_agent](file://e:\github\ai\agent\tools\agent_tools.py#L26-L39) 获取图片 Markdown 链接。
> 4. 前端自动渲染图片。

### 3. 知识库问答
> **用户**: "什么是关系型数据库？"
> **Agent**: 从 `data/数据库.txt` 中检索相关内容，结合 LLM 生成总结回答。

## ⚙️ 高级配置

### Prompt 管理
所有 System Prompt 均存储在 `prompts/` 目录下，可通过 `config/prompts.yml` 切换不同场景的提示词（如 `system_prompt`, `visualize_prompt`）。

### 日志查看
运行日志保存在 `logs/` 目录下，格式为 `agent_YYYYMMDD.log`，可用于排查工具调用错误。

## 📝 注意事项

1. **图片路径**: 确保 `app/main.py` 中挂载的 `/img` 静态目录权限正确，以便前端能访问生成的图表。
2. **字体支持**: [visualize_tools.py](file://e:\github\ai\agent\tools\visualize_tools.py) 中设置了中文字体 (`SimHei`, `Microsoft YaHei`)，请确保运行环境已安装这些字体，否则图表中文可能显示为方块。
3. **安全性**: 生产环境中请修改 `app/main.py` 中的 CORS 配置，限制 `allow_origins`。

## 📄 License

MIT License