from src.modules.get_alert.app.get_alert_controller import GetAlertController
from src.modules.get_alert.app.get_alert_usecase import GetAlertUseCase
from src.shared.infra.repositories.alert_repository_mock import AlertRepositoryMock
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.environments import Environments

observability = Environments.get_observability()(module_name="get_alert")

class TestGetAlertController:
    
    def test_get_alert_controller(self):
        
        repo = AlertRepositoryMock()
        
        usecase = GetAlertUseCase(repo=repo, observability=observability)
        
        controller = GetAlertController(usecase=usecase, observability=observability)
        
        id = repo.alerts[0].alert_id
        
        request = HttpRequest(
            query_params= {
                "alert_id": id
            }
        )
        
        alert = controller(
            request=request
        )
        
        