from src.modules.delete_alert.app.delete_alert_controller import DeleteAlertController
from src.modules.delete_alert.app.delete_alert_usecase import DeleteAlertUsecase
from src.shared.infra.repositories.alert_repository_mock import AlertRepositoryMock
from src.shared.helpers.external_interfaces.http_models import HttpRequest

class TestDeleteAlertController():
    
    def test_delete_alert_controller(self):
        
        repo = AlertRepositoryMock()
        
        usecase = DeleteAlertUsecase(repo=repo)
        
        controller = DeleteAlertController(usecase=usecase)
        
        id = repo.alerts[0].alert_id
        
        request = HttpRequest(
            body= {
                "alert_id": id,
                "user_from_authorizer": {
                    "role": "ADMIN"
                    # aqui tem mais campos, porem não são necessários para o teste
                }
            }
        )
        
        alert = controller(
            request=request
        )