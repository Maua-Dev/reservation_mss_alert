from src.shared.environments import Environments
from src.shared.domain.repositories.alert_repository_interface import IAlertRepository
from src.shared.clients.event_bridge_client import EventBridgeClient
from src.shared.helpers.errors.usecase_errors import ForbiddenAction

class DeleteAlertUsecase():
    
    def __init__(self, repo: IAlertRepository):
        
        self.repo = repo
        
    def __call__(self, 
                 alert_id: str,
                #  user_role: str
                 ):
        
        # if user_role != "ADMIN":
        #     raise ForbiddenAction("user, only admin can create rules and alerts")
        
        rule_name = f"one-time-trigger-for-alert-{alert_id}"
        
        if not Environments.get_envs().stage.value == "TEST" :
            
            try:
                
                EventBridgeClient.delete_trigger(rule_name=rule_name)
                
            except:
                
                #TODO Melhorar esse erro, criar algo no errors como: EventBridgeDeleteTriggerErorr
                raise Exception
        
        deletet_alert = self.repo.delete_alert(alert_id=alert_id)
        
        return deletet_alert