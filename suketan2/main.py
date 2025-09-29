from dataclasses import dataclass, field
from pathlib import Path
import json

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
    name: str
    duration: int
    description: str = ""
    tag: list[str] = field(default_factory=list)

class Suketan:
    def __init__(self):
        self.config = Config(**config_data)
        self.schedules: dict[str, list[Task]] = self.load_schedules()

    def load_schedules(self):
        if SCHEDULES_FILEPATH.exists():
            with open(SCHEDULES_FILEPATH, "r", encoding="utf-8") as f:
                schedules_data = json.load(f)
            return schedules_data
        else:
            return {}

    def save_schedules(self):
        APP_DIR.mkdir(parents=True, exist_ok=True)
        with open(SCHEDULES_FILEPATH, "w", encoding="utf-8") as f:
            json.dump(self.schedules, f, indent=4)

    def create_schedule(self, name: str):
        if name in self.schedules:
            raise ValueError(f"Schedule '{name}' already exists.")
        self.schedules[name] = []
        self.save_schedules()
    
    def rename_schedule(self, old_name: str, new_name: str):
        if old_name not in self.schedules:
            raise ValueError(f"Schedule '{old_name}' does not exist.")
        if new_name in self.schedules:
            raise ValueError(f"Schedule '{new_name}' already exists.")
        self.schedules[new_name] = self.schedules.pop(old_name)
        self.save_schedules()
    
    def delete_schedule(self, name: str):
        if name not in self.schedules:
            raise ValueError(f"Schedule '{name}' does not exist.")
        del self.schedules[name]
        self.save_schedules()
    
    def list_schedules(self):
        return list(self.schedules.keys())

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
def rename(old_name: str = typer.Argument(..., help="Current name of the schedule"),
           new_name: str = typer.Argument(..., help="New name for the schedule")):
    suketan.rename_schedule(old_name, new_name)
    print(f"Schedule renamed from '{old_name}' to '{new_name}'.")

@schedule_app.command("list")
def list_():
    """List all schedules"""
    schedules = suketan.list_schedules()
    if not schedules:
        print("No schedules found.")
        return
    for idx, name in enumerate(schedules, 1):
        print(f"{idx}. {name}")

if __name__ == "__main__":
    app()
