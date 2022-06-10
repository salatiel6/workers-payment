import re

from datetime import datetime, timedelta

from ioet_challenge.src.exceptions import FilePatternError
from ioet_challenge.src.constants import WEEK_DAYS, WEEKEND_DAYS, PERIODS, \
    HOUR_PAYMENT_VALUES


class Employee:
    def __init__(self, worked_schedule: str):
        self.name = ""
        self.worked_time = ""
        self.get_employee_data(worked_schedule)
        self.payment_amount = self.calculate_payment_amount()

    def get_employee_data(self, worked_schedule):
        worker_checkpoint = worked_schedule.rstrip()

        if not self.validate_schedule(worked_schedule):
            raise FilePatternError()

        worker_name = worker_checkpoint.split("=")[0]
        worker_schedule = worker_checkpoint.split("=")[1]

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

    @staticmethod
    def validate_schedule(worker_schedule: str) -> bool:
        rgx = "^(?:MO|TU|WE|TH|FR|SA|SU)(?:0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]" \
              "-(?:0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]"
        if worker_schedule.count("=") != 1:
            return False
        if worker_schedule.split("=")[0][-1] == ",":
            return False

        worked_time = [worked for worked in
                       worker_schedule.split("=")[1].split(",")]
        for worked_day in worked_time:
            if not re.findall(rgx, worked_day):
                return False

        return True

    @staticmethod
    def get_period(time) -> str:
        if PERIODS["P1"]["entering"] <= time <= PERIODS["P1"]["exiting"]:
            return "P1"
        if PERIODS["P2"]["entering"] <= time <= PERIODS["P2"]["exiting"]:
            return "P2"
        if PERIODS["P3"]["entering"] <= time >= PERIODS["P3"]["exiting"]:
            return "P3"

    @staticmethod
    def get_hour_payment(day, period) -> int:
        if day in WEEK_DAYS:
            return HOUR_PAYMENT_VALUES["week"][period]
        if day in WEEKEND_DAYS:
            return HOUR_PAYMENT_VALUES["weekend"][period]
