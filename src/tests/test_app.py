import os

from unittest import TestCase
from runner import Runner
from runner.controllers import FileHandler, ScheduleValidator, Adapter,\
    Worker, PaymentHandler
from exceptions import FileError, FilePatternError
from datetime import datetime


class TestApp(TestCase):
    def test_default_file(self):
        """
        Testing the FileHandler class with the default file.
        It must pass without raising any exception.
        """

        file_handler = FileHandler("../worked_schedules.txt")
        assert file_handler.worked_schedules

    def test_if_file_not_exists(self):
        """
        Testing FileHandler class trying to pass a nonexistent file.
        It must raise a FileError exception.
        """

        with self.assertRaises(FileError):
            FileHandler("test_file.txt")

    def test_with_new_valid_file(self):
        """
        Creating a new custom file, and passing it as a param
        for FileHandler class.
        It must pass without raising any exception.
        """

        file_lines = [
            "LANCE=MO08:00-12:00,TH01:00-04:00,FR14:00-18:00,SA17:00-21:00",
            "LEWIS=WE06:00-12:00,TH10:00-12:00,FR01:00-03:00,SU20:00-21:00"
        ]
        with open("test_file.txt", "w") as file:
            file.writelines([line + "\n" for line in file_lines])

        FileHandler("test_file.txt")

        os.remove("test_file.txt")

    def test_schedule_validator_with_valid_input(self):
        """
        Testing the ScheduleValidator class with a valid input.
        It must pass without raising any exception
        """

        valid_input = "JOHN=FR02:00-03:00,SA17:00-18:00,SU20:00-21:00"
        assert ScheduleValidator(valid_input)

    def test_schedule_validator_with_invalid_input(self):
        """
        Calling the ScheduleValidator class, passing some invalid inputs that
        are created in a list.
        It must raise an FilePatternError exception for every iteration
        in the invalid_inputs list.
        If some iteration does not raise an FilePatterError exception,
        a default exception is raised, specifying which iteration passed
        by the exception handler.
        """

        invalid_inputs = [
            "RENEMO10:00-12:00,TU10:00-12:00,SA14:00-18:00,SU20:00-21:00",
            "REN=EMO10:00-12:00,TU10:00-12:00,SA14:00-18:00,SU20:00-21:00",
            "RENEMO10:00-12:00,TU10:00-12:00,=SA14:00-18:00,SU20:00-21:00",
            "RENE=MO10:00-12:00,T=U10:00-12:00,SA14:00-18:00,SU20:00-21:00",
            "RENE=MO10:00-12:00,=TU10:00-12:00,SA14:00-18:00,SU20:00-21:00",
            "sdkurghsidfrjgh",
            "AZSDFSAD=ASDFSDAF"
            "RENE=MO55:00-12:00,TU10:00-12:00,SA14:00-18:00,SU20:00-21:00",
            "RENE=MO10:00-12:00,TU10:00-12:00,SA14:00-18:99,SU20:00-21:00",
            "RENEMO10:00-12:00=TU10:00-12:00,SA14:00-18:00,SU20:00-21:00"
        ]

        for invalid_input in invalid_inputs:
            try:
                self.assertRaises(
                    FilePatternError,
                    ScheduleValidator, invalid_input
                )
            except Exception:
                raise Exception(f"Exeption not raised for this input: "
                                f"{invalid_input}")

    def test_adapter(self):
        worked_schedule = "JAMES=TU09:00-12:00,WE10:00-14:00,TH01:00-04:00," \
                          "FR08:00-18:00,SU20:00-22:00"

        adapter = Adapter(worked_schedule)

        assert adapter.worker_data

    def test_worker_constructors(self):
        worker_data = {
            "name": "TESTER",
            "worked": [
                {
                    "day": "monday",
                    "start": datetime.strptime("10:00", "%H:%M"),
                    "finish": datetime.strptime("10:00", "%H:%M")
                },
                {
                    "day": "tuesday",
                    "start": datetime.strptime("10:00", "%H:%M"),
                    "finish": datetime.strptime("12:00", "%H:%M")
                }
            ]
        }

        worker = Worker(worker_data)

        assert worker.name == "TESTER"
        assert len(worker.worked) == 2

    def test_payment_handler(self):
        worker_data = {
            "name": "TESTER",
            "worked": [
                {
                    "day": "monday",
                    "start": datetime.strptime("10:00", "%H:%M"),
                    "finish": datetime.strptime("12:00", "%H:%M")
                },
                {
                    "day": "tuesday",
                    "start": datetime.strptime("10:00", "%H:%M"),
                    "finish": datetime.strptime("12:00", "%H:%M")
                },
                {
                    "day": "thursday",
                    "start": datetime.strptime("01:00", "%H:%M"),
                    "finish": datetime.strptime("03:00", "%H:%M")
                },
                {
                    "day": "saturday",
                    "start": datetime.strptime("14:00", "%H:%M"),
                    "finish": datetime.strptime("18:00", "%H:%M")
                },
                {
                    "day": "sunday",
                    "start": datetime.strptime("20:00", "%H:%M"),
                    "finish": datetime.strptime("21:00", "%H:%M")
                }
            ]
        }

        worker = Worker(worker_data)
        payment_handler = PaymentHandler(worker)

        worker.payment_amount = payment_handler.get_hour_payment()

        assert worker.payment_amount == 215

    def test_runner(self):
        runner = Runner()
        runner.build_components("../worked_schedules.txt")
        runner.run_components()