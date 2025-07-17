import os
from aws_cdk import (
    aws_lambda as lambda_,
    NestedStack, Duration,
    aws_apigateway as apigw
)
from constructs import Construct
from aws_cdk.aws_apigateway import Resource, LambdaIntegration


class LambdaStack(Construct):
    functions_that_need_dynamo_permissions = []

    def create_lambda_api_gateway_integration(self, module_name: str, method: str, mss_alert_api_resource: Resource,
                                              environment_variables: dict = {"STAGE": "TEST"}):
        function = lambda_.Function(
            self, module_name.title(),
            code=lambda_.Code.from_asset(f"../src/modules/{module_name}"),
            handler=f"app.{module_name}_presenter.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            layers=[self.lambda_layer, self.lambda_power_tools],
            environment=environment_variables,
            timeout=Duration.seconds(15)
        )

        mss_alert_api_resource.add_resource(module_name.replace("_", "-")).add_method(method,
                                                                                        integration=LambdaIntegration(
                                                                                            function))

        return function

    def __init__(self, scope: Construct, api_gateway_resource: Resource, environment_variables: dict) -> None:
        
        stage = environment_variables.get("STAGE", "errorStage")
        stack_name = environment_variables.get("STACK_NAME", "errorStackName")
        
        super().__init__(scope, f"{stack_name}_LambdaStack_{stage}")

        self.lambda_layer = lambda_.LayerVersion(self, f"{stack_name}_LambdaLayer_{stage}",
                                                 code=lambda_.Code.from_asset("./lambda_layer_out_temp"),
                                                 compatible_runtimes=[lambda_.Runtime.PYTHON_3_9]
                                                 )
        
        self.lambda_region = environment_variables.get("REGION", 'sa-east-1')
        self.lambda_power_tools = lambda_.LayerVersion.from_layer_version_arn(self, "Lambda_Power_Tools",
                                                                              layer_version_arn=f"arn:aws:lambda:{self.lambda_region}:017000801446:layer:AWSLambdaPowertoolsPythonV2:22")

        # authorizer_lambda = lambda_.Function(
        #     self, "AuthorizerUserMssReservationMssAlertLambda",
        #     code=lambda_.Code.from_asset("../src/shared/authorizer"),
        #     handler="authorizer_user_mss.lambda_handler",
        #     runtime=lambda_.Runtime.PYTHON_3_9,
        #     layers=[self.lambda_layer, self.lambda_power_tools],
        #     environment=environment_variables,
        #     timeout=Duration.seconds(15)
        # )

        # token_authorizer_lambda = apigw.TokenAuthorizer(
        #     self, "TokenAuthorizerReservationMssUser",
        #     handler=authorizer_lambda,
        #     identity_source=apigw.IdentitySource.header("Authorization"),
        #     authorizer_name="AuthorizerUserMssReservationMssAlertLambda",
        #     results_cache_ttl=Duration.seconds(0)
        # )
        
        self.delete_alert = self.create_lambda_api_gateway_integration(
            module_name="create_alert",
            method="POST",
            mss_alert_api_resource=api_gateway_resource,
            environment_variables=environment_variables
        )
        
        env_vars_for_create = environment_variables.copy()
        env_vars_for_create["DELETE_ALERT_LAMBDA_ARN"] = self.delete_alert.function_arn
        
        self.create_alert = self.create_lambda_api_gateway_integration(
            module_name="create_alert",
            method="POST",
            mss_alert_api_resource=api_gateway_resource,
            environment_variables=env_vars_for_create
        )
        
        self.delete_alert.grant_invoke(self.create_alert)
        self.functions_that_need_dynamo_permissions = []
