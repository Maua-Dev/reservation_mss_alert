from src.shared.infra.external.observability.observability_aws import ObservabilityAWS
from .get_alert_usecase import GetAlertUseCase
from .get_alert_viewmodel import GetAlertViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError, EntityParameterOrderDatesError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError
from uuid import UUID;


class GetAlertController:
    def __init__(self, usecase: GetAlertUseCase, observability: ObservabilityAWS):
        self.usecase = usecase
        self.observability = observability
        
    def __call__(self, request: IRequest) -> IResponse:
        try:
            self.observability.log_controller_in()
            if request.data.get('alert_id') is None:
                raise MissingParameters('alert_id')

            try:
                UUID(request.data.get('alert_id'))
            except ValueError:
                raise EntityError("alert_id")


            alert_response = self.usecase(alert_id=request.data.get("alert_id"))

            viewmodel = GetAlertViewmodel(alert_response)
            
            response = OK(viewmodel.to_dict())
            self.observability.log_controller_out(input=alert_response.alert_id)
            return response
        
        except NoItemsFound as err:
            self.observability.log_exception(message=err.message)
            return NotFound(body=err.message)

        except EntityParameterOrderDatesError as err:
            self.observability.log_exception(message=err.message)
            return BadRequest(body=err.message)
        
        except MissingParameters as err:
            self.observability.log_exception(message=err.message)
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            self.observability.log_exception(message=err.message)
            return BadRequest(body=err.message)

        except EntityError as err:
            self.observability.log_exception(message=err.message)
            return BadRequest(body=err.message)

        except Exception as err:
            self.observability.log_exception(message=err.args[0])
            return InternalServerError(body=err.args[0])
