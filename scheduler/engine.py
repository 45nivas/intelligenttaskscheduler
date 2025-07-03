import datetime
from typing import List, Dict


def generate_schedule(tasks: List[dict], daily_effort_cap: float = 6.0) -> List[dict]:
    """
    Assigns start and end times to tasks based on priority, urgency, dependencies, and constraints.
    """
    priority_map = {"high": 3, "med": 2, "low": 1}

    
    def score(task):
        deadline = task["deadline"]
        if isinstance(deadline, str):
            deadline = datetime.datetime.fromisoformat(deadline.replace("Z", "+00:00"))
        days_to_deadline = (deadline - datetime.datetime.now(datetime.timezone.utc)).days
        urgency_score = max(0, 30 - days_to_deadline)
        priority_score = priority_map.get(task["priority"], 1) * 10
        return urgency_score + priority_score

    
    id_to_task = {t["id"]: t for t in tasks}
    dep_finish_times = {}

    
    sorted_tasks = sorted(tasks, key=score, reverse=True)

    
    earliest_starts = []
    for t in sorted_tasks:
        es = t.get("earliest_start")
        if es:
            if isinstance(es, str):
                es = datetime.datetime.fromisoformat(es.replace("Z", "+00:00"))
            earliest_starts.append(es)
    if earliest_starts:
        current_day = min(earliest_starts)
        current_day = current_day.replace(hour=9, minute=0, second=0, microsecond=0)
    else:
        current_day = datetime.datetime.now(datetime.timezone.utc).replace(hour=9, minute=0, second=0, microsecond=0)

    WORK_START = datetime.time(9, 0)
    WORK_END = datetime.time(17, 0)
    LUNCH_START = datetime.time(12, 0)
    LUNCH_END = datetime.time(13, 0)

    scheduled = []
    day_hours_used = 0.0

    
    def next_workday(dt):
        return (dt + datetime.timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)

    for task in sorted_tasks:
        est = float(task["estimated_hours"])
        
        dep_end = current_day
        for dep_id in task.get("dependencies", []):
            if dep_id in dep_finish_times:
                dep_end = max(dep_end, dep_finish_times[dep_id])
        
        task_earliest = task.get("earliest_start")
        if task_earliest:
            if isinstance(task_earliest, str):
                task_earliest = datetime.datetime.fromisoformat(task_earliest.replace("Z", "+00:00"))
            dep_end = max(dep_end, task_earliest.replace(tzinfo=datetime.timezone.utc))
        
        candidate_start = dep_end
        while True:
            
            if candidate_start.time() < WORK_START or candidate_start.time() >= WORK_END:
                candidate_start = candidate_start.replace(hour=9, minute=0, second=0, microsecond=0)
                candidate_start = next_workday(candidate_start)
                day_hours_used = 0.0
            
            if day_hours_used + est > daily_effort_cap or (candidate_start.hour + est) > 17:
                candidate_start = next_workday(candidate_start)
                day_hours_used = 0.0
                continue
            
            if candidate_start.time() < LUNCH_START and (candidate_start + datetime.timedelta(hours=est)).time() > LUNCH_START:
                before_lunch = (datetime.datetime.combine(candidate_start.date(), LUNCH_START) - candidate_start).total_seconds() / 3600
                after_lunch = est - before_lunch
                start_time = candidate_start
                end_time = candidate_start + datetime.timedelta(hours=before_lunch)
                scheduled_task = task.copy()
                scheduled_task["start_time"] = start_time.isoformat()
                scheduled_task["end_time"] = end_time.isoformat()
                scheduled.append(scheduled_task)
                candidate_start = datetime.datetime.combine(candidate_start.date(), LUNCH_END).replace(tzinfo=datetime.timezone.utc)
                day_hours_used += before_lunch
                est = after_lunch
                continue
            
            start_time = candidate_start
            end_time = start_time + datetime.timedelta(hours=est)
            
            if end_time.time() > WORK_END or day_hours_used + est > daily_effort_cap:
                candidate_start = next_workday(candidate_start)
                day_hours_used = 0.0
                continue
            break
        scheduled_task = task.copy()
        scheduled_task["start_time"] = start_time.isoformat()
        scheduled_task["end_time"] = end_time.isoformat()
        scheduled.append(scheduled_task)
        dep_finish_times[task["id"]] = end_time
        day_hours_used += est
        current_day = end_time

    return scheduled


class ScheduleEngine:
    """Handles the scheduling and optimization of tasks.

    This class uses either OR-Tools CP-SAT or a greedy fallback method
    to create an optimized schedule based on the provided tasks.
    """

    def __init__(
        self,
        weight_urgency=1.0,
        weight_priority=1.0,
        weight_effort=1.0,
        working_hours=("09:00", "17:00"),
        daily_effort_cap=6.0,
        dont_fragment_tasks=False
    ):
        """Initializes the ScheduleEngine with tasks and configuration.

        Parameters
        ----------
        weight_urgency : float
        weight_priority : float
        weight_effort : float
        working_hours : tuple
        daily_effort_cap : float
        dont_fragment_tasks : bool
        """
        self.weight_urgency = weight_urgency
        self.weight_priority = weight_priority
        self.weight_effort = weight_effort
        self.working_hours = working_hours
        self.daily_effort_cap = daily_effort_cap
        self.dont_fragment_tasks = dont_fragment_tasks

    def schedule(self, tasks):
        """Schedules the tasks and returns the planned schedule (simple greedy fallback)."""
        # Sort by deadline, then priority (high > med > low)
        priority_map = {"high": 3, "med": 2, "low": 1}
        sorted_tasks = sorted(
            tasks,
            key=lambda t: (
                t.deadline,
                -priority_map.get(t.priority, 0)
            )
        )
        # Assign dummy start/end times for demo purposes
        base_date = datetime.datetime(2023, 10, 14, 9, 0)
        scheduled = []
        for i, t in enumerate(sorted_tasks):
            start_time = base_date + datetime.timedelta(hours=i * 3)
            end_time = start_time + datetime.timedelta(hours=t.estimated_hours)
            task_dict = t.__dict__.copy()
            task_dict['start_time'] = start_time.isoformat()
            task_dict['end_time'] = end_time.isoformat()
            scheduled.append(task_dict)
        return scheduled

    def _apply_constraints(self):
        """Applies scheduling constraints such as deadlines and dependencies.

        This method ensures that tasks are scheduled according to their
        deadlines and any specified dependencies.
        """
        # TODO: Implement constraint application logic
        pass

    def _optimize_schedule(self):
        """Optimizes the schedule based on the scoring of tasks.

        This method will prioritize tasks based on their urgency, priority,
        and estimated effort.
        """
        # TODO: Implement schedule optimization logic
        pass

    def _greedy_fallback(self):
        """Fallback scheduling method using a greedy approach.

        This method will schedule tasks in a simple greedy manner if
        OR-Tools is not available.
        """
        # TODO: Implement greedy scheduling logic
        pass