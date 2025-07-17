import boto3
from src.shared.environments import Environments
import uuid
from datetime import datetime, timezone

class EventBridgeClient:
    
    def __init__(self):
        
        self.__envs = Environments.get_envs()
        stage = self.__envs.stage.value
        
        self.delete_alert_lambda_arn = self.__envs.delete_alert_lambda_arn
        
        if stage == "TEST":
            self.eventbridge = boto3.client(
                "events",
                aws_access_key_id = self.__envs.client_id,
                aws_secret_access_key_id = self.__envs.client_secret,
                endpoint_url=self.__envs.endpoint_url,
                region_name=self.__envs.region,
            )
            
        else:
            self.eventbridge = boto3.client("events")
            
    def create_trigger_for_deletion(self, expire: int) -> str:
        
        dt = datetime.fromtimestamp(expire, tz=timezone.utc)

        if dt <= datetime.now(timezone.utc):
            raise ValueError("Timestamp 'expire' must be in the future.")
        
        rule_name = f"one-time-trigger-{uuid.uuid4()}"
        
        cron_expr = f"cron({dt.minute} {dt.hour} {dt.day} {dt.month} ? {dt.year})"
        rule_name = f"one-time-trigger-{uuid.uuid4()}"
        
        self.eventbridge.put_rule(
            Name=rule_name,
            ScheduleExpression=cron_expr,
            State="ENABLED"
        )
        
        self.eventbridge.put_targets(
            Rule=rule_name,
            Targets=[
                {
                    "Id": "1",
                    "Arn": lambda_arn,
                }
            ]
        )
        
        return rule_name
        
        

        