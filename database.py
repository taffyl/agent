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


    
# if __name__ == "__main__":
#     a = get_table_data("trades")
#     print(a)