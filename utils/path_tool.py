import os


def get_project_root_path() -> str:
    """
    获取工程所在的根目录

    """
    current_file_path = os.path.abspath(__file__)
    project_utils_path = os.path.dirname(current_file_path)
    project_root_path = os.path.dirname(project_utils_path)

    return project_root_path


def get_abs_path(relative_path: str) -> str:
    """
    获取文件绝对路径
    """
    project_root_path = get_project_root_path()

    return os.path.join(project_root_path, relative_path)


if __name__ == "__main__":
    path = get_abs_path(relative_path="logs")
