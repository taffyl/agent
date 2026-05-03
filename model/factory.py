from abc import ABC, abstractmethod
from typing import Optional

from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel

import os

# 1. 引入通用的 OpenAI 兼容类
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

from utils.config_hander import rag_conf

class BaseModelFactory(ABC):
    """
    模型工厂基类，定义生成 LangChain 模型实例的抽象接口。
    """

    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        """
        抽象方法：生成并返回一个模型实例。
        """
        pass
    

class ChatModelFactory(BaseModelFactory):
    """
    聊天模型工厂类，负责创建兼容 OpenAI 接口的聊天模型实例。
    """

    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        """
        创建并返回一个 ChatOpenAI 实例，配置为指向第三方服务商。
        """
        # 从配置中获取必要信息
        model_name = rag_conf.get("chat_model_name", "gpt-4o-mini")
        base_url = rag_conf.get("base_url", "https://api.openai.com/v1") # 默认值以防配置缺失
        api_key = os.getenv("OPENAI_API_KEY")

        return ChatOpenAI(
            model=model_name,
            base_url=base_url,
            api_key=api_key, # 如果为None，langchain会自动读取环境变量 OPENAI_API_KEY
            temperature=0.7, # 可选：设置温度
        )
        

class EmbeddingModelFactory(BaseModelFactory):
    """
    嵌入模型工厂类，负责创建兼容 OpenAI 接口的嵌入模型实例。
    """

    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        """
        创建并返回一个 OpenAIEmbeddings 实例，配置为指向第三方服务商。
        """
        # 从配置中获取必要信息
        model_name = rag_conf.get("embedding_model_name", "text-embedding-3-small")
        base_url = rag_conf.get("base_url", "https://api.openai.com/v1")
        api_key = rag_conf.get("api_key", None)

        return OpenAIEmbeddings(
            model=model_name,
            base_url=base_url,
            api_key=api_key,
        )
    
# 实例化
chat_model = ChatModelFactory().generator()
embedding_model = EmbeddingModelFactory().generator()