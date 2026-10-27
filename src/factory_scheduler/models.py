from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    id: str
    machine: str
    duration_minutes: int
    due_minute: int
    priority: int = 1

    def __post_init__(self):
        if not self.id or not self.machine:
            raise ValueError("Task id and machine must be non-empty")
        if self.duration_minutes <= 0 or self.due_minute < 0 or self.priority <= 0:
            raise ValueError("Invalid duration, due minute, or priority")


@dataclass(frozen=True)
class ScheduledTask:
    task: Task
    start_minute: int
    end_minute: int
