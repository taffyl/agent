import os
from openai import OpenAI

client = OpenAI(
    # API_KEY已配置于环境变量中
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    model = "qwen3.5-plus",
messages = [
    {
        "role": "system", 
        "content": "用户正在运行一个API测试程序，如果你接收到了用户内容，请告诉用户API正常"
    },
    
    {
        "role": "user", 
        "content": "你好"
    },
]
)
print("\n")
print(completion.model_dump_json())
print("\n")
