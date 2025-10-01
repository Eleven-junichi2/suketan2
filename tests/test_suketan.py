import pytest  # noqa: F401

from suketan2.main import Suketan

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