import re
from flask_restx.reqparse import RequestParser
from flask_restx import Model
from flask_restx.fields import DateTime, Nested, String
from dateutil import parser
from datetime import date, datetime, time, timezone
from src.robot_management.util.datetime_util import make_tzaware, DATE_MONTH_NAME


from src.robot_management.models.robot import Robot
from src.robot_management.models.task import Task


def parse_name(name):
    """Validation method for a string containing only letters, numbers, '-' and '_'."""
    if not re.compile(r"^[\w-]+$").match(name):
        raise ValueError(
            f"'{name}' contains one or more invalid characters. Widget name must "
            "contain only letters, numbers, hyphen and underscore characters."
        )
    return name.lower()


def future_date_from_string(date_str):
    """Validation method for a date in the future, formatted as a string."""
    try:
        parsed_date = parser.parse(date_str)
    except ValueError:
        raise ValueError(
            f"Failed to parse '{date_str}' as a valid date. You can use any format "
            "recognized by dateutil.parser. For example, all of the strings below "
            "are valid ways to represent the same date: '2018-5-13' -or- '05/13/2018' "
            "-or- 'May 13 2018'."
        )

    if parsed_date.date() < date.today():
        raise ValueError(
            f"Successfully parsed {date_str} as "
            f"{parsed_date.strftime(DATE_MONTH_NAME)}. However, this value must be a "
            f"date in the future and {parsed_date.strftime(DATE_MONTH_NAME)} is BEFORE "
            f"{datetime.now().strftime(DATE_MONTH_NAME)}"
        )
    deadline = datetime.combine(parsed_date.date(), time.max)
    deadline_utc = make_tzaware(deadline, use_tz=timezone.utc)
    return deadline_utc


def robot_id(id):
    robot = Robot.query.filter_by(id=id).first()
    if not robot:
        raise ValueError(f"Robot with id {id} does not exist")
    return robot.id


def task_id(id):
    task = Task.query.filter_by(id=id).first()
    if not task:
        raise ValueError(f"Task with id {id} does not exist")
    return task.id


def robot_from_name(name):
    robot = Robot.find_by_name(name)
    if not robot:
        raise ValueError(f"Robot with name {name} does not exist")
    return robot.name


def robots_from_type(type):
    robots = Robot.find_by_type(type)
    if not robots:
        raise ValueError(f"Robots of type {type} does not exist")
    return type


def task_from_name(name):
    task = Task.find_by_name(name)
    if not task:
        raise ValueError(f"Task with name {name} does not exist")
    return task.name


def tasks_from_type(type):
    tasks = Task.find_by_type(type)
    if not tasks:
        raise ValueError(f"Tasks of type {type} does not exist")
    return type


create_reqparser = RequestParser(bundle_errors=True)
create_reqparser.add_argument(
    "name",
    type=parse_name,
    location="form",
    required=True,
    nullable=False,
    case_sensitive=True,
)
create_reqparser.add_argument(
    "type",
    type=parse_name,
    location="form",
    required=True,
    nullable=False,
    case_sensitive=True,
)

task_execution_reqparser = RequestParser(bundle_errors=True)
task_execution_reqparser.add_argument(
    "robot_id", type=robot_id, location="form", required=True, nullable=False
)
task_execution_reqparser.add_argument(
    "task_id", type=task_id, location="form", required=True, nullable=False
)
task_execution_reqparser.add_argument(
    "start", type=datetime, location="form", required=False, nullable=False
)
task_execution_reqparser.add_argument(
    "end", type=future_date_from_string, location="form", required=True, nullable=False
)
task_execution_reqparser.add_argument(
    "status",
    type=str,
    location="form",
    choices=["Success", "Failure"],
    required=True,
    nullable=False,
)

filter_reqparser = RequestParser(bundle_errors=True)
filter_reqparser.add_argument("robot_name", type=robot_from_name)
filter_reqparser.add_argument("robot_type", type=robots_from_type)
filter_reqparser.add_argument("task_name", type=task_from_name)
filter_reqparser.add_argument("task_type", type=tasks_from_type)
filter_reqparser.add_argument("start", type=datetime)
filter_reqparser.add_argument("end", type=datetime)
filter_reqparser.add_argument("duration", type=datetime)
filter_reqparser.add_argument("status", type=str)


robot_model = Model(
    "Robot",
    {
        "name": String,
        "type": String,
    },
)
task_model = Model("Task", {"name": String, "type": String})
task_execution_model = Model(
    "Task execution",
    {
        "robot": Nested(robot_model),
        "task": Nested(task_model),
        "start": DateTime,
        "end": DateTime,
        "duration": String(attribute="deadline_str"),
        "status": String,
    },
)

update_reqparser = create_reqparser.copy()
