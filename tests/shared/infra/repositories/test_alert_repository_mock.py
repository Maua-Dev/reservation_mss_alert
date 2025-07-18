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