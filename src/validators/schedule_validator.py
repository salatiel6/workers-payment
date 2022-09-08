import re

from exceptions import FilePatternError


class ScheduleValidator:
    def __init__(self, worked_schedule: str) -> None:
        self.__worked_schedule = worked_schedule

    def validate(self) -> FilePatternError | bool:
        rgx = "^(?:[A-Z]+)=(?:(?:MO|TU|WE|TH|FR|SA|SU)" \
              "(?:0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]-(?:0[0-9]|1[0-9]|2[0-3]):" \
              "[0-5][0-9](?:,|))+"

        if not re.findall(rgx, self.__worked_schedule) or \
                re.findall(rgx, self.__worked_schedule)[0] != \
                self.__worked_schedule:
            raise FilePatternError()

        return True
