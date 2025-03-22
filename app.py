from flask import Flask, request, jsonify, render_template
from io import StringIO
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap
from ruamel.yaml.parser import ParserError
from deepdiff import DeepDiff

app = Flask(__name__)
yaml = YAML()
yaml.preserve_quotes = True  # 保留引号

def recursive_merge(base, add):
    """
    递归合并两个字典，将 add 中的键值对合并到 base 中
    如果递归检查发现key已存在，则不进行添加操作
    支持复制注释
    """
    if isinstance(base, dict) and isinstance(add, dict):
        for key, value in add.items():
            if key in base:
                if isinstance(base[key], dict) and isinstance(value, dict):
                    # 递归合并嵌套字典
                    base[key] = recursive_merge(base[key], value)
                # 若键已存在，不进行添加操作
                continue
            else:
                base[key] = value
                # 复制键值对行尾注释
                if hasattr(add, 'ca') and key in add.ca.items:
                    base.yaml_add_eol_comment(add.ca.items[key][2].value, key)
                # 复制键值对之前的注释
                if hasattr(add, 'ca') and add.ca.comment and len(add.ca.comment) > 1:
                    comment_before = add.ca.comment[1]
                    if comment_before:
                        # 检查 comment_before 是否为 CommentToken 对象
                        if hasattr(comment_before, 'value'):
                            base.yaml_set_comment_before_after_key(key, comment_before.value.strip(), indent=0)
                        else:
                            for line in comment_before:
                                if hasattr(line, 'value'):
                                    base.yaml_set_comment_before_after_key(key, line.value.strip(), indent=0)
    return base

def merge_yaml(yaml_base, yaml_add, yaml_del, yaml_change):
    """
    合并 YAML 数据, yaml_base 为基础数据，yaml_add 为要添加的数据, yaml_del 为要删除的数据, yaml_change 为要修改的数据,
    按照顺序执行删除、修改、添加操作
    """
    try:
        # 加载 YAML 数据并转换为 CommentedMap
        base_data = yaml.load(yaml_base) or CommentedMap()
        add_data = yaml.load(yaml_add) or CommentedMap()
        del_data = yaml.load(yaml_del) or CommentedMap()
        change_data = yaml.load(yaml_change) or CommentedMap()
    except ParserError as e:
        print(f"YAML 解析错误: {e}")
        return None

    # 删除指定的键
    for key in del_data:
        if key in base_data:
            del base_data[key]
    
    # 修改之前检查所有待修改的key在base中是否存在，不存在则报错，打印所有不存在的key
    not_exist_keys = []
    for key, value in change_data.items():
        if key not in base_data:
            not_exist_keys.append(key)
    if not_exist_keys:
        print(f"以下 key 在 base 中不存在，无法执行修改和合并操作，请先确认原因: {not_exist_keys}")
        return None
    

    # 修改指定的键的值
    for key, value in change_data.items():
        if key in base_data:
            base_data[key] = value


    # 递归合并添加的数据 添加新的键并保留注释
    base_data = recursive_merge(base_data, add_data)


    output = StringIO()
    yaml.dump(base_data, output)
    return output.getvalue()

def compare_yaml(yaml_a, yaml_b):
    try:
        # 加载 YAML 数据并转换为 CommentedMap
        data_a = yaml.load(yaml_a) or CommentedMap()
        data_b = yaml.load(yaml_b) or CommentedMap()
    except ParserError as e:
        print(f"YAML 解析错误: {e}")
        return None
    
    # 使用 DeepDiff 库来对比两个 YAML 文件的内容
    diff = DeepDiff(data_a, data_b, ignore_order=True)

    a_has_b_not = {}
    a_not_b_has = {}
    a_b_all_has = {}

    # 遍历 data_a 中的键值对
    for key, value in data_a.items():
        if key not in data_b or data_b[key] != value:
            a_has_b_not[key] = value
        else:
            a_b_all_has[key] = value

    # 遍历 data_b 中的键值对，找出 data_a 中没有的
    for key, value in data_b.items():
        if key not in data_a or data_a[key] != value:
            a_not_b_has[key] = value

    print(f"a_has_b_not: {a_has_b_not}")
    print(f"a_not_b_has: {a_not_b_has}")
    print(f"a_b_all_has: {a_b_all_has}")

    return {
        'a_has_b_not': a_has_b_not,
        'a_not_b_has': a_not_b_has,
        'a_b_all_has': a_b_all_has
    }

def deep_get(dictionary, key_path):
    keys = key_path.split('.')
    value = dictionary
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return None
    return value
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge', methods=['POST'])
def merge():
    yaml_base = request.form['yaml_base']
    yaml_add = request.form['yaml_add']
    yaml_del = request.form['yaml_del']
    yaml_change = request.form['yaml_change']
    merged_yaml = merge_yaml(yaml_base, yaml_add, yaml_del, yaml_change)
    if merged_yaml is None:
        return jsonify({'error': 'YAML 解析错误，请检查输入的 YAML 格式'}), 400
    return jsonify({'merged_yaml': merged_yaml})

@app.route('/compare_page')
def compare_page():
    return render_template('compare.html')

@app.route('/compare', methods=['POST'])
def compare():
    yaml_a = request.form['yaml_a']
    yaml_b = request.form['yaml_b']
    result = compare_yaml(yaml_a, yaml_b)
    return jsonify(
        {'a_has_b_not': result['a_has_b_not'], 
        'a_not_b_has': result['a_not_b_has'],
        'a_b_all_has': result['a_b_all_has'],})


if __name__ == '__main__':
    app.run(debug=True)
    