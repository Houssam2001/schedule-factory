from ..models import ScheduledTask


def summarize(plan: list[ScheduledTask]) -> dict:
    makespan = max((item.end_minute for item in plan), default=0)
    busy: dict[str, int] = {}
    for item in plan:
        busy[item.task.machine] = busy.get(item.task.machine, 0) + (item.end_minute - item.start_minute)
    utilization = {machine: round(minutes / makespan, 3) if makespan else 0.0
                   for machine, minutes in busy.items()}
    return {"tasks": len(plan),
            "late_tasks": sum(item.end_minute > item.task.due_minute for item in plan),
            "makespan_minutes": makespan,
            "total_late_minutes": sum(max(0, item.end_minute - item.task.due_minute) for item in plan),
            "utilization": utilization}
