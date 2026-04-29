import os

from langchain_core.documents import Document
from langchain_chroma import Chroma

from utils.config_hander import chroma_conf
from utils.path_tool import get_abs_path
from utils.file_handler import pdf_loader, txt_loader, listdir_with_allowed_types, get_file_md5_hex
from utils.logger_hander import logger

from model.factory import embedding_model
from langchain_text_splitters import RecursiveCharacterTextSplitter

class VectorStoreService(object):
        def __init__(self) -> None:
            """
            初始化向量存储和文本分割器。
    
            使用 Chroma 作为向量数据库，配置集合名称、嵌入函数和持久化目录。
            使用 RecursiveCharacterTextSplitter 进行文本分块，配置块大小、重叠部分、分隔符和长度计算函数。
            """
            self.vector_store = Chroma(
                collection_name = chroma_conf["collection_name"],
                embedding_function = embedding_model,
                persist_directory = chroma_conf["persist_directory"]
            )
            
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size = chroma_conf["chunk_size"],
                chunk_overlap = chroma_conf["chunk_overlap"],
                separators = chroma_conf["separators"],
                length_function = len,
            )
            
        def get_retriever(self) -> Chroma:
            """
            获取向量存储的检索器。

            Returns:
                Chroma: 配置了搜索参数（如返回结果数量 k）的检索器对象。
            """
            return self.vector_store.as_retriever(search_kwargs = {"k": chroma_conf["k"]})
            
        def load_documents(self) -> list[Document]:
            """
            从数据文件夹中加载文件，转为向量存入向量库中
            要计算文件的MD5值做去重

            Args:
                file_path (str): 要加载的文件路径。

            Returns:
                List[Document]: 加载并处理后的文档列表。
            """
            def check_md5_hex(md5_for_check: str):
                """
                检查给定的 MD5 哈希值是否已存在于存储文件中，用于去重判断。

                Args:
                    md5_for_check (str): 需要检查的文件 MD5 哈希值。

                Returns:
                    bool: 如果 MD5 存在则返回 True，否则返回 False。
                """
                if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                    # 创建文件
                    open(get_abs_path(chroma_conf["md5_hex_store"]), "w", encoding = "utf-8").close()
                    return False
                
                with open(get_abs_path(chroma_conf["md5_hex_store"]), "r", encoding = "utf-8") as f:
                    for line in f.readlines():
                        line = line.strip()
                        if line == md5_for_check:
                            return True
        
            def save_md5_hex(md5_for_check: str):
                """
                将文件的 MD5 哈希值保存到存储文件中，用于记录已处理的文件。

                Args:
                md5_for_check (str): 需要保存的文件 MD5 哈希值。
                """
                with open(get_abs_path(chroma_conf["md5_hex_store"]), "a", encoding = "utf-8") as f:
                    f.write(md5_for_check + "\n")
                
            def get_file_docments(file_path: str) -> list[str]:
                """
                根据文件扩展名加载文件内容。

                支持 .txt 和 .pdf 格式的文件加载。

                Args:
                    file_path (str): 文件路径。

                Returns:
                    List[str]: 加载后的文件内容列表。如果不支持该格式，返回空列表。
                """
                if file_path.endswith(".txt"):
                    return txt_loader(file_path)
            
                if file_path.endswith(".pdf"):
                    return pdf_loader(file_path)
            
                return []

            allowed_files_path: list[str] = listdir_with_allowed_types(
                get_abs_path(chroma_conf["data_path"]),
                tuple(chroma_conf["allowed_knowledge_file_type"])
                )

            for path in allowed_files_path:
                md5_hex = get_file_md5_hex(path)
            
                if check_md5_hex(md5_hex):
                    logger.info(f"[加载知识库]文件 {path} 已存在知识库内，跳过。")
                    continue
                
                try:
                    documents: list[Document] = get_file_docments(path)
                    
                    if not documents:
                        logger.warning(f"[加载知识库]文件 {path} 无有效内容，跳过。")
                        continue
                    
                    splited_document: list[Document] = self.text_splitter.split_documents(documents)
                    
                    print(f"[加载知识库]文件 {path} 已成功加载，共 {len(splited_document)} 条。")
                    print(f"[加载知识库]内容为{splited_document}")
                    
                    if not splited_document:
                        logger.warning(f"[加载知识库]文件 {path} 分片后无有效内容，跳过。")
                        continue
                        
                    self.vector_store.add_documents(splited_document)
                    
                    # 保存md5，避免下次重复加载
                    save_md5_hex(md5_hex)
                    
                    logger.info(f"[加载知识库]文件 {path} 加载成功。")
                
                except Exception as e:
                    # exc_info = true 记录详细报错堆栈
                    logger.error(f"[加载知识库]文件 {path} 加载失败。{e}", exc_info = True)

if __name__ == "__main__":
    vs = VectorStoreService()
    
    vs.load_documents()

    retriever = vs.get_retriever()
    
    res = retriever.invoke("数据库")
    for r in res:
        print(r.page_content)
        print("_______________________________")
