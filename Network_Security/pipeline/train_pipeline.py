from Network_Security.components.data_ingestion import Data_Ingestion
from Network_Security.components.data_validation import Data_validation
from Network_Security.entity.config import (Data_ingestion_Config,
                                            Data_validation_config) 
from Network_Security.entity.artifact import (Data_Ingestion_Artifact,
                                              Data_validation_Artifact)



class Training_Pipeline:
    def __init__(self):
        self.data_ingestion_config = Data_ingestion_Config()
        self.data_validation_config = Data_validation_config()


    def start_data_ingestion(self)->Data_Ingestion_Artifact:
        data_ingestion = Data_Ingestion(ingestion_config=self.data_ingestion_config)
        data_ingestion_artifact = data_ingestion.init_data_ingestion()
        return data_ingestion_artifact 
    
    def start_data_validation(self, data_ingestion_artifact: Data_Ingestion_Artifact) -> Data_validation_Artifact:
        data_valid = Data_validation(data_ingestion_artifact=data_ingestion_artifact,
                                    data_validation_config=self.data_validation_config)
        data_validation_artifact = data_valid.init_data_validation()
        return data_validation_artifact




    def run_pipeline(self)->None:
        data_ingestion_artifact = self.start_data_ingestion()
        data_validation_artifact=self.start_data_validation(data_ingestion_artifact)

        return None