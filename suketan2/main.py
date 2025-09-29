from dataclasses import dataclass, field
from pathlib import Path
import json

import typer

APP_DIR = Path(typer.get_app_dir("suketan2"))
SCHEDULES_FILEPATH = APP_DIR / "schedules.json"
CONFIG_FILEPATH = APP_DIR / "config.json"
if CONFIG_FILEPATH.exists():
    with open(CONFIG_FILEPATH, "r", encoding="utf-8") as f:
        config_data = json.load(f)
else:
    with open(Path(__file__).parent / "config.json", "r", encoding="utf-8") as f:
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

def item_selection_menu(commands: dict[str, str], items: tuple, items_title: str = "") -> str:
    options = tuple(commands.keys()) + tuple(items)
    for i, option in enumerate(options):
        if i == len(commands):
            print(f"--{items_title}--")
        print(f"{i} {option}")
    print("----")
    return input("> ")

def main():
    schedules: dict[str, list[Task]] = {}



if __name__ == "__main__":
    main()