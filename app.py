from flask import Flask, request, jsonify, render_template
from io import StringIO
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap
from ruamel.yaml.parser import ParserError

app = Flask(__name__)
yaml = YAML()
yaml.preserve_quotes = True  # 保留引号

def merge_yaml(yaml_base, yaml_add, yaml_del):
    try:
        # 加载 YAML 数据并转换为 CommentedMap
        base_data = yaml.load(yaml_base) or CommentedMap()
        add_data = yaml.load(yaml_add) or CommentedMap()
        del_data = yaml.load(yaml_del) or CommentedMap()
    except ParserError as e:
        print(f"YAML 解析错误: {e}")
        return None

    # 删除指定的键
    for key in del_data:
        if key in base_data:
            del base_data[key]

    # 添加新的键并保留注释
    for key, value in add_data.items():
        if key not in base_data:
            base_data[key] = value
            # 复制键值对行尾注释
            if hasattr(add_data, 'ca') and key in add_data.ca.items:
                base_data.yaml_add_eol_comment(add_data.ca.items[key][2].value, key)
            # 复制键值对之前的注释
            if hasattr(add_data, 'ca') and add_data.ca.comment and len(add_data.ca.comment) > 1:
                comment_before = add_data.ca.comment[1]
                if comment_before:
                    # base_data.yaml_set_comment_before_after_key(key, before=comment_before.value)
                    # 检查 comment_before 是否为 CommentToken 对象
                    if hasattr(comment_before, 'value'):
                        base_data.yaml_set_comment_before_after_key(key, comment_before.value.strip(), indent=0)
                    else:
                        for line in comment_before:
                            if hasattr(line, 'value'):
                                base_data.yaml_set_comment_before_after_key(key, line.value.strip(), indent=0)


    output = StringIO()
    yaml.dump(base_data, output)
    return output.getvalue()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge', methods=['POST'])
def merge():
    yaml_base = request.form['yaml_base']
    yaml_add = request.form['yaml_add']
    yaml_del = request.form['yaml_del']
    merged_yaml = merge_yaml(yaml_base, yaml_add, yaml_del)
    if merged_yaml is None:
        return jsonify({'error': 'YAML 解析错误，请检查输入的 YAML 格式'}), 400
    return jsonify({'merged_yaml': merged_yaml})

if __name__ == '__main__':
    app.run(debug=True)
    