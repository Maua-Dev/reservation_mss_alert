from src.modules.create_alert.app.create_alert_viewmodel import CreateAlertViewmodel
from src.shared.infra.repositories.alert_repository_mock import AlertRepositoryMock


class TestCreateAlertViewModel:
    
    def test_create_alert_viewmodel(self):
        
        repo = AlertRepositoryMock()
        
        test_alert = repo.alerts[0]
        
        viewmodel = CreateAlertViewmodel(alert = test_alert)
        
        assert viewmodel.alert_id == test_alert.alert_id
        assert viewmodel.title == test_alert.title
        assert viewmodel.description == test_alert.description
        assert viewmodel.start_date == test_alert.start_date
        assert viewmodel.end_date == test_alert.end_date
        assert viewmodel.is_rule == test_alert.is_rule
        
        
        
        
        
        
        