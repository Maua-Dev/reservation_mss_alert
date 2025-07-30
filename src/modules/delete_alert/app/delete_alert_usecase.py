from src.shared.domain.repositories.alert_repository_interface import IAlertRepository
from src.shared.clients.event_bridge_client import EventBridgeClient
from src.shared.environments import Environments

class DeleteAlertUsecase():
    
    def __init__(self, repo: IAlertRepository):
        
        self.AlertRepo = repo
        
    def __call__(self, alert_id: str):
        
        #TODO make more robust try catch here?
        
        if not Environments.get_envs().stage.value == "TEST" :
            eb_client = EventBridgeClient()
            resp = eb_client.delete_rule(
                alert_id=id,
            )
            
        deleted_alert = self.AlertRepo.delete_alert(alert_id=alert_id)
        
        return deleted_alert