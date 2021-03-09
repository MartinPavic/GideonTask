from http import HTTPStatus

from flask_restx import Namespace, Resource

from src.robot_management.api.parsers import (
    task_execution_model,
    task_execution_reqparser,
    filter_reqparser
)
from .business import (
    create_task_execution,
    retrieve_task_execution_list,
    retrieve_task_execution,
)

task_execution_ns = Namespace(name="task_executions", validate=True)
task_execution_ns.models[task_execution_model.name] = task_execution_model


@task_execution_ns.route("", endpoint="task_execution_list")
@task_execution_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@task_execution_ns.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@task_execution_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class TaskList(Resource):
    """Handles HTTP requests to URL: /task-executions."""

    @task_execution_ns.doc(security="Bearer")
    @task_execution_ns.response(int(HTTPStatus.OK), "Retrieved task execution list.")
    @task_execution_ns.expect(filter_reqparser)
    def get(self):
        """Retrieve a list of task executions."""
        filter_dict = filter_reqparser.parse_args()
        return retrieve_task_execution_list(filter_dict)

    @task_execution_ns.doc(security="Bearer")
    @task_execution_ns.response(int(HTTPStatus.CREATED), "Added new task execution.")
    @task_execution_ns.response(int(HTTPStatus.FORBIDDEN), "Admin token required.")
    @task_execution_ns.expect(task_execution_reqparser)
    def post(self):
        """Create a task execution."""
        task_execution_dict = task_execution_reqparser.parse_args()
        return create_task_execution(task_execution_dict)


@task_execution_ns.route("/<id>", endpoint="task_execution")
@task_execution_ns.param("id", "task execution id")
@task_execution_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@task_execution_ns.response(int(HTTPStatus.NOT_FOUND), "Task execution not found.")
@task_execution_ns.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@task_execution_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class Task(Resource):
    """Handles HTTP requests to URL: /task-executions/{id}."""

    @task_execution_ns.doc(security="Bearer")
    @task_execution_ns.response(int(HTTPStatus.OK), "Retrieved task execution.", task_execution_model)
    @task_execution_ns.marshal_with(task_execution_model)
    def get(self, id):
        """Retrieve a task execution."""
        return retrieve_task_execution(id)
