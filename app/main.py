from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles  # 新增导入
from fastapi.middleware.cors import CORSMiddleware  # 新增导入
from pydantic import BaseModel
from api.agent_api_handler import user_input_stream
from utils.logger_hander import logger
from utils.path_tool import get_abs_path
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

app.mount("/static", StaticFiles(directory = get_abs_path("app\static")), name = "static")
    # 访问 http://127.0.0.1:8000/static/index.html

app.mount("/img", StaticFiles(directory = get_abs_path("img")), name = "img")

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