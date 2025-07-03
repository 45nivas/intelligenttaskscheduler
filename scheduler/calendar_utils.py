from datetime import datetime, timedelta
from typing import List, Tuple

def is_within_working_hours(start: datetime, end: datetime) -> bool:
    """Check if the given time range is within working hours (Monday to Friday, 09:00 to 17:00).
    
    Parameters
    ----------
    start : datetime
        The start time of the task.
    end : datetime
        The end time of the task.
    
    Returns
    -------
    bool
        True if the time range is within working hours, False otherwise.
    """
    if start.weekday() >= 5 or end.weekday() >= 5:  # Saturday or Sunday
        return False
    if start.hour < 9 or end.hour > 17:
        return False
    return True

def get_working_days(start_date: datetime, end_date: datetime) -> List[datetime]:
    """Generate a list of working days between two dates.
    
    Parameters
    ----------
    start_date : datetime
        The start date.
    end_date : datetime
        The end date.
    
    Returns
    -------
    List[datetime]
        A list of working days (Monday to Friday) between the start and end dates.
    """
    current_date = start_date
    working_days = []
    while current_date <= end_date:
        if current_date.weekday() < 5:  # Monday to Friday
            working_days.append(current_date)
        current_date += timedelta(days=1)
    return working_days

def calculate_time_window(start: datetime, duration_hours: float) -> Tuple[datetime, datetime]:
    """Calculate the end time given a start time and duration in hours.
    
    Parameters
    ----------
    start : datetime
        The start time.
    duration_hours : float
        The duration in hours.
    
    Returns
    -------
    Tuple[datetime, datetime]
        A tuple containing the start and end time.
    """
    end_time = start + timedelta(hours=duration_hours)
    return start, end_time