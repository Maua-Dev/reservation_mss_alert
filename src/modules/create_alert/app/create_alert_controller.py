    
from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from .create_alert_usecase import CreateAlertUsecase
from .create_alert_viewmodel import CreateAlertViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError


class CreateAlertController:

    def __init__(self, usecase: CreateAlertUsecase):
        self.CreateAlertUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:        
        try:
            
            title = request.data.get("title", None)
            description = request.data.get("description", None)
            start_date = request.data.get("start_date", None)
            end_date = request.data.get("end_date", None)
            # severity = request.data.get("severity", None)
            is_rule = request.data.get("is_rule", None)
            
            #must do some more validaitions, this is only for testing if event bridge client is working correctly

            print("End controller")

            alert = self.CreateAlertUsecase(
                title=title,
                description=description,
                start_date=start_date,
                end_date=end_date,
                # severity=severity,
                is_rule=is_rule
            )

            viewmodel = CreateAlertViewmodel(alert=alert)

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
