import sys 
from sklearn.pipeline import Pipeline 
from Network_Security.exception.exception import NetworkSecurityException 

import pandas as pd 

class Network_model:
    def __init__(self, transform_object: Pipeline, best_model_details: object):
        self.transform_object = transform_object
        self.best_model_details = best_model_details

    def predict(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        try:
            transformed_features = self.transform_object.transform(dataframe)
            predictions = self.best_model_details.predict(transformed_features)
            return predictions
            #return pd.DataFrame(predictions, columns=['prediction'])
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def __repr__(self):
        return f"{type(self.best_model_details).__name__}()"

    def __str__(self):
        return f"{type(self.best_model_details).__name__}()"