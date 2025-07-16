from src.shared.domain.entities.alert import alert
from src.shared.helpers.errors.domain_errors import EntityError, EntityParameterOrderDatesError
import pytest
import time
import uuid

class Test_Alert:
    def test_alert(self):
        alert (alert_id=str(uuid.uuid4()), title = "Aviso", description = "quadra molhada por conta da chuva", start_date = int(time.time()), end_date =  int(time.time()) + 7200000, severity = 2)
    
    def test_alert_id_is_none(self):
        with pytest.raises(EntityError):
            alert(alert_id=None, title = None, description = "quadra molhada por conta da chuva", start_date = int(time.time()), end_date =  int(time.time()) + 7200000, severity = 2)
    
    def test_alert_id_is_not_string(self):
        with pytest.raises(EntityError):
            alert(alert_id=1, title = None, description = "quadra molhada por conta da chuva", start_date = int(time.time()), end_date =  int(time.time()) + 7200000, severity = 2)
    
    def test_alert_it_is_not_valid_uuid(self):
        with pytest.raises(EntityError):
            alert(alert_id="123321adf-asdas2122", title = None, description = "quadra molhada por conta da chuva", start_date = int(time.time()), end_date =  int(time.time()) + 7200000, severity = 2)
    
    def test_title_is_none(self):
        with pytest.raises(EntityError):
            alert(alert_id=str(uuid.uuid4()), title = None, description = "quadra molhada por conta da chuva", start_date = int(time.time()), end_date =  int(time.time()) + 7200000, severity = 2)
    
    def test_title_is_not_str(self):
        with pytest.raises(EntityError):
            alert(alert_id=str(uuid.uuid4()), title = 123, description = "quadra molhada por conta da chuva", start_date = int(time.time()), end_date =  int(time.time()) + 7200000, severity = 2)
    
    def test_title_first_char_is_not_uppercase(self):
        with pytest.raises(EntityError):
            alert(
                alert_id=str(uuid.uuid4()), title="aviso",description="quadra molhada por conta da chuva", start_date=int(time.time()), end_date=int(time.time()) + 7200000,severity=2)
    
    def test_description_is_none(self):
        with pytest.raises(EntityError):
            alert(
                alert_id=str(uuid.uuid4()), 
                title="Aviso",
                description=None,
                start_date=int(time.time()),
                end_date=int(time.time()) + 7200000,
                severity=2
            )
    
    def test_description_is_not_str(self):
        with pytest.raises(EntityError):
            alert(
                alert_id=str(uuid.uuid4()), 
                title="Aviso",
                description=123,
                start_date=int(time.time()),
                end_date=int(time.time()) + 7200000,
                severity=2
            )   
    
    def test_dates_are_not_ints(self):
        with pytest.raises(EntityError):
            alert(
                alert_id=str(uuid.uuid4()), 
                title="Aviso",
                description="quadra molhada",
                start_date="hoje",
                end_date="amanha",
                severity=2
            )
            
    def test_start_date_greater_than_end_date(self):
        with pytest.raises(EntityParameterOrderDatesError):
            now = int(time.time())
            alert(
                alert_id=str(uuid.uuid4()), 
                title="Aviso",
                description="quadra molhada",
                start_date=now + 7200000,
                end_date=now,
                severity=2
            )
    
    def test_severity_is_none(self):
        with pytest.raises(EntityError):
            alert(
                alert_id=str(uuid.uuid4()), 
                title="Aviso",
                description="quadra molhada",
                start_date=int(time.time()),
                end_date=int(time.time()) + 7200000,
                severity=None
            )
     
    @pytest.mark.parametrize("severity", [0, 4, -1, 10])
    def test_severity_out_of_bounds(self, severity):
        with pytest.raises(EntityError):
            alert(
                alert_id=str(uuid.uuid4()), 
                title="Aviso",
                description="quadra molhada",
                start_date=int(time.time()),
                end_date=int(time.time()) + 7200000,
                severity=severity
            )

     