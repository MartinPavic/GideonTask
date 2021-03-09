from http import HTTPStatus

from flask_restx import Namespace, Resource

from src.robot_management.api.parsers import (
    create_reqparser,
    task_model,
    update_reqparser,
)
from .business import (
    create_task,
    retrieve_task_list,
    retrieve_task,
    update_task,
    delete_task,
)

task_ns = Namespace(name="tasks", validate=True)
task_ns.models[task_model.name] = task_model


@task_ns.route("", endpoint="task_list")
@task_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@task_ns.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@task_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class TaskList(Resource):
    """Handles HTTP requests to URL: /tasks."""

    @task_ns.doc(security="Bearer")
    @task_ns.response(int(HTTPStatus.OK), "Retrieved task list.")
    def get(self):
        """Retrieve a list of tasks."""
        return retrieve_task_list()

    @task_ns.doc(security="Bearer")
    @task_ns.response(int(HTTPStatus.CREATED), "Added new task.")
    @task_ns.response(int(HTTPStatus.FORBIDDEN), "Admin token required.")
    @task_ns.response(int(HTTPStatus.CONFLICT), "task with that name already exists.")
    @task_ns.expect(create_reqparser)
    def post(self):
        """Create a task."""
        task_dict = create_reqparser.parse_args()
        return create_task(task_dict)


@task_ns.route("/<name>", endpoint="task")
@task_ns.param("name", "task name")
@task_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@task_ns.response(int(HTTPStatus.NOT_FOUND), "Task not found.")
@task_ns.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@task_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class Task(Resource):
    """Handles HTTP requests to URL: /tasks/{name}."""

    @task_ns.doc(security="Bearer")
    @task_ns.response(int(HTTPStatus.OK), "Retrieved task.", task_model)
    @task_ns.marshal_with(task_model)
    def get(self, name):
        """Retrieve a task."""
        return retrieve_task(name)

    @task_ns.doc(security="Bearer")
    @task_ns.response(int(HTTPStatus.OK), "Task was updated.", task_model)
    @task_ns.response(int(HTTPStatus.CREATED), "Added new task.")
    @task_ns.response(int(HTTPStatus.FORBIDDEN), "Administrator token required.")
    @task_ns.expect(update_reqparser)
    def put(self, name):
        """Update a task."""
        task_dict = update_reqparser.parse_args()
        return update_task(name, task_dict)

    @task_ns.doc(security="Bearer")
    @task_ns.response(int(HTTPStatus.NO_CONTENT), "Task was deleted.")
    @task_ns.response(int(HTTPStatus.FORBIDDEN), "Administrator token required.")
    def delete(self, name):
        """Delete a task."""
        return delete_task(name)
