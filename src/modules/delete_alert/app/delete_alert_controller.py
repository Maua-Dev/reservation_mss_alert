from .delete_alert_usecase import DeleteAlertUsecase
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError, NotFound
from src.shared.helpers.external_interfaces.http_models import IRequest, IResponse

class DeleteAlertController():
    
    def __init__(self, usecase: DeleteAlertUsecase):
        
        self.DeleteAlertUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        
        try:
            
            alert_id = request.data.get("alert_id", None)
            
            if alert_id is None:
                raise MissingParameters("alert_id")
            
            if not isinstance(alert_id, str):
                raise WrongTypeParameter(fieldName="alert_id",
                                         fieldTypeExpected="string",
                                         fieldTypeReceived=type(alert_id).__name__())
                
            alert = self.CreateAlertUsecase(
                alert_id=alert_id
            )
            
            viewmodel = DeleteAlertUsecase(alert=alert)

            return OK(viewmodel.to_dict())
            
        except NoItemsFound as err:

            return NotFound(body=err.message)

        except MissingParameters as err:

            return BadRequest(body=err.message)

        except WrongTypeParameter as err:

            return BadRequest(body=err.message)

        except EntityError as err:

            return BadRequest(body=err.message)

        except Exception as err:

            return InternalServerError(body=err.args[0])
