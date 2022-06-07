from checkpoint import CheckPoint

with open("worked_schedules.txt", "r") as worked_schedules:
    for worked_schedule in worked_schedules:
        worker_checkpoint = worked_schedule.rstrip()
        worker_name = worker_checkpoint.split("=")[0]
        worker_schedule = worker_checkpoint.split("=")[1]
        worked = [worked for worked in worker_schedule.split(",")]
        checkpoint = CheckPoint(worker_name, worked)
        print(checkpoint.payment())
