import os
import yaml
import sys
import pickle
import numpy as np
from Network_Security.exception.exception import NetworkSecurityException

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
    
def save_object(file_path: str, obj: object):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)  
    except Exception as e:
        raise NetworkSecurityException(e, sys)
     

def save_numpy_array(file_path: str, array: np.array):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)  
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def load_numpy_array(file_path:str)->np.array:
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'rb') as file_obj:
            np.load(file_obj)
    except Exception as e:
          raise NetworkSecurityException(e,sys)
    

def load_object(file_path: str) -> object:
    try:
        with open(file_path, "rb") as file_obj:
            obj = pickle.load(file_obj)
        return obj
    except Exception as e:
        raise NetworkSecurityException(e, sys)