from src.modules.update_alert.app.update_alert_viewmodel import UpdateAlertViewmodel
from src.shared.infra.repositories.alert_repository_mock import AlertRepositoryMock

class TestUpdateAlertViewmodel:
    def test_update_alert_viewmodel(self):
        repo = AlertRepositoryMock()
        test_alert = repo.alerts[0]
        viewmodel = UpdateAlertViewmodel(alert=test_alert)
        
        assert viewmodel.to_dict()["alert"]["new title"] == test_alert.title
        assert viewmodel.to_dict()["alert"]["new description"] == test_alert.description
        assert viewmodel.to_dict()["alert"]["new start_date"] == test_alert.start_date
        assert viewmodel.to_dict()["alert"]["new end_date"] == test_alert.end_date
        assert viewmodel.to_dict()["alert"]["new is_rule"] == test_alert.is_rule