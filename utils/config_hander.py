import yaml
from utils import path_tool

def load_rag_config(
    config_path: str = path_tool.get_abs_path("config/rag.yml"),
    encoding: str = "utf-8"
    ) -> yaml:
    """加载RAG配置文件。

    从指定的YAML文件路径中读取并解析配置内容，返回解析后的配置对象。

    """
    
    # 以指定编码打开配置文件并使用FullLoader安全加载YAML内容
    with open(file=config_path, encoding=encoding) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        return config
    
    
    
def load_chroma_config(
    config_path: str = path_tool.get_abs_path("config/chroma.yml"),
    encoding: str = "utf-8"
    ) -> yaml:
    """加载chroma配置文件。

    从指定的YAML文件路径中读取并解析配置内容，返回解析后的配置对象。

    """
    
    # 以指定编码打开配置文件并使用FullLoader安全加载YAML内容
    with open(file=config_path, encoding=encoding) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        return config
    
    
def load_prompts_config(
    config_path: str = path_tool.get_abs_path("config/prompts.yml"),
    encoding: str = "utf-8"
    ) -> yaml:
    """加载prompts配置文件。

    从指定的YAML文件路径中读取并解析配置内容，返回解析后的配置对象。

    """
    
    # 以指定编码打开配置文件并使用FullLoader安全加载YAML内容
    with open(file=config_path, encoding=encoding) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        return config
    
    
def load_agent_config(
    config_path: str = path_tool.get_abs_path("config/agent.yml"),
    encoding: str = "utf-8"
    ) -> yaml:
    """加载agent配置文件。

    从指定的YAML文件路径中读取并解析配置内容，返回解析后的配置对象。

    """
    
    # 以指定编码打开配置文件并使用FullLoader安全加载YAML内容
    with open(file=config_path, encoding=encoding) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        return config
    
    
rag_conf = load_rag_config()
chroma_conf = load_chroma_config()
prompts_conf = load_prompts_config()
agent_conf = load_agent_config()


if __name__ == "__main__":
    print(rag_conf["chat_model_name"])