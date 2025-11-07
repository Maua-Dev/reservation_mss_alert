from src.shared.domain.entities.alert import Alert
from src.shared.domain.repositories.alert_repository_interface import IAlertRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.clients.event_bridge_client import EventBridgeClient
from typing import Optional

class UpdateAlertUsecase:
    def __init__(self, repo: IAlertRepository):
        self.repo = repo

    def __call__(
        self, 
        alert_id: int, 
        new_title: Optional[str] = None,
        new_description: Optional[str] = None,
        new_start_date: Optional[int] = None,
        new_end_date: Optional[int] = None,
        new_is_rule: Optional[bool] = None) -> Alert:
        
        #...

        # LOGICA DE DETERMINAR O QUE VAI SER PASSADO COMO NOVO PARAMETRO, EX: SE O NOVO TITULO FOR DIFERENTE DE NONE,
        # NEW_TITLE = NEW_TITLE. CASO O CONTRARIO, CASO O NOVO TITULO SEJA NONE, NEW_TITLE = ALERT.TITLE (TITULO ANTIGO, 
        # POIS NAO O TITULO NAO SERA ATUALIZADO
        
        #...
        
        # acho que nao vai precisar mexer nessa logica aqui
        try:
            
            if new_end_date != None or new_end_date != current_alert.end_dade: # caso o new end date seja diferente
                
                eb_client = EventBridgeClient()
                
                eb_client.update_trigger_expiration(
                    alert_id=alert_id,
                    new_expire=new_end_date
                )
                
        except Exception as e:
            
            raise Exception
        # acho que nao vai precisar mexer nessa logica aqui

        return 
