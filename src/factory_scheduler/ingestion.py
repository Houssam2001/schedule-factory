import csv
from pathlib import Path

from .models import Task


_REQUIRED_COLUMNS = ("id", "machine", "duration_minutes", "due_minute")


def _parse_int(raw: object, *, row_num: int, column: str) -> int:
    text = "" if raw is None else str(raw).strip()
    try:
        return int(text)
    except (TypeError, ValueError):
        raise ValueError(f"row {row_num}: invalid integer for {column!r}: {text!r}") from None


def load_tasks_csv(path: str | Path) -> list[Task]:
    """Load a synthetic or approved CSV export. Time values are minutes from a shared origin."""
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("empty CSV: no header row")
        normalized_fields = [(h or "").strip() for h in reader.fieldnames]
        missing = [c for c in _REQUIRED_COLUMNS if c not in normalized_fields]
        if missing:
            raise ValueError(f"missing required columns: {', '.join(missing)}")
        tasks: list[Task] = []
        seen: dict[str, int] = {}
        for row_num, raw_row in enumerate(reader, start=2):
            row = {((k or "").strip()): v for k, v in raw_row.items() if k is not None}
            if all((v is None or str(v).strip() == "") for v in row.values()):
                continue
            task_id = "" if row.get("id") is None else str(row.get("id")).strip()
            machine = "" if row.get("machine") is None else str(row.get("machine")).strip()
            duration = _parse_int(row.get("duration_minutes"), row_num=row_num, column="duration_minutes")
            due = _parse_int(row.get("due_minute"), row_num=row_num, column="due_minute")
            priority_raw = row.get("priority")
            priority = 1 if priority_raw is None or str(priority_raw).strip() == "" else _parse_int(
                priority_raw, row_num=row_num, column="priority"
            )
            try:
                task = Task(
                    id=task_id,
                    machine=machine,
                    duration_minutes=duration,
                    due_minute=due,
                    priority=priority,
                )
            except ValueError as exc:
                raise ValueError(f"row {row_num}: {exc}") from None
            if task.id in seen:
                raise ValueError(
                    f"Duplicate task IDs: {task.id!r} (rows {seen[task.id]} and {row_num})"
                )
            seen[task.id] = row_num
            tasks.append(task)
        if not tasks:
            raise ValueError("empty CSV: no task rows")
        return tasks
