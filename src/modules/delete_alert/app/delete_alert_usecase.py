from src.shared.environments import Environments
from src.shared.domain.repositories.alert_repository_interface import IAlertRepository
from src.shared.clients.event_bridge_client import EventBridgeClient
from src.shared.helpers.errors.usecase_errors import ForbiddenAction

class DeleteAlertUsecase():
    
    def __init__(self, repo: IAlertRepository):
        
        self.repo = repo
        
    def __call__(self, 
        alert_id: str,
        requester_role: str
    ):
        
        if requester_role != "ADMIN":
            raise ForbiddenAction("user")
        
        rule_name = f"one-time-trigger-for-alert-{alert_id}"
        
        if not Environments.get_envs().stage.value == "TEST" :
            
            try:
                
                eb_client = EventBridgeClient()

                rule = eb_client.delete_trigger(rule_name=rule_name)
                
            except Exception as e:
                # Relança a exceção com uma mensagem clara
                raise Exception(f"Falha ao deletar o gatilho no EventBridge para a regra {rule_name}. Erro original: {e}")

        deleted_alert = self.repo.delete_alert(alert_id=alert_id)
        
        return deleted_alert