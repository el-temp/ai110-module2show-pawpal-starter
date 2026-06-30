from datetime import time
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet


def make_task():
    return Task(
        description="Feed dog",
        due_time=time(8, 0),
        duration_minutes=10,
        priority="high",
    )


def test_mark_complete_changes_status():
    task = make_task()
    assert task.completion_status is False
    task.mark_complete()
    assert task.completion_status is True


def test_add_task_increases_count():
    pet = Pet(pet_name="Buddy", pet_type="dog")
    assert len(pet.tasks) == 0
    pet.add_task(make_task())
    assert len(pet.tasks) == 1
    pet.add_task(make_task())
    assert len(pet.tasks) == 2
