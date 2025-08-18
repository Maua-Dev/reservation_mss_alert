from src.shared.domain.entities.alert import alert
from src.shared.domain.enums.state_enum import STATE


class GetAlertViewmodel:
    alert_id: str
    title: str
    description: str
    start_date: int
    end_date: int
    severity: int
    
    def __init__(self, alert: alert):
        self.alert_id = alert.alert_id  
        self.title = alert.title
        self.description = alert.description
        self.start_date = alert.start_date
        self.end_date = alert.end_date
        self.severity = alert.severity


    def to_dict(self):
        return {
            'alert_id': self.alert_id, 
            'title': self.title,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'severity': self.severity,
            'message': "the user was retrieved successfully"
        }