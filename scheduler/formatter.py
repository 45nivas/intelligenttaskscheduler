from typing import List, Dict, Any
import json
from rich.console import Console
from rich.table import Table

console = Console()

def print_schedule(schedule: List[Dict[str, Any]]) -> None:
    """Prints the schedule in a formatted console table.

    Parameters
    ----------
    schedule : List[Dict[str, Any]]
        A list of tasks with their scheduled times and details.
    """
    table = Table(title="Task Schedule")

    table.add_column("Task Title", justify="left")
    table.add_column("Start Time", justify="center")
    table.add_column("End Time", justify="center")
    table.add_column("Estimated Hours", justify="right")
    table.add_column("Tags", justify="left")

    for task in schedule:
        table.add_row(
            task['title'],
            task['start_time'],
            task['end_time'],
            str(task['estimated_hours']),
            ", ".join(task.get('tags', []))
        )

    console.print(table)

def write_schedule_to_json(schedule: List[Dict[str, Any]], filename: str) -> None:
    """Writes the schedule to a JSON file.

    Parameters
    ----------
    schedule : List[Dict[str, Any]]
        A list of tasks with their scheduled times and details.
    filename : str
        The name of the file to write the schedule to.
    """
    with open(filename, 'w') as f:
        json.dump(schedule, f, indent=4)

def generate_ics(schedule: List[Dict[str, Any]], filename: str) -> None:
    """Generates an ICS calendar file from the schedule.

    Parameters
    ----------
    schedule : List[Dict[str, Any]]
        A list of tasks with their scheduled times and details.
    filename : str
        The name of the ICS file to create.
    """
    # TODO: Implement ICS generation logic
    pass