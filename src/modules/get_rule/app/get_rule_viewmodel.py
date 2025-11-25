from src.shared.domain.entities.alert import Alert

class GetRuleViewmodel:
    
    alert_id: str       #required
    is_rule: bool       #required
    
    def __init__(self, alert: Alert):
        self.alert_id = alert.alert_id
        self.is_rule = alert.is_rule
        
    def to_dict(self):
        
        return {
            "Rule": {
                "alert_id": self.alert_id,
                "is_rule": self.is_rule,
            },
            "Message": "The rule was created successfully"
        }