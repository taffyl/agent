from typing import Callable

from utils.logger_hander import logger
from utils.prompt_loader import load_system_prompt, load_visualize_prompt
from langchain.agents import AgentState
from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langchain.tools.tool_node import ToolCallRequest
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from langgraph.runtime import Runtime

@wrap_tool_call
def monitor_tool(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage | Command],
) -> ToolMessage | Command:
    """
    监控工具调用执行过程。

    该函数作为工具调用的入口点，接收工具调用请求，并通过指定的处理函数执行具体逻辑。
    通常用于拦截、记录或增强工具调用的行为。

    Args:
        request: 工具调用请求对象，包含调用所需的参数和上下文信息。
        handler: 实际执行工具逻辑的处理函数，接收 ToolCallRequest 并返回 ToolMessage 或 Command。

    Returns:
        工具执行结果，类型为 ToolMessage 或 Command。
    """
    logger.info(f"[工具调用]开始执行工具 {request.tool_call['name']}")
    logger.info(f"[工具调用]工具参数: {request.tool_call['args']}")
    
    try:
        # 执行工具逻辑
        result = handler(request)
        
        if request.tool_call["name"] == "call_data_visualize_agent":
            request.runtime.context["prompt"] = "visualize"
        
        return result
        
    except Exception as e:
        logger.error(f"[工具调用]工具执行出错: {e}")
        raise e

@before_model
def log_before_model_call(
    state: AgentState, 
    runtime: Runtime
) -> None:
    
    message_count = len(state['messages'])
    messages_type_name = type(state['messages']).__name__
    
    if message_count == 0:
        print(state)
        raise Exception("[工具调用]消息列表为空")
    
    logger.info(f"[模型调用]开始执行模型，带有 {message_count} 条消息")
    logger.info(f"[模型调用]消息内容: {messages_type_name}:{state['messages']}")
    
    return None

@dynamic_prompt
def report_prompt_switch(request: ModelRequest):
    p = request.runtime.context.get("report", "system")
    if p == "visualize":
        logger.info("[模型调用]使用visualize提示语")
        return load_visualize_prompt()
    elif p == "system":
        return load_system_prompt()

