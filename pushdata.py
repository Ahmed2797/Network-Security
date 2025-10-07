import os 
import sys 
import json 
import certifi
import pandas as pd
import pymongo
from Network_Security.exception.exception import NetworkSecurityException 
from Network_Security.logging.logger import logging
from dotenv import load_dotenv 
load_dotenv()

MONGODB_URL = os.getenv('MONGODB_URL')
print("MongoDB URL:", MONGODB_URL)  

ca = certifi.where()

class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_convertor(self, file_path):
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
                
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = json.loads(data.to_json(orient="records"))
            logging.info(f"Successfully converted {len(records)} records from CSV to JSON")
            return records
        except Exception as e:
            logging.error(f"Error converting CSV to JSON: {str(e)}")
            raise NetworkSecurityException(e, sys)
        
    def insert_data_mongodb(self, records, database, collection):
        try:
            if not records:
                logging.warning("No records to insert")
                return 0
                
            if not database or not collection:
                raise ValueError("Database and collection names cannot be empty")

            self.mongo_client = pymongo.MongoClient(MONGODB_URL, tlsCAFile=ca)
            self.db = self.mongo_client[database]
            self.collection = self.db[collection]
          
            result = self.collection.insert_many(records)
            inserted_count = len(result.inserted_ids)
            
            logging.info(f"Successfully inserted {inserted_count} records into {database}.{collection}")

            self.mongo_client.close()
            
            return inserted_count
            
        except Exception as e:
            logging.error(f"Error inserting data into MongoDB: {str(e)}")
            raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    try:
        FILE_PATH = "Network_Data_\phishing_data.csv"
        DATABASE = "NETWORK_SECURITY"
        COLLECTION = "NETWORK_DATA"
        
        networkobj = NetworkDataExtract()
        records = networkobj.csv_to_json_convertor(file_path=FILE_PATH)
        print(records)
        print(f"Converted {len(records)} records")
        
        no_of_records = networkobj.insert_data_mongodb(records, DATABASE, COLLECTION)
        print(f"Inserted {no_of_records} records into MongoDB")
        
    except Exception as e:
        print(f"Error in main execution: {str(e)}")
        sys.exit(1)