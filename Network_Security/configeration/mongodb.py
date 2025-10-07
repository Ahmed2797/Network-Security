from Network_Security.constant import MONGOBD_URL, DATA_BASE_NAME
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging
from dotenv import load_dotenv 
import certifi 
import pymongo
import sys
import os 


load_dotenv()
# MONGOBD_URL = os.getenv("MONGOBD_URL")
ca = certifi.where()  

class MongoDBClient:
    def __init__(self, database=DATA_BASE_NAME):
        try:
            mongo_url = os.getenv(MONGOBD_URL)
            if mongo_url is None:
                logging.info("MongoDB URL not found in environment variables")
                raise ValueError("MongoDB URL is missing")

            MongoDBClient.client = pymongo.MongoClient(mongo_url, tlsCAFile=ca)
            self.client = MongoDBClient.client 
            self.database = self.client[database]
            self.database_name = database  

        except Exception as e:
            raise NetworkSecurityException(e, sys)
 
    

