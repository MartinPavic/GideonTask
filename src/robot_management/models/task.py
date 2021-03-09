from src.robot_management import db
from dataclasses import dataclass


class Task(db.Model):
    """Task model"""

    id: int
    name: str
    type: str

    __tablename__ = "task"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    type = db.Column(db.String(100))

    def __repr__(self) -> str:
        return f"<Task name={self.name}, type={self.type}>"

    def __str__(self) -> str:
        return self.__repr__()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def find_by_type(cls, type):
        return cls.query.filter_by(type=type).all()
