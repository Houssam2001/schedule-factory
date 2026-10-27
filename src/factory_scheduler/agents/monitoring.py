from ..models import Task


def detect_new_tasks(previous: list[Task], current: list[Task]) -> list[Task]:
    previous_ids = {task.id for task in previous}
    return [task for task in current if task.id not in previous_ids]
