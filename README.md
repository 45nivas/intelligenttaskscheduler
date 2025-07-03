[![Streamlit App](https://img.shields.io/badge/🚀%20Live%20App-Click%20Here-success?style=for-the-badge)](https://intelligenttaskscheduler-gyfj8zaxmbwj9v3k9qw2cj.streamlit.app/)

# 🧠 Intelligent Task Scheduler

A smart and human-centered scheduling system to optimize daily task planning based on deadlines, priorities, effort, and human productivity patterns.  
Built with modular Python and a beautiful Streamlit interface.

---

## 🔧 Features

- ✅ Greedy Scheduling Algorithm with deadline, priority & effort scoring
- 🧍 Human Productivity Aware: 9 AM–5 PM, lunch breaks, 5.5h/day cap
- 📊 Gantt-style timeline visualization (via Streamlit)
- 📋 Console / JSON / ICS outputs (via CLI)
- ⚙️ Extendable engine with dependency support (planned)

---

## 🖥️ Usage Options

### 1. Streamlit App (Web Interface)

#### 🔹 Install Requirements
```bash
pip install streamlit pandas altair
```

#### 🔹 Launch the App
```bash
streamlit run main.py
```

#### 🔹 Use the Sidebar Form
- Task Title
- Priority (`high`, `med`, `low`)
- Deadline & Earliest Start (e.g., `2024-07-05`)
- Estimated Hours (e.g., `2.0`)

📌 Click **"Generate Schedule"** to view a personalized task table and Gantt chart.

---

### 2. CLI Mode (Engine-Based)

#### 🔹 Run via Command Line
```bash
python engine.py --input sample_tasks.json
```

#### 🔹 CLI Options
- `--input FILE`: JSON or CSV task file  
- `--gantt`: Show ASCII Gantt chart  
- `--ics`: Export to .ics calendar file  
- `--weights`: Tune priority vs urgency impact  

---

## ⚙️ Scheduling Logic

**Score = Urgency + Priority Weight**

- Urgency = `30 - days_until_deadline`
- Priority Scores:  
  - `high = 30`  
  - `med = 20`  
  - `low = 10`  
- Tasks are sorted in descending score order.

---

## 👤 Human-Centered Rules

- Work Hours: **9:00 AM – 5:00 PM**
- Lunch Break: **12:00 PM – 1:00 PM**
- Max Effort/Day: **5.5 hours**
- Tasks are split smartly across breaks and days.

---

## ✅ Example

### Input (`sample_tasks.json`)
```json
[
  {
    "title": "Task A",
    "priority": "high",
    "deadline": "2024-07-05",
    "earliest_start": "2024-07-03",
    "estimated_hours": 2.5
  },
  {
    "title": "Task B",
    "priority": "med",
    "deadline": "2024-07-06",
    "earliest_start": "2024-07-04",
    "estimated_hours": 1.5
  }
]
```

### Output
- Task A is scheduled before Task B  
- Time blocks fit into work hours  
- Tasks split across lunch if needed  

---

## 📦 Project Structure
```
intelligent-task-scheduler/
├── streamlit.py               # Streamlit UI
├── engine.py             # CLI backend
├── sample_tasks.json     # Example input
├── requirements.txt
└── README.md
```

---

## 🔮 Future Enhancements

- ⛓️ Task dependency graph visualization  
- 🔁 Recurring task support  
- ⚡ Energy rhythm-based scheduling  
- 📅 Google Calendar integration  

---


