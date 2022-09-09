from datetime import datetime
from .config import Config


class Adapter:
    def __init__(self, worked_schedule: str) -> None:
        self.__worker_data = self.set_worker_data(worked_schedule)

    @property
    def worker_data(self) -> {}:
        return self.__worker_data

    @staticmethod
    def set_worker_data(worker_schedule: str) -> {}:
        worker_data = {
            "name": worker_schedule.split("=")[0],
            "worked": []
        }

        raw_worker_times = worker_schedule.split("=")[1]

        worker_times = [worked for worked in raw_worker_times.split(",")]

        config = Config()

        for day_n_hour in worker_times:
            worked = {}
            day = day_n_hour[0:2]

            if day in config.week_days.keys():
                worked["day"] = config.week_days[day]
            if day in config.weekend_days.keys():
                worked["day"] = config.weekend_days[day]

            str_entering = day_n_hour[2:].split("-")[0]
            str_exiting = day_n_hour[2:].split("-")[1]

            worked["start"] = datetime.strptime(str_entering, "%H:%M")
            worked["finish"] = datetime.strptime(str_exiting, "%H:%M")

            worker_data["worked"].append(worked)

        return worker_data
