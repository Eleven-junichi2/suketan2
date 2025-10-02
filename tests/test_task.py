import pytest

from suketan2.main import Task

def test_task():
    task = Task(title="Buy groceries", time="01:00", description="Milk, Bread, Eggs")
    assert task.title == "Buy groceries"
    assert task.time == "01:00"
    assert task.description == "Milk, Bread, Eggs"
    assert task.tag == []
