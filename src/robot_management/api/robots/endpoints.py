from http import HTTPStatus

from flask_restx import Namespace, Resource

from src.robot_management.api.parsers import (
    create_reqparser,
    robot_model,
    update_reqparser,
)
from .business import (
    create_robot,
    retrieve_robot_list,
    retrieve_robot,
    update_robot,
    delete_robot,
)

robot_ns = Namespace(name="robots", validate=True)
robot_ns.models[robot_model.name] = robot_model


@robot_ns.route("", endpoint="robot_list")
@robot_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@robot_ns.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@robot_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class RobotList(Resource):
    """Handles HTTP requests to URL: /robots."""

    @robot_ns.response(int(HTTPStatus.OK), "Retrieved robot list.")
    def get(self):
        """Retrieve a list of robots."""
        return retrieve_robot_list()

    @robot_ns.doc(security="Bearer")
    @robot_ns.response(int(HTTPStatus.CREATED), "Added new robot.")
    @robot_ns.response(int(HTTPStatus.FORBIDDEN), "Admin token required.")
    @robot_ns.response(int(HTTPStatus.CONFLICT), "Robot with that name already exists.")
    @robot_ns.expect(create_reqparser)
    def post(self):
        """Create a robot."""
        robot_dict = create_reqparser.parse_args()
        return create_robot(robot_dict)


@robot_ns.route("/<name>", endpoint="robot")
@robot_ns.param("name", "robot name")
@robot_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@robot_ns.response(int(HTTPStatus.NOT_FOUND), "robot not found.")
@robot_ns.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@robot_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class Robot(Resource):
    """Handles HTTP requests to URL: /robots/{name}."""

    @robot_ns.response(int(HTTPStatus.OK), "Retrieved robot.", robot_model)
    @robot_ns.marshal_with(robot_model)
    def get(self, name):
        """Retrieve a robot."""
        return retrieve_robot(name)

    @robot_ns.doc(security="Bearer")
    @robot_ns.response(int(HTTPStatus.OK), "Robot was updated.", robot_model)
    @robot_ns.response(int(HTTPStatus.CREATED), "Added new robot.")
    @robot_ns.response(int(HTTPStatus.FORBIDDEN), "Administrator token required.")
    @robot_ns.expect(update_reqparser)
    def put(self, name):
        """Update a robot."""
        robot_dict = update_reqparser.parse_args()
        return update_robot(name, robot_dict)

    @robot_ns.doc(security="Bearer")
    @robot_ns.response(int(HTTPStatus.NO_CONTENT), "Robot was deleted.")
    @robot_ns.response(int(HTTPStatus.FORBIDDEN), "Administrator token required.")
    def delete(self, name):
        """Delete a robot."""
        return delete_robot(name)
