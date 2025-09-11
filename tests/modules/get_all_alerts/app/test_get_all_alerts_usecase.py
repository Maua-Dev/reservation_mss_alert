from src.shared.infra.repositories.alert_repository_mock import AlertRepositoryMock
from src.modules.get_all_alerts.app.get_all_alerts_usecase import GetAllAlertsUsecase

class TestGetAllAlertsUsecase:
    def test_get_all_alerts_usecase(self):
        repo = AlertRepositoryMock()
        usecase = GetAllAlertsUsecase(repo=repo)
        all_warnings = usecase()
        repo_size = len(repo.alerts)
        
        for warning in all_warnings:
            assert warning.title == repo.alerts[(repo_size-1)].title
            assert warning.description == repo.alerts[(repo_size-1)].description
            assert warning.start_date == repo.alerts[(repo_size-1)].start_date
            assert warning.end_date == repo.alerts[(repo_size-1)].end_date
            assert warning.is_rule == repo.alerts[(repo_size-1)].is_rule
            repo_size-=1
            