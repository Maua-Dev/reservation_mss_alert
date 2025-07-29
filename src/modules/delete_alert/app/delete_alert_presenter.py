
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse


def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data=event)
    httpResponse = LambdaHttpResponse(status_code=200, body={"message": f"salve ben10 rl zona norte{str(httpRequest.body)}"}, headers={})

    return httpResponse.toDict()