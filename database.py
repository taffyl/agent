import os
from sqlalchemy import create_engine, inspect, Table, Row
from sqlalchemy.orm import declarative_base, sessionmaker

from utils.config_hander import database_conf
from utils.logger_hander import logger

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    
    f"{database_conf['driver']}://"
    f"{database_conf['username']}:{database_conf['password']}@"
    f"{database_conf['host']}:{database_conf['port']}/"
    f"{database_conf['database_name']}?"
    f"charset={database_conf['charset']}",
)

#print(DATABASE_URL)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
Base = declarative_base()

trades = Table("trades", Base.metadata, autoload_with=engine)


def get_all_table_names() -> list[str]:
    return inspect(engine).get_table_names()

def get_table_data(table_name: str) -> list[Row]:
    with engine.connect() as conn:
        
        data_list = []
        query = trades.select().limit(5)
        result = conn.execute(query)
        logger.info(f"[数据库] 在表 {table_name} 中查询数据成功")
        for row in result:
            data_list.append(row)

        return data_list


def get_table_columns(table_name: str) -> list[str]:
    """
    获取指定表中的所有字段名（列名）。
    
    Args:
        table_name: 数据库表名
        
    Returns:
        list[str]: 包含所有列名的列表
    """
    try:
        # 使用 inspect 获取表的元数据
        inspector = inspect(engine)
        
        # 检查表是否存在
        if table_name not in inspector.get_table_names():
            raise ValueError(f"表 '{table_name}' 不存在")
        
        # 获取列信息，每个元素是一个字典，包含 'name', 'type', 'nullable' 等键
        columns = inspector.get_columns(table_name)
        
        # 提取列名
        column_names = [col['name'] for col in columns]
        
        logger.info(f"[数据库] 成功获取表 '{table_name}' 的字段，共 {len(column_names)} 个")
        return column_names
        
    except Exception as e:
        logger.error(f"[数据库] 获取表 '{table_name}' 字段失败: {str(e)}")
        raise RuntimeError(f"获取表字段失败: {str(e)}")
    
    
def query_table_data(table_name: str, columns: list[str] = None, limit: int = 50) -> list[dict]:
    """
    根据表名和指定字段精确查询数据。
    
    Args:
        table_name: 数据库表名
        columns: 需要查询的字段列表。如果为 None 或空，则查询所有字段。
        limit: 限制返回的行数，默认为 50，防止数据量过大。
        
    Returns:
        list[dict]: 包含查询结果的字典列表，每个字典代表一行数据 {column_name: value}
    """
    from sqlalchemy import MetaData, select
    
    try:
        # 1. 验证表是否存在
        inspector = inspect(engine)
        if table_name not in inspector.get_table_names():
            raise ValueError(f"表 '{table_name}' 不存在")
        
        # 2. 动态反射表对象
        metadata = MetaData()
        # autoload_with 会自动从数据库加载表结构
        dynamic_table = Table(table_name, metadata, autoload_with=engine)
        
        # 3. 确定查询字段
        available_columns = [c.name for c in dynamic_table.columns]
        
        if not columns:
            # 如果未指定字段，默认查询所有字段
            selected_cols = dynamic_table.columns
        else:
            # 验证字段是否存在
            invalid_cols = [col for col in columns if col not in available_columns]
            if invalid_cols:
                raise ValueError(f"以下字段在表 '{table_name}' 中不存在: {invalid_cols}")
            
            # 获取对应的列对象
            selected_cols = [dynamic_table.c[col] for col in columns]

        # 4. 构建并执行查询
        query = select(*selected_cols).limit(limit)
        
        with engine.connect() as conn:
            result = conn.execute(query)
            
            # 5. 处理结果
            data_list = []
            keys = result.keys() # 获取列名
            
            for row in result:
                # 将 Row 元组转换为字典
                row_dict = dict(zip(keys, row))
                
                # 简单序列化处理：将 datetime 等对象转为字符串
                serialized_row = {}
                for k, v in row_dict.items():
                    if hasattr(v, 'isoformat'): # 处理 date/datetime
                        serialized_row[k] = v.isoformat()
                    elif isinstance(v, bytes): # 处理 bytes
                        serialized_row[k] = v.decode('utf-8', errors='ignore')
                    else:
                        serialized_row[k] = v
                
                data_list.append(serialized_row)
                
        logger.info(f"[数据库] 成功从表 '{table_name}' 查询 {len(data_list)} 条数据")
        return data_list
        
    except Exception as e:
        logger.error(f"[数据库] 查询表 '{table_name}' 数据失败: {str(e)}")
        raise RuntimeError(f"查询数据失败: {str(e)}")
# if __name__ == "__main__":
#     a = get_table_data("trades")
#     print(a)