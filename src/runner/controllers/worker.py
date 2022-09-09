class Worker:
    def __init__(self, worker_data: {}) -> None:
        self.__name = worker_data["name"]
        self.__worked = worker_data["worked"]
        self.__payment_amount = 0

    @property
    def name(self) -> str:
        return self.__name

    @property
    def worked(self) -> []:
        return self.__worked

    @property
    def payment_amount(self) -> int:
        return self.__payment_amount

    @payment_amount.setter
    def payment_amount(self, payment_amount):
        self.__payment_amount = payment_amount
