from aws_cdk import (
    aws_dynamodb as dynamodb, RemovalPolicy,
)
from constructs import Construct


class DynamoConstruct(Construct):
    
    table: dynamodb.Table

    def __init__(
        self, 
        scope: Construct, 
        construct_id: str, 
        stage: str,
        **kwargs
    ) -> None:
        
        super().__init__(
            scope, 
            construct_id, 
            **kwargs
        )
        
        # a criação da tabela deve corresponder com a configurada no arquivo src.infra.repositories.load_*_to_dynamo

        self.table = dynamodb.Table(
            self,
            id=f"ReservationMssAlertDynamoTable{stage.capitalize()}",
            partition_key=dynamodb.Attribute(
                name="PK",
                type=dynamodb.AttributeType.STRING,
            ),
            sort_key=dynamodb.Attribute(
                name="SK",
                type=dynamodb.AttributeType.STRING,
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=(
                RemovalPolicy.RETAIN if stage.lower() == "prod" else RemovalPolicy.DESTROY
            ),
        )
