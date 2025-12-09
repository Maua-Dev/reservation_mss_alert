import pytest
import json
from src.shared.infra.repositories.alert_repository_mock import AlertRepositoryMock

from src.modules.update_alert.app.update_alert_presenter import lambda_handler

class TestUpdateAlertPresenter:
    def test_lambda_handler(self):
        repo = AlertRepositoryMock()
        test_alert = repo.alerts[1]
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "parameter1=value1&parameter1=value2&parameter2=value",
            "cookies": [
                "cookie1",
                "cookie2"
            ],
            "headers": {
                "header1": "value1",
                "header2": "value1,value2"
            },
            "queryStringParameters": {
                "parameter1": "1"
            },
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {
                    "user": json.dumps({
                        "user": {
                            'user_id': '1f25448b-3429-4c19-8287-d9e64f17bc3a',
                            'name': 'Nome',
                            'email': 'user@email.com',
                            'role': 'ADMIN'
                        },
                        "message": "the user was retrieved"
                    })
                },
                "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
                "domainPrefix": "<url-id>",
                "external_interfaces": {
                    "method": "PUT",
                    "path": "/my/path",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "123.123.123.123",
                    "userAgent": "agent"
                },
            },
            "body": {
                "alert_id":  test_alert.alert_id,
                "title" : test_alert.title,
                "description" : test_alert.description,
                "start_date": test_alert.start_date,
                "end_date": test_alert.end_date,
                "is_rule" : test_alert.is_rule
            },
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }
        response = lambda_handler(event, None)
        assert response['statusCode'] == 200
        