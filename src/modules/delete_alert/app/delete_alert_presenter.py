
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
import json

def lambda_handler(event, context):
    
    print(json.dumps(event, indent=2))
    
    return {
        'statusCode': 200,
        'body': json.dumps('Evento recebido e registrado com sucesso pelo handler de debug.')
    }