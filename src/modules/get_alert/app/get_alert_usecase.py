from src.shared.domain.entities.alert import Alert
from src.shared.domain.repositories.alert_repository_interface import IAlertRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.infra.external.observability.observability_aws import ObservabilityAWS


class GetAlertUseCase:
    def __init__(self, repo: IAlertRepository, observability: ObservabilityAWS):
        self.repo = repo
        self.observability = observability
        
    def __call__(self, alert_id: str) -> Alert:
        self.observability.log_usecase_in()
        alert = self.repo.get_alert(alert_id)
        self.observability.log_usecase_out()
        return alert

