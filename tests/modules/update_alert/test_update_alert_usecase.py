import pytest
from src.shared.infra.repositories.alert_repository_mock import AlertRepositoryMock
from src.modules.update_alert.app.update_alert_usecase import UpdateAlertUsecase
from src.shared.helpers.errors.usecase_errors import ForbiddenAction 
import time


class TestUpdateAlertUsecase:
    def test_update_alert_usecase_user_is_admin(self):
        repo = AlertRepositoryMock()
        usecase = UpdateAlertUsecase(repo=repo)

        alert_id = repo.alerts[1].alert_id

        alert = usecase(
            role="ADMIN",
            alert_id=alert_id, 
            new_title="New Title", 
            new_description="cuidado",
            new_start_date=int(time.time()),
            new_end_date=int(time.time()+3600),
            new_is_rule=False
        )

        assert alert.alert_id == alert_id
        assert alert.title == "New Title"
        assert alert.description == "cuidado"
        assert abs(alert.start_date - time.time()) < 2  
        assert abs(alert.end_date - (time.time()+3600)) < 2
        assert alert.is_rule is False

    def test_update_alert_usecase_user_not_admin(self):
        repo = AlertRepositoryMock()
        usecase = UpdateAlertUsecase(repo=repo)

        alert_id = repo.alerts[1].alert_id

        with pytest.raises(ForbiddenAction) as error_info:
            usecase(
                role="notADMIN",
                alert_id=alert_id, 
                new_title="New Title", 
                new_description="cuidado",
                new_start_date=int(time.time()),
                new_end_date=int(time.time()+3600),
                new_is_rule=False
            )
    
        assert str(error_info.value) == 'That action is forbidden for this role'