import pytest  # noqa: F401

from suketan2.core import Suketan, Task

def test_create_schedule():
    suketan = Suketan()
    suketan.create_schedule("Work")
    assert "Work" in suketan.schedules

def test_rename_schedule():
    suketan = Suketan()
    suketan.create_schedule("Work1")
    suketan.create_schedule("Work2")
    suketan.create_schedule("Work3")
    suketan.rename_schedule("Work2", "Office")
    assert "Office" in suketan.schedules
    assert "Work2" not in suketan.schedules

def test_delete_schedule():
    suketan = Suketan()
    suketan.create_schedule("Personal")
    suketan.delete_schedule("Personal")
    assert "Personal" not in suketan.schedules

def test_get_schedule_titles():
    suketan = Suketan()
    suketan.create_schedule("Gym")
    suketan.create_schedule("Study")
    schedules = suketan.get_schedule_titles()
    assert "Gym" in schedules
    assert "Study" in schedules

def test_add_task():
    suketan = Suketan()
    suketan.create_schedule("Errands")
    task = Task(title="Buy groceries", time="01:00", description="Milk, Bread, Eggs")
    suketan.add_task("Errands", task)
    assert task == suketan.schedules["Errands"][0]
    assert suketan.schedules["Errands"][0].title == "Buy groceries"
    assert suketan.schedules["Errands"][0].time == "01:00"
    assert suketan.schedules["Errands"][0].description == "Milk, Bread, Eggs"
    assert suketan.schedules["Errands"][0].tag == []

def test_list_tasks():
    suketan = Suketan()
    suketan.create_schedule("Chores")
    task1 = Task(title="Clean room", time="02:00", description="Vacuum and dust")
    task2 = Task(title="Wash dishes", time="03:00", description="Use dishwasher")
    suketan.add_task("Chores", task1)
    suketan.add_task("Chores", task2)
    tasks = suketan.list_tasks("Chores")
    assert len(tasks) == 2
    assert tasks[0].title == "Clean room"
    assert tasks[1].title == "Wash dishes"

def test_overwrite_task():
    suketan = Suketan()
    suketan.create_schedule("Projects")
    task1 = Task(title="Project A", time="04:00", description="Initial setup")
    suketan.add_task("Projects", task1)
    new_task = Task(title="Project A Updated", time="05:00", description="Setup complete")
    suketan.overwrite_task("Projects", 0, new_task)
    assert suketan.schedules["Projects"][0].title == "Project A Updated"
    assert suketan.schedules["Projects"][0].time == "05:00"
    assert suketan.schedules["Projects"][0].description == "Setup complete"

def test_delete_task():
    suketan = Suketan()
    suketan.create_schedule("Learning")
    task1 = Task(title="Read book", time="06:00", description="Chapter 1-3")
    task2 = Task(title="Watch tutorial", time="07:00", description="Python basics")
    suketan.add_task("Learning", task1)
    suketan.add_task("Learning", task2)
    suketan.delete_task("Learning", 0)
    tasks = suketan.list_tasks("Learning")
    assert len(tasks) == 1
    assert tasks[0].title == "Watch tutorial"
