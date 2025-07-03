# Intelligent Task Scheduler

## Overview
The Intelligent Task Scheduler is a smart scheduling system designed to optimize task management by considering deadlines, priorities, estimated effort, and dependencies. It provides a modular architecture that allows for easy extension and integration of advanced algorithms in the future.

## Features
- **Task Ingestion & Validation**: Load tasks from JSON or CSV files with validation for required fields.
- **Priority Scoring**: Compute a numeric score for tasks based on urgency, priority level, and effort penalty.
- **Scheduling Engine**: Utilize OR-Tools CP-SAT or a greedy fallback for task scheduling, respecting deadlines and dependencies.
- **Human-Centric Tweaks**: Adjust task scheduling based on user preferences and task types.
- **Output Formats**: Generate console tables, JSON files, and ICS calendar files for scheduled tasks.

## Project Structure
```
intelligent-task-scheduler
├── scheduler
│   ├── __init__.py
│   ├── task.py
│   ├── loader.py
│   ├── scorer.py
│   ├── engine.py
│   ├── calendar_utils.py
│   └── formatter.py
├── cli.py
├── requirements.txt
├── sample_tasks.json
├── tests
│   ├── __init__.py
│   └── test_engine.py
└── README.md
```

## Installation
To set up the project, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd intelligent-task-scheduler
pip install -r requirements.txt
```

## Usage
You can run the scheduling system from the command line. Use the following command to load tasks from a specified file and generate a schedule:

```bash
python cli.py --input sample_tasks.json
```

### CLI Options
- `--input FILE`: Specify the input file (JSON or CSV) containing tasks.
- `--gantt`: Generate a Gantt-style ASCII chart of the schedule.
- Additional flags for tuning scoring weights and working hours can be added.

## Testing
Unit tests are provided in the `tests` directory. You can run the tests using:

```bash
pytest tests/
```
