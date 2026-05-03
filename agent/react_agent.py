from typing import Generator

from langchain.agents import create_agent
from model.factory import chat_model
from utils.prompt_loader import load_system_prompt, load_visualize_prompt

from agent.tools.agent_tools import rag_summarize, get_all_table_names, get_table_data, plot_two_list, call_data_visualize_agent
from agent.tools.middleware import monitor_tool, log_before_model_call
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

class VisualizeAgent(object):
    def __init__(self):
        self.agent = create_agent(
            model = chat_model,
            system_prompt = load_visualize_prompt(),
            tools = [plot_two_list],
            middleware = [monitor_tool, log_before_model_call] 
        )
        
    def execute_stream(self, data) -> Generator[str]:
        input_dict = {
            "messages": [
                    {
                    "role": "user",
                    "content": f"对给你的数据进行可视化{data}"
                    },
                ]
            }
        
        print(input_dict)
        
        for chunk in self.agent.stream(input_dict, stream_mode = "values"):
            lastest_message = chunk["messages"][-1]

            if type(lastest_message) is AIMessage:
                yield lastest_message.content.strip() + "\n"


class ReactAgent(object):
    def __init__(self):
        
        """
        初始化实例，创建并配置智能体（Agent）。

        该构造函数通过调用 create_agent 函数来初始化 self.agent 属性。
        配置包括指定聊天模型、系统提示词、可用的工具列表以及中间件处理链。
        """
        
        self.agent = create_agent(
            model = chat_model,
            system_prompt = load_system_prompt(),
            tools = [get_all_table_names, get_table_data, call_data_visualize_agent],
            middleware = [monitor_tool, log_before_model_call] 
        )
        
    def execute_stream(self, query: str) -> Generator[str]:
        
        input_dict = {
            "messages": [
                    {
                    "data":{
                        "user_authority": "read"
                    },
                    "role": "user",
                    "content": query
                    },
                ]
            }
        
        print(input_dict)
        
        for chunk in self.agent.stream(input_dict, stream_mode = "values"):
            lastest_message = chunk["messages"][-1]

            if type(lastest_message) is AIMessage:
                yield lastest_message.content.strip() + "\n"

agent = ReactAgent()



if __name__ == "__main__":
    agent = VisualizeAgent()
    for chunk in agent.execute_stream("data"):
        print(chunk, end = "", flush = True)
    
    # agent = create_agent(
    #         model = chat_model,
    #         system_prompt = load_system_prompt(),
    #         tools = [rag_summarize, get_all_table_names, get_table_data],
    #         middleware = [monitor_tool, log_before_model_call] 
    #     )
    
    # input_dict = {
    #         "messages": [
    #                 {
    #                 "role": "user",
    #                 "content": "获取数据库中所有表名"
    #                 },
    #             ]
    #         }
    
    # agent.invoke(input_dict)
    
    # print(agent)