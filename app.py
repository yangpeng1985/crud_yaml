from flask import Flask, request, jsonify, render_template
from io import StringIO
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

app = Flask(__name__)
yaml = YAML()
yaml.preserve_quotes = True  # 保留引号

def merge_yaml(yaml_base, yaml_add, yaml_del):
    base_data = yaml.load(yaml_base)
    add_data = yaml.load(yaml_add)
    del_data = yaml.load(yaml_del)

    # 删除指定的键
    if del_data:
        for key in del_data:
            if key in base_data:
                del base_data[key]

    # 添加新的键
    if add_data:
        for key, value in add_data.items():
            if key not in base_data:
                base_data[key] = value

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
    return jsonify({'merged_yaml': merged_yaml})

if __name__ == '__main__':
    app.run(debug=True)