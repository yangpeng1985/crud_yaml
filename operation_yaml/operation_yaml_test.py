import os
import yaml

"""
在target_file的基础上，
增加、删除、更新source_file，
输出为output_file
"""

def clear_yaml(file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('')

def append_yaml(source_file, target_file, output_file):
    with open(source_file, 'r', encoding='utf-8') as file:
        source_data = yaml.safe_load(file)

    with open(target_file, 'r', encoding='utf-8') as file:
        target_data = yaml.safe_load(file)

    if target_data is None:
        target_data = {}
    
    if source_data is None:
        return

    if isinstance(source_data, dict) and isinstance(target_data, dict):
        combined_data = {**target_data, **source_data}
    elif isinstance(source_data, list) and isinstance(target_data, list):
        combined_data = target_data + source_data
    else:
        raise ValueError("The source and target YAML files must be of the same type (both dicts or both lists).")

    with open(output_file, 'w', encoding='utf-8') as file:
        yaml.safe_dump(combined_data, file, allow_unicode=True)

def remove_keys_from_yaml(source_file, target_file, output_file):
    with open(source_file, 'r', encoding='utf-8') as file:
        source_data = yaml.safe_load(file)

    with open(target_file, 'r', encoding='utf-8') as file:
        target_data = yaml.safe_load(file)

    if source_data is None or target_data is None:
        return

    if isinstance(source_data, dict) and isinstance(target_data, dict):
        for key in source_data:
            if key in target_data:
                del target_data[key]
    else:
        raise ValueError("Both source and target YAML files must be dictionaries.")

    with open(output_file, 'w', encoding='utf-8') as file:
        yaml.safe_dump(target_data, file, allow_unicode=True)

def update_yaml(source_file, target_file, output_file):
    with open(source_file, 'r', encoding='utf-8') as file:
        source_data = yaml.safe_load(file)

    with open(target_file, 'r', encoding='utf-8') as file:
        target_data = yaml.safe_load(file)

    if source_data is None or target_data is None:
        return

    if isinstance(source_data, dict) and isinstance(target_data, dict):
        def update_dict(source, target):
            for key, value in source.items():
                if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                    update_dict(value, target[key])
                else:
                    target[key] = value

        update_dict(source_data, target_data)
    else:
        raise ValueError("Both source and target YAML files must be dictionaries.")

    with open(output_file, 'w', encoding='utf-8') as file:
        yaml.safe_dump(target_data, file, allow_unicode=True)


# 获取当前脚本文件的绝对路径
script_path = os.path.abspath(__file__)

# 获取当前脚本文件所在的目录
script_dir = os.path.dirname(script_path)

target_file = os.path.join(script_dir, "online_config", "current_test.yaml")
output_file = os.path.join(script_dir, "merged_config", "output_test.yaml")

# 修改之前先清空输出文件
clear_yaml(output_file)

# 临时文件
temp_file = os.path.join(script_dir, "temp.yaml")

# 增加
add_file = os.path.join(script_dir, "new_version_config", "add_test.yaml")
append_yaml(add_file, target_file, temp_file)

# 删除
del_file = os.path.join(script_dir, "new_version_config", "delete_test.yaml")
remove_keys_from_yaml(del_file, temp_file, temp_file)

# 更新
update_file = os.path.join(script_dir, "new_version_config", "update_test.yaml")
update_yaml(update_file, temp_file, output_file)

# 清空临时文件
clear_yaml(temp_file)

#todo 对代码做改进，在yaml文件target_file的基础上，
# 把另外三个yaml文件add_file、del_file、update_file，分别按照添加、删除、更新的动作进行yaml文件合并，
# 最后输出到output_file