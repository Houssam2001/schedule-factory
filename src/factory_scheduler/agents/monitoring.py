from ..models import Task


def detect_new_tasks(previous: list[Task], current: list[Task]) -> list[Task]:
    previous_ids = {task.id for task in previous}
    return [task for task in current if task.id not in previous_ids]


def detect_removed_tasks(previous: list[Task], current: list[Task]) -> list[Task]:
    current_ids = {task.id for task in current}
    return [task for task in previous if task.id not in current_ids]


def detect_changed_tasks(previous: list[Task], current: list[Task]) -> list[Task]:
    previous_by_id = {task.id: task for task in previous}
    return [task for task in current if task.id in previous_by_id and task != previous_by_id[task.id]]
