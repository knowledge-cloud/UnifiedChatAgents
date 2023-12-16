from aws_cdk import (Stack, aws_dynamodb as _dynamodb)
from constructs import Construct

class DynamodbStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        clients_table = _dynamodb.Table(
            self,
            "Clients",
            table_name="clients",
            partition_key=_dynamodb.Attribute(
                name="organization_id",
                type=_dynamodb.AttributeType.STRING
            ),
            sort_key=_dynamodb.Attribute(
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
                name="client_id",
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