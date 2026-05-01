# test_db_connection.py
import pymysql
import os
from utils.config_hander import database_conf

def test_mysql_connection():

    try:
        # 直接使用pymysql测试连接
        connection = pymysql.connect(
            host = database_conf["host"],
            user = database_conf["username"],
            password = database_conf["password"],
            port = database_conf["port"],
        )
        
        
        print("INFO MySQL服务器连接成功")
        
        # 检查数据库是否存在
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        db_names = [db[0] for db in databases]
        
        print(f"INFO 可用数据库: {db_names}")
        
        if 'langchain_app' in db_names:
            print("INFO 数据库 'langchain_app' 存在")
        else:
            print("ERROR 数据库 'langchain_app' 不存在")
            print("请创建数据库: CREATE DATABASE langchain_app CHARACTER SET utf8mb4;")
        
        connection.close()
        return True
        
    except pymysql.err.OperationalError as e:
        print(f"ERROR 连接失败: {e}")
        print("可能的原因:")
        print("1. MySQL服务没有运行")
        print("2. 用户名/密码错误")
        print("3. 主机/端口错误")
        return False
    except Exception as e:
        print(f"ERROR 其他错误: {e}")
        return False

if __name__ == "__main__":
    test_mysql_connection()
    