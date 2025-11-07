from decimal import Decimal
from typing import List, Dict, Optional
from src.shared.domain.entities.alert import Alert
from src.shared.domain.repositories.alert_repository_interface import IAlertRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.dto.alert_dynamo_dto import AlertDynamoDTO
from src.shared.infra.external.dynamo.datasources.dynamo_datasource import DynamoDatasource

class AlertRepositoryDynamo(IAlertRepository):
    
    @staticmethod
    def partition_key_format(alert_id: str) -> str:
        return f"alert#{alert_id}"

    @staticmethod
    def sort_key_format(alert_id: str) -> str:
        return f"#{alert_id}"
    
    def __init__(self):
        self.dynamo = DynamoDatasource(endpoint_url=Environments.get_envs().endpoint_url,
                                       dynamo_table_name=Environments.get_envs().dynamo_table_name,
                                       region=Environments.get_envs().region,
                                       partition_key=Environments.get_envs().dynamo_partition_key,
                                       sort_key=Environments.get_envs().dynamo_sort_key)
    
    def get_alert(self, alert_id: str) -> Alert:
        resp = self.dynamo.get_item(partition_key=self.partition_key_format(alert_id= alert_id), sort_key=self.sort_key_format(alert_id=alert_id))
        
        if resp.get('Item') == None:
            raise NoItemsFound("Alert_id")
        
        alert_dto = AlertDynamoDTO.from_dynamo(resp["Item"])
        
        return alert_dto.to_entity()
    
    def get_all_alerts(self) -> List[Alert]:
        resp = self.dynamo.get_all_items()
        alerts = []
        
        for item in resp["Items"]:
            
            alert_dto = AlertDynamoDTO.from_dynamo(item)
            alerts.append(alert_dto.to_entity())
            
        if len(alerts) == 0:
            raise NoItemsFound("Alerts")
        
        return alerts
    
    def create_alert(self, new_alert:Alert) -> Alert:
        
        alert_DTO = AlertDynamoDTO.from_entity(new_alert).to_dynamo()
        resp = self.dynamo.put_item(item=alert_DTO,
                                    partition_key = self.partition_key_format(alert_id = new_alert.alert_id),
                                    sort_key = self.sort_key_format(alert_id = new_alert.alert_id))
        
        return new_alert
    
    def delete_alert(self, alert_id) -> Alert:
        resp = self.dynamo.delete_item(partition_key=self.partition_key_format(alert_id), sort_key=self.sort_key_format(alert_id))

        if "Attributes" not in resp:
            raise NoItemsFound("alert_id")

        return AlertDynamoDTO.from_dynamo(resp['Attributes']).to_entity()
    
    def update_alert(self, 
                     alert_id: str,
                     new_title: Optional[str] = None, 
                     new_description: Optional[str] = None, 
                     new_start_date: Optional[int] = None, 
                     new_end_date: Optional[int] = None,
                     new_is_rule: Optional[bool] = None) -> Alert:
        
        item_to_update_dict = {}
        
        if new_title is not None:
            item_to_update_dict["title"] = new_title 
        if new_description is not None:
            item_to_update_dict["description"] = new_description
        if new_start_date is not None:
            item_to_update_dict["start_date"] = new_start_date
        if new_end_date is not None:
            item_to_update_dict["end_date"] = new_end_date
        if new_is_rule is not None: 
            item_to_update_dict["is_rule"] = new_is_rule
        
        if not item_to_update_dict:
            raise ValueError("No update parameters provided.") 
        
        resp = self.dynamo.update_item(
            partition_key=self.partition_key_format(alert_id), 
            sort_key=self.sort_key_format(alert_id),
            update_dict=item_to_update_dict 
        )
        
        return AlertDynamoDTO.from_dynamo(resp['Attributes']).to_entity()     
        
    
    
    
