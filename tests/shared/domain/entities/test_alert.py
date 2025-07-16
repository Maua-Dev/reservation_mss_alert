from src.shared.domain.entities.alert import alert
from src.shared.helpers.errors.domain_errors import EntityError
import pytest
import time

class Test_Alert:
    def test_alert(self):
        alert (title = "Aviso", description = "quadra molhada por conta da chuva", start_date = time.time(), end_date =  time.time() + 7200000, severity = 2)
    