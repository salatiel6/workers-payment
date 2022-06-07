class CheckPoint:
    def __init__(self, name: str, worked: []):
        self.name = name
        self.worked = worked

    def payment(self):
        return self.name, self.worked
