from src.shared.domain.entities.alert import Alert
from src.shared.domain.repositories.alert_repository_interface import IAlertRepository
from src.shared.clients.event_bridge_client import EventBridgeClient
import uuid
from datetime import datetime, timezone, timedelta
from src.shared.environments import Environments
from zoneinfo import ZoneInfo
from src.shared.helpers.errors.usecase_errors import *

class GetRuleUsecase:
    def __init__(self, repo: IAlertRepository):
        self.repo = repo

    def __call__( 
        self,
        rule_id: str
    ) -> Alert:
        
        print("Entered usecase")

        alert = self.repo.get_alert(alert_id=rule_id)
        
        if alert.is_rule:
            
            return alert

        else:
            
            raise NotRuleError()
