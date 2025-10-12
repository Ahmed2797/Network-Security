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
import mlflow
import sys
import dagshub
dagshub.init(repo_owner='Ahmed2797', repo_name='Network-Security', mlflow=True)


class Network_model:
    def __init__(self, transform_object: Pipeline, best_model_details: object):
        self.transform_object = transform_object
        self.best_model_details = best_model_details

    def predict(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        try:
            transformed_features = self.transform_object.transform(dataframe)
            predictions = self.best_model_details.predict(transformed_features)

            return pd.DataFrame(predictions, columns=['prediction'])
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def __repr__(self):
        return f"{type(self.best_model_details).__name__}()"

    def __str__(self):
        return f"{type(self.best_model_details).__name__}()"

class Model_Train:
    def __init__(self, data_transformation_artifact: Data_Transformation_Artifact,
                 model_trainer_config: Model_Trainer_Config):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config 
    
    def track_mlflow(self,best_model,metrics_artifact):
        try:
            with mlflow.start_run():
                f1 = metrics_artifact.f1_score
                precision = metrics_artifact.precision_score
                accuracy = metrics_artifact.accuracy_score
                recall = metrics_artifact.recall_score

                mlflow.log_metric('f1_score', f1)
                mlflow.log_metric('precision_score', precision)
                mlflow.log_metric('accuracy_score', accuracy)
                mlflow.log_metric('recall_score', recall)
                try:
                    mlflow.sklearn.log_model(best_model,'model')
                except Exception as e:
                    logging.info(f"[WARNING] Failed to log model to MLflow/DagsHub: {e}")
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
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
            # track_mlflow
            self.track_mlflow(best_model,metrics_artifact)
            
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


