from Network_Security.entity.artifact import (Data_Ingestion_Artifact,
                                              Model_Trainer_Artifact,
                                              Model_Evalution_Artifact)
from Network_Security.entity.config import Model_Evalution_Config
from Network_Security.entity.s3_estimator import NetworkEstimator
from Network_Security.constant import TARGET_COLUMN
from sklearn.metrics import f1_score
from dataclasses import dataclass
import pandas as pd

@dataclass 
class ModelEvalutionResponse:
    is_model_accept:bool
    difference:float 
    train_model_f1_score:float 
    s3_model_f1_score:float 

class ModelEvalution:
    def __init__(self,data_ingestion_artifact:Data_Ingestion_Artifact ,
                 model_trainer_artifact:Model_Trainer_Artifact,
                 model_evalution_config:Model_Evalution_Config):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.model_trainer_artifact = model_trainer_artifact
        self.model_evalution_config = model_evalution_config

    def get_best_model(self):
        bucket_name = self.model_evalution_config.bucket_name 
        model_path = self.model_evalution_config.s3_model_path 
        network_model = NetworkEstimator(bucket_name,model_path)
        if network_model.is_model_present(model_path):
            # return network_model.load_model()
            return True
        return None 
    def evaluate_model(self):
        test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
        x = test_df.drop([TARGET_COLUMN],axis=1)
        y = test_df[TARGET_COLUMN]
        y = y.replace(-1,0) 
        best_model = self.get_best_model()
        best_model_score = None
         
        if best_model is not None:
            pred = best_model.predict(x)
            best_model_score = f1_score(y,pred)
        temp_model_score = 0 if best_model_score is None else best_model_score
        train_model_score = self.model_trainer_artifact.metrics.f1_score

        model_evalution_response = ModelEvalutionResponse(
            is_model_accept=train_model_score > temp_model_score,
            difference=train_model_score - temp_model_score,
            train_model_f1_score=train_model_score,
            s3_model_f1_score=best_model_score
        )
        return model_evalution_response
    
    def init_model_evaluation(self):
        model_evalution_response = self.evaluate_model()
        s3_model = self.model_evalution_config.s3_model_path 
        model_evalution_artifact = Model_Evalution_Artifact(
            is_model_accepted= model_evalution_response.is_model_accept,
            changed_accuracy=model_evalution_response.difference,
            s3_model_path=s3_model,
            train_model_path=self.model_trainer_artifact.model_pkl
        )
        return model_evalution_artifact

