import re

from datetime import datetime, timedelta

from ioet_challenge.src.exceptions import FilePatternError
from ioet_challenge.src.config import Config


class Employee:
    def __init__(self, worked_schedule: str):
        self.name = ""
        self.worked_time = ""
        self.worked_schedule = worked_schedule
        self.get_employee_data()
        self.payment_amount = self.calculate_payment_amount()

    def __str__(self):
        return f"The amount to pay {self.name} is: " \
               f"{self.payment_amount} USD"

    def get_employee_data(self):
        if not self.validate_schedule():
            raise FilePatternError()

        worker_name = self.worked_schedule.split("=")[0]
        worker_schedule = self.worked_schedule.split("=")[1]

        worked_time = [worked for worked in worker_schedule.split(",")]

        self.name = worker_name
        self.worked_time = worked_time

    def calculate_payment_amount(self) -> int:
        amount = 0
        for day_n_hour in self.worked_time:
            day = day_n_hour[0:2]
            str_entering = day_n_hour[2:].split("-")[0]
            str_exiting = day_n_hour[2:].split("-")[1]

            entering = datetime.strptime(str_entering, "%H:%M")
            exiting = datetime.strptime(str_exiting, "%H:%M")

            time_counter = entering

            while entering <= time_counter < exiting:
                time_counter += timedelta(hours=1)
                period = self.get_period(time_counter)
                amount += self.get_hour_payment(day, period)

        return amount

    def validate_schedule(self) -> bool:
        rgx = "^(?:[A-Z]+)=(?:(?:MO|TU|WE|TH|FR|SA|SU)" \
              "(?:0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]-(?:0[0-9]|1[0-9]|2[0-3]):" \
              "[0-5][0-9](?:,|))+"

        if not re.findall(rgx, self.worked_schedule) or \
                re.findall(rgx, self.worked_schedule)[0] != \
                self.worked_schedule:
            return False

        return True

    @staticmethod
    def get_period(time) -> str:
        config = Config()

        periods = config.periods

        if periods["P1"]["entering"] <= time <= periods["P1"]["exiting"]:
            return "P1"
        if periods["P2"]["entering"] <= time <= periods["P2"]["exiting"]:
            return "P2"
        if periods["P3"]["entering"] <= time >= periods["P3"]["exiting"]:
            return "P3"

    @staticmethod
    def get_hour_payment(day, period) -> int:
        config = Config()

        week_days = config.week_days
        weekend_days = config.weekend_days
        hourly_payment_values = config.hourly_payment_values

        if day in week_days:
            return hourly_payment_values["week"][period]
        if day in weekend_days:
            return hourly_payment_values["weekend"][period]
