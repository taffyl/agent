from abc import ABC, abstractmethod
from typing import Optional

from langchain_core.embeddings import Embeddings
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models.tongyi import BaseChatModel
from langchain_community.chat_models.tongyi import ChatTongyi

from utils.config_hander import rag_conf

class BaseModelFactory(ABC):
    """
    模型工厂基类，定义生成 LangChain 模型实例的抽象接口。
    
    所有具体的模型工厂子类都应继承此类并实现 generator 方法，
    以确保统一的模型创建标准。
    """

    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        """
        抽象方法：生成并返回一个模型实例。
        
        Returns:
            Optional[Embeddings | BaseChatModel]: 返回 Embeddings 或 BaseChatModel 实例，
            如果创建失败则返回 None。
        """
        pass
    

class ChatModelFactory(BaseModelFactory):
    """
    聊天模型工厂类，负责创建和配置 ChatTongyi 聊天模型实例。
    """

    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        """
        创建并返回一个 ChatTongyi 聊天模型实例。
        
        使用配置文件 rag_conf 中的 'chat_model_name' 作为模型名称。
        
        Returns:
            Optional[Embeddings | BaseChatModel]: 返回配置好的 ChatTongyi 实例。
        """
        return ChatTongyi(model=rag_conf["chat_model_name"])
        

class EmbeddingModelFactory(BaseModelFactory):
    """
    嵌入模型工厂类，负责创建和配置 DashScopeEmbeddings 嵌入模型实例。
    """

    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        """
        创建并返回一个 DashScopeEmbeddings 嵌入模型实例。
        
        使用配置文件 rag_conf 中的 'embedding_model_name' 作为模型名称。
        
        Returns:
            Optional[Embeddings | BaseChatModel]: 返回配置好的 DashScopeEmbeddings 实例。
        """
        return DashScopeEmbeddings(model=rag_conf["embedding_model_name"])
    
chat_model = ChatModelFactory().generator()
embedding_model = EmbeddingModelFactory().generator()