import os
import click
from src.robot_management.models.robot import Robot
from src.robot_management.models.task import Task
from src.robot_management.models.task_execution import TaskExecution

from src.robot_management import create_app, db
from src.robot_management.models.user import User
from src.robot_management.models.token_blacklist import BlacklistedToken

app = create_app(os.getenv("FLASK_ENV", "development"))


@app.shell_context_processor
def shell():
    return {
        "db": db, 
        "User": User, 
        "BlacklistedToken": BlacklistedToken,
        "Robot": Robot,
        "Task": Task,
        "TaskExecution": TaskExecution
    }

@app.cli.command("add-user", short_help="Add a new user")
@click.argument("email")
@click.option(
    "--admin", is_flag=True, default=False, help="New user has administrator role"
)
@click.password_option(help="Do not set password on the command line!")
def add_user(email, admin, password):
    """Add a new user to the database with email address = EMAIL."""
    if User.find_by_email(email):
        error = f"Error: {email} is already registered"
        click.secho(f"{error}\n", fg="red", bold=True)
        return 1
    new_user = User(email=email, password=password, admin=admin)
    db.session.add(new_user)
    db.session.commit()
    user_type = "admin user" if admin else "user"
    message = f"Successfully added new {user_type}:\n {new_user}"
    click.secho(message, fg="blue", bold=True)
    return 0
