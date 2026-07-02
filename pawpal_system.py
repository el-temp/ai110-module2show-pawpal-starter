import calendar
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from typing import Optional

RECURRENCE_INTERVALS = {"daily": timedelta(days=1), "weekly": timedelta(days=7)}


def _add_one_month(d: date) -> date:
    """Return the date one calendar month after d, clamping the day to
    whatever the target month actually has (e.g. Jan 31 -> Feb 28)."""
    month = d.month % 12 + 1
    year = d.year + (d.month // 12)
    day = min(d.day, calendar.monthrange(year, month)[1])
    return d.replace(year=year, month=month, day=day)


@dataclass
class Task:
    description: str
    due_time: time
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    frequency: str = "once"  # "once", "daily", "weekly", "monthly"
    completion_status: bool = False
    due_date: date = field(default_factory=date.today)

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

    def next_occurrence(self) -> Optional["Task"]:
        """Return a fresh pending Task for this task's next occurrence, or
        None if the task doesn't recur (frequency == "once").

        Daily/weekly occurrences use timedelta for an exact day offset;
        monthly occurrences advance by one calendar month.
        """
        if self.frequency == "once":
            return None

        if self.frequency in RECURRENCE_INTERVALS:
            next_due_date = self.due_date + RECURRENCE_INTERVALS[self.frequency]
        elif self.frequency == "monthly":
            next_due_date = _add_one_month(self.due_date)
        else:
            return None

        return Task(
            description=self.description,
            due_time=self.due_time,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            frequency=self.frequency,
            completion_status=False,
            due_date=next_due_date,
        )

    def end_time(self) -> time:
        """Return the time this task finishes, based on due_time + duration."""
        start = datetime.combine(datetime.min, self.due_time)
        end = start + timedelta(minutes=self.duration_minutes)
        return end.time()


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
        if any(pet in owner.pets for owner in self.owners):
            return list(pet.tasks)
        return []

    def _find_pet_for_task(self, task: Task) -> Optional[Pet]:
        """Locate the pet that owns the given task instance."""
        for owner in self.owners:
            for pet in owner.pets:
                if any(t is task for t in pet.tasks):
                    return pet
        return None

    def complete_task(self, task: Task) -> Optional[Task]:
        """Mark a task complete and, if it recurs, schedule its next
        occurrence so the owner never has to manually re-add daily/weekly/
        monthly chores.
        """
        task.mark_complete()

        next_task = task.next_occurrence()
        if next_task is not None:
            pet = self._find_pet_for_task(task)
            if pet is not None:
                pet.add_task(next_task)

        return next_task

    def find_time_conflicts(self) -> list[tuple[Task, Task]]:
        """Return pairs of pending tasks whose time windows overlap.

        An owner can't physically perform two overlapping tasks at once, so
        surfacing these lets them notice and reschedule before the day starts.
        """
        pending = [t for t in self.get_all_tasks() if not t.completion_status]
        sorted_tasks = sorted(pending, key=lambda t: t.due_time)

        conflicts = []
        for earlier, later in zip(sorted_tasks, sorted_tasks[1:]):
            start = datetime.combine(datetime.min, earlier.due_time)
            end = start + timedelta(minutes=earlier.duration_minutes)
            later_start = datetime.combine(datetime.min, later.due_time)
            if later_start < end:
                conflicts.append((earlier, later))

        return conflicts

    def total_care_minutes(self) -> int:
        """Return the total minutes of pending pet care tasks, so an owner
        can see at a glance how much of their day is committed."""
        return sum(
            t.duration_minutes for t in self.get_all_tasks() if not t.completion_status
        )

    def build_schedule(self) -> list[dict]:
        """Build a prioritized schedule of all pending tasks sorted by due time."""
        pending = [t for t in self.get_all_tasks() if not t.completion_status]
        sorted_tasks = sorted(
            pending,
            key=lambda t: (t.due_time, PRIORITY_ORDER.get(t.priority, 1)),
        )
        conflicting_ids = {id(t) for pair in self.find_time_conflicts() for t in pair}

        schedule = []
        for task in sorted_tasks:
            reason = f"Priority: {task.priority}, due at {task.due_time.strftime('%I:%M %p')}"
            if id(task) in conflicting_ids:
                reason += " -- CONFLICT: overlaps with another task"
            schedule.append({
                "description": task.description,
                "due_time": task.due_time.strftime("%I:%M %p"),
                "duration_minutes": task.duration_minutes,
                "priority": task.priority,
                "reason": reason,
            })

        return schedule
