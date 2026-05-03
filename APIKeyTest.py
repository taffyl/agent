import os
from openai import OpenAI

client = OpenAI(
    # API_KEY已配置于环境变量中
    base_url = "https://rinkoai.com/v1",
)


try:
    models = client.models.list()
    print("支持的模型列表:")
    for model in models.data:
        print(model.id)
except Exception as e:
    print(f"获取模型列表失败: {e}")


completion = client.chat.completions.create(

    model= "Qwen/Qwen3-14B",

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
