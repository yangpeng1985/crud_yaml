from flask import Flask, request, jsonify, render_template
from io import StringIO
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import PreservedScalarString

# app.py
app = Flask(__name__)
yaml = YAML(typ='rt')

def merge_yaml(yaml1, yaml2):
    yaml1_data = yaml.load(yaml1)
    yaml2_data = yaml.load(yaml2)
    
    for key, value in yaml2_data.items():
        if key not in yaml1_data:
            yaml1_data[key] = value
    
    output = StringIO()
    yaml.dump(yaml1_data, output)
    return output.getvalue()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge', methods=['POST'])
def merge():
    yaml1 = request.form['yaml1']
    yaml2 = request.form['yaml2']
    merged_yaml = merge_yaml(yaml1, yaml2)
    return jsonify({'merged_yaml': merged_yaml})

if __name__ == '__main__':
    app.run(debug=True)