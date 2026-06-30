from datetime import time
from pawpal_system import Owner, Pet, Task, Scheduler

# Create owner
owner = Owner(name="Jamie Rivera", address="123 Maple St, Springfield")

# Create pets
buddy = Pet(pet_name="Buddy", pet_type="Dog", special_notes="Allergic to chicken")
whiskers = Pet(pet_name="Whiskers", pet_type="Cat", special_notes="Indoor only")

# Create tasks for Buddy
morning_walk = Task(
    description="Morning walk for Buddy",
    due_time=time(7, 0),
    duration_minutes=30,
    priority="high",
    frequency="daily",
)
feeding_buddy = Task(
    description="Feed Buddy breakfast",
    due_time=time(8, 0),
    duration_minutes=10,
    priority="high",
    frequency="daily",
)
evening_walk = Task(
    description="Evening walk for Buddy",
    due_time=time(18, 30),
    duration_minutes=45,
    priority="medium",
    frequency="daily",
)

# Create tasks for Whiskers
feeding_whiskers = Task(
    description="Feed Whiskers wet food",
    due_time=time(8, 30),
    duration_minutes=5,
    priority="high",
    frequency="daily",
)
litter_box = Task(
    description="Clean Whiskers' litter box",
    due_time=time(12, 0),
    duration_minutes=10,
    priority="medium",
    frequency="daily",
)
playtime = Task(
    description="Interactive playtime with Whiskers",
    due_time=time(19, 0),
    duration_minutes=20,
    priority="low",
    frequency="daily",
)

# Assign tasks to pets
buddy.add_task(morning_walk)
buddy.add_task(feeding_buddy)
buddy.add_task(evening_walk)

whiskers.add_task(feeding_whiskers)
whiskers.add_task(litter_box)
whiskers.add_task(playtime)

# Add pets to owner
owner.add_pet(buddy)
owner.add_pet(whiskers)

# Set up scheduler
scheduler = Scheduler()
scheduler.add_owner(owner)

# Build and print schedule
schedule = scheduler.build_schedule()

print(f"=== Daily Pet Care Schedule for {owner.name} ===\n")
for i, entry in enumerate(schedule, start=1):
    print(f"{i}. [{entry['due_time']}] {entry['description']}")
    print(f"   Duration: {entry['duration_minutes']} min | {entry['reason']}")
    print()
