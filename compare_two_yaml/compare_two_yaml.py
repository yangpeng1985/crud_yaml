import os
import yaml
from deepdiff import DeepDiff

def compare_yaml_files(new_file, target_file):
    # 读取 new_file 的内容
    with open(new_file, 'r', encoding='utf-8') as file:
        new_data = yaml.safe_load(file)

    # 读取 target_file 的内容
    with open(target_file, 'r', encoding='utf-8') as file:
        target_data = yaml.safe_load(file)

    # 使用 DeepDiff 库来对比两个 YAML 文件的内容
    diff = DeepDiff(target_data, new_data, ignore_order=True)

    added = diff.get('dictionary_item_added', {})
    removed = diff.get('dictionary_item_removed', {})
    changed = diff.get('values_changed', {})

    print("Added items:")
    for item in added:
        print(item)
        # print(item, ":", new_data[item.split('root')[1].strip("[']")])

    print("\nRemoved items:")
    for item in removed:
        print(item)
        # print(item, ":", target_data[item.split('root')[1].strip("[']")])

    print("\nChanged items:")
    for item in changed:
        key = item.split('root')[1].strip("[']")
        print(key, ":")
        print("Old value:", changed[item]['old_value'])
        print("New value:", changed[item]['new_value'])

new_file = 'new.yaml'
target_file = 'target.yaml'

# 获取当前脚本文件的绝对路径
script_path = os.path.abspath(__file__)

# 获取当前脚本文件所在的目录
script_dir = os.path.dirname(script_path)

# 构建文件的绝对路径
new_file_path = os.path.join(script_dir, new_file)
print(new_file_path)
target_file_path = os.path.join(script_dir, target_file)

compare_yaml_files(new_file_path, target_file_path)






