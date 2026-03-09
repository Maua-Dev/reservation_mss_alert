from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct
from aws_cdk.aws_apigateway import RestApi, Cors, CorsOptions, GatewayResponse, ResponseType

from .lambda_stack import LambdaStack
from .sm_stack import SmStack
from .dynamo_stack import DynamoStack

import os

class IacStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        outside_tags = kwargs.get("tags", {})
        stage = outside_tags.get("stage")
        
        cors_options = CorsOptions(
            allow_origins =
                [
                    "https://reservation.maua.br",
                    "https://reservation.devmaua.com"
                ] 
            if stage == 'PROD'
            else 
                [
                    "https://reservation.hml.devmaua.com",
                    "https://reservation.dev.devmaua.com",
                    "https://localhost:3000",
                    "http://localhost:3000"
                ],
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allow_headers=Cors.DEFAULT_HEADERS
        )
        
        self.rest_api = RestApi(
            self, 
            f"{self.stack_name}_RestApi_{stage}",
            rest_api_name=f"{self.stack_name}_RestApi_{stage}",
            description=f"This is the {self.stack_name} {stage} RestApi",
            default_cors_preflight_options=cors_options
        )
        
        GatewayResponse(
            self,
            "AuthorizerDenyResponse",
            rest_api=self.rest_api,
            type=ResponseType.ACCESS_DENIED,
            response_headers={
                "Access-Control-Allow-Origin": "'*'",
                "Access-Control-Allow-Headers": "'*'",
                "Access-Control-Allow-Methods": "'*'",
            },
            status_code="403"
        )
        
        GatewayResponse(
            self,
            "AuthorizerUnauthorizedResponse",
            rest_api=self.rest_api,
            type=ResponseType.UNAUTHORIZED,
            response_headers={
                "Access-Control-Allow-Origin": "'*'",
                "Access-Control-Allow-Headers": "'*'",
                "Access-Control-Allow-Methods": "'*'",
            },
            status_code="401"
        )

        api_gateway_resource = self.rest_api.root.add_resource(
            "reservation-mss-alert", 
            default_cors_preflight_options=cors_options
        )

        self.dynamo_table = DynamoStack(self)
                
        ENVIRONMENT_VARIABLES = {
            "STAGE": stage,
            "DYNAMO_TABLE_NAME": self.dynamo_table.table.table_name,
            "DYNAMO_PARTITION_KEY": "PK",
            "DYNAMO_SORT_KEY": "SK",
            "REGION": self.region,
            "STACK_NAME": self.stack_name,
            "USER_API_URL": os.environ.get("USER_API_URL")
        }
        
        self.sm_stack = SmStack(self, environment_variables=ENVIRONMENT_VARIABLES)
        
        ENVIRONMENT_VARIABLES["EVENT_SECRET_ARN"] = self.sm_stack.event_secret.secret_arn

        self.lambda_stack = LambdaStack(
            self,
            api_gateway_resource=api_gateway_resource,
            environment_variables=ENVIRONMENT_VARIABLES,
            sm_stack=self.sm_stack
        )

        for function in self.lambda_stack.functions_that_need_dynamo_permissions:
            self.dynamo_table.table.grant_read_write_data(function)

        