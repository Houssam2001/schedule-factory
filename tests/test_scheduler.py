from factory_scheduler.models import Task
from factory_scheduler.scheduler import schedule
from factory_scheduler.agents.monitoring import detect_changed_tasks, detect_new_tasks, detect_removed_tasks
from factory_scheduler.agents.decision_support import summarize


def test_no_machine_overlap():
    tasks = [Task("a", "M1", 30, 100), Task("b", "M1", 20, 100)]
    plan = schedule(tasks)
    assert plan[0].end_minute <= plan[1].start_minute


def test_new_tasks():
    a = Task("a", "M1", 30, 100)
    b = Task("b", "M2", 20, 100)
    assert detect_new_tasks([a], [a, b]) == [b]


def test_summary_reports_lateness_and_utilization():
    tasks = [Task("a", "M1", 30, 20), Task("b", "M1", 20, 100)]
    summary = summarize(schedule(tasks))
    assert summary["tasks"] == 2
    assert summary["late_tasks"] == 1
    assert summary["total_late_minutes"] == 10
    assert summary["makespan_minutes"] == 50
    assert summary["utilization"] == {"M1": 1.0}


def test_removed_and_changed_tasks():
    old = [Task("a", "M1", 30, 100), Task("b", "M1", 20, 100, priority=1)]
    new = [Task("a", "M1", 30, 100), Task("b", "M1", 20, 90, priority=2)]
    assert detect_removed_tasks(old, new) == []
    assert detect_removed_tasks(new, old) == []
    assert detect_removed_tasks(old, [old[0]]) == [old[1]]
    assert detect_changed_tasks(old, new) == [new[1]]
    assert detect_changed_tasks(old, old) == []
