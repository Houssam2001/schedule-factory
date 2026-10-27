from collections import defaultdict
from .models import Task, ScheduledTask


def schedule(tasks: list[Task]) -> list[ScheduledTask]:
    """Simple deterministic baseline: one task at a time per machine.

    Not an optimizer: ignores shifts, precedence, setup times, material and downtime.
    """
    available = defaultdict(int)
    result = []
    for task in sorted(tasks, key=lambda t: (-t.priority, t.due_minute, t.id)):
        start = available[task.machine]
        end = start + task.duration_minutes
        result.append(ScheduledTask(task, start, end))
        available[task.machine] = end
    return result
