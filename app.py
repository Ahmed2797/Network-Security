from Network_Security.pipeline.train_pipeline import Training_Pipeline
from Network_Security.logging.logger import logging
from Network_Security.exception.exception import NetworkSecurityException
import sys 

if __name__ == '__main__':
    try:
        logging.info('Data Ingestion')
        data_ingestion = Training_Pipeline()
        data_ingestion_artifact = data_ingestion.run_pipeline()
        logging.info('Data_Ingestion Succesfull')
        
    except Exception as e:
        raise NetworkSecurityException(e, sys)