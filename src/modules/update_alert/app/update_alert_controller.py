from src.shared.domain.entities.alert import Alert
from src.shared.domain.repositories.alert_repository_interface import IAlertRepository
from src.shared.helpers.external_interfaces.http_models import IRequest, IResponse
from src.modules.update_alert.app.update_alert_usecase import UpdateAlertUsecase
from src.modules.update_alert.app.update_alert_viewmodel import UpdateAlertViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError, EntityParameterOrderDatesError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError

class UpdateAlertController:
    def __init__(self, usecase: UpdateAlertUsecase):
        self.usecase = usecase
        
    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get("alert_id") is None:
                raise MissingParameters("alert_id")
            if request.data.get('user_from_authorizer') is None:
                raise MissingParameters('user authorizer')  

            user = request.data.get('user_from_authorizer')
            
            if user.get("role") != "ADMIN":
                raise ForbiddenAction('user')
            
            alert_id = request.data.get("alert_id")
            title= request.data.get("title", None)
            description = request.data.get("description", None)
            start_date = request.data.get("start_date", None)
            end_date = request.data.get("end_date", None)
            # severity = request.data.get("severity", None)
            is_rule = request.data.get("is_rule", None)
                        
            if not isinstance(title, str):
                raise WrongTypeParameter(fieldName="title",
                                         fieldTypeExpected="string",
                                         fieldTypeReceived=type(title).__name__())
            if not isinstance(description, str):
                raise WrongTypeParameter(fieldName="description",
                                         fieldTypeExpected="string",
                                         fieldTypeReceived=type(description).__name__())
            if not isinstance(start_date, int):
                raise WrongTypeParameter(fieldName="start_date",
                                         fieldTypeExpected="int",
                                         fieldTypeReceived=type(start_date).__name__())
            if not isinstance(end_date, int):
                raise WrongTypeParameter(fieldName="end_date",
                                         fieldTypeExpected="int",
                                         fieldTypeReceived=type(end_date).__name__())
            if not isinstance(is_rule, bool):
                raise WrongTypeParameter(fieldName="is_rule",
                                         fieldTypeExpected="bool",
                                         fieldTypeReceived=type(is_rule).__name__())
                
            updated_alert = self.usecase(
                alert_id=alert_id,
                new_title = title,
                new_description = description,
                new_start_date = start_date,
                new_end_date = end_date,
                new_is_rule = is_rule 
            )
            
            viewmodel = UpdateAlertViewmodel(updated_alert)
            
            return OK(viewmodel.to_dict())

        except MissingParameters as err:
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            return BadRequest(body=err.message)

        except EntityParameterOrderDatesError as err:
            return BadRequest(body=err.message)
        
        except EntityError as err:
            return BadRequest(body=err.message)
        
        except NoItemsFound as err:
            return NotFound(body=f"Booking not found: {err.message}")
        
        except Exception as err:
            return InternalServerError(body=err.args[0])
