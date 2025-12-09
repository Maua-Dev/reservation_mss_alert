from src.shared.helpers.errors.base_error import BaseError


class EntityError(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Field {message} is not valid')

class EntityParameterTypeError(EntityError):
    def __init__(self, message: str):
        super().__init__(message)
        self.__message = message

    @property
    def message(self):
        return self.__message

class EntityParameterError(EntityError):
    def __init__(self, message: str):
        super().__init__(message)
        self.__message = message

    @property
    def message(self):
        return self.__message
    
class EntityParameterOrderDatesError(EntityError):
    def __init__(self, start_date: int, end_date: int):
        super().__init__(f'Initial date {start_date} must be less than or equal to end date {end_date}')