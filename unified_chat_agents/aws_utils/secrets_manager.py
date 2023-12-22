import boto3
from botocore.exceptions import ClientError
from utils.log_utils import logger
import json
from typing import Dict


class SecretsManager:

    @staticmethod
    def get_secret(secret_name: str) -> Dict[str, str]:
        try:
            logger.info(f"SecretsManager:: fetching secret:{secret_name}")
            client = boto3.session.Session().client(
                service_name='secretsmanager',
                region_name="ap-south-1"
            )
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
            secret_string = get_secret_value_response['SecretString']
            secret_json = json.loads(secret_string)
            return secret_json
        except ClientError as e:
            logger.error(f"SecretsManager::get_secret failed with {e.response}")
            raise e
            

