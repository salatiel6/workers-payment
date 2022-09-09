import config_path # noqa

from runner.controllers import FileHandler
from validators import ScheduleValidator

if __name__ == "__main__":
    file_handler = FileHandler("worked_schedules.txt")
    for worked_schedule in file_handler.worked_schedules:
        schedule_validator = ScheduleValidator(worked_schedule.rstrip())
        if schedule_validator.validate():
            pass
