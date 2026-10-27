from ..models import ScheduledTask


def summarize(plan: list[ScheduledTask]) -> dict[str, int]:
    return {"tasks": len(plan),
            "late_tasks": sum(item.end_minute > item.task.due_minute for item in plan),
            "makespan_minutes": max((item.end_minute for item in plan), default=0)}
