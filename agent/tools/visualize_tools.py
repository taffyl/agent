import glob
from langchain_core.tools import tool
from rag.rag_service import RagSummarizeService

from utils.table_data import TableData
from utils.path_tool import get_abs_path
from utils.logger_hander import logger

import time
import database
from typing import Generator
import json
import matplotlib.pyplot as plt
import os
import tempfile
from matplotlib import use as plt_use

#from agent.react_agent import VisualizeAgent

from sqlalchemy import String, Integer, Float, Row
from sqlalchemy.orm import DeclarativeBase


plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

def to_frontend() -> str:
    img_dir = get_abs_path("img")
    list_of_files = glob.glob(os.path.join(img_dir, '*.png'))
    latest_file = max(list_of_files, key=os.path.getmtime)
    
    # 构建相对路径 (假设前端通过 /static/img 或类似方式访问，或者直接返回相对路径由前端拼接)
    # 这里我们返回 Markdown 格式，方便 marked.js 直接解析
    # 注意：需要确保后端静态文件服务配置了 /img 目录的访问权限
    filename = os.path.basename(latest_file)
    relative_path = f"/../img/{filename}"
    return f"![数据可视化结果]({relative_path})"

@tool(description="这个工具用于对index和n组value数据进行可视化，绘制n组折线图，并将结果保存为图片文件")
def plot_two_list(index: list[float] = [],
                  value: list[list[float]] | list[float] = [],
                  title: str = "default_title",
                  label: list[str] = []
) -> str:
    """
    对n列数据进行可视化，保存为临时图片文件，并返回文件路径。
    """


    # 设置非交互式后端 'Agg'，避免在主线程外启动 GUI 的警告和错误
    plt_use('Agg')

    
    img_dir = get_abs_path("img")
    
    n = len(value)
    
    if not isinstance(value[0], list): # 兼容单组数据
        value = [value]
    
    if index == []:
        index = [i for i in range(len(value[0]))]
        logger.info("[plot_two_list] index 为空，已自动生成索引")
        
    if label == []:
        label = [f"value_{i}" for i in range(n)]
        logger.info("[plot_two_list] label 为空，已自动生成标签")
        
    # 1. 输入验证
    if not index or not value:
        logger.error("[plot_two_list] 输入列表不能为空")
        return "数据可视化失败，error: 输入列表不能为空"
    
    if len(index) != len(value[0]):
        logger.error(f"[plot_two_list] 两个列表长度必须一致，当前长度分别为 {len(index)} 和 {len(value[0])}")
        return False
    try:
        # 2. 创建图形
        plt.figure()
        
        for i in range(n):
            plt.plot(index, value[i], label=label[i])
        
        plt.title(title)
        plt.xlabel('Index')
        plt.ylabel('Value')
        plt.legend()

        # 3. 保存图像到临时文件
        # 创建临时文件，后缀为 .png
        timestamp = int(time.time() * 1000) # 使用毫秒级时间戳避免冲突
        filename = f"plot_{timestamp}.png"
        full_path = os.path.join(img_dir, filename)
        
        # 保存图形到该路径
        plt.savefig(full_path, format='png', bbox_inches='tight')
        
        # 4. 清理资源：关闭图形以防止内存泄漏
        plt.close()
        
        return to_frontend()
        
    except Exception as e:
        # 确保发生异常时也关闭图形
        plt.close()
        return f"数据可视化失败，error: {str(e)}，请咨询管理员"

@tool(description="这个工具用于对单列数据进行直方图可视化，并将结果保存为图片文件")
def plot_histogram(data: list[float], bins: int = 10, title: str = "Histogram") -> bool:
    """
    对单列数据进行直方图可视化，保存为图片文件至 img 目录，并返回文件路径。
    
    Args:
        data: 需要绘制直方图的数据列表
        bins: 直方图的柱状数量，默认为 10
        title: 图表标题，默认为 "Histogram"
        
    Returns:
        str: 生成的图片文件相对路径 (例如: img/hist_123456.png)
    """
    if not data:
        logger.error("数据列表不能为空")
    
    if not isinstance(bins, int) or bins <= 0:
        raise ValueError("bins 必须为正整数")

    # 2. 定义保存路径
    img_dir = get_abs_path("img")
    
    # 确保 img 目录存在
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    try:
        # 3. 创建图形
        plt.figure()
        # 绘制直方图
        plt.hist(data, bins=bins, color='skyblue', edgecolor='black')
        plt.title(title)
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        
        # 4. 生成唯一文件名
        timestamp = int(time.time() * 1000) # 使用毫秒级时间戳避免冲突
        filename = f"hist_{timestamp}.png"
        full_path = os.path.join(img_dir, filename)
        
        # 5. 保存图像
        plt.savefig(full_path, format='png', bbox_inches='tight')
        
        # 6. 清理资源：关闭图形以防止内存泄漏
        plt.close()
        
        return to_frontend()
        
    except Exception as e:
        # 确保发生异常时也关闭图形
        plt.close()
        return False

# if __name__ == "__main__":
#     plot_two_list([1, 2, 3, 4, 5], [6, 7, 8, 9, 10])