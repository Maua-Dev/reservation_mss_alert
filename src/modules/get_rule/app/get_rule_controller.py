    
from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from .get_rule_usecase import GetRuleUsecase
from .get_rule_viewmodel import GetRuleViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, NotRuleError
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError


class GetRuleController:

    def __init__(self, usecase: GetRuleUsecase):
        self.GetRuleUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            
            rule_id = request.data.get("rule_id", None)
            
            if rule_id is None:
                raise MissingParameters("rule_id")
            
            if not isinstance(rule_id, str):
                raise WrongTypeParameter(fieldName="rule_id",
                                         fieldTypeExpected="string",
                                         fieldTypeReceived=type(rule_id).__name__())

            print("End controller")

            alert = self.GetRuleUsecase(rule_id=rule_id)

            viewmodel = GetRuleViewmodel(alert=alert)

            return OK(viewmodel.to_dict())

        except NoItemsFound as err:

            return NotFound(body=err.message)

        except MissingParameters as err:

            return BadRequest(body=err.message)

        except WrongTypeParameter as err:

            return BadRequest(body=err.message)

        except EntityError as err:

            return BadRequest(body=err.message)
        
        except NotRuleError as err:
            
            return BadRequest(body=err.message)

        except Exception as err:

            return InternalServerError(body=err.args[0])
