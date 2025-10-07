import os
import sys
from sklearn.model_selection import train_test_split
import pandas as pd
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging
from Network_Security.entity.config import Data_ingestion_Config
from Network_Security.entity.artifact import Data_Ingestion_Artifact
from Network_Security.configeration.mongodb import MongoDBClient  
from Network_Security.data_acess.networkdata_acess import NetworkData 

class Data_Ingestion:
    def __init__(self, ingestion_config: Data_ingestion_Config):
        try:
            self.ingestion_config = ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def get_feature_extract_data(self):
        try:
            logging.info("Extracting data from MongoDB...")
            networkdata = NetworkData()
            
            dataframe = networkdata.get_dataframe(
                collection_name=self.ingestion_config.data_ingestion_collection_path
            )
            # start feature_store
            feature_data_path = self.ingestion_config.data_ingestion_feature_path
            os.makedirs(os.path.dirname(feature_data_path), exist_ok=True)
            dataframe.to_csv(feature_data_path, index=False, header=True)
            logging.info(f"Data stored at {feature_data_path}")
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data(self, dataframe: pd.DataFrame):
        try:
            train_data, test_data = train_test_split(
                dataframe, 
                test_size=self.ingestion_config.split_ratio
            )

            train_file_path = self.ingestion_config.train_data_path
            os.makedirs(os.path.dirname(train_file_path), exist_ok=True)
            train_data.to_csv(train_file_path, index=False, header=True)

            test_file_path = self.ingestion_config.test_data_path
            os.makedirs(os.path.dirname(test_file_path), exist_ok=True)
            test_data.to_csv(test_file_path, index=False, header=True)

            logging.info("Train & Test datasets saved successfully.")
            return train_data, test_data
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def init_data_ingestion(self):
        try:
            dataframe = self.get_feature_extract_data()
            print(dataframe.head())
            self.split_data(dataframe)

            data_ingestion_artifact = Data_Ingestion_Artifact(
                train_file_path=self.ingestion_config.train_data_path,
                test_file_path=self.ingestion_config.test_data_path
            )
            logging.info("Data Ingestion completed successfully.")
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) 
        

        
