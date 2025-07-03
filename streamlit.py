import json
import datetime
from typing import List, Dict

import pandas as pd
import altair as alt
import streamlit as st



def parse_dt(ts: str) -> datetime.datetime:
    if ts.endswith("Z"):
        ts = ts.replace("Z", "+00:00")
    dt = datetime.datetime.fromisoformat(ts)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    return dt


def generate_schedule(tasks: List[dict]) -> List[dict]:
    priority_map = {"high": 3, "med": 2, "low": 1}

    def score(task):
        deadline = parse_dt(task["deadline"])
        days_to_deadline = (deadline - datetime.datetime.now(datetime.timezone.utc)).days
        urgency_score = max(0, 30 - days_to_deadline)
        return urgency_score + priority_map.get(task["priority"], 1) * 10

    tasks_sorted = sorted(tasks, key=score, reverse=True)

    earliest_starts = [parse_dt(t["earliest_start"]) for t in tasks_sorted if t.get("earliest_start")]
    if earliest_starts:
        current_day = min(earliest_starts)
    else:
        current_day = datetime.datetime.now(datetime.timezone.utc)
    current_day = current_day.replace(hour=9, minute=0, second=0, microsecond=0)

    WORK_START = datetime.time(9, 0)
    WORK_END = datetime.time(17, 0)
    LUNCH_START = datetime.time(12, 0)
    LUNCH_END = datetime.time(13, 0)
    DAILY_CAP = 5.5  # Assume average productive work hours

    dep_finish: Dict[int, datetime.datetime] = {}
    scheduled: List[dict] = []
    day_hours_used = 0.0

    def next_workday(dt: datetime.datetime) -> datetime.datetime:
        return (dt + datetime.timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)

    for task in tasks_sorted:
        est = float(task.get("estimated_hours", 1.0))
        pointer = current_day

        for dep_id in task.get("dependencies", []):
            if dep_id in dep_finish:
                pointer = max(pointer, dep_finish[dep_id])

        if task.get("earliest_start"):
            pointer = max(pointer, parse_dt(task["earliest_start"]))

        while True:
            if pointer.time() < WORK_START or pointer.time() >= WORK_END:
                pointer = next_workday(pointer)
                day_hours_used = 0.0

            if day_hours_used + est > DAILY_CAP or (pointer.hour + est) > 17:
                pointer = next_workday(pointer)
                day_hours_used = 0.0
                continue

            if (
                pointer.time() < LUNCH_START
                and (pointer + datetime.timedelta(hours=est)).time() > LUNCH_START
            ):
                before = (datetime.datetime.combine(pointer.date(), LUNCH_START, tzinfo=pointer.tzinfo) - pointer).total_seconds() / 3600
                after = est - before
                scheduled.append({**task, "start_time": pointer.isoformat(), "end_time": (pointer + datetime.timedelta(hours=before)).isoformat()})
                day_hours_used += before
                est = after
                pointer = datetime.datetime.combine(pointer.date(), LUNCH_END, tzinfo=pointer.tzinfo)
                continue
            break

        start_time = pointer
        end_time = start_time + datetime.timedelta(hours=est)
        scheduled.append({**task, "start_time": start_time.isoformat(), "end_time": end_time.isoformat()})
        dep_finish[task["id"]] = end_time
        day_hours_used += est
        current_day = end_time

    return scheduled


st.set_page_config(page_title="Smart Task Scheduler", layout="wide")
st.title("🧠 Smart Task Scheduler – Human‑Centered")

if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "next_id" not in st.session_state:
    st.session_state.next_id = 1

with st.sidebar:
    st.header("Add Task")
    with st.form("add_task"):
        title = st.text_input("Task Title")
        priority = st.selectbox("Priority", ("high", "med", "low"))
        deadline = st.date_input("Deadline")
        earliest_start = st.date_input("Can Start On", value=deadline)
        estimated_hours = st.number_input("Estimated Hours", min_value=0.5, max_value=8.0, value=1.0, step=0.5)
        submitted = st.form_submit_button("Add Task")
        if submitted:
            deadline_dt = datetime.datetime.combine(deadline, datetime.time(17, 0), tzinfo=datetime.timezone.utc)
            start_dt = datetime.datetime.combine(earliest_start, datetime.time(9, 0), tzinfo=datetime.timezone.utc)
            st.session_state.tasks.append({
                "id": st.session_state.next_id,
                "title": title or f"Task {st.session_state.next_id}",
                "priority": priority,
                "deadline": deadline_dt.isoformat(),
                "earliest_start": start_dt.isoformat(),
                "estimated_hours": estimated_hours,
                "dependencies": [],
            })
            st.session_state.next_id += 1
            st.success("Task added!")

st.subheader("Task List")
if st.session_state.tasks:
    st.dataframe(pd.DataFrame(st.session_state.tasks), use_container_width=True)
else:
    st.info("No tasks yet. Use the sidebar to add one.")

if st.button("Generate Schedule"):
    if not st.session_state.tasks:
        st.warning("Please add at least one task first.")
    else:
        schedule = generate_schedule(st.session_state.tasks)
        df = pd.DataFrame(schedule)
        df["start_time"] = pd.to_datetime(df["start_time"])
        df["end_time"] = pd.to_datetime(df["end_time"])

        st.success("Schedule created!")
        tab1, tab2 = st.tabs(["Table", "Timeline"])

        with tab1:
            st.dataframe(df[["id", "title", "priority", "estimated_hours", "start_time", "end_time"]], use_container_width=True)

        with tab2:
            gantt = (
                alt.Chart(df)
                .mark_bar()
                .encode(
                    x="start_time:T",
                    x2="end_time:T",
                    y=alt.Y("title:N", sort='-x'),
                    color="priority:N",
                    tooltip=["title", "priority", "estimated_hours", "start_time", "end_time"],
                )
                .properties(height=400)
            )
            st.altair_chart(gantt, use_container_width=True)
else:
    st.caption("⬅️ Add tasks with priority and deadline, then generate a smart schedule.")
