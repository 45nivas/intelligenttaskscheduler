import argparse
import json
import os
from scheduler.loader import load_tasks
from scheduler.engine import ScheduleEngine
from scheduler.formatter import print_schedule  # Updated import

def main():
    parser = argparse.ArgumentParser(description="Intelligent Task Scheduler")
    parser.add_argument('--input', type=str, required=True, help='Input file (JSON or CSV)')
    parser.add_argument('--gantt', action='store_true', help='Display Gantt-style chart')
    
    # Add flags for tunable constants
    parser.add_argument('--weight-urgency', type=float, default=1.0, help='Weight for urgency in scoring')
    parser.add_argument('--weight-priority', type=float, default=1.0, help='Weight for priority in scoring')
    parser.add_argument('--weight-effort', type=float, default=1.0, help='Weight for effort penalty in scoring')
    
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: The input file '{args.input}' does not exist.")
        return

    tasks = load_tasks(args.input)

    engine = ScheduleEngine(
        weight_urgency=args.weight_urgency,
        weight_priority=args.weight_priority,
        weight_effort=args.weight_effort
    )

    schedule = engine.schedule(tasks)

    if args.gantt:
        print("Gantt Chart:")
        # TODO: Implement Gantt chart display logic
    else:
        print_schedule(schedule)  # Updated usage

    with open('schedule.json', 'w') as f:
        json.dump(schedule, f, indent=4)

if __name__ == "__main__":
    main()