from Network_Security.cloud.aws_service import SimpleStorageService
#from Network_Security.components.model_train import Network_model
from Network_Security.entity.estimator import Network_model

class NetworkEstimator:
    def __init__(self,bucket_name,model_path):
        self.model_path = model_path 
        self.bucket_name = bucket_name
        self.s3 = SimpleStorageService() 
        self.loaded_model:Network_model=None

    def is_model_present(self,model_path):
     return self.s3.s3_key_path_available(bucket_name=self.bucket_name,
                                          model_path=model_path)
    def load_model(self)->Network_model:
        model_pkl = self.s3.load_model(bucket_name=self.bucket_name,
                                  model_name=self.model_path)
        return model_pkl