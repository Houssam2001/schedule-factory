from pathlib import Path

from factory_scheduler.agents.decision_support import summarize
from factory_scheduler.ingestion import load_tasks_csv
from factory_scheduler.models import Task
from factory_scheduler.scheduler import schedule

SAMPLE = Path(__file__).resolve().parents[1] / "data" / "sample_tasks.csv"


def _by_id(plan):
    return {item.task.id: item for item in plan}


def test_baseline_sample_tasks():
    plan = schedule(load_tasks_csv(SAMPLE))
    by_id = _by_id(plan)
    assert (by_id["JOB-002"].start_minute, by_id["JOB-002"].end_minute) == (0, 45)
    assert (by_id["JOB-001"].start_minute, by_id["JOB-001"].end_minute) == (45, 135)
    assert (by_id["JOB-003"].start_minute, by_id["JOB-003"].end_minute) == (0, 60)
    assert summarize(plan) == {
        "tasks": 3,
        "late_tasks": 0,
        "makespan_minutes": 135,
        "total_late_minutes": 0,
        "utilization": {"CNC-1": 1.0, "CNC-2": 0.444},
    }


def test_urgent_order_job004():
    tasks = load_tasks_csv(SAMPLE) + [Task("JOB-004", "CNC-1", 30, 100, priority=5)]
    plan = schedule(tasks)
    by_id = _by_id(plan)
    assert (by_id["JOB-004"].start_minute, by_id["JOB-004"].end_minute) == (0, 30)
    assert (by_id["JOB-002"].start_minute, by_id["JOB-002"].end_minute) == (30, 75)
    assert (by_id["JOB-001"].start_minute, by_id["JOB-001"].end_minute) == (75, 165)
    assert (by_id["JOB-003"].start_minute, by_id["JOB-003"].end_minute) == (0, 60)
    assert summarize(plan) == {
        "tasks": 4,
        "late_tasks": 0,
        "makespan_minutes": 165,
        "total_late_minutes": 0,
        "utilization": {"CNC-1": 1.0, "CNC-2": 0.364},
    }


def test_delay_edit_due_180_to_60():
    tasks = [
        Task(t.id, t.machine, t.duration_minutes, 60 if t.id == "JOB-001" else t.due_minute, t.priority)
        for t in load_tasks_csv(SAMPLE)
    ]
    plan = schedule(tasks)
    by_id = _by_id(plan)
    assert (by_id["JOB-002"].start_minute, by_id["JOB-002"].end_minute) == (0, 45)
    assert (by_id["JOB-001"].start_minute, by_id["JOB-001"].end_minute) == (45, 135)
    assert (by_id["JOB-003"].start_minute, by_id["JOB-003"].end_minute) == (0, 60)
    assert summarize(plan) == {
        "tasks": 3,
        "late_tasks": 1,
        "makespan_minutes": 135,
        "total_late_minutes": 75,
        "utilization": {"CNC-1": 1.0, "CNC-2": 0.444},
    }
