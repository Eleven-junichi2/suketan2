import pytest  # noqa: F401

from suketan2.core import ScheduleManager, Task

def test_create_schedule():
    schedule_manager = ScheduleManager()
    schedule_manager.create_schedule("Work")
    assert "Work" in schedule_manager.schedules

def test_rename_schedule():
    schedule_manager = ScheduleManager()
    schedule_manager.create_schedule("Work1")
    schedule_manager.create_schedule("Work2")
    schedule_manager.create_schedule("Work3")
    schedule_manager.rename_schedule("Work2", "Office")
    assert "Office" in schedule_manager.schedules
    assert "Work2" not in schedule_manager.schedules

def test_delete_schedule():
    schedule_manager = ScheduleManager()
    schedule_manager.create_schedule("Personal")
    schedule_manager.delete_schedule("Personal")
    assert "Personal" not in schedule_manager.schedules

def test_get_schedule_titles():
    schedule_manager = ScheduleManager()
    schedule_manager.create_schedule("Gym")
    schedule_manager.create_schedule("Study")
    schedules = schedule_manager.get_schedule_titles()
    assert "Gym" in schedules
    assert "Study" in schedules

def test_add_task():
    schedule_manager = ScheduleManager()
    schedule_manager.create_schedule("Errands")
    task = Task(title="Buy groceries", time="01:00", description="Milk, Bread, Eggs")
    schedule_manager.add_task("Errands", task)
    assert task == schedule_manager.schedules["Errands"][0]
    assert schedule_manager.schedules["Errands"][0].title == "Buy groceries"
    assert schedule_manager.schedules["Errands"][0].time == "01:00"
    assert schedule_manager.schedules["Errands"][0].description == "Milk, Bread, Eggs"
    assert schedule_manager.schedules["Errands"][0].tag == []

def test_list_tasks():
    schedule_manager = ScheduleManager()
    schedule_manager.create_schedule("Chores")
    task1 = Task(title="Clean room", time="02:00", description="Vacuum and dust")
    task2 = Task(title="Wash dishes", time="03:00", description="Use dishwasher")
    schedule_manager.add_task("Chores", task1)
    schedule_manager.add_task("Chores", task2)
    tasks = schedule_manager.list_tasks("Chores")
    assert len(tasks) == 2
    assert tasks[0].title == "Clean room"
    assert tasks[1].title == "Wash dishes"

def test_overwrite_task():
    schedule_manager = ScheduleManager()
    schedule_manager.create_schedule("Projects")
    task1 = Task(title="Project A", time="04:00", description="Initial setup")
    schedule_manager.add_task("Projects", task1)
    new_task = Task(title="Project A Updated", time="05:00", description="Setup complete")
    schedule_manager.overwrite_task("Projects", 0, new_task)
    assert schedule_manager.schedules["Projects"][0].title == "Project A Updated"
    assert schedule_manager.schedules["Projects"][0].time == "05:00"
    assert schedule_manager.schedules["Projects"][0].description == "Setup complete"

def test_delete_task():
    schedule_manager = ScheduleManager()
    schedule_manager.create_schedule("Learning")
    task1 = Task(title="Read book", time="06:00", description="Chapter 1-3")
    task2 = Task(title="Watch tutorial", time="07:00", description="Python basics")
    schedule_manager.add_task("Learning", task1)
    schedule_manager.add_task("Learning", task2)
    schedule_manager.delete_task("Learning", 0)
    tasks = schedule_manager.list_tasks("Learning")
    assert len(tasks) == 1
    assert tasks[0].title == "Watch tutorial"
