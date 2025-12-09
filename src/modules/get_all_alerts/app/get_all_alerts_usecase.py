from src.shared.domain.repositories.alert_repository_interface import IAlertRepository


class GetAllAlertsUsecase:
    
    def __init__(self, repo = IAlertRepository):
        
        self.repo = repo
        
    def __call__(self):
        
        all_alerts = self.repo.get_all_alerts()
        
        all_warnings = []
        
        for warning in all_alerts:
            
            if not warning.is_rule:
                
                all_warnings.append(warning)
                
        return all_warnings