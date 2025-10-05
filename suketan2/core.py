from dataclasses import dataclass, field
import json
import os
from pathlib import Path


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
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
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
