from aws_cdk import (Stack, aws_dynamodb as _dynamodb, aws_s3 as _s3)
from constructs import Construct


class DatabaseStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        clients_table = _dynamodb.Table(
            self,
            "Clients",
            table_name="clients",
            partition_key=_dynamodb.Attribute(
                name="id",
                type=_dynamodb.AttributeType.STRING
            ),
            billing_mode=_dynamodb.BillingMode.PAY_PER_REQUEST
        )

        sessions_table = _dynamodb.Table(
            self,
            "Sessions",
            table_name="sessions",
            partition_key=_dynamodb.Attribute(
                name="id",
                type=_dynamodb.AttributeType.STRING
            ),
            billing_mode=_dynamodb.BillingMode.PAY_PER_REQUEST
        )

        messages_table = _dynamodb.Table(
            self,
            "Messages",
            table_name="messages",
            partition_key=_dynamodb.Attribute(
                name="session_id",
                type=_dynamodb.AttributeType.STRING
            ),
            sort_key=_dynamodb.Attribute(
                name="created_at",
                type=_dynamodb.AttributeType.STRING
            ),
            billing_mode=_dynamodb.BillingMode.PAY_PER_REQUEST
        )

        chroma_db_bucket = _s3.Bucket(
            self,
            "VectorDB",
            bucket_name="uca-vector-store"
        )
