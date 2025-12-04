from datetime import datetime
from core.entities import LicencePlate
from services.predictor import Predictor
from strategies.quito_strategy import QuitoStrategy

if __name__ == '__main__':
    print("Welcome to the \"Pico y Placa\" Predictor")
    while True:
        plate_input = input("Enter your licence plate (format ABC-1234) or 'exit' to quit: ")
        if plate_input.lower() == 'exit':
            break
        try:
            plate = LicencePlate(plate_input)
        except ValueError as e:
            print(e)
            continue
        date_input = input("Enter the date (YYYY-MM-DD): ")
        time_input = input("Enter the time (HH:MM): ")
        try:
            date = datetime.strptime(date_input, "%Y-%m-%d").date()
            time = datetime.strptime(time_input, "%H:%M").time()
            print(f"You entered plate: {plate}, date: {date}, time: {time}")
            predictor = Predictor()
            predictor.set_restriction_strategy(QuitoStrategy())
            if predictor.can_drive(plate, date, time):
                 print("You can drive!")
            else:
                 print("You cannot drive")
        except Exception as e:
            print("Invalid date or time format. Please try again.")
            continue