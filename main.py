from datetime import datetime, timedelta

from employee import Employee
from contants import WEEK_DAYS, WEEKEND_DAYS, PERIODS, HOUR_PAYMENT_VALUES

file = open("worked_schedules.txt", "r")
worked_schedules = file.readlines()
file.close()


def main() -> None:
    for worked_schedule in worked_schedules:
        employee_data = get_employee_data(worked_schedule)
        employee = Employee(
            employee_data["name"],
            employee_data["worked_time"]
        )

        payment_amount = calculate_payment_amount(employee)

        print(f"The amount to pay {employee.name} is: {payment_amount} USD")


def get_employee_data(worked_schedule) -> {}:
    worker_checkpoint = worked_schedule.rstrip()
    worker_name = worker_checkpoint.split("=")[0]
    worker_schedule = worker_checkpoint.split("=")[1]
    worked_time = [worked for worked in worker_schedule.split(",")]

    return {
        "name": worker_name,
        "worked_time": worked_time
    }


def calculate_payment_amount(employee: Employee) -> int:
    amount = 0
    for day_n_hour in employee.worked_time:
        day = day_n_hour[0:2]
        str_entering = day_n_hour[2:].split("-")[0]
        str_exiting = day_n_hour[2:].split("-")[1]

        entering = datetime.strptime(str_entering, "%H:%M")
        exiting = datetime.strptime(str_exiting, "%H:%M")
        time_counter = entering

        while entering <= time_counter < exiting:
            time_counter += timedelta(hours=1)
            period = get_period(time_counter)
            amount += get_hour_payment(day, period)

    return amount


def get_period(time) -> str:
    if PERIODS["P1"]["entering"] <= time <= PERIODS["P1"]["exiting"]:
        return "P1"
    if PERIODS["P2"]["entering"] <= time <= PERIODS["P2"]["exiting"]:
        return "P2"
    if PERIODS["P3"]["entering"] <= time >= PERIODS["P3"]["exiting"]:
        return "P3"


def get_hour_payment(day, period) -> int:
    if day in WEEK_DAYS:
        return HOUR_PAYMENT_VALUES["week"][period]
    if day in WEEKEND_DAYS:
        return HOUR_PAYMENT_VALUES["weekend"][period]


if __name__ == '__main__':
    main()
