import abc
from src.shared.helpers.errors.domain_errors import EntityError, EntityParameterOrderDatesError

class alert(abc.ABC):
    title: str
    description: str
    start_date: int
    end_date: int
    severity: int
    
    def __init__(self, title: str, description: str, start_date: int, end_date: int, severity: int):
        if not alert.validate_title(title): 
            raise EntityError(title)
        self.title = title
        
        if not alert.validate_title_first_char(title):
            raise EntityError(title)
        self.title = title
        
        if not alert.validate_description(description): 
            raise EntityError("title")
        self.description = description
        
        if not alert.validate_dates(start_date, end_date): 
            raise EntityError("dates")
        self.start_date = start_date
        self.end_date = end_date
        
        if not alert.validate_order_dates(start_date, end_date):
            raise EntityParameterOrderDatesError(start_date, end_date)
        self.start_date = start_date
        self.end_date = end_date
        
        if not alert.validate_severity(severity):
            raise EntityError("severity")
        self.severity = severity
    
    
    #Lógica das validações:
    @staticmethod
    def validate_title(title: str) -> bool:
        if not isinstance(title, str):
            return False
        return True
    
    def validate_title_first_char(title: str) -> bool:
        first_char = title[0]
        if title[0].upper != first_char:
            return False
        return True
    
    @staticmethod
    def validate_description(description: str) -> bool:
        if not isinstance(description, str):
            return False
        return True
    
    @staticmethod
    def validate_dates(start_date: int, end_date: int) -> bool:
        if not isinstance(start_date, int) or not isinstance(end_date, int):
            return False
        return True
    
    @staticmethod
    def validate_order_dates(start_date: int, end_date: int) -> bool:
        if start_date >= end_date:
            return False
        return True
    
    @staticmethod
    def validate_severity(severity) -> bool:
        if not isinstance(severity, int):
            return False
        if severity<1 or severity>3:
            return False
        return True
    
   
        
        
        
    
    
