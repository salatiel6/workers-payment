from unittest import TestCase
from ioet_challenge.src import main
from ioet_challenge.src.exceptions import FileError


class TestEmployee(TestCase):
    def test_create_file_if_not_exists(self):
        with self.assertRaises(FileError):
            main.payment("test_file.txt")
