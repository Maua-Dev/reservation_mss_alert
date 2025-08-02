import os
import pytest
from src.shared.infra.repositories.alert_repository_dynamo import AlertRepositoryDynamo
from src.shared.infra.repositories.alert_repository_mock import AlertRepositoryMock
from src.shared.domain.entities.alert import Alert
import time

class Test_AlertRepositoryDynamo:
    
    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_create_alert(self):
        os.environ["STAGE"] = "TEST"

        alert_repository = AlertRepositoryDynamo()
        alert_repository_mock = AlertRepositoryMock()
        resp = alert_repository.create_alert(alert_repository_mock.alerts[0])

        assert alert_repository_mock.alerts[0].title == resp.title
        
    @pytest.mark.skip(reason="Needs dynamoDB")    
    def test_get_alert(self):
        os.environ["STAGE"] = "TEST"

        alert_repository = AlertRepositoryDynamo()
        alert_repository_mock = AlertRepositoryMock()
        alert_test = alert_repository.create_alert(alert_repository_mock.alerts[0])
        
        resp = alert_repository.get_alert(alert_test.alert_id)
        
        assert resp.alert_id == alert_test.alert_id
        pass
    
    @pytest.mark.skip(reason="Needs dynamoDB")    
    def test_get_all_alerts(self):
        os.environ["STAGE"] = "TEST"

        alert_repository = AlertRepositoryDynamo()
        alert_repository_mock = AlertRepositoryMock()
        resp = alert_repository.get_all_alerts()
        
        assert len(alert_repository_mock.alerts) == len(resp)
    
    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_update_alert(self):
        os.environ["STAGE"] = "TEST"

        alert_repository = AlertRepositoryDynamo()
        alert_repository_mock = AlertRepositoryMock()
        
        test_alert = alert_repository.create_alert(alert_repository_mock.alerts[1])
        
        resp = alert_repository.update_alert(alert_id=test_alert.alert_id, new_title="AVISO!!!!")

        assert resp.title == "AVISO!!!!"
    
    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_delete_user(self):
        os.environ["STAGE"] = "TEST"

        alert_repository = AlertRepositoryDynamo()
        alert_repository_mock = AlertRepositoryMock()
        test_alert = alert_repository.create_alert(alert_repository_mock.alerts[0])
        db_len_before = len(alert_repository.get_all_alerts())
        
        alert_repository.delete_alert(test_alert.alert_id)
        db_len_after = len(alert_repository.get_all_alerts())

        assert db_len_after == (db_len_before - 1)
        

        
        