"""Business logic for /robots API endpoints."""
from http import HTTPStatus

from flask import jsonify, url_for, current_app
from flask_restx import abort

from src.robot_management import db
from src.robot_management.api.auth.decorators import (
    token_required,
    admin_token_required,
)
from src.robot_management.api.parsers import parse_name
from src.robot_management.models.robot import Robot


@admin_token_required
def create_robot(robot_dict):
    name = robot_dict["name"]
    if Robot.find_by_name(name):
        error = f"Robot name: {name} already exists, must be unique."
        current_app.logger.error(error)
        abort(HTTPStatus.CONFLICT, error, status="fail")
    robot = Robot(**robot_dict)
    db.session.add(robot)
    db.session.commit()
    response = jsonify(status="success", message=f"New robot added: {name}.")
    current_app.logger.info(f"Added robot: {robot}")
    response.status_code = HTTPStatus.CREATED
    response.headers["Location"] = url_for("api.robot", name=name)
    return response


def retrieve_robot_list():
    current_app.logger.info("Robot list requested")
    response = jsonify(Robot.query.all())
    return response


def retrieve_robot(name):
    current_app.logger.info(f"Robot {name} requested")
    return Robot.query.filter_by(name=name.lower()).first_or_404(
        description=f"{name} not found."
    )


@token_required
def update_robot(name, robot_dict):
    robot = Robot.find_by_name(name.lower())
    if robot:
        for k, v in robot_dict.items():
            setattr(robot, k, v)
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
    robot_dict["name"] = valid_name
    current_app.logger.info(f"Robot {name} updated")
    return create_robot(robot_dict)


@admin_token_required
def delete_robot(name):
    robot = Robot.query.filter_by(name=name.lower()).first_or_404(
        description=f"{name} not found in database."
    )
    db.session.delete(robot)
    db.session.commit()
    current_app.logger.info(f"Robot {name} deleted")
    return "", HTTPStatus.NO_CONTENT
