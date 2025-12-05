import pytest, datetime
from src.core.entities import LicencePlate, DaysOfWeek
from src.strategies.quito_strategy import QuitoStrategy

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
    with pytest.raises(ValueError):
        LicencePlate("ABC-123D")

def test_day_of_week_from_date():
    date = datetime.date(2025, 12, 1)  # Monday
    assert DaysOfWeek.from_date(date) == DaysOfWeek.MONDAY
    date = datetime.date(2025, 12, 7)  # Sunday
    assert DaysOfWeek.from_date(date) == DaysOfWeek.SUNDAY

def test_day_of_week_from_holiday():
    date = datetime.date(2025, 5, 24)  # Batalla de Pichincha
    assert DaysOfWeek.from_date(date) == DaysOfWeek.HOLIDAY
    date = datetime.date(2025, 1, 1)  # New Year's Day
    assert DaysOfWeek.from_date(date) == DaysOfWeek.HOLIDAY
    date = datetime.date(2025, 5, 25)
    assert DaysOfWeek.from_date(date) != DaysOfWeek.HOLIDAY

def test_quito_strategy_restricted():
    strategy = QuitoStrategy()
    calendar = strategy.get_calendar()
    hour_ranges = strategy.get_hour_ranges()

    # Test Monday
    monday_digits = calendar[DaysOfWeek.MONDAY]
    test_digit = list(monday_digits)[0]
    plate = LicencePlate(f"ABC-123{test_digit}")
    date = datetime.date(2025, 12, 1)  # Monday
    time = hour_ranges[0].start
    assert strategy.is_restricted(plate, date, time) is True

    # Test Tuesday
    tuesday_digits = calendar[DaysOfWeek.TUESDAY]
    test_digit = list(tuesday_digits)[0]
    plate = LicencePlate(f"ABC-123{test_digit}")
    date = datetime.date(2025, 12, 2)  # Tuesday
    time = datetime.time(hour_ranges[0].start.hour, hour_ranges[0].start.minute + 30)
    assert strategy.is_restricted(plate, date, time) is True

    # Test Friday
    friday_digits = calendar[DaysOfWeek.FRIDAY]
    test_digit = list(friday_digits)[1]  # Get second digit (0)
    plate = LicencePlate(f"ABC-123{test_digit}")
    date = datetime.date(2025, 12, 5)  # Friday
    time = hour_ranges[1].start
    assert strategy.is_restricted(plate, date, time) is True

def test_quito_strategy_not_restricted():
    strategy = QuitoStrategy()
    calendar = strategy.get_calendar()
    hour_ranges = strategy.get_hour_ranges()

    # Test with wrong day
    tuesday_digits = calendar[DaysOfWeek.TUESDAY]
    test_digit = list(tuesday_digits)[1]
    plate = LicencePlate(f"ABC-123{test_digit}")
    date = datetime.date(2025, 12, 3)  # Wednesday
    time = hour_ranges[0].start
    assert strategy.is_restricted(plate, date, time) is False

    # Test with correct day but outside time ranges
    friday_digits = calendar[DaysOfWeek.FRIDAY]
    test_digit = list(friday_digits)[1]
    plate = LicencePlate(f"ABC-123{test_digit}")
    date = datetime.date(2025, 12, 5)  # Friday
    time = datetime.time(
        (hour_ranges[0].end.hour + hour_ranges[1].start.hour) // 2, 0
    )
    assert strategy.is_restricted(plate, date, time) is False

    # Test on weekend
    monday_digits = calendar[DaysOfWeek.MONDAY]
    test_digit = list(monday_digits)[0]
    plate = LicencePlate(f"ABC-123{test_digit}")
    date = datetime.date(2025, 11, 30)  # Sunday
    time = hour_ranges[0].start
    assert strategy.is_restricted(plate, date, time) is False

def test_quito_strategy_holiday():
    strategy = QuitoStrategy()
    calendar = strategy.get_calendar()
    hour_ranges = strategy.get_hour_ranges()

    # Test that holidays have no restrictions
    tuesday_digits = calendar[DaysOfWeek.TUESDAY]
    test_digit = list(tuesday_digits)[0]
    plate = LicencePlate(f"ABC-123{test_digit}")
    date = datetime.date(2025, 5, 24)  # Holiday (Batalla de Pichincha)
    time = hour_ranges[0].start
    assert strategy.is_restricted(plate, date, time) is False

def test_quito_strategy_edge_times():
    strategy = QuitoStrategy()
    calendar = strategy.get_calendar()

    # Test exact start time
    monday_digits = calendar[DaysOfWeek.MONDAY]
    test_digit = list(monday_digits)[0]
    plate = LicencePlate(f"ABC-123{test_digit}")
    date = datetime.date(2025, 12, 1)  # Monday
    time = strategy.get_hour_ranges()[0].start
    assert strategy.is_restricted(plate, date, time) is True

    # Test exact end time
    time = strategy.get_hour_ranges()[0].end
    assert strategy.is_restricted(plate, date, time) is True