# test_app.py
import pytest
from crud_yaml.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_merge_yaml(client):
    response = client.post('/merge', data={
        'yaml1': 'key1: value1\nkey2: value2',
        'yaml2': 'key3: value3\nkey4: value4'
    })
    assert response.status_code == 200
    assert 'key1: value1' in response.json['merged_yaml']
    assert 'key3: value3' in response.json['merged_yaml']

def test_merge_with_comments(client):
    yaml1 = """
    # Comment for key1
    key1: value1
    key2: value2
    """
    yaml2 = """
    # Comment for key3
    key3: value3
    key4: value4
    """
    response = client.post('/merge', data={'yaml1': yaml1, 'yaml2': yaml2})
    assert response.status_code == 200
    merged_yaml = response.json['merged_yaml']
    assert '# Comment for key1' in merged_yaml
    assert '# Comment for key3' in merged_yaml

def test_merge_with_quotes(client):
    yaml1 = """
    key1: "value1"
    key2: 'value2'
    """
    yaml2 = """
    key3: "value3"
    key4: 'value4'
    """
    response = client.post('/merge', data={'yaml1': yaml1, 'yaml2': yaml2})
    assert response.status_code == 200
    merged_yaml = response.json['merged_yaml']
    assert 'key1: "value1"' in merged_yaml
    assert "key2: 'value2'" in merged_yaml
    assert 'key3: "value3"' in merged_yaml
    assert "key4: 'value4'" in merged_yaml

def test_merge_with_nested_keys(client):
    yaml1 = """
    parent1:
      child1: value1
    """
    yaml2 = """
    parent2:
      child2: value2
    """
    response = client.post('/merge', data={'yaml1': yaml1, 'yaml2': yaml2})
    assert response.status_code == 200
    merged_yaml = response.json['merged_yaml']
    assert 'parent1:\n  child1: value1' in merged_yaml
    assert 'parent2:\n  child2: value2' in merged_yaml

def test_merge_with_existing_keys(client):
    yaml1 = """
    key1: value1
    key2: value2
    """
    yaml2 = """
    key1: new_value1
    key3: value3
    """
    response = client.post('/merge', data={'yaml1': yaml1, 'yaml2': yaml2})
    assert response.status_code == 200
    merged_yaml = response.json['merged_yaml']
    assert 'key1: value1' in merged_yaml  # Original value should be retained
    assert 'key3: value3' in merged_yaml


def test_merge_with_comments(client):
    yaml1 = """
    # Comment for key1
    key1: value1
    key2: value2
    """
    yaml2 = """
    # Comment for key3
    key3: value3
    key4: value4
    """
    response = client.post('/merge', data={'yaml1': yaml1, 'yaml2': yaml2})
    assert response.status_code == 200
    merged_yaml = response.json['merged_yaml']
    assert '# Comment for key1' in merged_yaml
    assert '# Comment for key3' in merged_yaml

def test_merge_with_quotes(client):
    yaml1 = """
    key1: "value1"
    key2: 'value2'
    """
    yaml2 = """
    key3: "value3"
    key4: 'value4'
    """
    response = client.post('/merge', data={'yaml1': yaml1, 'yaml2': yaml2})
    assert response.status_code == 200
    merged_yaml = response.json['merged_yaml']
    assert 'key1: "value1"' in merged_yaml
    assert "key2: 'value2'" in merged_yaml
    assert 'key3: "value3"' in merged_yaml
    assert "key4: 'value4'" in merged_yaml
    
def test_merge_with_nested_keys(client):
    yaml1 = """
    parent1:
      child1: value1
    """
    yaml2 = """
    parent2:
      child2: value2
    """
    response = client.post('/merge', data={'yaml1': yaml1, 'yaml2': yaml2})
    assert response.status_code == 200
    merged_yaml = response.json['merged_yaml']
    assert 'parent1:\n  child1: value1' in merged_yaml
    assert 'parent2:\n  child2: value2' in merged_yaml