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

@dataclass 
class Metrics_Artifact:
    f1_score:float 
    accuracy_score:float
    recall_score:float 
    precision_score:float

@dataclass 
class Model_Trainer_Artifact:
    model_pkl:str 
    metrics : Metrics_Artifact 

@dataclass 
class Model_Evalution_Artifact:
    is_model_accepted:bool 
    changed_accuracy:float
    train_model_path:str 
    s3_model_path:str