from dataclasses import dataclass, field
from datetime import time
from typing import Optional


@dataclass
class Task:
    description: str
    due_time: time
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    frequency: str = "once"  # "once", "daily", "weekly", "monthly"
    completion_status: bool = False

    def edit_description(self, description: str):
        """Update the task's description text."""
        self.description = description

    def edit_due_time(self, due_time: time):
        """Update the time the task is due."""
        self.due_time = due_time

    def edit_frequency(self, frequency: str):
        """Set how often the task recurs; ignores invalid values."""
        valid = {"once", "daily", "weekly", "monthly"}
        if frequency in valid:
            self.frequency = frequency

    def mark_complete(self):
        """Mark the task as completed."""
        self.completion_status = True


@dataclass
class Pet:
    pet_name: str
    pet_type: str
    special_notes: str = ""
    tasks: list[Task] = field(default_factory=list)

    def add_info(self, note: str):
        """Append a note to the pet's existing special notes."""
        self.special_notes = f"{self.special_notes} {note}".strip()

    def delete_info(self):
        """Clear all special notes for the pet."""
        self.special_notes = ""

    def edit_info(self, note: str):
        """Replace the pet's special notes with the given text."""
        self.special_notes = note

    def add_task(self, task: Task):
        """Attach a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task):
        """Remove a task from this pet's task list if it exists."""
        if task in self.tasks:
            self.tasks.remove(task)


@dataclass
class Owner:
    name: str
    address: str
    pets: list[Pet] = field(default_factory=list)

    def edit_name(self, name: str):
        """Update the owner's name."""
        self.name = name

    def edit_address(self, address: str):
        """Update the owner's address."""
        self.address = address

    def add_pet(self, pet: Pet):
        """Add a pet to the owner's pet list."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet):
        """Remove a pet from the owner's pet list if it exists."""
        if pet in self.pets:
            self.pets.remove(pet)

    def edit_pet(self, old_pet: Pet, new_pet: Pet):
        """Replace an existing pet entry with a new one."""
        if old_pet in self.pets:
            index = self.pets.index(old_pet)
            self.pets[index] = new_pet

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all of the owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]

    def get_tasks_for_pet(self, pet: Pet) -> list[Task]:
        """Return the task list for a specific pet owned by this owner."""
        if pet in self.pets:
            return list(pet.tasks)
        return []


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


class Scheduler:
    def __init__(self):
        self.owners: list[Owner] = []

    def add_owner(self, owner: Owner):
        """Register an owner with the scheduler if not already present."""
        if owner not in self.owners:
            self.owners.append(owner)

    def remove_owner(self, owner: Owner):
        """Unregister an owner from the scheduler if present."""
        if owner in self.owners:
            self.owners.remove(owner)

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all registered owners and their pets."""
        return [task for owner in self.owners for task in owner.get_all_tasks()]

    def organize_by_due_date(self) -> list[Task]:
        """Return all tasks sorted chronologically by due time."""
        return sorted(self.get_all_tasks(), key=lambda t: t.due_time)

    def filter_by_pet(self, pet: Pet) -> list[Task]:
        """Return tasks belonging to a specific pet across all owners."""
        for owner in self.owners:
            tasks = owner.get_tasks_for_pet(pet)
            if tasks:
                return tasks
        return []

    def build_schedule(self) -> list[dict]:
        """Build a prioritized schedule of all pending tasks sorted by due time."""
        pending = [t for t in self.get_all_tasks() if not t.completion_status]
        sorted_tasks = sorted(
            pending,
            key=lambda t: (t.due_time, PRIORITY_ORDER.get(t.priority, 1)),
        )

        schedule = []
        for task in sorted_tasks:
            schedule.append({
                "description": task.description,
                "due_time": task.due_time.strftime("%I:%M %p"),
                "duration_minutes": task.duration_minutes,
                "priority": task.priority,
                "reason": f"Priority: {task.priority}, due at {task.due_time.strftime('%I:%M %p')}",
            })

        return schedule
