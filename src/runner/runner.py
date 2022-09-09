from .controllers import FileHandler, ScheduleValidator, Adapter, Worker,\
    PaymentHandler


class Runner:
    def __init__(self) -> None:
        self.__components = []

    def build_components(self, file) -> None:
        file_handler = FileHandler(file)
        worked_schedules = file_handler.worked_schedules

        for worked_schedule in worked_schedules:
            worked_schedule = worked_schedule.rstrip()

            ScheduleValidator(worked_schedule)

            adapter = Adapter(worked_schedule)
            self.__components.append(adapter.worker_data)

    def run_components(self):
        for component in self.__components:
            worker = Worker(component)
            payment_handler = PaymentHandler(worker)

            worker.payment_amount = payment_handler.get_hour_payment()

            print(
                f"The amount to pay {worker.name} is: {worker.payment_amount}"
            )
