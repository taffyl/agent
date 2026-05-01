from pathlib import Path
import os

# 创建 Path 对象
file_path = Path(__file__).parent/"testfile"/"test.txt"

print(file_path)
# 方法2：使用 missing_ok 参数（Python 3.8+）
try:
    file_path.unlink(missing_ok=True)  # 文件不存在也不会报错
    print("文件已删除或不存在")
except PermissionError:
    print("没有删除权限")
    
    
for i in ["sad",2,3]:
    print(i)