from src.modules.get_all_alerts.app.get_all_alerts_controller import GetAllAlertsController
from src.modules.get_all_alerts.app.get_all_alerts_usecase import GetAllAlertsUsecase
from src.shared.infra.repositories.alert_repository_mock import AlertRepositoryMock
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.environments import Environments

observability = Environments.get_observability()(module_name="get_alert")

class TestGetAllAlertsController:
    
    def test_get_all_alerts_controller(self):
        
        repo = AlertRepositoryMock()
        
        usecase = GetAllAlertsUsecase(repo=repo)
        
        controller = GetAllAlertsController(usecase=usecase)
        
        id = repo.alerts[0].alert_id
        
        request = HttpRequest()
        
        alerts = controller(
            request=request
        )
        
        assert alerts.status_code == 200        
        