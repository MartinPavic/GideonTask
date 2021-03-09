"""API blueprint configuration."""
from flask import Blueprint
from flask_restx import Api
from .auth.endpoints import auth_ns
from .robots.endpoints import robot_ns
from .tasks.endpoints import task_ns
from .task_executions.endpoints import task_execution_ns

api_bp = Blueprint("api", __name__, url_prefix="/api")
authorizations = {
    "Bearer": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

api = Api(
    api_bp,
    version="1.0",
    title="Robot management web service",
    description="Flask API with JWT-Based Authentication",
    doc="/ui",
    authorizations=authorizations,
)
api.add_namespace(auth_ns, path="/auth")
api.add_namespace(robot_ns, path="/robots")
api.add_namespace(task_ns, path="/tasks")
api.add_namespace(task_execution_ns, path="/task-executions")
