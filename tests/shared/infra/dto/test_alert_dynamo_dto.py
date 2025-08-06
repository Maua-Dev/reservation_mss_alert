from decimal import Decimal
from src.shared.domain.entities.alert import Alert
from src.shared.infra.dto.alert_dynamo_dto import AlertDynamoDTO
from src.shared.domain.entities.alert import Alert
from src.shared.infra.dto.alert_dynamo_dto import AlertDynamoDTO
from src.shared.infra.repositories.alert_repository_mock import AlertRepositoryMock

class Test_AlertDynamoDTO:
    
    def test_from_entity(self):
        
        repo = AlertRepositoryMock()
        
        AlertDTO = AlertDynamoDTO.from_entity(alert = repo.alerts[0])
        
        assert AlertDTO == repo.alerts[0]
   

    def test_to_dynamo(self):
        repo = AlertRepositoryMock()
        
        AlertDTO = AlertDynamoDTO.from_entity(alert = repo.alerts[0])
         
        assert AlertDTO.to_dynamo()["entity"] == "alert"
        assert AlertDTO.to_dynamo()["alert_id"] == repo.alerts[0].alert_id
        assert AlertDTO.to_dynamo()["title"] == repo.alerts[0].title
        assert AlertDTO.to_dynamo()["description"] == repo.alerts[0].description
        assert AlertDTO.to_dynamo()["start_date"] == repo.alerts[0].start_date
        assert AlertDTO.to_dynamo()["end_date"] == repo.alerts[0].end_date
        assert AlertDTO.to_dynamo()["is_rule"] == repo.alerts[0].is_rule
        
    def test_from_dynamo(self):
        repo = AlertRepositoryMock()
        
        AlertDTO = AlertDynamoDTO.from_entity(alert = repo.alerts[0])
        AlertDynamo = AlertDynamoDTO.from_entity(alert = repo.alerts[0]).to_dynamo()
        
        assert AlertDTO == AlertDTO.from_dynamo(alert_data = AlertDynamo)
    
    def test_to_entity(self):
        
        repo = AlertRepositoryMock()
        
        AlertDTO = AlertDynamoDTO.from_entity(alert = repo.alerts[0])
        
        assert repo.alerts[0] == AlertDTO.to_entity()
        