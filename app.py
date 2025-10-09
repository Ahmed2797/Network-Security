from Network_Security.pipeline.train_pipeline import Training_Pipeline
from Network_Security.logging.logger import logging
from Network_Security.exception.exception import NetworkSecurityException
import sys 

if __name__ == '__main__':
    try:
        logging.info('Starting Training Pipeline...')
        pipeline = Training_Pipeline()

        # Data Ingestion
        logging.info('>>> Starting Data Ingestion')
        data_ingestion_artifact = pipeline.start_data_ingestion()
        logging.info(f'>>> Data Ingestion Completed: {data_ingestion_artifact}')

        # Data Validation
        logging.info('>>> Starting Data Validation')
        data_validation_artifact = pipeline.start_data_validation(data_ingestion_artifact)
        logging.info(f'>>> Data Validation Completed: {data_validation_artifact}')

        # Data Transformation
        logging.info('>>> Starting Data Transformation')
        data_transformation_artifact = pipeline.start_data_transformation(data_ingestion_artifact,data_validation_artifact)
        logging.info(f'>>> Data Transformation Completed: {data_transformation_artifact}')

        logging.info('Pipeline finished successfully')
        
    except Exception as e:
        raise NetworkSecurityException(e, sys)