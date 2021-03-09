from datetime import datetime, timedelta, timezone
from src.robot_management.models.robot import Robot
from src.robot_management import db
from src.robot_management.util.datetime_util import format_timedelta_str, utc_now
from sqlalchemy.ext.hybrid import hybrid_property
from dataclasses import dataclass


@dataclass
class TaskExecution(db.Model):
    """Task execution model"""

    id: int
    robot_id: int
    task_id: int
    start: datetime
    end: datetime
    success: bool

    __tablename__ = "task_execution"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    robot_id = db.Column(db.Integer, db.ForeignKey("robot.id"), nullable=False)
    robot = db.relationship("Robot", backref=db.backref("task_executions"))
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)
    task = db.relationship("Task", backref=db.backref("task_executions"))
    start = db.Column(db.DateTime, default=utc_now)
    end = db.Column(db.DateTime)
    success = db.Column(db.Boolean)

    @property
    def duration(self):
        return self.end.replace(tzinfo=timezone.utc) - utc_now()

    @property
    def robot_name(self):
        return self.robot.name

    @property
    def robot_type(self):
        return self.robot.type

    @property
    def task_name(self):
        return self.task.name

    @property
    def task_type(self):
        return self.task.type

    @property
    def status(self):
        return "Success" if self.success else "Failed"

    @hybrid_property
    def duration_str(self):
        timedelta_str = format_timedelta_str(self.duration)
        return timedelta_str
