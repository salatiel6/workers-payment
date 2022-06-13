import os

from unittest import TestCase
from ioet_challenge.src import main
from ioet_challenge.src.employee import Employee
from ioet_challenge.src.exceptions import FileError, FilePatternError


class TestEmployee(TestCase):
    def test_valid_file(self):
        """
        Testing the main.payment() function with the default file.
        It must pass without raising any exception.
        """

        main.payment("../worked_schedules.txt")

    def test_if_file_not_exists(self):
        """
        Testing main.payment() function trying to pass a nonexistent file.
        It must raise a FileError exception.
        """

        with self.assertRaises(FileError):
            main.payment("test_file.txt")

    def test_with_new_file(self):
        """
        Creating a new custom file, and passing it as a param
        for main.payment().
        It must pass without raising any exception.
        """

        file_lines = [
            "LANCE=MO08:00-12:00,TH01:00-04:00,FR14:00-18:00,SA17:00-21:00",
            "LEWIS=WE06:00-12:00,TH10:00-12:00,FR01:00-03:00,SU20:00-21:00"
        ]
        with open("test_file.txt", "w") as file:
            file.writelines([line + "\n" for line in file_lines])

        main.payment("test_file.txt")

        os.remove("test_file.txt")

    def test_valid_input(self):
        """
        Calling the Employee class directly, passing a valid input.
        It must not raise any exception, and must assert the name and the
        payment amount.
        """

        valid_input = "JOHN=FR02:00-03:00,SA17:00-18:00,SU20:00-21:00"
        employee = Employee(valid_input)
        print(employee)
        self.assertEqual(employee.name, "JOHN")
        self.assertEqual(employee.payment_amount, 70)

    def test_input_out_of_pattern(self):
        """
        Calling the Employee class directly, passing some invalid inputs that
        are created by create_invalid_input().
        It must raise an FilePatternError excerption for every iteration
        in the invalid_inputs list.
        If some iteration does not raise an FilePatterError exception,
        a default exception is raised, specifying which iteration passed
        by the exception handler.
        """

        invalid_inputs = self.create_invalid_inputs()

        for invalid_input in invalid_inputs:
            try:
                self.assertRaises(
                    FilePatternError,
                    Employee, invalid_input
                )
            except Exception:
                raise Exception(f"Exeption not raised for this input: "
                                f"{invalid_input}")

    @staticmethod
    def create_invalid_inputs():
        return [
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
