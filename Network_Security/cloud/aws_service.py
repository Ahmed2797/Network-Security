from Network_Security.configeration.aws_connection import S3Client


from typing import List,Union
from io import StringIO
import pickle
class SimpleStorageService:
    def __init__(self):
        s3_client = S3Client()
        self.s3_client = s3_client.s3_client
        self.resource = s3_client.resource

    def s3_key_path_available(self,bucket_name,s3_key)->bool:
        bucket = self.resource.Bucket(bucket_name)
        file_object = [file_object for file_object in bucket.objects.filter(prefix=s3_key)]
        if len(file_object)>0:
            return True 
        else:
            return False  
    def get_file_object(self,bucket_name,model_path)->Union[List[object],object]:
        bucket = self.resource.Bucket(bucket_name)
        file_object = [file_object for file_object in bucket.objects.filter(prefix=model_path)]
        func = lambda x:x[0] if len(x)==1 else x
        file_obj = func(file_object)
        return file_obj


    @staticmethod
    def read_object(file_object,decode: bool=True,model_readable: bool=False):
        func = (lambda:file_object.get()['Body'].read().decode()
                if decode is True 
                else file_object.get()['Body'].read())
        conv_func = lambda:StringIO(func()) if model_readable is True else func()
        return conv_func 
    
    def load_model(self,bucket_name,model_name,model_dir=None):
        func = (lambda: model_name
                if model_dir is None
                else model_dir + '/' + model_name)
        model_path = func()
        file_object = self.get_file_object(bucket_name=bucket_name,model_path=model_path)
        model_object = self.read_object(file_object,decode=False)
        model = pickle.load(model_object)
        return model

