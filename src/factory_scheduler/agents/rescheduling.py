from ..models import ScheduledTask, Task
from ..scheduler import schedule
from .decision_support import summarize
from .monitoring import detect_new_tasks, detect_removed_tasks


def propose_reschedule(tasks: list[Task]) -> list[ScheduledTask]:
    """Generate a proposal only; do not write changes to an ERP."""
    return schedule(tasks)


def compare_plans(old_plan: list[ScheduledTask], new_plan: list[ScheduledTask]) -> dict:
    """Pure diff of two plans: ID adds/removes via monitoring plus summary deltas.

    late_delta is defined as new total_late_minutes minus old total_late_minutes.
    No I/O, no ERP write-back.
    """
    old_tasks = [item.task for item in old_plan]
    new_tasks = [item.task for item in new_plan]
    old_summary = summarize(old_plan)
    new_summary = summarize(new_plan)
    return {
        "added": [task.id for task in detect_new_tasks(old_tasks, new_tasks)],
        "removed": [task.id for task in detect_removed_tasks(old_tasks, new_tasks)],
        "makespan_delta": new_summary["makespan_minutes"] - old_summary["makespan_minutes"],
        "late_delta": new_summary["total_late_minutes"] - old_summary["total_late_minutes"],
    }
