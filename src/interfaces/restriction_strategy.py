from abc import ABC, abstractmethod
from src.core.entities import DaysOfWeek, LicencePlate, HourRange
import datetime

class RestrictionStrategy(ABC):
    @abstractmethod
    def get_calendar(self) -> dict[DaysOfWeek, set[int]]:
        pass

    @abstractmethod
    def is_restricted(self, licence_plate: LicencePlate, date: datetime.date, time: datetime.time) -> bool:
        pass

    @abstractmethod
    def get_hour_ranges(self) -> list[HourRange]:
        pass