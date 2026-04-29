import os
import hashlib

from utils.logger_hander import logger

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader

def get_file_md5_hex(filepath: str):
    """
    计算指定文件的 MD5 哈希值，并返回其十六进制字符串表示。

    该函数通过分块读取文件的方式处理大文件，避免内存溢出。
    如果文件不存在、路径不是文件或计算过程中发生异常，将记录错误日志并返回 None。

    Args:
        filepath (str): 需要计算 MD5 的文件完整路径。

    Returns:
        str: 文件的 MD5 十六进制字符串，若出错则返回 None。
    """
    
    
    # 1. 前置校验：检查文件路径是否存在
    if not os.path.exists(filepath):
        logger.error(f"[md5计算]文件 {filepath} 不存在")
        return None
    
    
    # 2. 前置校验：确保路径指向的是一个普通文件，而非目录或其他特殊文件
    if not os.path.isfile(filepath):
        logger.error(f"[md5计算]路径 {filepath} 不是文件")
        return None
    
    md5_obj = hashlib.md5()
    
    chunk_size = 4096    # 4KB分片，防止文件过大
    
    try:
        with open(filepath, "rb") as f:          # 打开文件，rb模式
            while chunk := f.read(chunk_size):   # 逐块读取文件，若为空则停止循环
                md5_obj.update(chunk)            # 将当前读取的数据块更新到 MD5 哈希对象中
            
            # 所有数据块读取完毕后，获取最终的 MD5 哈希值的十六进制表示
            md5_hex = md5_obj.hexdigest()
            
            return md5_hex
    except Exception as e:
        logger.error(f"计算文件 {filepath} MD5失败: {e}")
        return None


def listdir_with_allowed_types(path: str, allowed_types: list) -> list:
    """列出指定目录下的所有文件，并筛选出指定类型的文件

    Args:
        path (str): 需要遍历的目录路径
        allowed_types (list): 允许的文件后缀名列表

    Returns:
        list: 匹配指定类型的文件完整路径列表（注：实际返回类型为 tuple）
    """
    files = []
    
    # 校验路径是否为有效目录，若无效则记录错误并返回
    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_types] {path} 不是一个目录")
        return allowed_types
    
    # 遍历目录内容，筛选符合后缀要求的文件并构建完整路径
    for f in os.listdir(path):
        if f.endswith(allowed_types):
            files.append(os.path.join(path, f))
            
    return tuple(files)

def pdf_loader(file_path: str, passwd: str = None) -> list[Document]:
    """
    PDF文件加载器
    """
    PDFfile = PyPDFLoader(file_path, passwd).load()
    return PDFfile

def txt_loader(file_path: str) -> list[Document]:
    """
    txt文件加载器
    """
    txtfile = TextLoader(file_path, encoding = "utf-8").load()
    return txtfile