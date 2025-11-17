from src.modules.create_alert.app.create_alert_controller import CreateAlertController
from src.modules.create_alert.app.create_alert_usecase import CreateAlertUsecase
from src.shared.infra.repositories.alert_repository_mock import AlertRepositoryMock
from src.shared.helpers.external_interfaces.http_models import HttpRequest
import time

class TestCreateAlertController:
    
    def test_create_alert_controller(self):
        
        repo = AlertRepositoryMock()
        
        usecase = CreateAlertUsecase(repo=repo)
        
        controller = CreateAlertController(usecase=usecase)
        
        request = HttpRequest(
            body= {
                "title": "Titulo",
                "description": "Description",
                "start_date": int(time.time()),
                "end_date": int(time.time()) + 720000,
                # "severity": 2
                "is_rule": True,
                "user_from_authorizer": {
                    "role": "ADMIN"
                    # aqui vem outros parametros, por motivos de pratica nao foram colocados
                }
            }
        )
        
        alert = controller(
            request=request
        )
        
        
        
        