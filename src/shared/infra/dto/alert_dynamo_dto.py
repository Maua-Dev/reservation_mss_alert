from decimal import Decimal
from src.shared.domain.entities.alert import Alert

class AlertDynamoDTO:
    alert_id: str        
    title: str           
    description: str     
    start_date: int      
    end_date: int        
    # severity: int      
    is_rule: bool   
     
    def __init__(self, alert_id: str, title: str, description: str, start_date: int, end_date: int, is_rule: bool):
        
        self.alert_id = alert_id
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.is_rule = is_rule
        
    @staticmethod
    def from_entity (alert: Alert) -> "AlertDynamoDTO":
        """
        Parse data from Alert to AlertDynamoDTO
        """
        return AlertDynamoDTO(
            alert_id = alert.alert_id,
            title = alert.title,
            description = alert.description,
            start_date = alert.start_date,
            end_date = alert.end_date,
            is_rule = alert.is_rule
        )
        
    def to_dynamo(self) -> dict:
        """
        Parse data from AlertDynamoDTO to dict
        """
        return{
            "entity":"alert",
            "alert_id":self.alert_id,
            "title":self.title,
            "description":self.description,
            "start_date":Decimal(self.start_date),
            "end_date":Decimal(self.end_date),
            "is_rule":self.is_rule
        }
        
    @staticmethod
    def from_dynamo(alert_data: dict) -> "AlertDynamoDTO":
        """
        Parse data from DynamoDB to AlertDynamoDTO
        @param alert_data: dict from DynamoDB
        """
        
        return AlertDynamoDTO(
            alert_id = alert_data["alert_id"],
            title = alert_data["title"],
            description = alert_data["description"],
            start_date = int(alert_data["start_date"]),
            end_date = int(alert_data["end_date"]),
            is_rule = alert_data["is_rule"]
        )
        
    def to_entity(self) -> Alert:
        """
        Parse data from AlertDynamoDTO to Alert
        """
        return Alert(
            alert_id =self.alert_id,
            title = self.title,
            description = self.description,
            start_date = self.start_date,
            end_date = self.end_date,
            is_rule = self.is_rule    
        )
        
    def __repr__(self):
        return f"AlertDynamoDto(alert_id={self.alert_id}, title={self.title}, description={self.description}, start_date={self.start_date}, end_date={self.end_date}, is_rule={self.is_rule})"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__