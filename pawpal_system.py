from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    description: str
    due_time: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    completion_status: bool = False

    def edit_description(self, description: str):
        self.description = description

    def edit_due_time(self, due_time: str):
        self.due_time = due_time

    def mark_complete(self):
        self.completion_status = True


@dataclass
class Pet:
    pet_name: str
    pet_type: str
    special_notes: str = ""
    tasks: list[Task] = field(default_factory=list)

    def add_info(self, note: str):
        self.special_notes = note

    def delete_info(self):
        self.special_notes = ""

    def edit_info(self, note: str):
        self.special_notes = note

    def add_task(self, task: Task):
        self.tasks.append(task)

    def remove_task(self, task: Task):
        self.tasks.remove(task)


@dataclass
class Owner:
    name: str
    address: str
    pets: list[Pet] = field(default_factory=list)

    def edit_name(self, name: str):
        self.name = name

    def edit_address(self, address: str):
        self.address = address

    def add_pet(self, pet: Pet):
        self.pets.append(pet)

    def remove_pet(self, pet: Pet):
        self.pets.remove(pet)

    def edit_pet(self, old_pet: Pet, new_pet: Pet):
        index = self.pets.index(old_pet)
        self.pets[index] = new_pet


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


class Scheduler:
    def __init__(self):
        self.tasks: list[Task] = []

    def load_tasks_from_owner(self, owner: Owner):
        self.tasks = []
        for pet in owner.pets:
            self.tasks.extend(pet.tasks)

    def organize_by_due_date(self) -> list[Task]:
        return sorted(self.tasks, key=lambda t: t.due_time)

    def filter_by_pet(self, pet: Pet) -> list[Task]:
        return [t for t in self.tasks if t in pet.tasks]

    def build_schedule(self, owner: Optional[Owner] = None) -> list[dict]:
        if owner:
            self.load_tasks_from_owner(owner)

        pending = [t for t in self.tasks if not t.completion_status]
        sorted_tasks = sorted(
            pending,
            key=lambda t: (t.due_time, PRIORITY_ORDER.get(t.priority, 1)),
        )

        schedule = []
        for task in sorted_tasks:
            schedule.append({
                "description": task.description,
                "due_time": task.due_time,
                "duration_minutes": task.duration_minutes,
                "priority": task.priority,
                "reason": f"Priority: {task.priority}, due at {task.due_time}",
            })

        return schedule
