import datetime
import os
from utils.path_tool import get_abs_path
import logging

# 日志目录
LOG_ROOT = get_abs_path("logs")

# 确保日志的目录存在
os.makedirs(LOG_ROOT, exist_ok=True)

# 日志格式配置
DEFAULT_LOG_FORMAT = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)


# 获取日志
def get_logger(
    name: str = "agent",
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG,
    log_file=None,
) -> logging.Logger:
    """
    获取日志
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 避免重复添加Handler
    if logger.handlers:
        return logger

    # 控制台Handler
    console_hander = logging.StreamHandler()
    console_hander.setLevel(console_level)
    console_hander.setFormatter(DEFAULT_LOG_FORMAT)

    logger.addHandler(console_hander)

    # 文件Handler
    if not log_file:
        # 配置日志文件存放路径以及文件名称
        log_file = os.path.join(
            LOG_ROOT, f"{name}_{datetime.datetime.now().strftime('%Y%m%d')}.log"
        )
    print(f"log_file:[{log_file}]")
    
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)

    logger.addHandler(file_handler)

    return logger


# 快捷获取日志
logger = get_logger()

if __name__ == "__main__":
    logger.warning("test")
    logger.warning("test2")
    
