from Network_Security.components.data_ingestion import Data_Ingestion
from Network_Security.components.data_validation import Data_validation
from Network_Security.components.data_transformation import DataTransformation
from Network_Security.components.model_train import Model_Train
from Network_Security.entity.config import (Data_ingestion_Config,
                                            Data_validation_config,
                                            Data_Transformation_Config,
                                            Model_Trainer_Config) 
from Network_Security.entity.artifact import (Data_Ingestion_Artifact,
                                              Data_validation_Artifact,
                                              Data_Transformation_Artifact)

from Network_Security.exception.exception import NetworkSecurityException
import sys


class Training_Pipeline:
    def __init__(self):
        self.data_ingestion_config = Data_ingestion_Config()
        self.data_validation_config = Data_validation_config()
        self.data_transformation_config = Data_Transformation_Config()
        self.model_trainer_config = Model_Trainer_Config()


    def start_data_ingestion(self)->Data_Ingestion_Artifact:
        try:
            data_ingestion = Data_Ingestion(ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.init_data_ingestion()
            return data_ingestion_artifact 
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def start_data_validation(self, data_ingestion_artifact: Data_Ingestion_Artifact) -> Data_validation_Artifact:
        try:
            data_valid = Data_validation(data_ingestion_artifact=data_ingestion_artifact,
                                        data_validation_config=self.data_validation_config)
            data_validation_artifact = data_valid.init_data_validation()
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def start_data_transformation(self,data_ingestion_artifact: Data_Ingestion_Artifact,
                                  data_validation_artifact:Data_validation_Artifact)->Data_Transformation_Artifact:
        try:
            data_transformation = DataTransformation(data_ingestion_artifact=data_ingestion_artifact,
                                                data_validation_artifact=data_validation_artifact,
                                                data_transformation_config=self.data_transformation_config)
            data_transformation_artifact = data_transformation.init_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def strat_model_trainer(self,data_transformation_artifact:Data_Transformation_Artifact):
        try:
            model_train = Model_Train(data_transformation_artifact=data_transformation_artifact,
                                    model_trainer_config=self.model_trainer_config)
            model_trainer_artifact=model_train.init_best_model()
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def run_pipeline(self)->None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact,data_validation_artifact)
            model_trainer_artifact = self.strat_model_trainer(data_transformation_artifact)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

        return None