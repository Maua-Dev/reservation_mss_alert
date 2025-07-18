from src.shared.domain.entities.alert import Alert

class CreateAlertViewmodel:
    
    alert_id: str       #required
    title: str          #required
    description: str    #required
    start_date: int     #required
    end_date: int       #required
    # severity: int       #required
    is_rule: bool  #required
    
    def __init__(self, alert: Alert):
        self.alert_id = alert.alert_id
        self.title = alert.title
        self.description = alert.description
        self.start_date = alert.start_date
        self.end_date = alert.end_date
        # self.severity = alert.severity
        self.is_rule = alert.is_rule
        
    def to_dict(self):
        
        return {
            "Alert": {
                "alert_id": self.alert_id,
                "title": self.title,
                "description": self.description,
                "start_date": self.start_date,
                "end_date": self.end_date,
                # "self.severity": self.severity,
                "is_rule": self.is_rule
            },
            "Message": "The alert was created successfully"
        }