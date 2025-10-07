import os

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


SEHEMA_FILE_PATH = os.path.join('config','config.yaml')