from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
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
            timeout=Duration.seconds(30),
            environment={
                "WEAVIATE_URL": "https://unified-chat-agents-el9cpwl9.weaviate.network"
            }
        )

        api = RestApi(
            self, 
            "UnifiedChatAgentsAPIGateway", 
            rest_api_name="UnifiedChatAgentsAPIGateway", 
            default_integration=LambdaIntegration(unified_chat_agents_function)
        )
        api.root.add_resource("chat").add_method(
            "POST",
            LambdaIntegration(unified_chat_agents_function)
        )
        api.root.add_resource("docs").add_method(
            "POST",
            LambdaIntegration(unified_chat_agents_function)
        )

        class_name_resource = api.root.add_resource("{class_name}")
        class_name_resource.add_resource("docs").add_method(
            "GET",
            LambdaIntegration(unified_chat_agents_function)
        )
        class_name_resource.add_method(
            "DELETE",
            LambdaIntegration(unified_chat_agents_function)
        )

        unified_chat_agents_function.add_to_role_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["dynamodb:*"],
            resources=["*"]
        ))

        unified_chat_agents_function.add_to_role_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["secretsmanager:GetSecretValue"],
            resources=["*"]
        ))