"""Planning agent (prototype): pure priority-ordering helpers.

No I/O, no Llama connection, no ERP write-back. Ordering mirrors the
baseline scheduler sort key ``(-priority, due_minute, id)`` so the
explanation matches actual schedule order. See
``src/factory_scheduler/scheduler.py:12`` and ``docs/WORKFLOWS.md:35``.
"""

from ..models import Task


def prioritize(tasks: list[Task]) -> list[Task]:
    """Return tasks ordered by ``(-priority, due_minute, id)``.

    Pure function: does not mutate the input list.
    """
    return sorted(tasks, key=lambda t: (-t.priority, t.due_minute, t.id))


def explain_order(tasks: list[Task]) -> list[str]:
    """Return one human-readable line per task in priority order.

    Example: ``"JOB-002 first: priority 3, due 120"``.
    """
    ordered = prioritize(tasks)
    ordinals = {1: "first", 2: "second", 3: "third"}
    lines = []
    for rank, task in enumerate(ordered, start=1):
        position = ordinals.get(rank, f"#{rank}")
        lines.append(
            f"{task.id} {position}: priority {task.priority}, due {task.due_minute}"
        )
    return lines
