from src.shared.domain.entities.alert import Alert


class DeleteAlertViewmodel():
    
    title: str
    description: str
    start_date: int
    end_date: str
    is_rule: bool
    
    def __init__(self, alert: Alert):
        
        self.title = alert.title
        self.description = alert.description
        self.start_date = alert.start_date
        self.end_date = alert.end_date
        self.is_rule = alert.is_rule
        
    def to_dict(self) -> dict:
        
        return {
            "alert":
                {
                    "title": self.title,
                    "description": self.description,
                    "start_date": self.start_date,
                    "end_date": self.end_date,
                    "is_rule": self.is_rule
                },
            "message": f"The {self.is_rule if self.is_rule else 'alert'} was deleted successfuly"        
        }