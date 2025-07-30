from src.shared.domain.entities.alert import Alert

class DeleteAlertViewmodel():
    
    alert_id: str
    title: str
    description: str
    start_date: str
    end_date: str
    is_rule: bool
    
    def __init__(self, alert: Alert):
        
        self.alert_id = alert.alert_id
        self.title = alert.title
        self.description = alert.description
        self.start_date = alert.start_date
        self.end_date = alert.end_date
        self.is_rule = alert.is_rule
        
    def to_dict(self):
        
        return {
            "alert": {
                "alert_id": self.alert_id,
                "title": self.title,
                "description": self.description,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "is_rule": self.is_rule
            },
            "message": "The alert was deleted successfully"

        }