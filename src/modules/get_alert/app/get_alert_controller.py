from src.shared.infra.external.observability.observability_aws import ObservabilityAWS
from .get_alert_usecase import GetAlertUseCase
from .get_alert_viewmodel import GetAlertViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError, EntityParameterOrderDatesError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError
from aws_lambda_powertools import Logger
from uuid import uuid4


class GetAlertController:
    def __init__(self, usecase: GetAlertUseCase, observability: ObservabilityAWS):
        self.usecase = usecase
        self.observability = observability
        
    def __call__(self, request: IRequest) -> IResponse:
        try:
            self.observability.log_controller_in()
            if request.data.get('alert_id') is None:
                raise MissingParameters('alert_id')

            if type(request.data.get('alert_id')) != str:
                raise WrongTypeParameter(
                    fieldName="alert_id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data.get('alert_id').__class__.__name__
                )
                
            if len(request.data.get('alert_id')) != 36 :
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
