"""Business logic for /task-executions API endpoints."""
from http import HTTPStatus

from flask import jsonify, url_for, current_app

from src.robot_management import db
from src.robot_management.api.auth.decorators import token_required
from src.robot_management.models.task_execution import TaskExecution


@token_required
def create_task_execution(task_execution_dict):
    start = task_execution_dict.get("start")
    if not start:
        task_execution_dict.pop("start")
    status = task_execution_dict.pop("status", "Failed")
    task_execution_dict["success"] = status != "Failed"
    task_execution = TaskExecution(**task_execution_dict)
    db.session.add(task_execution)
    db.session.commit()
    response = jsonify(
        status="success",
        message=f"New task execution added: {task_execution.robot}: {task_execution.task}.",
    )
    current_app.logger.info("Added new task execution")
    response.status_code = HTTPStatus.CREATED
    response.headers["Location"] = url_for("api.task_execution", id=task_execution.id)
    return response


@token_required
def retrieve_task_execution_list(filter_dict):
    current_app.logger.info("Task execution list requested")
    filter_dict = dict(filter(lambda x: x[1], filter_dict.items()))
    task_executions = [
        te for te in TaskExecution.query.all() if _match(te, filter_dict)
    ]
    response = jsonify(task_executions)
    return response


@token_required
def retrieve_task_execution(id):
    current_app.logger.info(f"Task execution {id} requested")
    return TaskExecution.query.filter_by(id=id).first_or_404(
        description=f"Task execution [{id}] not found."
    )


def _match(te: TaskExecution, filter_dict: dict):
    for k, v in filter_dict.items():
        if getattr(te, k) != v:
            return False
    return True