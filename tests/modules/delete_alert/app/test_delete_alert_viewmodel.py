from src.modules.delete_alert.app.delete_alert_viewmodel import DeleteAlertViewmodel
from src.shared.infra.repositories.alert_repository_mock import AlertRepositoryMock 

class TestDeleteAlertViewmodel:
    def test_delete_alert_viewmodel(self):
        repo = AlertRepositoryMock()
        test_alert = repo.alerts[0]
        viewmodel = DeleteAlertViewmodel(alert=test_alert)
        viewmodel_dict = viewmodel.to_dict()
        
        assert viewmodel_dict["alert"]["title"] == test_alert.title
        assert viewmodel_dict["alert"]["description"] == test_alert.description
        assert viewmodel_dict["alert"]["start_date"] == test_alert.start_date
        assert viewmodel_dict["alert"]["end_date"] == test_alert.end_date
        assert viewmodel_dict["alert"]["is_rule"] == test_alert.is_rule
    