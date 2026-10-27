from ..models import Task, ScheduledTask
from ..scheduler import schedule


def propose_reschedule(tasks: list[Task]) -> list[ScheduledTask]:
    """Generate a proposal only; do not write changes to an ERP."""
    return schedule(tasks)
