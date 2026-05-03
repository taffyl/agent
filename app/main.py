from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles  # 新增导入
from fastapi.middleware.cors import CORSMiddleware  # 新增导入
from pydantic import BaseModel
from api.agent_api_handler import user_input_stream
from utils.logger_hander import logger
import os

# 初始化 FastAPI 应用
app = FastAPI(
    title="AI Agent Chat API",
    description="基于 React Agent 的流式对话接口",
    version="1.0.0"
)

# 1. 配置 CORS (允许前端访问)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境建议指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. 挂载静态文件目录
# 假设 static 文件夹在 app 目录下
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    # 你也可以选择将根路径指向 index.html，但这通常需要更复杂的路由处理
    # 简单起见，你可以访问 http://127.0.0.1:8000/static/index.html

# ... 其余代码保持不变 ...

# 定义请求体模型
class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    if not request.prompt or not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    logger.info(f"收到流式请求: {request.prompt[:50]}...")

    return StreamingResponse(
        user_input_stream(request.prompt),
        media_type="text/event-stream"
    )

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)