from unittest import TestCase
from ioet_challenge.src import main
from ioet_challenge.src.employee import Employee
from ioet_challenge.src.exceptions import FileError, FilePatternError


class TestEmployee(TestCase):
    def test_create_file_if_not_exists(self):
        with self.assertRaises(FileError):
            main.payment("test_file.txt")

    def test_input_out_of_pattern(self):
        invalid_inputs = self.create_invalid_inputs()

        for invalid_input in invalid_inputs:
            try:
                self.assertRaises(
                    FilePatternError,
                    Employee, invalid_input
                )
            except Exception:
                raise Exception(f"Exeption not thrown for this input: "
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
            "RENE=MO10:00-12:00,TU10:00-12:00,SA14:00-18:99,SU20:00-21:00"
        ]
