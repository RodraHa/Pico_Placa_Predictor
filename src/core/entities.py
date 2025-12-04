from enum import Enum
from dataclasses import dataclass
import re, datetime, holidays

class LicencePlate:
    def __init__(self, plate_number: str):
        if not self.is_plate_valid(plate_number):
            raise ValueError("Invalid plate number format")
        self.plate_number = plate_number

    def __str__(self):
        return self.plate_number

    def get_last_digit(self) -> int:
        return int(self.plate_number[-1])

    @staticmethod
    def is_plate_valid(plate_number: str) -> bool:
        pattern = r'^[A-Z]{3}-\d{4}$'
        return re.match(pattern, plate_number) is not None


class DaysOfWeek(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6
    HOLIDAY = 7

    @staticmethod
    def from_date(date: datetime.date):
        ec_holidays = holidays.EC(years=date.year)
        if date in ec_holidays:
            return DaysOfWeek.HOLIDAY
        return DaysOfWeek(date.weekday())

@dataclass(frozen=True)
class HourRange:
    start: datetime.time
    end: datetime.time

    def contains(self, time: datetime.time) -> bool:
        return self.start <= time <= self.end