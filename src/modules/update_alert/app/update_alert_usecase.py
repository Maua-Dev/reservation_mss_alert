from src.shared.domain.entities.alert import Alert
from src.shared.domain.repositories.alert_repository_interface import IAlertRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.domain_errors import EntityError, EntityParameterOrderDatesError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.clients.event_bridge_client import EventBridgeClient
from typing import Optional

class UpdateAlertUsecase:
    def __init__(self, repo: IAlertRepository):
        self.repo = repo

    def __call__(
        self,
        role:str, 
        alert_id: int, 
        new_title: Optional[str] = None,
        new_description: Optional[str] = None,
        new_start_date: Optional[int] = None,
        new_end_date: Optional[int] = None,
        new_is_rule: Optional[bool] = None) -> Alert:
        
        if role != "ADMIN":
                    raise ForbiddenAction("role")
        
        current_alert = self.repo.get_alert(alert_id=alert_id)
        
                                                
        if new_end_date == None:
            raise NoItemsFound("new_end_date")
        
        if new_start_date == None:
              raise NoItemsFound("new_start_date")

        
        updated_alert = self.repo.update_alert(alert_id=alert_id,
                                               new_title=new_title,
                                               new_description=new_description,
                                               new_start_date=new_start_date,
                                               new_end_date=new_end_date,
                                               new_is_rule=new_is_rule
                                               )   
        
        if updated_alert.validate_dates(updated_alert.start_date, updated_alert.end_date) is False:
                    raise EntityError("date")

        if updated_alert.validate_order_dates(updated_alert.start_date, updated_alert.end_date) is False:
            raise EntityParameterOrderDatesError(start_date=new_start_date, end_date=new_end_date)
        
        if not Environments.get_envs().stage.value == "TEST":
            print(f"Updating trigger for alert {alert_id}...")
            try:
                eb_client = EventBridgeClient()
                
                eb_client.update_trigger_expiration(
                    alert_id=alert_id,
                    new_expire=new_end_date
                )

            except Exception as e:
                print(f"Error updating EventBridge: {e}. Rolling back repository changes...")
                
                self.repo.update_alert(
                    alert_id=alert_id,
                    new_title=current_alert.title,
                    new_description=current_alert.description,
                    new_start_date=current_alert.start_date,
                    new_end_date=current_alert.end_date,
                    new_is_rule=current_alert.is_rule
                )
                
                # Relançamos o erro original
                raise e

               


         
        
        
        
        #...

        # LOGICA DE DETERMINAR O QUE VAI SER PASSADO COMO NOVO PARAMETRO, EX: SE O NOVO TITULO FOR DIFERENTE DE NONE,
        # NEW_TITLE = NEW_TITLE. CASO O CONTRARIO, CASO O NOVO TITULO SEJA NONE, NEW_TITLE = ALERT.TITLE (TITULO ANTIGO, 
        # POIS NAO O TITULO NAO SERA ATUALIZADO
        
        #...     

        # acho que nao vai precisar mexer nessa logica aqui
    
        # try:
        #     eb_client = EventBridgeClient()
            
        #     if new_title != None or new_title != alertUpdate.title: # caso o new end date seja diferente
                
        #         eb_client.update_trigger_expiration(
        #             alert_id=alert_id,
        #             new_expire=new_title
        #         )
            
        #     if new_description != None or new_description != alertUpdate.description: # caso o new end date seja diferente
                
        #         eb_client.update_trigger_expiration(
        #             alert_id=alert_id,
        #             new_expire=new_description
        #         )
                
        #     if new_start_date != None or new_start_date != alertUpdate.start_date: # caso o new end date seja diferente
                
        #         eb_client.update_trigger_expiration(
        #             alert_id=alert_id,
        #             new_expire=new_start_date
        #         )
                
        #     if new_end_date != None or new_end_date != alertUpdate.end_date: # caso o new end date seja diferente
                
        #         eb_client.update_trigger_expiration(
        #             alert_id=alert_id,
        #             new_expire=new_end_date
        #         )
                
        #     if new_is_rule != None or new_is_rule != alertUpdate.is_rule: # caso o new end date seja diferente
                
        #         eb_client.update_trigger_expiration(
        #             alert_id=alert_id,
        #             new_expire=new_is_rule
        #         )
                  
        # except Exception as e:
        # if updated_alert.validate_dates(alertUpdate.start_date, alertUpdate.end_date) is False:
        #     raise EntityError("date")
    
        # if alertUpdate.validate_order_dates(alertUpdate.start_date, alertUpdate.end_date) is False:
        #     raise EntityParameterOrderDatesError(alertUpdate.start_date, alertUpdate.end_date)

            ##raise Exception 
        # acho que nao vai precisar mexer nessa logica aqui
        
        return updated_alert