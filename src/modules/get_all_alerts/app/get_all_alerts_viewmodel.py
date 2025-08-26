from typing import List
from src.shared.domain.entities.alert import Alert


class GetAllAlertsViewmodel:
    
    alerts: List[Alert]
    
    def __init__(self, alerts: Alert) -> List[Alert]:
        
        self.alerts = alerts
        
    def to_dict(self):
        
        return {
            "Alerts": [ alert.to_dict() for alert in self.alerts ],
            "message": "Alerts were retreived successfully"
        }