import os
import yaml

def clear_yaml(file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('')

import yaml
from collections import OrderedDict

def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        lambda loader, node: object_pairs_hook(loader.construct_pairs(node)))
    return yaml.load(stream, OrderedLoader)

def ordered_dump(data, stream=None, Dumper=yaml.Dumper, **kwargs):
    class OrderedDumper(Dumper):
        pass
    OrderedDumper.add_representer(OrderedDict,
        lambda dumper, data: dumper.represent_dict(data.items()))
    return yaml.dump(data, stream, OrderedDumper, **kwargs)

def append_yaml(source_file, target_file, output_file):
    """
    append_yaml函数不会更新target_file文件中key的value，只添加新的key，输出到output_file
    """
    with open(target_file, 'r') as t_file:
        target_data = ordered_load(t_file, yaml.SafeLoader)
    
    with open(source_file, 'r') as s_file:
        source_data = ordered_load(s_file, yaml.SafeLoader)
    
    # Merge source data into target data without updating existing keys
    def merge_dicts(target, source):
        for key, value in source.items():
            if key not in target:
                target[key] = value
            elif isinstance(target[key], dict) and isinstance(value, dict):
                merge_dicts(target[key], value)
            elif isinstance(target[key], list) and isinstance(value, list):
                target[key].extend(x for x in value if x not in target[key])

    merge_dicts(target_data, source_data)

    with open(output_file, 'w') as out_file:
        ordered_dump(target_data, out_file, Dumper=yaml.SafeDumper, default_flow_style=False)


def remove_keys_from_yaml(source_file, target_file, output_file):
    with open(target_file, 'r') as t_file:
        target_data = ordered_load(t_file, yaml.SafeLoader)
    
    with open(source_file, 'r') as s_file:
        try:
            source_data = ordered_load(s_file, yaml.SafeLoader)
        except yaml.YAMLError:
            source_data = {}

    # Remove keys from target_data based on source_data keys
    def remove_keys(target, source):
        for key, value in source.items():
            if key in target:
                if isinstance(value, dict) and isinstance(target[key], dict):
                    remove_keys(target[key], value)
                    # If after removing nested keys, the dictionary is empty, remove the key
                    if not target[key]:
                        del target[key]
                else:
                    del target[key]

    if source_data:
        remove_keys(target_data, source_data)

    with open(output_file, 'w') as out_file:
        ordered_dump(target_data, out_file, Dumper=yaml.SafeDumper, default_flow_style=False)
