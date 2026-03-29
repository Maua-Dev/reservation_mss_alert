from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct
from aws_cdk.aws_apigateway import RestApi, Cors, CorsOptions, GatewayResponse, ResponseType

from components.lambda_construct import LambdaConstruct
from components.sm_construct import SmConstruct
from components.dynamo_construct import DynamoConstruct
from components.ssm_construct import SsmConstruct
from components.apigw_construct import ApigwConstruct


import os

class IacStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        outside_tags = kwargs.get("tags", {})
        stage = outside_tags.get("stage")
        
        self.apigw_construct = ApigwConstruct(
            self,
            construct_id="ReservationMssAlertApigw",
            stage=stage
        )

        self.dynamo_table = DynamoConstruct(
            self,
            construct_id="ReservationMssAlertDynamo",
            stage=stage
        )
                
        ENVIRONMENT_VARIABLES = {
            "STAGE": stage,
            "DYNAMO_TABLE_NAME": self.dynamo_table.table.table_name,
            "DYNAMO_PARTITION_KEY": "PK",
            "DYNAMO_SORT_KEY": "SK",
            "REGION": self.region,
            "STACK_NAME": self.stack_name,
            "USER_API_URL": os.environ.get("USER_API_URL")
        }
        
        self.sm_construct = SmConstruct(
            self,
            construct_id="ReservationMssAlertSecretsManager",
            stage=stage,
            environment_variables=ENVIRONMENT_VARIABLES,
        )
        
        ENVIRONMENT_VARIABLES["EVENT_SECRET_ARN"] = self.sm_construct.event_secret.secret_arn

        self.lambda_construct = LambdaConstruct(
            self,
            construct_id="ReservationMssAlertLambda",
            api_gateway_resource=self.apigw_construct.api_gateway_resource,
            sm_construct=self.sm_construct,
            environment_variables=ENVIRONMENT_VARIABLES
        )

        for function in self.lambda_stack.functions_that_need_dynamo_permissions:
            self.dynamo_table.table.grant_read_write_data(function)

        