import csv
from pathlib import Path
from .models import Task


def load_tasks_csv(path: str | Path) -> list[Task]:
    """Load a synthetic or approved CSV export. Time values are minutes from a shared origin."""
    with open(path, newline="", encoding="utf-8") as handle:
        rows = csv.DictReader(handle)
        tasks = [Task(id=row["id"].strip(), machine=row["machine"].strip(),
                      duration_minutes=int(row["duration_minutes"]),
                      due_minute=int(row["due_minute"]),
                      priority=int(row.get("priority") or 1)) for row in rows]
    if len({task.id for task in tasks}) != len(tasks):
        raise ValueError("Duplicate task IDs")
    return tasks
