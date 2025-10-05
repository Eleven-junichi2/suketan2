# TODO: Replace check existing schedule for each function with _schedule_exists
from dataclasses import dataclass
from pathlib import Path
import json
import datetime

# from prompt_toolkit.shortcuts import choice
import typer

from suketan2.core import Suketan, Task

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

suketan = Suketan(Suketan.load_schedules(SCHEDULES_FILEPATH))

app = typer.Typer()
schedule_app = typer.Typer()
task_app = typer.Typer()
app.add_typer(schedule_app, name="schedule", help="Manage schedules")
app.add_typer(task_app, name="task", help="Manage tasks")


@schedule_app.command()
def create(title: str):
    """Create a new schedule"""
    suketan.create_schedule(title)
    suketan.save_schedules(SCHEDULES_FILEPATH)
    print(f"Schedule '{title}' created.")


@schedule_app.command()
def delete(name: str = typer.Argument(..., help="Name of the schedule to delete")):
    """Delete an existing schedule"""
    suketan.delete_schedule(name)
    suketan.save_schedules(SCHEDULES_FILEPATH)
    print(f"Schedule '{name}' deleted.")


@schedule_app.command()
def rename(
    old_name: str = typer.Argument(..., help="Current name of the schedule"),
    new_name: str = typer.Argument(..., help="New name for the schedule"),
):
    suketan.rename_schedule(old_name, new_name)
    suketan.save_schedules(SCHEDULES_FILEPATH)
    print(f"Schedule renamed from '{old_name}' to '{new_name}'.")


@schedule_app.command("list")
def list_():
    """List all schedules"""
    schedules = suketan.get_schedule_titles()
    if not schedules:
        print("No schedules found.")
        return
    for name in schedules:
        print(f"- {name}")

@task_app.command("add")
def add(
    schedule_title: str = typer.Argument(..., help="Title of the schedule to add the task to"),
    title: str = typer.Argument(..., help="Title of the task"),
    time: str = typer.Argument(..., help="Time of the task in HH:MM format"),
    description: str = typer.Option("", "--description", "-d", help="Description of the task"),
    tag: list[str] = typer.Option([], "--tag", "-t", help="Tags for the task"),
):
    """Add a new task to a schedule"""
    try:
        datetime.datetime.strptime(time, "%H:%M")
    except ValueError:
        print("Time must be in HH:MM format.")
        return
    task = Task(title=title, time=time, description=description, tag=tag)
    suketan.add_task(schedule_title, task)
    suketan.save_schedules(SCHEDULES_FILEPATH)
    print(f"Task '{title}' added to schedule '{schedule_title}'.")


if __name__ == "__main__":
    app()
