from src.modules.get_all_alerts.app.get_all_alerts_viewmodel import GetAllAlertsViewmodel
from src.shared.infra.repositories.alert_repository_mock import AlertRepositoryMock

class TestGetAllAlertsViewmodel:
    def test_get_all_alerts_viewmodel(self):
        repo = AlertRepositoryMock()
        viewmodel = GetAllAlertsViewmodel(repo.alerts)
        
        response = viewmodel.to_dict()
        
        assert response["Alerts"] == [alert.to_dict() for alert in repo.alerts]
        assert response["message"] == "Alerts were retreived successfully"