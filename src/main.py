from datetime import datetime
from core.entities import LicencePlate
from services.predictor import Predictor
from src.interfaces.restriction_strategy import RestrictionStrategy
from strategies.quito_strategy import QuitoStrategy

def print_header():
    print("=" * 50)
    print(" " * 13 + "Pico y Placa Predictor")
    print("=" * 50)

def print_rules(concrete_strategy: RestrictionStrategy):
    print("-" * 50)
    print("Restriction Rules:")
    calendar = concrete_strategy.get_calendar()
    hour_ranges = concrete_strategy.get_hour_ranges()
    for day, digits in calendar.items():
        digits_str = ', '.join(str(d) for d in digits) if digits else "No restrictions"
        print(f"{day.name}: Restricted digits: {digits_str}")
    print("Restricted Hours:")
    for hr in hour_ranges:
        print(f"From {hr.start.strftime('%H:%M')} to {hr.end.strftime('%H:%M')}")
    print("-" * 50 + "\n")

def get_plate_input() -> LicencePlate:
    while True:
        plate_input = input("Enter your licence plate (format ABC-1234): ").strip().upper()
        try:
            return LicencePlate(plate_input)
        except ValueError as e:
            print(e)

def get_date_input() -> datetime.date:
    while True:
        date_input = input("Enter the date (YYYY-MM-DD): ").strip()
        try:
            return datetime.strptime(date_input, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please try again.")

def get_time_input() -> datetime.time:
    while True:
        time_input = input("Enter the time (HH:MM): ").strip()
        try:
            return datetime.strptime(time_input, "%H:%M").time()
        except ValueError:
            print("Invalid time format. Please try again.")

def show_result(can_drive: bool):
    print("\n" + "-" * 50)
    if can_drive:
        print("Result: You can drive! （￣︶￣）↗")
    else:
        print("Result: You cannot drive. (┬┬﹏┬┬)")

if __name__ == '__main__':
    strategy = QuitoStrategy()

    print_header()
    print_rules(strategy)
    plate = get_plate_input()
    date = get_date_input()
    time = get_time_input()

    predictor = Predictor()
    predictor.set_restriction_strategy(strategy)
    can_drive = predictor.can_drive(plate, date, time)

    show_result(can_drive)