from factory_scheduler.models import Task
from factory_scheduler.scheduler import schedule
from factory_scheduler.agents.monitoring import detect_new_tasks


def test_no_machine_overlap():
    tasks = [Task("a", "M1", 30, 100), Task("b", "M1", 20, 100)]
    plan = schedule(tasks)
    assert plan[0].end_minute <= plan[1].start_minute


def test_new_tasks():
    a = Task("a", "M1", 30, 100)
    b = Task("b", "M2", 20, 100)
    assert detect_new_tasks([a], [a, b]) == [b]
