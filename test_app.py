import pytest
from crud_yaml.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_merge_yaml(client):
    yaml_base = 'key1: value1\nkey2: value2'
    yaml_add = 'key3: value3\nkey4: value4'
    yaml_del = 'key2: value2'
    yaml_change = ''
    response = client.post('/merge', data={
        'yaml_base': yaml_base,
        'yaml_add': yaml_add,
        'yaml_del': yaml_del,
        'yaml_change': yaml_change
    })
    assert response.status_code == 200
    assert 'key1: value1' in response.json['merged_yaml']
    assert 'key3: value3' in response.json['merged_yaml']
    assert 'key2: value2' not in response.json['merged_yaml']

def test_merge_with_comments(client):
    yaml_base = """
    # Comment for key1
    key1: value1
    key2: value2
    """
    yaml_add = """
    # Comment for key3
    key3: value3
    key4: value4
    """
    yaml_del = """
    key2: value2
    """
    yaml_change = ''
    response = client.post('/merge', data={
        'yaml_base': yaml_base,
        'yaml_add': yaml_add,
        'yaml_del': yaml_del,
        'yaml_change': yaml_change
    })
    assert response.status_code == 200
    merged_yaml = response.json['merged_yaml']
    assert '# Comment for key1' in merged_yaml
    assert '# Comment for key3' in merged_yaml
    assert 'key2: value2' not in merged_yaml

def test_merge_with_quotes(client):
    yaml_base = """
    key1: "value1"
    key2: 'value2'
    """
    yaml_add = """
    key3: "value3"
    key4: 'value4'
    """
    yaml_del = """
    key2: value2
    """
    yaml_change = ''
    response = client.post('/merge', data={
        'yaml_base': yaml_base,
        'yaml_add': yaml_add,
        'yaml_del': yaml_del,
        'yaml_change': yaml_change
    })
    assert response.status_code == 200
    merged_yaml = response.json['merged_yaml']
    assert 'key1: "value1"' in merged_yaml
    assert "key2: 'value2'" not in merged_yaml
    assert 'key3: "value3"' in merged_yaml
    assert "key4: 'value4'" in merged_yaml

def test_merge_with_nested_keys(client):
    yaml_base = """
    parent1:
      child1: value1
    """
    yaml_add = """
    parent2:
      child2: value2
    """
    yaml_del = """
    parent1:
      child1: value1
    """
    yaml_change = ''
    response = client.post('/merge', data={
        'yaml_base': yaml_base,
        'yaml_add': yaml_add,
        'yaml_del': yaml_del,
        'yaml_change': yaml_change
    })
    assert response.status_code == 200
    merged_yaml = response.json['merged_yaml']
    assert 'parent1:\n  child1: value1' not in merged_yaml
    assert 'parent2:\n  child2: value2' in merged_yaml