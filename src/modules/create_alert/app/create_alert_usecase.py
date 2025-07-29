from src.shared.domain.entities.alert import Alert
from src.shared.domain.repositories.alert_repository_interface import IAlertRepository
from src.shared.clients.event_bridge_client import EventBridgeClient
import uuid
from datetime import datetime, timezone, timedelta
from src.shared.environments import Environments
from zoneinfo import ZoneInfo

class CreateAlertUsecase:
    def __init__(self, repo: IAlertRepository):
        self.repo = repo

    def __call__(self, title: str, description: str, start_date: int, end_date: int, 
                # severity: int,
                is_rule: bool) -> Alert:
        
        print("Entered usecase")

        id = str(uuid.uuid4())
        
        new_alert = Alert(
            alert_id=id,
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            # severity=severity
            is_rule=is_rule
        )
          
        if not Environments.get_envs().stage.value == "TEST" :
            eb_client = EventBridgeClient()
            rule = eb_client.create_trigger_for_deletion(
                alert_id=id,
                expire=int((datetime.now(timezone.utc) + timedelta(minutes=1)).timestamp())
            )

        created_alert = self.repo.create_alert(alert=new_alert)

        return created_alert
