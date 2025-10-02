# TODO: Replace check existing schedule for each function with _schedule_exists
from dataclasses import dataclass, field
from pathlib import Path
import json
import os
import datetime

# from prompt_toolkit.shortcuts import choice
import typer

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


@dataclass
class Task:
    """A task in a schedule
    
    Attributes:
        name (str): The name of the task
        time (str): The time of the task in HH:MM format
        description (str): A brief description of the task
        tag (list[str]): A list of tags
    """
    title: str
    time: str
    description: str = ""
    tag: list[str] = field(default_factory=list)


class Suketan:
    def __init__(self, schedules: dict[str, list[Task]] | None = None):
        self.schedules: dict[str, list[Task]] = schedules if schedules else {}

    @staticmethod
    def load_schedules(filepath: os.PathLike) -> dict[str, list[Task]]:
        if Path(filepath).exists():
            with open(filepath, "r", encoding="utf-8") as f:
                schedules_data = json.load(f)
            return schedules_data
        else:
            return {}

    def save_schedules(self, filepath: os.PathLike):
        APP_DIR.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.schedules, f, indent=4)

    def create_schedule(self, title: str):
        if title in self.schedules:
            raise ValueError(f"Schedule '{title}' already exists.")
        self.schedules[title] = []

    def rename_schedule(self, old_name: str, new_name: str):
        if old_name not in self.schedules:
            raise ValueError(f"Schedule '{old_name}' does not exist.")
        if new_name in self.schedules:
            raise ValueError(f"Schedule '{new_name}' already exists.")
        self.schedules[new_name] = self.schedules.pop(old_name)

    def delete_schedule(self, title: str):
        if title not in self.schedules:
            raise ValueError(f"Schedule '{title}' does not exist.")
        del self.schedules[title]

    def get_schedule_titles(self) -> set[str]:
        return set(self.schedules.keys())

    def add_task(self, schedule_title: str, task: Task):
        if schedule_title not in self.schedules:
            raise ValueError(f"Schedule '{schedule_title}' does not exist.")
        self.schedules[schedule_title].append(task)

    def list_tasks(self, schedule_title: str) -> list[Task]:
        if schedule_title not in self.schedules:
            raise ValueError(f"Schedule '{schedule_title}' does not exist.")
        return self.schedules[schedule_title]

    def overwrite_task(self, schedule_title: str, task_id: int, new_task: Task):
        if schedule_title not in self.schedules:
            raise ValueError(f"Schedule '{schedule_title}' does not exist.")
        if task_id < 0 or task_id >= len(self.schedules[schedule_title]):
            raise IndexError("Task ID out of range.")
        self.schedules[schedule_title][task_id] = new_task

    def delete_task(self, schedule_title: str, task_id: int):
        if schedule_title not in self.schedules:
            raise ValueError(f"Schedule '{schedule_title}' does not exist.")
        if task_id < 0 or task_id >= len(self.schedules[schedule_title]):
            raise IndexError("Task ID out of range.")
        del self.schedules[schedule_title][task_id]


suketan = Suketan(Suketan.load_schedules(SCHEDULES_FILEPATH))

app = typer.Typer()
schedule_app = typer.Typer()
task_app = typer.Typer()
app.add_typer(schedule_app, name="schedule", help="Manage schedules")
app.add_typer(task_app, name="task", help="Manage tasks")


@schedule_app.command()
def create(title: str | None = None):
    """Create a new schedule"""
    if title is None:
        title = typer.prompt("Enter schedule name")
    if title is None:
        # TODO: set current date and time str
        # title = 
        raise NotImplementedError
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


if __name__ == "__main__":
    app()
