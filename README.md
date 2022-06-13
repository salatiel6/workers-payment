![](https://img.shields.io/badge/release-v0.7.4-gold)  
![](https://img.shields.io/badge/python-v3.10.1-blue)

![](https://img.shields.io/badge/passed_tests-2-brightgreen)
![](https://img.shields.io/badge/failed_tests-0-red)  
![](https://img.shields.io/badge/coverage-0%25-green)

## Solution Tree
### The `main.py` module:
The running process occurs in `main.py`. Module responsible for making every method of `Employee` class work.  
Its main function is `payment()`, which receives `worked_schedules.txt` by default as a param.
But you can create another file and pass it when calling the method.  

The first thing the function do, is to check if the param file exists:
```
if not os.path.isfile(file):
    raise FileError()
```
If not, a custom error is raised `FileError`, explainig what happened, and what should be done:
```
The employee schedule file was not found.
Please attach your file in the root of the project
By default, the file should be called 'worked_schedules.txt'. But you can use another name.
Just remember to put your custom file name in the params of payment() function
```
After validating that the file exists, the function read its content, allocating every line inside `worked_schedules` list:
```
f = open(file, "r")
    worked_schedules = f.readlines()
    f.close()
```

Then, for every line, we create an instance of the `Employee` class:
```
for worked_schedule in worked_schedules:
    employee = Employee(worked_schedule.rstrip())
```
> *Obs**: The `Employee` class, can be called just passing the schedule string in the right format:
> ```
> >>> from ioet_challenge.src.employee import Employee
> >>> worker_schedule = "ROBERT=MO06:00-12:00,WE11:00-15:00,TH01:00-03:00,FR15:00-18:00,SA19:00-21:00"
> >>> employee = Employee(worker_schedule)
> ```
> And then you can check every detail:
> ```
> >>> employee.name
> 'ROBERT'
>     
> >>> employee.worked_time
> ['MO06:00-12:00', 'WE11:00-15:00', 'TH01:00-03:00', 'FR15:00-18:00', 'SA19:00-21:00']
>     
> >>> employee.payment_amount
> 325
> ```

Finishing, we print the `employee__str__`, which contains the name, and the amount for the employee:
```
print(employee)
```
---
### The `employee.py` module
It's the module that contains the Employee class, which its methods make all the necessary validations and processes for 
calculating the payment amount.  

Its `__init__` method receives the `worked_schedule` variable, which must contain a line of `worked_schedules.txt`. This line must be a string
in the default format, e.g: `"JOHN=FR02:00-03:00,SA17:00-18:00,SU20:00-21:00"`.  
As we can see, the name, and the worked time of an employee, is on the file. So the variables `name` and `worked_time` are initiated as empty strings.  
After that, the method `get_employee_data()` will be responsable for bringing value to these variables.
```
def __init__(self, worked_schedule: str):
    self.name = ""
    self.worked_time = ""
    self.worked_schedule = worked_schedule
    self.get_employee_data()
    self.payment_amount = self.calculate_payment_amount()
```
---
The `get_emplyoee_data` at first it calls `validate_schedule()` method, which checks if the string is on the pattern format.

```
def get_employee_data(self):
    if not self.validate_schedule():
        raise FilePatternError()
```
> The `validate_schedule` method uses a regular expression to validate if the input is on the right pattern
> ```
> def validate_schedule(self) -> bool:
>      rgx = "^(?:[A-Z]+)=(?:(?:MO|TU|WE|TH|FR|SA|SU)" \
>            "(?:0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]-(?:0[0-9]|1[0-9]|2[0-3]):" \
>            "[0-5][0-9](?:,|))+"
> ```
> Regex explanation:  
> **1.** (name) - `^(?:[A-Z]+)=`: The string must start with one or more ocurrences of upper case letters, and then has a '=' sign  
> **2.** (day of week) - `(?:MO|TU|WE|TH|FR|SA|SU)`: After the '=' the string must continue with one of the seven initials of the week  
> **3.** (entering hour) - `(?:0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]-`: Validates if the hour and minute is valid within the 24hrs format, then it must have a '-' sign  
> **4.** (exiting hour) - `(?:0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]`: The same as above, but not containig '-'  
> **5.** (end of statement) - `(?:,|)`: After the enterign and exiting times, the string must have a ',' if there's another one after. Or must finish without any symbol  
> `(?:)+`: Encapsulates parts from 2 to 5, telling that it must have one or more ocurrences  
> 
> After that we use `re.findall()` to discover if the expression is valid. If it is we return `True`, if not, `False`:
>```
>  if not re.findall(rgx, self.worked_schedule) or \
>          re.findall(rgx, self.worked_schedule)[0] != \
>          self.worked_schedule:
>      return False
>
>  return True
> ```
If the input is not valid, a custom error is raised `FilePatternError`, explainig what happened, and what should be done:
```
The employee schedule file is out of the pattern.
Please review your file content
```
With everythin valid, lets split the string in two parts, through `=` signal.  
`worker_name` receives the name at index 0  
`worker_schedule` receives the rest of the string containing the days and times worked:
```
worker_name = self.worked_schedule.split("=")[0]
worker_schedule = self.worked_schedule.split("=")[1]
```
For `worker_schedule` we create a list called `worked_time` spliting the times by `,` signal
```
worked_time = [worked for worked in worker_schedule.split(",")]
```
After all we set the name and the working time in them respective variables:
```
self.name = worker_name
self.worked_time = worked_time
```

With `worker_name` and `worked_time` set, we still need to set the employee payment amount, and what does it, is the `calculate_payment_amount()`
```
self.payment_amount = self.calculate_payment_amount()
```
---
The `calculate_payment_amount()` is the main method for getting the right values within time and day worked.  
At first, we define the amount as 0.  
And then, for every registry at `worked_time` list, we pick three variables:
```
def calculate_payment_amount(self) -> int:
    amount = 0
    for day_n_hour in self.worked_time:
        day = day_n_hour[0:2]
        str_entering = day_n_hour[2:].split("-")[0]
        str_exiting = day_n_hour[2:].split("-")[1]
```
Let's use this registry as example: `WE06:00-12:00`  
So we'll have:  
`day`: `WE`  
`str_entering`: `06:00`  
`str_exiting`: `12:00`

Then, we convert `str_entering` and `str_exiting` to datetime, and start a counter variable with the same value as `entering`
```
entering = datetime.strptime(str_entering, "%H:%M")
exiting = datetime.strptime(str_exiting, "%H:%M")

time_counter = entering
```

So, now we can star our calculation telling that, while our counter is between `entering` and `exiting` times, we're going to
count one more hour, get this hour period, and then sum the amount based on the day and the period worked .  
The period is got by `get_period()` method.  
The amount is got by `get_hour_payment()` method.
```
while entering <= time_counter < exiting:
    time_counter += timedelta(hours=1)
    period = self.get_period(time_counter)
    amount += self.get_hour_payment(day, period)
```
---
The `get_period()` method is a static method, which recieves the hour worked and evaluates which period this is part.  
We have three periods:  
`P1`: From `00:01` to `09:00`  
`P2`: From `09:01` to `18:00`  
`P3`: From `18:01` to `00:00`  
These periods are allocated in a constant dictionary present in `constants.py` module

**Obs:** Note that, when validating `P3`, we need to check if the time is **greater** or equal than the exiting time. Because on `P3`, exiting
time is `00:00`, and `datetime` interprets `00:00` as the lowest time value.
```
@staticmethod
def get_period(time) -> str:
    if PERIODS["P1"]["entering"] <= time <= PERIODS["P1"]["exiting"]:
        return "P1"
    if PERIODS["P2"]["entering"] <= time <= PERIODS["P2"]["exiting"]:
        return "P2"
    if PERIODS["P3"]["entering"] <= time >= PERIODS["P3"]["exiting"]:
        return "P3"
```
PERIODS dictionary at contants.py
```
PERIODS = {
    "P1": {
        "entering": datetime.strptime("00:01", "%H:%M"),
        "exiting": datetime.strptime("09:00", "%H:%M")
    },
    "P2": {
        "entering": datetime.strptime("09:01", "%H:%M"),
        "exiting": datetime.strptime("18:00", "%H:%M")
    },
    "P3": {
        "entering": datetime.strptime("18:01", "%H:%M"),
        "exiting": datetime.strptime("00:00", "%H:%M")
    }
}
```

---
The `get_hour_payment()` method is also static. It receives the day worked and the period got by the method above.  
With these two information, first we see if the day is of a week or weekend.  
And then we get the amount value by a constant dictionary present in `constants.py`
```
@staticmethod
def get_hour_payment(day, period) -> int:
    if day in WEEK_DAYS:
        return HOUR_PAYMENT_VALUES["week"][period]
    if day in WEEKEND_DAYS:
        return HOUR_PAYMENT_VALUES["weekend"][period]
```
Constants used by this method at `constants.py`  
```
WEEK_DAYS = ["MO", "TU", "WE", "TH", "FR"]
WEEKEND_DAYS = ["SA", "SU"]
HOUR_PAYMENT_VALUES = {
    "week": {
        "P1": 25,
        "P2": 15,
        "P3": 20
    },
    "weekend": {
        "P1": 30,
        "P2": 20,
        "P3": 25
    }
}
```
Finishing, the `Employee` class also contains a `__str__` method, which describes the payment amount:
```
def __str__(self):
    return f"The amount to pay {self.name} is: " \
           f"{self.payment_amount} USD"
```
---
