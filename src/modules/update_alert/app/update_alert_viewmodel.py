from src.shared.domain.entities.alert import Alert

class UpdateAlertViewmodel:
    
    title: str          #required
    description: str    #required
    start_date: int     #required
    end_date: int       #required
    # "self.severity": self.severity
    is_rule: bool       #required
    
    def __init__(self, alert: Alert):

        self.title = alert.title
        self.description = alert.description
        self.start_date = alert.start_date
        self.end_date = alert.end_date
        # self.severity = alert.severity
        self.is_rule = alert.is_rule
        
    def to_dict(self):
        
        return {
            "alert": {
                "new title": self.title,
                "new description": self.description,
                "new start_date": self.start_date,
                "new end_date": self.end_date,
                # "new self.severity": self.severity,
                "new is_rule": self.is_rule
            },
            "Message": "The alert was updated successfully"
        }