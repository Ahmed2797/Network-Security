import os
import yaml

# def read_yaml_file(file_path:str)->dict:
#     if not os.path.exists(file_path):
#         raise FileNotFoundError(f"File not found: {file_path}")
#     with open(file_path, 'rb') as file:
#         yaml.safe_load(file) 
    
def read_yaml_file(file_path: str) -> dict:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, 'r') as file:  # text mode is fine for YAML
        data = yaml.safe_load(file)
    if data is None:
        raise ValueError(f"YAML file is empty: {file_path}")
    return data


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)   
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  
        with open(file_path, "w") as file:
            yaml.dump(content, file)  
    
