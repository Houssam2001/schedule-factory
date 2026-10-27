import argparse
from .ingestion import load_tasks_csv
from .scheduler import schedule
from .agents.decision_support import summarize


def main():
    parser = argparse.ArgumentParser(description="Factory scheduling baseline prototype")
    parser.add_argument("csv_file", help="Path to approved task CSV")
    args = parser.parse_args()
    plan = schedule(load_tasks_csv(args.csv_file))
    for item in plan:
        print(f"{item.task.id}: {item.task.machine} [{item.start_minute}, {item.end_minute})")
    print(summarize(plan))


if __name__ == "__main__":
    main()
