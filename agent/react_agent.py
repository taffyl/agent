from typing import Generator

from langchain.agents import create_agent
from model.factory import chat_model
from utils.prompt_loader import load_system_prompt, load_visualize_prompt

from agent.tools.agent_tools import rag_summarize, get_all_table_names, get_table_data, get_table_columns, query_database_tool
from agent.tools.visualize_tools import plot_two_list
from agent.tools.middleware import monitor_tool, log_before_model_call
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage



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
            tools = [get_all_table_names, get_table_columns, query_database_tool ,plot_two_list],
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
        
        for chunk in self.agent.stream(input_dict, stream_mode = "values", context = {"prompt": "system"}):
            lastest_message = chunk["messages"][-1]

            if isinstance(lastest_message, AIMessage):
                yield lastest_message.content
            elif isinstance(lastest_message, ToolMessage):
                if lastest_message.name == "plot_two_list":
                    yield lastest_message.content


agent = ReactAgent()

if __name__ == "__main__":
    for chunk in agent.execute_stream("我有鼠标五天的销量[2,2,4,3,3]，键盘5天的销量[7,1,2,3,3]，请帮我可视化"):
        print(chunk)

# 对[1,2,3,4,5],[1.8,3.3,2.1,3.4,5.2]进行可视化]
    
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