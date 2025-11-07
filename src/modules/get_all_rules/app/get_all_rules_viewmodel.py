from typing import List
from src.shared.domain.entities.alert import Alert


class GetAllRulesViewmodel:
    
    rules: List[Alert]
    
    def __init__(self, rules: Alert) -> List[Alert]:
        
        self.rules = rules
        
    def to_dict(self):
        
        return {
            "Alerts": [ rule.to_dict() for rule in self.rules ],
            "message": "Rules were retreived successfully"
        }