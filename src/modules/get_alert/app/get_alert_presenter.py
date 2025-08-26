from .get_alert_controller import GetAlertController
from .get_alert_usecase import GetAlertUseCase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

observability = Environments.get_observability()(module_name="get_alert")

repo = Environments.get_alert_repo()()
usecase = GetAlertUseCase(repo=repo, observability=observability)
controller = GetAlertController(usecase=usecase, observability=observability)

@observability.presenter_decorators
def get_alert_presenter(event):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    return httpResponse.toDict()

@observability.handler_decorators
def lambda_handler(event, context):
    
    response = get_alert_presenter(event)
    
    observability.add_metric(name="ErrorCount", unit="Count", value=1) if response["statusCode"] != 200 else None 
    
    return response