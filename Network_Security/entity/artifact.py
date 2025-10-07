from dataclasses import dataclass 

@dataclass 
class Data_Ingestion_Artifact:
    train_file_path:str
    test_file_path:str