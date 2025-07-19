from src.shared.domain.repositories.alert_repository_interface import IAlertRepository
from src.shared.domain.entities.alert import Alert
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from typing import List
import uuid
import time

class AlertRepositoryMock(IAlertRepository):
    
    alerts: List[Alert] 
    
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
        return alert
    
    def get_alert(self, alert_id: str) -> Alert:     
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                return alert
        raise NoItemsFound(alert_id)
    
    def get_all_alerts(self) -> List[Alert]:
        return self.alerts
    
    def delete_alert(self, alert_id: str) -> Alert:
        for i, alert in enumerate(self.alerts):
            if alert.alert_id == alert_id:
                return self.alerts.pop(i)
        raise NoItemsFound(alert_id)
    
    def update_alert(self, 
                     alert_id: str, 
                     new_title: str, 
                     new_description: str, 
                     new_start_date: int, 
                     new_end_date: int, 
                     new_is_permanent: bool) -> Alert:
        
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.title = new_title
                alert.description = new_description
                alert.start_date = new_start_date
                alert.end_date = new_end_date
                alert.is_permanent = new_is_permanent
                
                return alert
            
        raise NoItemsFound(alert_id)
