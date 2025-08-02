from decimal import Decimal
from typing import List, Dict
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
    
    def get_all_alerts(self, alert_id: str) -> List[Alert]:
        resp = self.dynamo.get_item(partition_key=self.partition_key_format(alert_id= alert_id), sort_key=self.sort_key_format(alert_id=alert_id))
        alerts = []
        
        for item in resp["Items"]:
            if item.get('Item') == None:
                raise NoItemsFound("Alert_id")
            
            alerts.append(AlertDynamoDTO.from_dynamo(item["Item"]))
        
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
    
    def update_alert(self, alert_id, new_title, new_description, new_start_date, new_end_date, new_is_rule) -> Alert:
        alert_to_update = self.get_alert(alert_id=alert_id)
        
        item_to_update = {"new_title":new_title, "new_description":new_description, "new_start_date" : new_start_date, "new_end_date":new_end_date, "new_is_rule":new_is_rule}
        item_to_update_dict = {}
        count = 0
        
        for items in item_to_update:
            if item_to_update[items]:
                item_to_update_dict.update({items:item_to_update[items]})
            count +=1
            
        if count == len(item_to_update) and item_to_update_dict == {}:
            raise NoItemsFound("Nothing to update")
        
        resp = self.dynamo.update_item(partition_key=self.partition_key_format(alert_id), 
                                       sort_key=self.sort_key_format(alert_id),
                                       update_dict=item_to_update_dict)
        
        return AlertDynamoDTO.from_dynamo(resp['Attributes']).to_entity()     
        
    
    
    
