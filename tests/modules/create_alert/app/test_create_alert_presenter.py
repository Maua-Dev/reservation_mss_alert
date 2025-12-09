from src.modules.create_alert.app.create_alert_presenter import lambda_handler
from src.shared.infra.repositories.alert_repository_mock import AlertRepositoryMock
import json


class TestCreateAlertPresenter:
    def test_create_alert_presenter(self):

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
                                    "user_id": "c8435c66-13a4-4641-9d54-773b4b8ccc98",
                                    "role": "ADMIN"
                                },
                                "message": "the user was retrieved"
                            })
                        },
                        "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
                        "domainPrefix": "<url-id>",
                        "external_interfaces": {
                            "method": "POST",
                            "path": "/my/path",
                            "protocol": "HTTP/1.1",
                            "sourceIp": "123.123.123.123",
                            "userAgent": "agent"
                        },
                        "requestId": "id",
                        "routeKey": "$default",
                        "stage": "$default",
                        "time": "12/Mar/2020:19:03:58 +0000",
                        "timeEpoch": 1583348638390
                    },
                    "body": {
                             "title": test_alert.title, 
                             "description": test_alert.description, 
                             "start_date": test_alert.start_date, 
                             "end_date": test_alert.end_date,
                             "is_rule": test_alert.is_rule},
                    "pathParameters": None,
                    "isBase64Encoded": None,
                    "stageVariables": None
        }
        
        response = lambda_handler(event, None)
        print(response)
        
        assert response['statusCode'] == 201
        assert json.loads(response["body"])["Alert"]["title"] == test_alert.title
        assert json.loads(response["body"])["Alert"]["description"] == test_alert.description
        assert json.loads(response["body"])["Alert"]["start_date"] == test_alert.start_date
        assert json.loads(response["body"])["Alert"]["end_date"] == test_alert.end_date
        assert json.loads(response["body"])["Alert"]["is_rule"] == test_alert.is_rule
        assert json.loads(response["body"])["Message"] == "The alert was created successfully"
        
        