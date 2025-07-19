from abc import ABC, abstractmethod
from typing import List

from src.shared.domain.entities.alert import Alert


class IAlertRepository(ABC):

    @abstractmethod
    def create_alert(self, alert: Alert) -> Alert:
        pass
    
    @abstractmethod
    def get_alert(self, alert: Alert) -> Alert:
        """
        If alert not found raise NoItemsFound
        """
        pass
    
    @abstractmethod
    def get_all_alerts(self, alert: Alert) -> Alert:
        pass
    
    @abstractmethod
    def delete_alert(self, alert: Alert) -> Alert:
        """
        If alert not found raise NoItemsFound
        """
        pass
    
    @abstractmethod
    def update_alert(self, alert: Alert) -> Alert:
        """
        If alert not found raise NoItemsFound
        """
        pass
