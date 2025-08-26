from .get_all_alerts_controller import GetAllAlertsController
from .get_all_alerts_usecase import GetAllAlertsUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo = Environments.get_alert_repo()()
usecase = GetAllAlertsUsecase(repo)
controller = GetAllAlertsController(usecase)


def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()
