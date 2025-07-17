from abc import ABC, abstractmethod
from typing import List

from src.shared.domain.entities.alert import Alert


class IAlertRepository(ABC):

    @abstractmethod
    def create_alert(self, alert: Alert) -> Alert:
        """
        If user not found raise NoItemsFound
        """
        pass

