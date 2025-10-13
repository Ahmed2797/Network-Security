import os
import numpy as np 
from datetime import date

# MongoDB
DATA_BASE_NAME = 'NETWORK_SECURITY'
COLLECTION_NAME = 'NETWORK_DATA'
MONGOBD_URL = 'MONGODB_URL'

# Artifacts
ARTIFACTS = 'artifacts'
PIPELINE_DIR = 'network'

# DATA 
RAW_DATA = 'raw.csv'
TRAIN_DATA = 'train.csv'
TEST_DATA = 'test.csv'


# Data_ingestion
DATA_INGESTION_DIR: str = 'data_ingestion'
DATA_INGESTION_COLLECTION_NAME:str = 'NETWORK_DATA'
DATA_INGESTION_FEATURE_STORED_DIR:str = 'feature'
DATA_INGESTION_INGESTED_DIR:str = 'ingested'
DATA_INGESTION_SPLIT_RATIO:float = 0.2 

# Data_validation
DATA_VALIDATION_DIR:str = 'data_validation'
DATA_VALIDATION_REPORT_DIR:str = 'drift_report'
DATA_VALIDATION_REPORT_YAML:str = 'report.yaml'

# Data_transformation
DATA_TRANSFORMATION_DIR:str = 'data_tranasformation'
DATA_TRANSFORMATION_TRANSFORM_FILE:str = 'transform'
DATA_TRANSFORMATION_TRANSFORM_0BJECT_FILE:str = 'transform_obj'
PREPROCESSING_FILE:str = 'preprocessing.pkl'
TARGET_COLUMN = 'result'
CURRENT_YEAR = date.today().year
# KNNImputer
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict={ 
    'missing_values': np.nan,
    'n_neighbors':3,
    'weights':'uniform'
}
SCHEMA_FILE_PATH = os.path.join('data_schema','column.yaml')

# model_trainer
MODEL_TRAINER_DIR:str = 'model_trainer'
MODEL_TRAINER_FILE_NAME:str = 'trained_model'
MODEL_TRAINER_TRAINED_MODEL_NAME:str = 'model.pkl'
MODEL_TRAINER_CONFIG_PARAM_PATH:str = os.path.join('data_schema','best_param.yaml')
MODEL_TRAINER_EXCEPTED_RATIO:float = 0.6 

#AWS Configeration
REGION = 'us-east-1'
AWS_ACCESS_KEY = 'AWS_ACCESS_KEY_ID'
AWS_SECRET_KEY = 'AWS_SECRET_ACCESS_KEY' 

# model_evalution 
MODEL_BUCKET_NAME:str = 'network_security'
MODEL_EVALUTION_CHANGED_THRESHOLD:float = 0.8 
MODEL_TRAINER_TRAINED_MODEL_NAME:str = 'model.pkl'



