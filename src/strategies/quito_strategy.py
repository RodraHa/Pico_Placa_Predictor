from src.core.entities import DaysOfWeek, HourRange, LicencePlate
from src.interfaces.restriction_strategy import RestrictionStrategy
import datetime

class QuitoStrategy(RestrictionStrategy):
    def __init__(self):
        self.hour_ranges = [
            HourRange(start=datetime.time(7, 0), end=datetime.time(9, 30)),
            HourRange(start=datetime.time(16, 0), end=datetime.time(19, 30))
        ]
        self.restriction_calendar = {
            DaysOfWeek.MONDAY: {1, 2},
            DaysOfWeek.TUESDAY: {3, 4},
            DaysOfWeek.WEDNESDAY: {5, 6},
            DaysOfWeek.THURSDAY: {7, 8},
            DaysOfWeek.FRIDAY: {9, 0},
            DaysOfWeek.SATURDAY: {},
            DaysOfWeek.SUNDAY: {},
            DaysOfWeek.HOLIDAY: {}
        }

    def is_restricted(self, licence_plate: LicencePlate, date: datetime.date, time: datetime.time) -> bool:
        plate_last_digit = licence_plate.get_last_digit()
        day_of_week = DaysOfWeek.from_date(date)
        if plate_last_digit not in self.restriction_calendar.get(day_of_week, set()):
            return False
        for hour_range in self.hour_ranges:
            if hour_range.contains(time):
                return True
        return False

    def get_calendar(self) -> dict[DaysOfWeek, set[int]]:
        return self.restriction_calendar

    def get_hour_ranges(self) -> list[HourRange]:
        return self.hour_ranges