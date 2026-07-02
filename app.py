from datetime import time

import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
**PawPal+** is a pet care planning assistant. Create an owner, add pets, give each
pet some care tasks, then build a prioritized daily schedule.
"""
)

# ---------------------------------------------------------------------------
# Session state: created once, then reused on every re-run.
# Streamlit re-runs this whole script on every interaction, so anything that
# needs to survive across button clicks/inputs must live in st.session_state
# instead of a plain local variable.
# ---------------------------------------------------------------------------
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

if "owner" not in st.session_state:
    st.session_state.owner = None

st.divider()

# ---------------------------------------------------------------------------
# Owner setup
# ---------------------------------------------------------------------------
st.subheader("Owner")

if st.session_state.owner is None:
    with st.form("owner_form"):
        owner_name = st.text_input("Owner name", value="Jordan")
        owner_address = st.text_input("Owner address", value="123 Main St")
        create_owner = st.form_submit_button("Create owner")

    if create_owner:
        owner = Owner(name=owner_name, address=owner_address)
        st.session_state.scheduler.add_owner(owner)
        st.session_state.owner = owner
        st.rerun()
else:
    owner = st.session_state.owner
    st.success(f"Owner: **{owner.name}** ({owner.address})")
    if st.button("Reset owner"):
        st.session_state.scheduler.remove_owner(owner)
        st.session_state.owner = None
        st.rerun()

if st.session_state.owner is None:
    st.info("Create an owner to continue.")
    st.stop()

owner = st.session_state.owner

st.divider()

# ---------------------------------------------------------------------------
# Pet setup
# ---------------------------------------------------------------------------
st.subheader("Pets")

with st.form("pet_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        pet_name = st.text_input("Pet name", value="Mochi")
    with col2:
        pet_type = st.selectbox("Species", ["dog", "cat", "other"])
    special_notes = st.text_input("Special notes (optional)", value="")
    add_pet = st.form_submit_button("Add pet")

if add_pet and pet_name:
    owner.add_pet(Pet(pet_name=pet_name, pet_type=pet_type, special_notes=special_notes))

if owner.pets:
    st.write("Current pets:")
    for pet in owner.pets:
        st.write(f"- **{pet.pet_name}** ({pet.pet_type}) — {len(pet.tasks)} task(s)")
else:
    st.info("No pets yet. Add one above.")
    st.stop()

st.divider()

# ---------------------------------------------------------------------------
# Task setup
# ---------------------------------------------------------------------------
st.subheader("Tasks")

pet_names = [pet.pet_name for pet in owner.pets]
selected_pet_name = st.selectbox("Pet", pet_names)
selected_pet = next(pet for pet in owner.pets if pet.pet_name == selected_pet_name)

with st.form("task_form", clear_on_submit=True):
    description = st.text_input("Task description", value="Morning walk")
    col1, col2, col3 = st.columns(3)
    with col1:
        due_time = st.time_input("Due time", value=time(7, 0))
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    frequency = st.selectbox("Frequency", ["once", "daily", "weekly", "monthly"])
    add_task = st.form_submit_button("Add task")

if add_task and description:
    selected_pet.add_task(
        Task(
            description=description,
            due_time=due_time,
            duration_minutes=int(duration),
            priority=priority,
            frequency=frequency,
        )
    )

if selected_pet.tasks:
    st.write(f"Tasks for **{selected_pet.pet_name}**:")
    st.table(
        [
            {
                "description": t.description,
                "due_time": t.due_time.strftime("%I:%M %p"),
                "duration_minutes": t.duration_minutes,
                "priority": t.priority,
                "frequency": t.frequency,
            }
            for t in selected_pet.tasks
        ]
    )
else:
    st.info(f"No tasks yet for {selected_pet.pet_name}.")

st.divider()

# ---------------------------------------------------------------------------
# Build schedule
# ---------------------------------------------------------------------------
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    schedule = st.session_state.scheduler.build_schedule()
    if schedule:
        for i, entry in enumerate(schedule, start=1):
            st.write(f"**{i}. [{entry['due_time']}] {entry['description']}**")
            st.caption(f"Duration: {entry['duration_minutes']} min | {entry['reason']}")
    else:
        st.info("No pending tasks to schedule.")
