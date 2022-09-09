from datetime import timedelta
from .worker import Worker
from .config import Config


class PaymentHandler:
    def __init__(self, worker: Worker):
        self.__worker = worker
        self.days_n_periods = self.set_days_n_periods()

    def set_days_n_periods(self):
        days_n_periods = []

        for worked in self.__worker.worked:
            start = worked["start"]
            finish = worked["finish"]

            time_counter = start

            while start <= time_counter < finish:
                time_counter += timedelta(hours=1)

                day_n_period = {
                    "day": worked["day"],
                    "period": self.get_period(time_counter)
                }

                days_n_periods.append(day_n_period)

        return days_n_periods

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

    def get_hour_payment(self) -> int:
        config = Config()

        week_days = config.week_days
        weekend_days = config.weekend_days
        hourly_payment_values = config.hourly_payment_values

        payment_amount = 0

        for day_n_period in self.days_n_periods:
            if day_n_period["day"] in week_days.values():
                payment_amount += \
                    hourly_payment_values["week"][day_n_period["period"]]
            if day_n_period["day"] in weekend_days.values():
                payment_amount += \
                    hourly_payment_values["weekend"][day_n_period["period"]]

        return payment_amount
