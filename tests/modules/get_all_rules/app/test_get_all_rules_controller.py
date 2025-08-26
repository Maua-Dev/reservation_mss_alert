from src.modules.get_all_rules.app.get_all_rules_controller import GetAllRulesController
from src.modules.get_all_rules.app.get_all_rules_usecase import GetAllRulesUsecase
from src.shared.infra.repositories.alert_repository_mock import AlertRepositoryMock
from src.shared.helpers.external_interfaces.http_models import HttpRequest

class TestGetAllRulesController:
    
    def test_get_all_rules_controller(self):
    
        repo = AlertRepositoryMock()
        
        usecase = GetAllRulesUsecase(repo=repo)
        
        controller = GetAllRulesController(usecase=usecase)
                
        request = HttpRequest()
        
        rules = controller(
            request=request
        )
        
        assert rules.status_code == 200
                
        