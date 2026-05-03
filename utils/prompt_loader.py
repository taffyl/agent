from utils.config_hander import prompts_conf
from utils.path_tool import get_abs_path
from utils.logger_hander import logger
def load_system_prompt() -> str:
    """
    加载系统提示语。

    从配置文件中读取并返回系统提示语。

    """
    try:
        system_prompt_path = get_abs_path(prompts_conf["system_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_system_prompt]在yaml配置文件中未找到system_prompt_path字段")
        raise e
    
    try:
        f = open(system_prompt_path, "r", encoding="utf-8").read()
        logger.info(f"[load_system_prompt]加载系统提示词成功")
        return f
    except Exception as e:
        logger.error(f"[load_system_prompt]读取系统提示文件失败: {e}")
        raise e
        
        
def load_rag_prompt() -> str:
    """加载RAG提示语。

    从配置文件中读取并返回RAG提示语。

    """
    try:
        rag_prompt_path = get_abs_path(prompts_conf["rag_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_rag_prompt]在yaml配置文件中未找到rag_prompt_path字段")
        raise e
    
    try:
        f = open(rag_prompt_path, "r", encoding="utf-8").read()
        return f
    except Exception as e:
        logger.error(f"[load_rag_prompt]读取RAG提示文件失败: {e}")
        raise e
        
        
def load_report_prompt() -> str:
    """
    加载报告提示语。

    从配置文件中读取并报告系统提示语。

    """
    try:
        report_prompt_path = get_abs_path(prompts_conf["report_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_report_prompt] 在yaml配置文件中未找到report_prompt_path字段")
        raise e
    
    try:
        f = open(report_prompt_path, "r", encoding="utf-8").read()
        return f
    except Exception as e:
        logger.error(f"[load_report_prompt] 读取报告提示文件失败: {e}")
        raise e
    
    
    
def load_visualize_prompt() -> str:
    """
    加载系统提示语。

    从配置文件中读取并返回系统提示语。

    """
    try:
        visualize_prompt_path = get_abs_path(prompts_conf["visualize_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_visualize_prompt]在yaml配置文件中未找到visualize_prompt_path字段")
        raise e

    try:
        f = open(visualize_prompt_path, "r", encoding="utf-8").read()
        logger.info(f"[load_visualize_prompt]加载系统提示词成功")
        return f
    except Exception as e:
        logger.error(f"[load_visualize_prompt]读取系统提示文件失败: {e}")
        raise e
        
if __name__ == "__main__":
    print(load_system_prompt())