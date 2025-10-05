import pytest
from src.shared.domain.entities.alert import Alert
from src.shared.infra.repositories.alert_repository_mock import AlertRepositoryMock
from src.shared.helpers.errors.domain_errors import EntityError, EntityParameterOrderDatesError
from src.modules.update_alert.app.update_alert_usecase import UpdateAlertUsecase
import time


class Test_UpdateAlertUsecase:
    def test_update_alert_usecase_update_title(self):
        repo = AlertRepositoryMock()
        usecase = UpdateAlertUsecase(repo=repo)

        alert_id = repo.alerts[1].alert_id

        alert = usecase(
            alert_id=alert_id, 
            new_title="New Title", 
            new_description="cuidado",
            new_start_date=time.time(),
            new_end_date=time.time()+3600,
            new_is_rule=False
        )

        assert alert.alert_id == alert_id
        assert alert.title == "New Title"
        assert alert.description == "cuidado"
        assert abs(alert.start_date - time.time()) < 2  
        assert abs(alert.end_date - (time.time()+3600)) < 2
        assert alert.is_rule is False

        