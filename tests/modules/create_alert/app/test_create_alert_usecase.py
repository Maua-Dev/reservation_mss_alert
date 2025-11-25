from src.modules.create_alert.app.create_alert_usecase import CreateAlertUsecase
from src.shared.infra.repositories.alert_repository_mock import AlertRepositoryMock
import time

class TestCreateAlertUsecase:
    
    def test_create_alert_usecase(self):
        
        repo = AlertRepositoryMock()
        
        usecase = CreateAlertUsecase(repo=repo)
        
        created_alert = usecase (
            requester_role="ADMIN",
            title="Titulo3", 
            description="descrição3", 
            start_date=int(time.time()), 
            end_date=int(time.time()+3600),
            is_rule=False
        )
        
        assert repo.alerts[2] == created_alert
        