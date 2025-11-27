
from src.modules.get_alert.app.get_alert_presenter import lambda_handler, repo
import json

class TestGetAlertPresenter:
    def test_get_alert_presenter(self):
        
        id = repo.alerts[1].alert_id
        
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "parameter1=value1&parameter1=value2&parameter2=value",
            "cookies": [
                "cookie1",
                "cookie2"
            ],
            "queryStringParameters": {
                "alert_id": id
            },
            "headers": {
                "header1": "value1",
                "header2": "value1,value2"
            },
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {},
                "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
                "domainPrefix": "<url-id>",
                "external_interfaces": {
                    "method": "GET",
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
            "body":{},
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
            }
        
        response = lambda_handler(event, None)
        print("Response Body:", response.get("body"))
        
        assert response['statusCode'] == 200
        assert json.loads(response['body'])['message'] == "the alert was retrieved successfully"
        assert json.loads(response['body'])['alert_id'] == repo.alerts[1].alert_id
        assert json.loads(response['body'])['title'] == repo.alerts[1].title
        assert json.loads(response['body'])['description'] == repo.alerts[1].description
        assert json.loads(response['body'])['start_date'] == repo.alerts[1].start_date
        assert json.loads(response['body'])['end_date'] == repo.alerts[1].end_date
        assert json.loads(response['body'])['is_rule'] == repo.alerts[1].is_rule
        
        