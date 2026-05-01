from langchain_core.tools import tool
from rag.rag_service import RagSummarizeService
from utils.table_data import TableData

from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import DeclarativeBase


rag = RagSummarizeService()

@tool(description = "这个工具用于从向量存储中检索参考资料")
def rag_summarize(query: str) -> str:
    return rag.rag_summary(query)

@tool(description = "这个工具用于获取数据库中所有表名")
def get_table_name() -> list[str]:
    pass

@tool(description = "这个工具用于获取指定表中的数据，如果超过20条，则只获取前二十条")
def get_table_data(table_name: str) -> list[TableData]:
    pass