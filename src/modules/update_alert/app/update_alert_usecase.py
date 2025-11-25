from src.shared.domain.entities.alert import Alert
from src.shared.domain.repositories.alert_repository_interface import IAlertRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.domain_errors import EntityError, EntityParameterOrderDatesError
from src.shared.clients.event_bridge_client import EventBridgeClient
from typing import Optional

class UpdateAlertUsecase:
    def __init__(self, repo: IAlertRepository):
        self.repo = repo

    def __call__(
        self, 
        alert_id: int, 
        new_title: Optional[str] = None,
        new_description: Optional[str] = None,
        new_start_date: Optional[int] = None,
        new_end_date: Optional[int] = None,
        new_is_rule: Optional[bool] = None) -> Alert:
        
        
        if not Environments.get_envs().stage.value == "TEST":
            print(f"Updating trigger for alert {alert_id}...")
            eb_client = EventBridgeClient()
            
            eb_client.update_trigger_expiration(
                alert_id=alert_id,
                new_expire=new_end_date
            )
        
        updated_alert = self.repo.update_alert(alert_id=alert_id,
                                          new_title=new_title,
                                          new_description=new_description,
                                          new_start_date=new_start_date,
                                          new_end_date=new_end_date,
                                          new_is_rule=new_is_rule)
        
        return updated_alert