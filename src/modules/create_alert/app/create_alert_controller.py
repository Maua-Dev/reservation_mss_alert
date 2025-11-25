    
import json
from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from .create_alert_usecase import CreateAlertUsecase
from .create_alert_viewmodel import CreateAlertViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError, Forbidden


class CreateAlertController:

    def __init__(self, usecase: CreateAlertUsecase):
        self.CreateAlertUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:        
        try:
            
            user = request.data.get("user_from_authorizer")
            
            if not isinstance(user, dict):
                
                user = json.loads(user)
            
            requester_role = user.get("role", None)
            
            if requester_role is None:
                raise MissingParameters("user role from authorizer")
            
            title = request.data.get("title", None)
            description = request.data.get("description", None)
            start_date = request.data.get("start_date", None)
            end_date = request.data.get("end_date", None)
            # severity = request.data.get("severity", None)
            is_rule = request.data.get("is_rule", None)
                        
            if title is None:
                raise MissingParameters("title")
            if description is None:
                raise MissingParameters("description")
            if start_date is None:
                raise MissingParameters("start_date")
            if end_date is None:
                raise MissingParameters("end_date")
            if is_rule is None:
                raise MissingParameters("is_rule")
            
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

            print("End controller")

            alert = self.CreateAlertUsecase(
                requester_role=requester_role,
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
        
        except ForbiddenAction as err:
            
            return Forbidden(body=err.message)

        except Exception as err:

            return InternalServerError(body=err.args[0])
