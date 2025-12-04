import pytest, datetime
from src.core.entities import LicencePlate, DaysOfWeek

def test_valid_plate_creation():
    plate = LicencePlate("ABC-1234")
    assert str(plate) == "ABC-1234"
    assert plate.get_last_digit() == 4

def test_invalid_plate_creation():
    with pytest.raises(ValueError):
        LicencePlate("INVALID-PLATE")
    with pytest.raises(ValueError):
        LicencePlate("AB-1234")
    with pytest.raises(ValueError):
        LicencePlate("ABC-12345")
    with pytest.raises(ValueError):
        LicencePlate("ABC 1234")
    with pytest.raises(ValueError):
        LicencePlate("ABCD-1234")

def test_day_of_week_from_date():
    date = datetime.date(2025, 12, 1)  # Monday
    assert DaysOfWeek.from_date(date) == DaysOfWeek.MONDAY
    date = datetime.date(2025, 12, 7)  # Sunday
    assert DaysOfWeek.from_date(date) == DaysOfWeek.SUNDAY

def test_day_of_week_from_holiday():
    date = datetime.date(2025, 5, 24)  # Batalla de Pichincha
    assert DaysOfWeek.from_date(date) == DaysOfWeek.HOLIDAY
    date = datetime.date(2025, 5, 25)
    assert DaysOfWeek.from_date(date) != DaysOfWeek.HOLIDAY