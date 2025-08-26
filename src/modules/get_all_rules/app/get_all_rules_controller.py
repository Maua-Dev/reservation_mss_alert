from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from .get_all_rules_viewmodel import GetAllRulesViewmodel
from .get_all_rules_usecase import GetAllRulesUsecase
from src.shared.helpers.external_interfaces.http_codes import *
from src.shared.helpers.errors.controller_errors import *
from src.shared.helpers.errors.usecase_errors import *
from src.shared.helpers.errors.domain_errors import *


class GetAllRulesController:
    
    def __init__(self, usecase: GetAllRulesUsecase):
        
        self.usecase = usecase
        
    def __call__(self, request: IRequest) -> IResponse:
        
        try:
            
            usecase_reponse = self.usecase()
            
            return OK(GetAllRulesViewmodel(usecase_reponse).to_dict())

        except EntityError as err:

            return BadRequest(body=err.message)
        
        except NoItemsFound as err:
            
            return BadRequest(body=err)

        except Exception as err:

            return InternalServerError(body=err.args[0])
            
            
        
    