import os

from exceptions import FileError


class FileHandler:
    def __init__(self, file) -> None:
        self.__worked_schedules = self.read_file(file)

    @property
    def worked_schedules(self) -> []:
        return self.__worked_schedules

    def read_file(self, file):
        self.file_exists(file)

        f = open(file, "r")
        worked_schedules = f.readlines()
        f.close()

        return worked_schedules

    @staticmethod
    def file_exists(file) -> None:
        if not os.path.isfile(file):
            raise FileError()
