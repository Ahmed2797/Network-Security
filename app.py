from Network_Security.pipeline.train_pipeline import Training_Pipeline
from Network_Security.logging.logger import logging
from Network_Security.exception.exception import NetworkSecurityException
import sys 

pipeline = Training_Pipeline()
pipeline.run_pipeline()

