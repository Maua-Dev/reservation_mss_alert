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

    def create_lambda_api_gateway_integration(self, module_name: str, method: str, mss_student_api_resource: Resource,
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

        mss_student_api_resource.add_resource(module_name.replace("_", "-")).add_method(method,
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
        
        self.lambda_power_tools = lambda_.LayerVersion.from_layer_version_arn(self, "Lambda_Power_Tools", layer_version_arn="arn:aws:lambda:us-east-2:017000801446:layer:AWSLambdaPowertoolsPythonV2:22")
        
        authorizer_lambda = lambda_.Function(
            self, "AuthorizerUserMssReservationMssAlertLambda",
            code=lambda_.Code.from_asset("../src/shared/authorizer"),
            handler="authorizer_user_mss.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            layers=[self.lambda_layer, self.lambda_power_tools],
            environment=environment_variables,
            timeout=Duration.seconds(15)
        )

        token_authorizer_lambda = apigw.TokenAuthorizer(
            self, "TokenAuthorizerReservationMssUser",
            handler=authorizer_lambda,
            identity_source=apigw.IdentitySource.header("Authorization"),
            authorizer_name="AuthorizerUserMssReservationMssAlertLambda",
            results_cache_ttl=Duration.seconds(0)
        )

        self.functions_that_need_dynamo_permissions = []
