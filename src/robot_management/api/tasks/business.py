"""Business logic for /tasks API endpoints."""
from http import HTTPStatus

from flask import jsonify, url_for, current_app
from flask_restx import abort

from src.robot_management import db
from src.robot_management.api.auth.decorators import (
    token_required,
    admin_token_required,
)
from src.robot_management.api.parsers import parse_name
from src.robot_management.models.task import Task


@admin_token_required
def create_task(task_dict):
    name = task_dict["name"]
    type = task_dict["type"]
    if Task.find_by_name(name):
        error = f"Task name: {name} already exists, must be unique."
        current_app.logger.error(error)
        abort(HTTPStatus.CONFLICT, error, status="fail")
    task = Task(**task_dict)
    db.session.add(task)
    db.session.commit()
    response = jsonify(status="success", message=f"New task added: {name}.")
    current_app.logger.info(f"Added task: {task}")
    response.status_code = HTTPStatus.CREATED
    response.headers["Location"] = url_for("api.task", name=name)
    return response


@token_required
def retrieve_task_list():
    current_app.logger.info("Task list requested")
    tasks = Task.query.all()
    response = jsonify(tasks)
    return response

@token_required
def retrieve_task(name):
    current_app.logger.info(f"Task {name} requested")
    return Task.query.filter_by(name=name.lower()).first_or_404(
        description=f"{name} not found."
    )

@token_required
def update_task(name, task_dict):
    task = Task.find_by_name(name.lower())
    if task:
        for k, v in task_dict.items():
            setattr(task, k, v)
        db.session.commit()
        message = f"'{name}' was successfully updated"
        current_app.logger.info(message)
        response_dict = dict(status="success", message=message)
        return response_dict, HTTPStatus.OK
    try:
        valid_name = parse_name(name.lower())
    except ValueError as e:
        current_app.logger.error(str(e))
        abort(HTTPStatus.BAD_REQUEST, str(e), status="fail")
    task_dict["name"] = valid_name
    return create_task(task_dict)

@admin_token_required
def delete_task(name):
    task = Task.query.filter_by(name=name.lower()).first_or_404(
        description=f"{name} not found in database."
    )
    db.session.delete(task)
    db.session.commit()
    current_app.logger.info(f"Task {name} deleted")
    return "", HTTPStatus.NO_CONTENT
