from src.modules.update_alert.app.update_alert_usecase import UpdateAlertUsecase
from src.modules.update_alert.app.update_alert_viewmodel import UpdateAlertViewmodel
from src.modules.update_alert.app.update_alert_controller import UpdateAlertController
from src.shared.infra.repositories.alert_repository_mock import AlertRepositoryMock
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
import json

repo = Environments.get_alert_repo()()
usecase = UpdateAlertUsecase(repo=repo)
controller = UpdateAlertController(usecase=usecase)

def lambda_handler(event, context):
        httpRequest = LambdaHttpRequest(data=event)

        user_info_string = event.get('requestContext', {}).get('authorizer', {}).get('user')
        if user_info_string:
            try:
                user_data = json.loads(user_info_string).get('user')
                httpRequest.data['user_from_authorizer'] = user_data
            except (json.JSONDecodeError, AttributeError):
                 httpRequest.data['user_from_authorizer'] = None
        else:
            httpRequest.data['user_from_authorizer'] = None

        response = controller(request=httpRequest)
        httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

        return httpResponse.toDict()