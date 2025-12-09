from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from .get_all_alerts_usecase import GetAllAlertsUsecase
from .get_all_alerts_viewmodel import GetAllAlertsViewmodel
from src.shared.helpers.external_interfaces.http_codes import *
from src.shared.helpers.errors.controller_errors import *
from src.shared.helpers.errors.usecase_errors import *
from src.shared.helpers.errors.domain_errors import *


class GetAllAlertsController:
    
    def __init__(self, usecase: GetAllAlertsUsecase):
        
        self.usecase = usecase
        
    def __call__(self, request: IRequest) -> IResponse:
        
        try:
            
            usecase_reponse = self.usecase()
            
            return OK(GetAllAlertsViewmodel(usecase_reponse).to_dict())

        except EntityError as err:

            return BadRequest(body=err.message)
        
        except NoItemsFound as err:
            
            return BadRequest(body=err)

        except Exception as err:

            return InternalServerError(body=err.args[0])
            
            
        
    