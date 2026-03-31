from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct

from components.lambda_construct import LambdaConstruct
from components.sm_construct import SmConstruct
from components.dynamo_construct import DynamoConstruct
from components.ssm_construct import SsmConstruct
from components.apigw_construct import ApigwConstruct


import os

class IacStack(Stack):

    def __init__(
        self, 
        scope: Construct, 
        stack_id: str,
        stage: str,
        stack_name: str,
        **kwargs
    ) -> None:
    
        super().__init__(scope, stack_id, **kwargs)
        
        self.apigw_construct = ApigwConstruct(
            self,
            construct_id=f"{stack_name}_Apigw",
            stage=stage,
            stack_name=stack_name
        )

        self.dynamo_table = DynamoConstruct(
            self,
            construct_id=f"{stack_name}_Dynamo",
            stage=stage,
            stack_name=stack_name
        )
        
        self.ssm_construct = SsmConstruct(
            self,
            construct_id=f"{stack_name}_Ssm",
            stage=stage,
            stack_name=stack_name,
            # atenção para esse próximo parâmetro. de preferencia deixe tudo minusculo sem _
            # isso deve corresponder ao prefixo de caminho passado no CD dos outros mss (inclusive front)
            # que acessam os parametros no ssm.
            mss_name_identification_for_path="reservationmssalert",
            api=self.apigw_construct.rest_api,
            api_gateway_resource=self.apigw_construct.api_gateway_resource
        )
                
        ENVIRONMENT_VARIABLES = {
            "STAGE": stage.upper(),
            "DYNAMO_TABLE_NAME": self.dynamo_table.table.table_name,
            "DYNAMO_PARTITION_KEY": "PK",
            "DYNAMO_SORT_KEY": "SK",
            "REGION": self.region,
            "STACK_NAME": self.stack_name,
            "USER_API_URL": os.environ.get("USER_API_URL")
        }
        
        self.sm_construct = SmConstruct(
            self,
            construct_id=f"{stack_name}_Manager",
            stage=stage,
            stack_name=stack_name,
            environment_variables=ENVIRONMENT_VARIABLES,
        )
        
        ENVIRONMENT_VARIABLES["EVENT_SECRET_ARN"] = self.sm_construct.event_secret.secret_arn

        self.lambda_construct = LambdaConstruct(
            self,
            construct_id=f"{stack_name}_Lambda",
            stage=stage,
            stack_name=stack_name,
            api_gateway_resource=self.apigw_construct.api_gateway_resource,
            sm_construct=self.sm_construct,
            environment_variables=ENVIRONMENT_VARIABLES
        )

        for function in self.lambda_construct.functions_that_need_dynamo_permissions:
            self.dynamo_table.table.grant_read_write_data(function)

        