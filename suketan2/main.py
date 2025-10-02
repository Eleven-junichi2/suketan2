# TODO: Replace check existing schedule for each function with _schedule_exists
from dataclasses import dataclass, field
from pathlib import Path
import json
import os

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

    def load_schedules(self, filepath: os.PathLike) -> dict[str, list[Task]]:
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

    def _schedule_exists(self, name: str, raise_err: bool = True) -> bool:
        result = name in self.schedules
        if raise_err and result:
            raise ValueError(f"Schedule '{name}' does not exist.")
        else:
            return result

    def create_schedule(self, name: str):
        self._schedule_exists(name)
        self.schedules[name] = []

    def rename_schedule(self, old_name: str, new_name: str):
        self._schedule_exists(old_name)
        if self._schedule_exists(new_name, raise_err=False):
            raise ValueError(f"Schedule '{new_name}' already exists.")
        self.schedules[new_name] = self.schedules.pop(old_name)

    def delete_schedule(self, name: str):
        self._schedule_exists(name)
        del self.schedules[name]

    def get_schedule_titles(self) -> set[str]:
        return set(self.schedules.keys())

    def add_task(self, schedule_name: str, task: Task):
        self._schedule_exists(schedule_name)
        self.schedules[schedule_name].append(task)

    def list_tasks(self, schedule_name: str) -> list[Task]:
        self._schedule_exists(schedule_name)
        return self.schedules[schedule_name]

    def overwrite_task(self, schedule_name: str, task_id: int, new_task: Task):
        self._schedule_exists(schedule_name)
        if task_id < 0 or task_id >= len(self.schedules[schedule_name]):
            raise IndexError("Task ID out of range.")
        self.schedules[schedule_name][task_id] = new_task

    def delete_task(self, schedule_name: str, task_id: int):
        self._schedule_exists(schedule_name)
        if task_id < 0 or task_id >= len(self.schedules[schedule_name]):
            raise IndexError("Task ID out of range.")
        del self.schedules[schedule_name][task_id]


suketan = Suketan()

app = typer.Typer()
schedule_app = typer.Typer()
task_app = typer.Typer()
app.add_typer(schedule_app, name="schedule", help="Manage schedules")
app.add_typer(task_app, name="task", help="Manage tasks")


@schedule_app.command()
def create():
    """Create a new schedule"""
    name = typer.prompt("Enter schedule name")
    suketan.create_schedule(name)
    print(f"Schedule '{name}' created.")


@schedule_app.command()
def delete(name: str = typer.Argument(..., help="Name of the schedule to delete")):
    """Delete an existing schedule"""
    suketan.delete_schedule(name)
    print(f"Schedule '{name}' deleted.")


@schedule_app.command()
def rename(
    old_name: str = typer.Argument(..., help="Current name of the schedule"),
    new_name: str = typer.Argument(..., help="New name for the schedule"),
):
    suketan.rename_schedule(old_name, new_name)
    print(f"Schedule renamed from '{old_name}' to '{new_name}'.")


@schedule_app.command("list")
def list_():
    """List all schedules"""
    schedules = suketan.get_schedule_titles()
    if not schedules:
        print("No schedules found.")
        return
    for idx, name in enumerate(schedules, 1):
        print(f"{idx}. {name}")


if __name__ == "__main__":
    app()
