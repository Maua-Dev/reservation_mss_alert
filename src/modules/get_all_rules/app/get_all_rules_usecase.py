from src.shared.domain.repositories.alert_repository_interface import IAlertRepository


class GetAllRulesUsecase:
    
    def __init__(self, repo = IAlertRepository):
        
        self.repo = repo
        
    def __call__(self):
        
        all_alerts = self.repo.get_all_alerts()
        
        all_rules = []
        
        for alert in all_alerts:
            
            if alert.is_rule:
                
                all_rules.append(alert)
                
        return all_rules