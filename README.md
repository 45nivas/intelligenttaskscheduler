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
# Smart Task Scheduler 🧠

A human-centered task scheduler built using Python and Streamlit. It automatically generates an optimal daily schedule for your tasks by considering:

* **Priority** (high / med / low)
* **Deadline**
* **Earliest Start**
* **Estimated Hours**
* Human productivity constraints (9 AM – 5 PM, 1 hour lunch, max \~5.5 hours/day)

---

## Features

* Simple web interface with task input form
* Gantt-style timeline chart and data table output
* Smart greedy scheduling logic based on urgency and effort
* Auto-handles work hours and lunch breaks

---

## Usage

### 1. Install requirements

```bash
pip install streamlit pandas altair
```

### 2. Run the app

```bash
streamlit run main.py
```

### 3. Add Tasks via Sidebar Form

Fields:

* **Task Title**: Name of the task
* **Priority**: Choose high, medium, or low
* **Deadline**: The last date by which task must finish
* **Can Start On**: Optional earliest allowed start date
* **Estimated Hours**: How long the task takes (0.5–8 hours)

### 4. Click "Generate Schedule"

* See your task schedule as a **table** and **timeline graph**.

---

## Scheduling Logic

### Total Score = Urgency + Priority Weight

* Urgency = `30 - days_until_deadline`
* Priority: high = 30, med = 20, low = 10
* Tasks with highest total score scheduled first

### Human Productivity Rules:

* Work day: **9 AM – 5 PM**
* **Lunch break**: 12 PM – 1 PM
* Max \~5.5 productive hours per day
* Tasks fragment intelligently around lunch

---

## Future Ideas

* Support task dependencies
* Support recurring tasks
* Personal energy curve modeling
* Export to Google Calendar or .ics

---

## Example

**Input Tasks:**

```json
[
  {"title": "Task 1", "priority": "high", "deadline": "2023-10-15", "earliest_start": "2023-10-14", "estimated_hours": 2.5},
  {"title": "Task 2", "priority": "med", "deadline": "2023-10-16", "earliest_start": "2023-10-15", "estimated_hours": 1.0}
]
```

**Output:**

* Task 1 scheduled before Task 2
* Shows exact start/end timestamps for each task
* Honors work day boundaries

---

Made with ❤️ using Python & Streamlit.
