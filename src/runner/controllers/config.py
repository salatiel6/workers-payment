from datetime import datetime


class Config:
    _week_days = {
        "MO": "monday",
        "TU": "tuesday",
        "WE": "wednesday",
        "TH": "thursday",
        "FR": "friday"
    }

    _weekend_days = {
        "SA": "saturday",
        "SU": "sunday"
    }

    _periods = {
        "P1": {
            "entering": datetime.strptime("00:01", "%H:%M"),
            "exiting": datetime.strptime("09:00", "%H:%M")
        },
        "P2": {
            "entering": datetime.strptime("09:01", "%H:%M"),
            "exiting": datetime.strptime("18:00", "%H:%M")
        },
        "P3": {
            "entering": datetime.strptime("18:01", "%H:%M"),
            "exiting": datetime.strptime("00:00", "%H:%M")
        }
    }

    _hourly_payment_values = {
        "week": {
            "P1": 25,
            "P2": 15,
            "P3": 20
        },
        "weekend": {
            "P1": 30,
            "P2": 20,
            "P3": 25
        }
    }

    @property
    def week_days(self):
        return self._week_days

    @property
    def weekend_days(self):
        return self._weekend_days

    @property
    def periods(self):
        return self._periods

    @property
    def hourly_payment_values(self):
        return self._hourly_payment_values
