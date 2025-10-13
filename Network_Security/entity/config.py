from dataclasses import dataclass 
from datetime import datetime
from Network_Security.constant import *
from Network_Security.entity.artifact import Metrics_Artifact


TIMESTAMP = datetime.now().strftime('%m_%d_%Y_%H_%M_%S')

@dataclass 
class NS_Train_Configeration:
    artifact_dir:str = os.path.join(ARTIFACTS,TIMESTAMP)
    pipeline_dir:str = PIPELINE_DIR
    TIMESTAMP:str = TIMESTAMP

train_config = NS_Train_Configeration()


@dataclass 
class Data_ingestion_Config:
    data_ingestion_path = os.path.join(train_config.artifact_dir,DATA_INGESTION_DIR)
    data_ingestion_collection_path = DATA_INGESTION_COLLECTION_NAME 
    data_ingestion_feature_path = os.path.join(data_ingestion_path,DATA_INGESTION_FEATURE_STORED_DIR,RAW_DATA)
    train_data_path = os.path.join(data_ingestion_path,DATA_INGESTION_INGESTED_DIR,TRAIN_DATA)
    test_data_path = os.path.join(data_ingestion_path,DATA_INGESTION_INGESTED_DIR,TEST_DATA)
    split_ratio = DATA_INGESTION_SPLIT_RATIO 

@dataclass
class Data_validation_config:
    data_validation_dir = os.path.join(train_config.artifact_dir,DATA_VALIDATION_DIR)
    data_validation_report = os.path.join(data_validation_dir,DATA_VALIDATION_REPORT_DIR,DATA_VALIDATION_REPORT_YAML)

@dataclass 
class Data_Transformation_Config:
    data_transformation_dir = os.path.join(train_config.artifact_dir,DATA_TRANSFORMATION_DIR)
    data_transformation_train_file = os.path.join(data_transformation_dir,DATA_TRANSFORMATION_TRANSFORM_FILE,TRAIN_DATA.replace('csv','npy'))
    data_transformation_test_file = os.path.join(data_transformation_dir,DATA_TRANSFORMATION_TRANSFORM_FILE,TEST_DATA.replace('csv','npy'))
    data_transformation_object_pkl = os.path.join(data_transformation_dir,DATA_TRANSFORMATION_TRANSFORM_0BJECT_FILE,PREPROCESSING_FILE)

@dataclass 
class Model_Trainer_Config:
    model_trainer_dir = os.path.join(train_config.artifact_dir, MODEL_TRAINER_DIR)
    model_trained_path = os.path.join(model_trainer_dir, MODEL_TRAINER_FILE_NAME, MODEL_TRAINER_TRAINED_MODEL_NAME)
    model_trained_config_param_path = MODEL_TRAINER_CONFIG_PARAM_PATH
    excepted_ratio = MODEL_TRAINER_EXCEPTED_RATIO

@dataclass 
class Model_Evalution_Config:
    bucket_name:str = MODEL_BUCKET_NAME 
    s3_model_path:str = MODEL_TRAINER_TRAINED_MODEL_NAME
    changed_model_score:float =  MODEL_EVALUTION_CHANGED_THRESHOLD


