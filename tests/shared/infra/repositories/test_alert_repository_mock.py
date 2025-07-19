from src.shared.infra.repositories.alert_repository_mock import AlertRepositoryMock
from src.shared.domain.entities.alert import Alert
import uuid
import time

class TestAlertRepositoryMock():
    def test_create_alert(self):
        
        repo = AlertRepositoryMock()
        
        id = str(uuid.uuid4())
        
        new_alert = Alert (
                alert_id=id,
                title = "AvisoTest", 
                description = "quadra molhada por conta da chuva", 
                start_date = int(time.time()), 
                end_date =  int(time.time()) + 7200000, 
                # severity = 2,
                is_rule=True
            )
        
        repo.create_alert(new_alert)
        
        assert new_alert.alert_id == repo.alerts[-1].alert_id
        assert new_alert.title == repo.alerts[-1].title
    
    def test_get_alert(self):
        repo = AlertRepositoryMock()
        
        test_alert_id = repo.alerts[0].alert_id
        
        test_alert = repo.get_alert(test_alert_id)
        
        assert test_alert.alert_id == repo.alerts[0].alert_id
        assert test_alert.title == "Aviso1"
        assert test_alert.description == "quadra molhada por conta da chuva"
        assert test_alert.start_date == repo.alerts[0].start_date
        assert test_alert.end_date == repo.alerts[0].end_date
        assert test_alert.is_rule == True
        
    def test_get_all_alerts(self):
        repo = AlertRepositoryMock()
        
        alerts = repo.get_all_alerts()
        assert len(alerts) == 2
        
    def test_delete_alert(self):
        repo = AlertRepositoryMock()
        
        ini_size = len(repo.get_all_alerts())
        test_alert_id = repo.alerts[0].alert_id
        repo.delete_alert(test_alert_id)
        
        assert len(repo.get_all_alerts()) == ini_size - 1 
    
    def test_update_alert(self):
        repo = AlertRepositoryMock()
        
        test_alert_id = repo.alerts[0].alert_id
        updated_alert = repo.update_alert(alert_id = test_alert_id,
                          new_title = "Aviso2",
                          new_description = "falta de material esportivo",
                          new_start_date = time.time()+7200,
                          new_end_date=time.time()+14400,
                          new_is_rule=False
                          )
        test_alert = repo.get_alert(test_alert_id)
        
        assert test_alert == updated_alert       
