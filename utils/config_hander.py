import yaml
from utils import path_tool


def load_config(config_file: str, 
                config_folder: str = "config", 
                encoding: str = "utf-8"
                ) -> dict[str]:
    """
    加载配置文件。

    从指定的YAML文件路径中读取并解析配置内容，返回解析后的配置对象。
    """

    config_path = path_tool.get_abs_path(f"{config_folder}/{config_file}")
    
    with open(file=config_path, encoding=encoding) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        return config
    
    
rag_conf = load_config("rag.yml")
chroma_conf = load_config("chroma.yml")
prompts_conf = load_config("prompts.yml")
agent_conf = load_config("agent.yml")
database_conf = load_config("database.yml")


if __name__ == "__main__":
    print(rag_conf.chat_model_name)