# TODO: Replace check existing schedule for each function with _schedule_exists
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated
import json
# import datetime

# from prompt_toolkit.shortcuts import choice
import typer

from core import ScheduleManager

APP_DIR = Path(typer.get_app_dir("suketan2"))
SCHEDULES_FILEPATH = APP_DIR / "schedules.json"
CONFIG_FILEPATH = APP_DIR / "config.json"
if not CONFIG_FILEPATH.exists():
    CONFIG_FILEPATH = Path(__file__).parent / "config.json"
with open(CONFIG_FILEPATH, "r", encoding="utf-8") as f:
    config_data = json.load(f)


@dataclass
class Config:
    locale: str = "ja"


schedule_manager = ScheduleManager(ScheduleManager.load_schedules(SCHEDULES_FILEPATH))

app = typer.Typer()
schedule_app = typer.Typer()
task_app = typer.Typer()
app.add_typer(schedule_app, name="schedule", help="Manage schedules")
app.add_typer(task_app, name="task", help="Manage tasks")


@schedule_app.command()
def create(title: Annotated[str, typer.Option(prompt=True, help="Title of the new schedule")]):
    """Create a new schedule"""
    schedule_manager.create_schedule(title)
    schedule_manager.save_schedules(SCHEDULES_FILEPATH)
    print(f"Schedule '{title}' created.")


@schedule_app.command()
def delete(name: Annotated[str | None, typer.Argument(help="Name of the schedule to delete")] = None):
    """Delete an existing schedule"""
    if name is None:
        schedules = schedule_manager.get_schedule_titles()
        # TODO: Show a prompt to select a schedule to delete
    else:
        schedule_manager.delete_schedule(name)
        schedule_manager.save_schedules(SCHEDULES_FILEPATH)
        print(f"Schedule '{name}' deleted.")


@schedule_app.command()
def rename(
    old_name: str = typer.Argument(..., help="Current name of the schedule"),
    new_name: str = typer.Argument(..., help="New name for the schedule"),
):
    schedule_manager.rename_schedule(old_name, new_name)
    schedule_manager.save_schedules(SCHEDULES_FILEPATH)
    print(f"Schedule renamed from '{old_name}' to '{new_name}'.")


@schedule_app.command("list")
def list_():
    """List all schedules"""
    schedules = schedule_manager.get_schedule_titles()
    if not schedules:
        print("No schedules found.")
        return
    for name in schedules:
        print(f"- {name}")


# @task_app.command("add")
# def add_task(
#     title: Annotated[str, typer.Optip(prompt=True, help="Title of the task")],
#     time: Annotated[str, typer.Argument(help="Time required for the task (e.g., 1h30m, 45m)")]):
#     """Add a task to a schedule"""
#     schedules = schedule_manager.get_schedule_titles()


if __name__ == "__main__":
    app()
