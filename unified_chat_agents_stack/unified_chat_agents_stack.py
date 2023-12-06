from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
)
from constructs import Construct
from aws_cdk.aws_apigateway import (
    LambdaIntegration,
    RestApi,
)


class UnifiedChatAgentsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        unified_chat_agents_function = _lambda.DockerImageFunction(
            self,
            id="UnifiedChatAgents",
            function_name="UnifiedChatAgentsAPI",
            code=_lambda.DockerImageCode.from_image_asset(directory=""),
            architecture=_lambda.Architecture.ARM_64,
        )

        api = RestApi(
            self, "UnifiedChatAgentsAPIGateway", rest_api_name="UnifiedChatAgentsAPIGateway", default_integration=LambdaIntegration(unified_chat_agents_function))
        api.root.add_resource("chat").add_method(
            "POST",
            LambdaIntegration(unified_chat_agents_function)
        )