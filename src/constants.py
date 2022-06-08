from datetime import datetime

FILE_LINES = [
    "RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,"
    "SU20:00-21:00",
    "ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00"
]

WEEK_DAYS = ["MO", "TU", "WE", "TH", "FR"]
WEEKEND_DAYS = ["SA", "SU"]

PERIODS = {
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

HOUR_PAYMENT_VALUES = {
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
