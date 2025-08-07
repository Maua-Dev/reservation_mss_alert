from abc import ABC, abstractmethod
from typing import List

from src.shared.domain.entities.alert import Alert


class IAlertRepository(ABC):

    @abstractmethod
    def create_alert(self, new_alert: Alert) -> Alert:
        pass
    
    @abstractmethod
    def get_alert(self, alert_id: str) -> Alert:
        """
        If alert not found raise NoItemsFound
        """
        pass
    
    @abstractmethod
    def get_all_alerts(self) -> Alert:
        pass
    
    @abstractmethod
    def delete_alert(self, alert_id: str) -> Alert:
        """
        If alert not found raise NoItemsFound
        """
        pass
    
    @abstractmethod
    def update_alert(
            self,
            alert_id: str, 
            new_title: str, 
            new_description: str, 
            new_start_date: int, 
            new_end_date: int, 
            new_is_rule: bool
        ) -> Alert:
        """
        If alert not found raise NoItemsFound
        """
        pass
