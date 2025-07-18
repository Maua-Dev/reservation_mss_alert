from src.shared.domain.repositories.alert_repository_interface import IAlertRepository
from src.shared.domain.entities.alert import Alert
from typing import List
import uuid
import time

class AlertRepositoryMock(IAlertRepository):
    
    alerts = List[Alert]
    
    def __init__(self):
        
        self.alerts = [
            Alert (
                alert_id=str(uuid.uuid4()), 
                title = "Aviso1", 
                description = "quadra molhada por conta da chuva", 
                start_date = int(time.time()), 
                end_date =  int(time.time()) + 7200000, 
                # severity = 2,
                is_rule=True
            ),
            Alert (
                alert_id=str(uuid.uuid4()), 
                title = "Aviso2", 
                description = "quadra molhada por conta da chuva", 
                start_date = int(time.time()), 
                end_date =  int(time.time()) + 7200000, 
                # severity = 2,
                is_rule=False
            )
        ]
        
    def create_alert(self, alert: Alert) -> Alert:
        
        self.alerts.append(alert)
        
        return Alert