from .delete_alert_usecase import DeleteAlertUsecase
from .delete_alert_viewmodel import DeleteAlertViewmodel
from src.shared.helpers.external_interfaces.http_models import IRequest, IResponse
from src.shared.helpers.errors.controller_errors import WrongTypeParameter, MissingParameters
from src.shared.helpers.external_interfaces.http_codes import InternalServerError, OK

class DeleteAlertController():
    
    def __init__(self, usecase: DeleteAlertUsecase):
        
        self.usecase = usecase
        
    def __call__(self, request: IRequest) -> IResponse:
        
        try:
            
            user = request.data.get("user_from_authorizer", None)
            alert_id = request.data.get("alert_id", None)
            
            # if user is None:
            #     raise MissingParameters("user_from_authorizer")
            
            if alert_id is None:
                raise MissingParameters("alert_id")
            if not isinstance(alert_id, str):
                raise WrongTypeParameter(fieldName="alert_id",
                                         fieldTypeExpected="str",
                                         fieldTypeReceived=type(alert_id).__name__)
                
            # user_role = user.get("role")
                
            deleted_alert = self.usecase(alert_id=alert_id, 
                                        #  user_role=user_role
                                         )
            
            return OK(DeleteAlertViewmodel(alert=deleted_alert).to_dict())
            
        except Exception as err:
            
            return InternalServerError(body=err.args[0])