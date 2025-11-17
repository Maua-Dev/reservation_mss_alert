import json
import time
from src.modules.create_alert.app.create_alert_presenter import lambda_handler


class TestCreateAlertPresenter:
    
    def test_create_alert_presenter_success(self):
        
        event = event = {
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
                            "role": "ADMIN",
                            # aqui vem outros parametros, por motivos de pratica nao foram colocados
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
                "title": "Titulo",
                "description": "Description",
                "start_date": int(time.time()),
                "end_date": int(time.time()) + 720000,
                # "severity": 2
                "is_rule": True
            },
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }
        
        response = lambda_handler(event=event, context=None)
        
        assert response['statusCode'] == 200        
        