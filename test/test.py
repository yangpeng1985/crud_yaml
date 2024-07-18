import os
import sys

# 获取当前脚本文件的绝对路径
script_path = os.path.abspath(__file__)

# 获取当前脚本文件所在的目录
script_dir = os.path.dirname(script_path)

# 获取项目的根目录
project_root = os.path.dirname(script_dir)
# 添加xx目录到sys.path
sys.path.append(os.path.join(project_root, "operation_yaml"))

#导入函数
from operation_yaml_test import append_yaml,remove_keys_from_yaml

target_file = os.path.join(script_dir, "config1_for_append_test.yaml")
output_file = os.path.join(script_dir, "output_for_append_test.yaml")

# 增加
add_file = os.path.join(script_dir, "config2_for_append_test.yaml")
# append_yaml当前的能力是保持了target_file的顺序；
# 更新了target_file已有key的值的问题，append只添加，不更新；
append_yaml(add_file, target_file, output_file)

target_file_for_del_test = os.path.join(script_dir, "target_for_del_test.yaml")
output_file_for_del_test = os.path.join(script_dir, "output_for_del_test.yaml")

# 删除
del_file = os.path.join(script_dir,  "source_for_del_test.yaml")
remove_keys_from_yaml(del_file, target_file_for_del_test, output_file_for_del_test)
