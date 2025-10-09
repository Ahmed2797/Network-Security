from dataclasses import dataclass 

@dataclass 
class Data_Ingestion_Artifact:
    train_file_path:str
    test_file_path:str 

@dataclass 
class Data_validation_Artifact:
    validation_status:bool 
    message_error:str 
    drift_report_file_path:str

@dataclass 
class Data_Transformation_Artifact:
    transform_object:str
    transform_train_file:str 
    transform_test_file:str 