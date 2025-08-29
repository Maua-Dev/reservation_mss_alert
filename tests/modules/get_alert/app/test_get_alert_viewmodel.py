from src.modules.get_alert.app.get_alert_viewmodel import GetAlertViewmodel
from src.shared.infra.repositories.alert_repository_mock import AlertRepositoryMock
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.environments import Environments

class TestGetAlertViewModel:
    def test_get_alert_viewmodel(self):
        repo = AlertRepositoryMock()
        alert_test = repo.alerts[0]
        viewmodel = GetAlertViewmodel(alert=alert_test)
        viewmodel_dict = viewmodel.to_dict()
        
        assert viewmodel_dict.get('alert_id') == alert_test.alert_id
        assert viewmodel_dict.get('title') == alert_test.title
        assert viewmodel_dict.get('description') == alert_test.description
        assert viewmodel_dict.get('start_date') == alert_test.start_date
        assert viewmodel_dict.get('end_date') == alert_test.end_date
        assert viewmodel_dict.get('is_rule') == alert_test.is_rule
            
    