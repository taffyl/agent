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

    def execute_stream(self, data_json: str) -> Generator[str]:
        input_dict = {
            "messages": [
                    {
                    "role": "user",
                    "content": f"对给你的数据进行可视化{data_json}"
                    },
                ]
            }
        
        print(input_dict)
        
        for chunk in self.agent.stream(input_dict, stream_mode = "values"):
            lastest_message = chunk["messages"][-1]

            if type(lastest_message) is AIMessage:
                yield lastest_message.content.strip() + "\n"
