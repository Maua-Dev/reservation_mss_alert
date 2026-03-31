from aws_cdk import aws_apigateway as apigateway
from constructs import Construct
from aws_cdk.aws_apigateway import RestApi, Cors, CorsOptions, GatewayResponse, ResponseType

class ApigwConstruct(Construct):
    rest_api: RestApi
    
    def __init__(
        self, 
        scope: Construct,
        construct_id: str,
        stage: str,
        stack_name: str,
        **kwargs
    ):
        
        super().__init__(scope, construct_id, **kwargs)
        
        self.stage = stage
        
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
            id=f"{stack_name}_RestApi_{self.stage}",
            rest_api_name=f"{stack_name}_RestApi_{self.stage}",
            description=f"This is the ReservationMssAlert RestApi for {self.stage}",
            deploy_options=apigateway.StageOptions(
                stage_name=stage.lower(),
                logging_level=apigateway.MethodLoggingLevel.OFF,
                data_trace_enabled=False,
                metrics_enabled=True,
            ),
            default_cors_preflight_options=cors_options,
        )
        
        self.api_gateway_resource = self.rest_api.root.add_resource(
            "reservation-mss-alert", 
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
