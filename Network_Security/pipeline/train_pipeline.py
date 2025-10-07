from Network_Security.components.data_ingestion import Data_Ingestion
from Network_Security.entity.config import (Data_ingestion_Config) 
from Network_Security.entity.artifact import (Data_Ingestion_Artifact)



class Training_Pipeline:
    def __init__(self):
        self.data_ingestion_config = Data_ingestion_Config()



    def start_data_ingestion(self)->Data_Ingestion_Artifact:
        data_ingestion = Data_Ingestion(ingestion_config=self.data_ingestion_config)
        data_ingestion_artifacet = data_ingestion.init_data_ingestion()
        return data_ingestion_artifacet 



    def run_pipeline(self)->None:
        data_ingestion_artifacet = self.start_data_ingestion()

        return None