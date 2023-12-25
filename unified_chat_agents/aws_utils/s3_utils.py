import boto3
from utils.log_utils import logger
import os

class S3Utils:
    
    @staticmethod
    def download_to_directory(bucket_name: str, directory: str) -> None:
        logger.info(f"S3Utils:: downloading bucket:{bucket_name} to directory:{directory}")
        s3 = boto3.client('s3')
        objects = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' not in objects:
            logger.info(f"S3Utils:: bucket:{bucket_name} is empty")
            return
        
        for obj in objects['Contents']:
            path = os.path.join(directory, obj['Key'])
            if not os.path.exists(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))
            s3.download_file(bucket_name, obj['Key'], path)
        return
    
    @staticmethod
    def upload_diretory(bucket_name: str, directory: str) -> None:
        logger.info(f"S3Utils:: uploading directory:{directory} to bucket:{bucket_name}")
        s3 = boto3.client('s3')
        for root, _, files in os.walk(directory):
            for filename in files:
                local_path = os.path.join(root, filename)
                relative_path = os.path.relpath(local_path, directory)
                s3_path = os.path.join(directory, relative_path)
                s3.upload_file(local_path, bucket_name, s3_path)
                logger.info(f"S3Utils:: uploaded file:{local_path} to s3_path:{s3_path}")
        return
    
    @staticmethod
    def empty_bucket(bucket_name: str) -> None:
        logger.info(f"S3Utils:: emptying bucket:{bucket_name}")
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        bucket.objects.all().delete()
        return