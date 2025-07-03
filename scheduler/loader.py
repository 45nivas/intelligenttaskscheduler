from typing import List, Union
import json
import csv
from .task import Task

def load_tasks_from_json(file_path: str) -> List[Task]:
    """Load tasks from a JSON file.

    Parameters
    ----------
    file_path : str
        The path to the JSON file containing task data.

    Returns
    -------
    List[Task]
        A list of Task objects loaded from the JSON file.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
        return [Task(**task) for task in data]

def load_tasks_from_csv(file_path: str) -> List[Task]:
    """Load tasks from a CSV file.

    Parameters
    ----------
    file_path : str
        The path to the CSV file containing task data.

    Returns
    -------
    List[Task]
        A list of Task objects loaded from the CSV file.
    """
    tasks = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tasks.append(Task(**row))
    return tasks

def load_tasks(file_path: str) -> List[Task]:
    """Load tasks from a file, either JSON or CSV.

    Parameters
    ----------
    file_path : str
        The path to the file containing task data.

    Returns
    -------
    List[Task]
        A list of Task objects loaded from the specified file.
    
    Raises
    ------
    ValueError
        If the file format is unsupported or if there is an error in loading tasks.
    """
    if file_path.endswith('.json'):
        return load_tasks_from_json(file_path)
    elif file_path.endswith('.csv'):
        return load_tasks_from_csv(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a JSON or CSV file.")