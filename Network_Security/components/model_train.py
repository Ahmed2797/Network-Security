from Network_Security.entity.artifact import (Data_Transformation_Artifact,
                                              Metrics_Artifact,
                                              Model_Trainer_Artifact)
from Network_Security.entity.config import Model_Trainer_Config
from Network_Security.utils import load_numpy_array,load_object,save_object
from Network_Security.logging.logger import logging
from Network_Security.exception.exception import NetworkSecurityException

from sklearn.metrics import accuracy_score,f1_score,precision_score,recall_score
from sklearn.pipeline import Pipeline
from neuro_mf import ModelFactory
from typing import Tuple
import numpy as np 
import pandas as pd
import sys



class Network_model:
    def __init__(self, transform_object: Pipeline, best_model_details: object)->Tuple[object,object]:
        self.transform_object = transform_object
        self.best_model_details = best_model_details
    def predict(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        try:
            transformed_features = self.transform_object.transform(dataframe)
            predictions = self.best_model_details.predict(transformed_features)

            return pd.DataFrame(predictions, columns=['prediction'])
        except Exception as e:
            raise NetworkSecurityException(e,sys)

class Model_Train:
    def __init__(self, data_transformation_artifact: Data_Transformation_Artifact,
                 model_trainer_config: Model_Trainer_Config):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config
    
    def get_best_model_indentify(self, train_arr: np.array, test_arr: np.array):
        try:
            model_factory = ModelFactory(self.model_trainer_config.model_trained_config_param_path)
        
            xtrain, ytrain = train_arr[:, :-1], train_arr[:, -1]
            xtest, ytest = test_arr[:, :-1], test_arr[:, -1]

            best_model_details = model_factory.get_best_model(
                                X=xtrain,y=ytrain,
                                base_accuracy=self.model_trainer_config.excepted_ratio)
            
            best_model = best_model_details.best_model
            print(best_model)
            pred = best_model.predict(xtest)

            acc = accuracy_score(ytest, pred)
            f1 = f1_score(ytest, pred)
            recall = recall_score(ytest, pred)
            precision = precision_score(ytest, pred)
            
            metrics_artifact = Metrics_Artifact(f1_score=f1,
                                                accuracy_score=acc,
                                                recall_score=recall,
                                                precision_score=precision)
            
            print(metrics_artifact)
            print(best_model_details.best_score)
            print(best_model_details.best_parameters)
            
            return best_model_details, metrics_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def init_best_model(self):
        try:
            train_arr = load_numpy_array(self.data_transformation_artifact.transform_train_file)
            test_arr = load_numpy_array(self.data_transformation_artifact.transform_test_file)

            best_model_details, metrics_artifact = self.get_best_model_indentify(train_arr, test_arr)
            transform_object = load_object(self.data_transformation_artifact.transform_object)
            print(best_model_details)
            print(metrics_artifact)
            if best_model_details.best_score < self.model_trainer_config.excepted_ratio:
                logging.info("Best model not found with expected accuracy.")

            network_model_obj = Network_model(transform_object, best_model_details)
            save_object(self.model_trainer_config.model_trained_path, network_model_obj)

            model_trainer_artifact = Model_Trainer_Artifact(
                model_pkl=self.model_trainer_config.model_trained_path,
                metrics=metrics_artifact
            )

            return model_trainer_artifact
        except Exception as e:
                raise NetworkSecurityException(e,sys)


