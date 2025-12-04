from abc import ABC, abstractmethod

from src.core.entities import DaysOfWeek


class RestrictionStrategy(ABC):
    @abstractmethod
    def get_calendar(self) -> dict[DaysOfWeek, set[int]]:
        pass

    @abstractmethod
    def is_restricted(self, licence_plate: str, date: str, time: str) -> bool:
        pass