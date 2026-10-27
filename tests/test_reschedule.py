from factory_scheduler.agents.rescheduling import compare_plans, propose_reschedule
from factory_scheduler.models import Task
from factory_scheduler.scheduler import schedule


def _base_tasks():
    return [
        Task("JOB-001", "CNC-1", 90, 180, priority=2),
        Task("JOB-002", "CNC-1", 45, 120, priority=3),
        Task("JOB-003", "CNC-2", 60, 150, priority=1),
    ]


def test_propose_matches_schedule():
    tasks = _base_tasks() + [Task("JOB-004", "CNC-1", 30, 100, priority=5)]
    assert propose_reschedule(tasks) == schedule(tasks)


def test_compare_detects_added_and_makespan_delta():
    old_plan = schedule(_base_tasks())
    new_plan = propose_reschedule(_base_tasks() + [Task("JOB-004", "CNC-1", 30, 100, priority=5)])
    assert compare_plans(old_plan, new_plan) == {
        "added": ["JOB-004"],
        "removed": [],
        "makespan_delta": 30,
        "late_delta": 0,
    }


def test_compare_detects_removed():
    old_plan = schedule(_base_tasks() + [Task("JOB-004", "CNC-1", 30, 100, priority=5)])
    new_plan = schedule(_base_tasks())
    comparison = compare_plans(old_plan, new_plan)
    assert comparison["added"] == []
    assert comparison["removed"] == ["JOB-004"]
    assert comparison["makespan_delta"] == -30
    assert comparison["late_delta"] == 0


def test_compare_late_delta():
    old_plan = schedule([Task("a", "M1", 30, 20)])
    new_plan = propose_reschedule([Task("a", "M1", 30, 20), Task("b", "M1", 20, 100, priority=5)])
    comparison = compare_plans(old_plan, new_plan)
    assert comparison["added"] == ["b"]
    assert comparison["removed"] == []
    assert comparison["makespan_delta"] == 20
    assert comparison["late_delta"] == 20


def test_compare_empty_plans():
    assert compare_plans([], []) == {"added": [], "removed": [], "makespan_delta": 0, "late_delta": 0}
