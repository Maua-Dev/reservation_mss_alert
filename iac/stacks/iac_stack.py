from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct
from aws_cdk.aws_apigateway import RestApi, Cors

from .lambda_stack import LambdaStack
from .dynamo_stack import DynamoStack

import os

class IacStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        outside_tags = kwargs.get("tags", {})
        stage = outside_tags.get("stage")
        
        self.rest_api = RestApi(self, f"{self.stack_name}_RestApi_{stage}",
                                    rest_api_name=f"{self.stack_name}_RestApi_{stage}",
                                    description=f"This is the {self.stack_name} {stage} RestApi",
                                    default_cors_preflight_options=
                                    {
                                        "allow_origins": Cors.ALL_ORIGINS,
                                        "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                                        "allow_headers": ["*"]
                                    },
                                )

        api_gateway_resource = self.rest_api.root.add_resource("reservation-mss-alert", default_cors_preflight_options=
        {
            "allow_origins": Cors.ALL_ORIGINS,
            "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": Cors.DEFAULT_HEADERS
        }
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


        self.lambda_stack = LambdaStack(self, api_gateway_resource=api_gateway_resource,
                                        environment_variables=ENVIRONMENT_VARIABLES)

        for function in self.lambda_stack.functions_that_need_dynamo_permissions:
            self.dynamo_table.table.grant_read_write_data(function)

        