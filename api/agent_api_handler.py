import json
from typing import Generator
from agent.react_agent import ReactAgent  
from utils.logger_hander import logger

agent = ReactAgent()

def format_sse(data: str) -> str:
    """
    将数据格式化为 SSE (Server-Sent Events) 标准格式
    """
    return f"data: {data}\n\n"

def user_input_stream(prompt: str) -> Generator[str, None, None]:
    """
    改造后的流式输入处理函数
    :param prompt: 用户输入
    :return: 生成器，产出 SSE 格式的字符串
    """
    
    logger.info(f"[user_input_stream] 开始调用Agent智能体")
    
    try:
        for chunk in agent.execute_stream(prompt):
            if chunk:
                #  yield SSE 格式数据
                # 如果前端需要 JSON 对象，可以这样写:
                # payload = json.dumps({"content": chunk}, ensure_ascii=False)
                # yield format_sse(payload)
                
                # 如果前端只需要纯文本流（类似大多数简单实现）:
                yield format_sse(chunk)
                
    except Exception as e:
        # 发生错误时，发送错误信息给前端
        error_payload = json.dumps({"error": str(e)}, ensure_ascii=False)
        yield format_sse(error_payload)
    
    finally:
        # 发送结束标记，方便前端判断流结束
        yield format_sse("[DONE]")
        
        
if __name__ == "__main__":
    """
    本地测试入口
    运行命令: python e:\github\ai\api\agent_api_handler.py
    """
    import time
    
    # 1. 定义测试问题
    test_prompt = "告诉我交易表里有哪些数据"
    
    print(f"--- 开始测试流式输出 (Prompt: {test_prompt}) ---")
    start_time = time.time()
    
    try:
        # 2. 获取生成器
        stream = user_input_stream(test_prompt)
        
        # 3. 模拟前端接收并解析 SSE 数据
        for sse_data in stream:
            # sse_data 格式为: "data: content\n\n"s
            # 这里我们简单地去掉前缀和后缀，还原出原始内容用于打印
            if sse_data.startswith("data: "):
                print(sse_data, end="*****test*****", flush=True)
                content = sse_data[6:].strip() # 去掉 "data: " 和末尾换行
                
                if content == "[DONE]":
                    print("\n--- [DONE] 流结束 ---")
                else:
                    # 使用 end="" 实现打字机效果
                    print(content, end="*****test*****", flush=True)
                    
    except Exception as e:
        print(f"\n测试过程中发生错误: {e}")
        
    end_time = time.time()
    logger.info(f"[user_input_stream] 调用完成，共耗时: {end_time - start_time:.2f} 秒")