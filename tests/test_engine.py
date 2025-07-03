import pytest
from scheduler.engine import ScheduleEngine
from scheduler.task import Task
from datetime import datetime, timedelta

def test_schedule_engine_basic():
    tasks = [
        Task(title="Task 1", deadline=datetime.now() + timedelta(days=1), priority="high", estimated_hours=2.0),
        Task(title="Task 2", deadline=datetime.now() + timedelta(days=2), priority="med", estimated_hours=1.5),
        Task(title="Task 3", deadline=datetime.now() + timedelta(days=3), priority="low", estimated_hours=3.0),
    ]
    
    engine = ScheduleEngine()
    schedule = engine.schedule(tasks)

    assert len(schedule) == 3
    assert all(task.title in [t.title for t in schedule] for task in tasks)

def test_schedule_engine_with_dependencies():
    tasks = [
        Task(title="Task A", deadline=datetime.now() + timedelta(days=2), priority="high", estimated_hours=2.0, dependencies=[]),
        Task(title="Task B", deadline=datetime.now() + timedelta(days=3), priority="med", estimated_hours=1.0, dependencies=["Task A"]),
    ]
    
    engine = ScheduleEngine()
    schedule = engine.schedule(tasks)

    assert len(schedule) == 2
    assert schedule[0].title == "Task A"
    assert schedule[1].title == "Task B"

def test_schedule_engine_impossible_schedule():
    tasks = [
        Task(title="Task 1", deadline=datetime.now() + timedelta(days=1), priority="high", estimated_hours=8.0),
        Task(title="Task 2", deadline=datetime.now() + timedelta(days=1), priority="med", estimated_hours=8.0),
    ]
    
    engine = ScheduleEngine()
    schedule = engine.schedule(tasks)

    assert schedule is None  # Expecting None or some indication of an impossible schedule

def test_schedule_engine_edge_case():
    tasks = [
        Task(title="Task 1", deadline=datetime.now() + timedelta(days=1), priority="high", estimated_hours=0.25),
        Task(title="Task 2", deadline=datetime.now() + timedelta(days=1), priority="med", estimated_hours=0.5),
    ]
    
    engine = ScheduleEngine()
    schedule = engine.schedule(tasks)

    assert len(schedule) == 2
    assert schedule[0].estimated_hours == 0.25
    assert schedule[1].estimated_hours == 0.5

def test_schedule_engine_with_focus_window():
    tasks = [
        Task(title="Task 1", deadline=datetime.now() + timedelta(days=1), priority="high", estimated_hours=2.0),
        Task(title="Task 2", deadline=datetime.now() + timedelta(days=1), priority="med", estimated_hours=1.0),
    ]
    
    engine = ScheduleEngine(focus_window=(13, 15))  # Focus window from 1 PM to 3 PM
    schedule = engine.schedule(tasks)

    assert all(task.start_time.hour < 13 or task.start_time.hour >= 15 for task in schedule)  # Ensure tasks are outside focus window