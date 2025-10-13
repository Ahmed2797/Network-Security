import os
import boto3
from Network_Security.constant import (REGION,AWS_ACCESS_KEY,AWS_SECRET_KEY)
from dotenv import load_dotenv
load_dotenv()

class S3Client:
    s3_client = None
    s3_resource = None 

    def __init__(self, region_name=REGION):    
        _access_key = os.getenv(AWS_ACCESS_KEY)
        _secret_key = os.getenv(AWS_SECRET_KEY)  

        if _access_key is None or _secret_key is None:
            raise ValueError("Missing AWS credentials in environment variables")

        if S3Client.s3_client is None and S3Client.s3_resource is None:

            S3Client.s3_resource = boto3.resource(
                's3',
                aws_access_key_id=_access_key,
                aws_secret_access_key=_secret_key,
                region_name=region_name
            )
            S3Client.s3_client = boto3.client(
                's3',
                aws_access_key_id=_access_key,
                aws_secret_access_key=_secret_key,
                region_name=region_name
            )
        self.s3_client = S3Client.s3_client
        self.s3_resource = S3Client.s3_resource
