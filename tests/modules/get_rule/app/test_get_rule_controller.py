from src.modules.get_rule.app.get_rule_controller import GetRuleController
from src.modules.get_rule.app.get_rule_usecase import GetRuleUsecase
from src.shared.infra.repositories.alert_repository_mock import AlertRepositoryMock
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.environments import Environments

class TestGetRuleController:
    
    def test_get_rule_controller(self):
        
        repo = AlertRepositoryMock()
        
        usecase = GetRuleUsecase(repo=repo)
        
        controller = GetRuleController(usecase=usecase)
        
        id = repo.alerts[0].alert_id
        
        request = HttpRequest(
            query_params= {
                "rule_id": id
            }
        )
        
        alert = controller(
            request=request
        )
        
        assert alert.status_code == 200
        
        