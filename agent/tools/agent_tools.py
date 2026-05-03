from langchain_core.tools import tool
from rag.rag_service import RagSummarizeService
from utils.table_data import TableData
import database
from typing import Generator

from agent.react_agent import VisualizeAgent

from sqlalchemy import String, Integer, Float, Row
from sqlalchemy.orm import DeclarativeBase


rag = RagSummarizeService()

@tool(description = "这个工具用于调用数据库操作智能体，该智能体可以进行增删改查等操作")
def call_db_operation_agent() -> None:
    pass

@tool(description = "这个工具用于调用数据可视化智能体，该智能体可以进行数据可视化")
def call_data_visualize_agent(data) -> Generator[str, None, None]:
    agent = VisualizeAgent()
    for chunk in agent.execute_stream(data):
        yield chunk
    

@tool(description = "这个工具用于调用网络爬虫智能体，该智能体可以在网上爬取需要的数据")
def call_web_crawler_agent() -> None:
    pass

@tool(description = "这个工具用于从向量存储中检索参考资料")
def rag_summarize(query: str) -> str:
    return rag.rag_summary(query)

@tool(description = "这个工具用于获取数据库中所有表名")
def get_all_table_names() -> list[str]:
    return database.get_all_table_names()

@tool(description = "这个工具用于获取指定表中的数据，如果超过5条，则只获取前5条")
def get_table_data(table_name: str) -> list[Row]:
    print("_____________________________________test_____________________________________")
    return database.get_table_data(table_name)

# @tool(description = "这个工具用于打印数据")
# def print_table_data(data_list: list[Row]) -> None:
#     for row in data_list:
#         print(row)

@tool(description="这个工具用于对两列数据进行可视化，并将结果保存为图片文件")
def plot_two_list(list_1: list[float], list_2: list[float]) -> str:
    """
    对两列数据进行可视化，保存为临时图片文件，并返回文件路径。
    
    Args:
        list_1: 第一列数据
        list_2: 第二列数据
        
    Returns:
        str: 生成的图片文件路径
    """
    import matplotlib
    # 关键修复：设置非交互式后端 'Agg'，避免在主线程外启动 GUI 的警告和错误
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import os
    import tempfile

    # 1. 输入验证
    if not list_1 or not list_2:
        raise ValueError("输入列表不能为空")
    
    if len(list_1) != len(list_2):
        raise ValueError(f"两个列表长度必须一致，当前长度分别为 {len(list_1)} 和 {len(list_2)}")

    try:
        # 2. 创建图形
        plt.figure()
        plt.plot(list_1, label='List 1')
        plt.plot(list_2, label='List 2')
        plt.title('Visualization of Two Lists')
        plt.xlabel('Index')
        plt.ylabel('Value')
        plt.legend()
        
        # 3. 保存图像到临时文件
        # 创建临时文件，后缀为 .png
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
            temp_path = tmp_file.name
        
        # 保存图形到该路径
        plt.savefig(temp_path, format='png', bbox_inches='tight')
        
        # 4. 清理资源：关闭图形以防止内存泄漏
        plt.close()
        
        return temp_path
        
    except Exception as e:
        # 确保发生异常时也关闭图形
        plt.close()
        raise RuntimeError(f"绘图失败: {str(e)}")
    
    # 4. 清理资源：关闭图形以防止内存泄漏，特别是在多次调用时




