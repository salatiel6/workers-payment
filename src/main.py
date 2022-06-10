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
        employee = Employee(worked_schedule)

        print(
            f"The amount to pay {employee.name} is: "
            f"{employee.payment_amount} USD"
        )


if __name__ == '__main__':
    payment()
