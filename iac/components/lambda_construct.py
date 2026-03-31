from typing import Optional
from aws_cdk import (
    aws_lambda as lambda_,
    Duration,
    aws_apigateway as apigw,
    Stack,
    aws_iam as iam,
    Aws
)
from constructs import Construct
from aws_cdk.aws_apigateway import Resource, LambdaIntegration, TokenAuthorizer


class LambdaConstruct(Construct):
    functions_that_need_dynamo_permissions: list
    stage: str
    stack_name: str

    def create_lambda_api_gateway_integration(
            self,
            module_name: str,
            method: str,
            mss_alert_api_resource: Resource,
            environment_variables: dict = {"STAGE": "TEST"},
            authorizer: Optional[TokenAuthorizer] = None
    ):
        function = lambda_.Function(
            self, 
            id=module_name.title(),
            function_name=f"{module_name}-{self.stack_name}-{self.stage}"[:63],
            code=lambda_.Code.from_asset(f"../src/modules/{module_name}"),
            handler=f"app.{module_name}_presenter.lambda_handler",
            runtime=lambda_.Runtime("python3.13"),
            layers=[self.lambda_layer, self.lambda_power_tools],
            environment=environment_variables,
            timeout=Duration.seconds(15)
        )

        mss_alert_api_resource.add_resource(
            module_name.replace("_", "-")
        ).add_method(
            method,
            integration=LambdaIntegration(
                function
            ),
            authorization_type=apigw.AuthorizationType.CUSTOM if authorizer else apigw.AuthorizationType.NONE,
            authorizer=authorizer
        )

        return function

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        stage: str,
        stack_name: str,
        api_gateway_resource: Resource,
        sm_construct: Construct,
        environment_variables: dict,
        **kargs,
    ) -> None:
        super().__init__(scope, construct_id, **kargs)
        
        self.stage = stage
        self.stack_name = stack_name

        self.lambda_layer = lambda_.LayerVersion(
            self, 
            id=f"{stack_name}_LambdaLayer_{stage}",
            layer_version_name=f"{stack_name}-LambdaLayer-{self.stage}",
            # a pasta .build foi obtida do adjust layer directory, certifique-se de que a configuração da pasta layer gerada la esta igual
            code=lambda_.Code.from_asset("./build"),
            compatible_runtimes=[lambda_.Runtime("python3.13")]
        )
        
        self.lambda_power_tools = lambda_.LayerVersion.from_layer_version_arn(
            self, 
            id=f"Lambda_Power_Tools-{stack_name}-{stage}",
            layer_version_arn=f"arn:aws:lambda:{Aws.REGION}:017000801446:layer:AWSLambdaPowertoolsPythonV3-python313-x86_64:30"
        )
        
        authorizer_lambda = lambda_.Function(
            self, 
            id=f"LambdaUserMssAuthorizer-{self.stack_name}-{self.stage}",
            function_name=f"lambda_user_mss_authorizer-{self.stack_name}-{self.stage}",
            code=lambda_.Code.from_asset("../src/shared/authorizer"),
            handler="user_mss_authorizer.lambda_handler",
            runtime=lambda_.Runtime("python3.13"),
            layers=[self.lambda_layer],
            environment=environment_variables,
            timeout=Duration.seconds(15)
        )

        token_authorizer_lambda = apigw.TokenAuthorizer(
            self, 
            id=f"TokenUserMssAuthorizer-{self.stack_name}-{self.stage}",
            authorizer_name=f"user_mss_authorizer-{self.stack_name}-{self.stage}",
            handler=authorizer_lambda,
            identity_source=apigw.IdentitySource.header("Authorization"),
            results_cache_ttl=Duration.seconds(0)
        )
        
        self.delete_alert = self.create_lambda_api_gateway_integration(
            module_name="delete_alert",
            method="DELETE",
            mss_alert_api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=token_authorizer_lambda
        )
        
        self.delete_alert.add_permission(
            "AllowEventBridgeToInvoke",
            principal=iam.ServicePrincipal("events.amazonaws.com"),
            action="lambda:InvokeFunction",
            source_arn=f"arn:aws:events:{Stack.of(self).region}:{Stack.of(self).account}:rule/one-time-trigger-*"
        )
        
        env_vars_with_arn = environment_variables.copy()
        env_vars_with_arn["DELETE_ALERT_LAMBDA_ARN"] = self.delete_alert.function_arn
        
        self.create_alert = self.create_lambda_api_gateway_integration(
            module_name="create_alert",
            method="POST",
            mss_alert_api_resource=api_gateway_resource,
            environment_variables=env_vars_with_arn,
            authorizer=token_authorizer_lambda
        )

        self.update_alert = self.create_lambda_api_gateway_integration(
            module_name="update_alert",
            method="PUT",
            mss_alert_api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=token_authorizer_lambda
        )
        
        # ALL LAMBDAS THAT USE EVENT BRIDGE CLIENT NEED READ ACCESS TO THE SECRET
        
        secret = sm_construct.event_secret
                
        secret.grant_read(self.create_alert)
        secret.grant_read(self.delete_alert)
        secret.grant_read(self.update_alert)
        
        # ALL LAMBDAS THAT USE EVENT BRIDGE CLIENT NEED READ ACCESS TO THE SECRET
        
        event_bridge_policy = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "events:PutRule",
                "events:PutTargets",
                "events:DeleteRule",
                "events:RemoveTargets",
                "events:DescribeRule"
            ],
            resources=[
                f"arn:aws:events:{Stack.of(self).region}:{Stack.of(self).account}:rule/one-time-trigger-*"
            ]
        )
        
        self.get_alert = self.create_lambda_api_gateway_integration(
            module_name="get_alert",
            method="GET",
            mss_alert_api_resource=api_gateway_resource,
            environment_variables=environment_variables,
        )
        
        self.get_all_alerts = self.create_lambda_api_gateway_integration(
            module_name="get_all_alerts",
            method="GET",
            mss_alert_api_resource=api_gateway_resource,
            environment_variables=environment_variables,
        )
        
        self.get_all_rules = self.create_lambda_api_gateway_integration(
            module_name="get_all_rules",
            method="GET",
            mss_alert_api_resource=api_gateway_resource,
            environment_variables=environment_variables,
        )
    
        self.create_alert.add_to_role_policy(event_bridge_policy)
        self.delete_alert.add_to_role_policy(event_bridge_policy)
        self.update_alert.add_to_role_policy(event_bridge_policy)
        
        self.functions_that_need_dynamo_permissions = [
            self.create_alert, 
            self.delete_alert,
            self.get_alert,
            self.get_all_alerts,
            self.get_all_rules,
            self.update_alert
        ]
