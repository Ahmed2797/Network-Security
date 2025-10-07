from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging
from Network_Security.configeration.mongodb import MongoDBClient 
from typing import Optional
import pandas as pd
import numpy as np 
import sys


class NetworkData:
    def __init__(self):
        try:
            self.mongo_client = MongoDBClient()   
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def get_dataframe(self, collection_name: str, database_name: Optional[str] = None)->pd.DataFrame:
        try:
            if database_name:
                collection = self.mongo_client.client[database_name][collection_name]
            else:
                collection = self.mongo_client.database[collection_name]

            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True)
            df.replace("na", np.nan, inplace=True)

            logging.info("DataFrame Extract Successful")
            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)
