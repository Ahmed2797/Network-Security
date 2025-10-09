from Network_Security.constant import * 
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging
from Network_Security.utils import read_yaml_file, save_object, save_numpy_array
from Network_Security.entity.artifact import (
    Data_Ingestion_Artifact,
    Data_validation_Artifact,
    Data_Transformation_Artifact
)
from Network_Security.entity.config import Data_Transformation_Config

from sklearn.pipeline import Pipeline
from sklearn.impute import KNNImputer
import pandas as pd 
import numpy as np
import sys


class DataTransformation:
    def __init__(self,
                 data_ingestion_artifact: Data_Ingestion_Artifact,
                 data_validation_artifact: Data_validation_Artifact,
                 data_transformation_config: Data_Transformation_Config):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def get_data_transformation(self) -> Pipeline:
        try:
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor = Pipeline([('imputer', imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def init_data_transformation(self):
        try:
            logging.info("Data read and apply preprocessing & transformation")
            train_df = DataTransformation.read_data(self.data_ingestion_artifact.train_file_path)
            test_df = DataTransformation.read_data(self.data_ingestion_artifact.test_file_path)

            # Train features & target
            input_feature_train = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train = train_df[TARGET_COLUMN].replace(-1, 0)

            # Test features & target
            input_feature_test = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test = test_df[TARGET_COLUMN].replace(-1, 0)

            # Preprocessor
            preprocessor = self.get_data_transformation()
            input_feature_train_arr = preprocessor.fit_transform(input_feature_train)
            input_feature_test_arr = preprocessor.transform(input_feature_test)

            # Combine arrays
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test)]

            # Save transformation pipeline and arrays
            save_object(self.data_transformation_config.data_transformation_object_pkl, obj=preprocessor)
            save_numpy_array(self.data_transformation_config.data_transformation_train_file, array=train_arr)
            save_numpy_array(self.data_transformation_config.data_transformation_test_file, array=test_arr)
            logging.info('Array loaded succesfully')

            data_transformation_artifact = Data_Transformation_Artifact(
                transform_object=self.data_transformation_config.data_transformation_object_pkl,
                transform_train_file=self.data_transformation_config.data_transformation_train_file,
                transform_test_file=self.data_transformation_config.data_transformation_test_file
            )

            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
