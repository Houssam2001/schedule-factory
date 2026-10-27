from factory_scheduler.agents.planning import explain_order, prioritize
from factory_scheduler.models import Task


def test_prioritize_orders_by_priority_then_due():
    tasks = [
        Task("JOB-001", "CNC-1", 90, 180, priority=2),
        Task("JOB-002", "CNC-1", 45, 120, priority=3),
        Task("JOB-003", "CNC-2", 60, 150, priority=1),
    ]
    assert [t.id for t in prioritize(tasks)] == ["JOB-002", "JOB-001", "JOB-003"]


def test_prioritize_tie_break_due_then_id():
    earlier = Task("b", "M1", 10, 50, priority=1)
    later = Task("a", "M1", 10, 100, priority=1)
    assert prioritize([later, earlier]) == [earlier, later]
    # Same priority and due -> lexicographic id decides.
    t1 = Task("b", "M1", 10, 100, priority=1)
    t2 = Task("a", "M1", 10, 100, priority=1)
    assert prioritize([t1, t2]) == [t2, t1]


def test_prioritize_empty_and_does_not_mutate():
    assert prioritize([]) == []
    tasks = [Task("b", "M1", 10, 100, priority=1), Task("a", "M1", 10, 100, priority=2)]
    snapshot = list(tasks)
    prioritize(tasks)
    assert tasks == snapshot


def test_explain_order_mentions_id_and_is_empty_safe():
    assert explain_order([]) == []
    tasks = [
        Task("JOB-001", "CNC-1", 90, 180, priority=2),
        Task("JOB-002", "CNC-1", 45, 120, priority=3),
    ]
    lines = explain_order(tasks)
    assert len(lines) == 2
    assert lines[0].startswith("JOB-002")
    assert "JOB-002" in lines[0] and "JOB-001" in lines[1]
    assert "priority 3" in lines[0] and "due 120" in lines[0]
