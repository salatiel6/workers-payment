import os.path

from ioet_challenge.src.employee import Employee
from ioet_challenge.src.exceptions import FileError


def payment(file="../worked_schedules.txt") -> None:
    if not os.path.isfile(file):
        raise FileError()

    f = open(file, "r")
    worked_schedules = f.readlines()
    f.close()

    for worked_schedule in worked_schedules:
        employee = Employee(worked_schedule.rstrip())

        print(employee)


if __name__ == '__main__':
    payment()
