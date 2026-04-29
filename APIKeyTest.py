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
        "content": "你是一个医疗顾问，需要用严谨的医疗知识回答下面问题："
    },
    
    {
        "role": "user", 
        "content": "我最近三天一直头痛，该怎么办？"
    },
]
)
print("\n")
print(completion.model_dump_json())
print("\n")
