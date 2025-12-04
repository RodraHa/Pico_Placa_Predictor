from datetime import datetime
from src.core.entities import LicencePlate
from src.interfaces.restriction_strategy import RestrictionStrategy

class Predictor:
    def __init__(self):
        self.strategy = None

    def set_restriction_strategy(self, strategy: RestrictionStrategy):
        self.strategy = strategy

    def can_drive(self, licence_plate: LicencePlate, date: datetime.date, time: datetime.time) -> bool:
        return not self.strategy.is_restricted(licence_plate, date, time)