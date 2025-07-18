from src.shared.domain.entities.alert import Alert
from src.shared.domain.repositories.alert_repository_interface import IAlertRepository
from src.shared.clients.event_bridge_client import EventBridgeClient
import uuid
from datetime import datetime, timezone

class CreateAlertUsecase:
    def __init__(self, repo: IAlertRepository):
        self.repo = repo

    def __call__(self, title: str, description: str, start_date: int, end_date: int, 
                # severity: int,
                is_rule: bool) -> Alert:
        
        print("Entered usecase")

        id = str(uuid.uuid4())
        
        eb_client = EventBridgeClient()
        rule_name = eb_client.create_trigger_for_deletion(int(datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc).timestamp()))
        
        new_alert = Alert(
            alert_id=id,
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            # severity=severity
            is_rule=is_rule
        )

        created_alert = self.repo.create_alert(alert=new_alert)

        return created_alert
