from src.modules.delete_alert.app.delete_alert_usecase import DeleteAlertUsecase
from src.shared.infra.repositories.alert_repository_mock import AlertRepositoryMock

class TestAlertUsecase:
    def test_alert_usecase(self):
        repo = AlertRepositoryMock()
        usecase = DeleteAlertUsecase(repo)
        
        test_alert = repo.alerts[0]
        
        deleted_alert = usecase(
            alert_id=test_alert.alert_id,
            requester_role="ADMIN"
        )
        
        assert deleted_alert == test_alert
        assert len(repo.alerts) == 1