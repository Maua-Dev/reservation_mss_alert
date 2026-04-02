import json
from aws_cdk import (
    aws_secretsmanager as secretsmanager,
)
from constructs import Construct

class SmConstruct(Construct):
    
    event_secret: secretsmanager.ISecret
    
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        stage: str,
        stack_name: str,
        environment_variables: dict,
        **kargs
    ):
        
        super().__init__(scope, construct_id, **kargs)
        
        self.event_secret = secretsmanager.Secret(
            self,
            id=f"{stack_name}_EventBridgeDeleteSecret",
            secret_name=f"event_bridge_delete_secret_{stack_name}_{stage}".lower(),
            description="Secret used to sign EventBridge delete triggers in reservation mss alerts",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template=json.dumps({"EVENT_SECRET": ""}),
                generate_string_key="EVENT_SECRET",
                password_length=64,
                exclude_punctuation=True
            )
        )
        
        
