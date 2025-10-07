from dataclasses import dataclass 
from datetime import datetime
from Network_Security.constant import *


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