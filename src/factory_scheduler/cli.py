import argparse
import json

from .agents.decision_support import summarize
from .agents.rescheduling import compare_plans, propose_reschedule
from .ingestion import load_tasks_csv
from .scheduler import schedule


def _plan_to_dicts(plan):
    return [
        {
            "id": item.task.id,
            "machine": item.task.machine,
            "start_minute": item.start_minute,
            "end_minute": item.end_minute,
            "due_minute": item.task.due_minute,
            "priority": item.task.priority,
        }
        for item in plan
    ]


def main(argv=None):
    parser = argparse.ArgumentParser(description="Factory scheduling baseline prototype")
    parser.add_argument("csv_file", nargs="?", default=None, help="Path to approved task CSV")
    parser.add_argument(
        "--compare",
        nargs=2,
        metavar=("BASE_CSV", "CURRENT_CSV"),
        default=None,
        help="Compare base plan against current plan (proposal only, no ERP write-back)",
    )
    parser.add_argument("--json", dest="json_output", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args(argv)

    if args.compare is not None:
        old_plan = schedule(load_tasks_csv(args.compare[0]))
        new_plan = propose_reschedule(load_tasks_csv(args.compare[1]))
        comparison = compare_plans(old_plan, new_plan)
        if args.json_output:
            print(
                json.dumps(
                    {
                        "old_summary": summarize(old_plan),
                        "new_summary": summarize(new_plan),
                        "comparison": comparison,
                        "new_plan": _plan_to_dicts(new_plan),
                    },
                    indent=2,
                )
            )
            return
        for item in new_plan:
            print(f"{item.task.id}: {item.task.machine} [{item.start_minute}, {item.end_minute})")
        print(f"Added: {comparison['added']}")
        print(f"Removed: {comparison['removed']}")
        print(f"Makespan delta: {comparison['makespan_delta']}")
        print(f"Late delta: {comparison['late_delta']}")
        print(summarize(new_plan))
        return

    if args.csv_file is None:
        parser.error("csv_file is required unless --compare is given")
    plan = schedule(load_tasks_csv(args.csv_file))
    if args.json_output:
        print(json.dumps({"plan": _plan_to_dicts(plan), "summary": summarize(plan)}, indent=2))
        return
    for item in plan:
        print(f"{item.task.id}: {item.task.machine} [{item.start_minute}, {item.end_minute})")
    print(summarize(plan))


if __name__ == "__main__":
    main()
