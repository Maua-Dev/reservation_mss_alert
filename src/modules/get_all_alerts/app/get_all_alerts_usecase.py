from src.shared.domain.repositories.alert_repository_interface import IAlertRepository


class GetAllAlertsUsecase:
    
    def __init__(self, repo = IAlertRepository):
        
        self.repo = repo
        
    def __call__(self):
        
        return self.repo.get_all_alerts()