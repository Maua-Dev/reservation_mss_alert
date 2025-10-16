from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.modules.update_alert.app.update_alert_usecase import UpdateAlertUsecase
from src.modules.update_alert.app.update_alert_controller import UpdateAlertController
from src.shared.infra.repositories.alert_repository_mock import AlertRepositoryMock

class TestUpdateAlertController:
    def test_update_alert_controller(self):
        repo = AlertRepositoryMock()
        
        usecase = UpdateAlertUsecase(repo=repo)
        
        controller = UpdateAlertController(usecase=usecase)
        
        request = HttpRequest(body={
            "alert_id":  repo.alerts[0].alert_id,
            "title" : repo.alerts[0].title,
            "description" : repo.alerts[0].description,
            "start_date": repo.alerts[0].start_date,
            "end_date": repo.alerts[0].end_date,
            "is_rule" : repo.alerts[0].is_rule,
            "user_from_authorizer": {
                'user_id': 'qualquer-id',
                'name': 'Nome',
                'email': 'user@email.com',
                'role': 'ADMIN'
             }
        })
        
        response = controller(request=request)
        
        assert response.status_code == 200
        assert response.body["Message"] == "The alert was updated successfully"
        
        
        