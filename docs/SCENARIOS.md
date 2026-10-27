# Representative Scenarios (prototype, synthetic only)

Status: static prototype. No auth, no ERP write-back, no optimizer.
Scheduler: `src/factory_scheduler/scheduler.py:5` sorts by `(-priority, due_minute, id)`,
one task at a time per machine, `available` starts at 0.
Metrics: `src/factory_scheduler/agents/decision_support.py:4 summarize()`.
Time unit: minutes from a shared origin (`src/factory_scheduler/ingestion.py:6`).

Input contract: CSV `id,machine,duration_minutes,due_minute,priority`
(`src/factory_scheduler/models.py:12`, `src/factory_scheduler/ingestion.py:6`).

---

## Scenario 1 — Baseline (`data/sample_tasks.csv`)

**Given** the committed synthetic input:

```csv
id,machine,duration_minutes,due_minute,priority
JOB-001,CNC-1,90,180,2
JOB-002,CNC-1,45,120,3
JOB-003,CNC-2,60,150,1
```

**When** the planner runs the baseline:

```sh
PYTHONPATH=src python -m factory_scheduler.cli data/sample_tasks.csv
```

**Then** the deterministic plan is:

- `JOB-002: CNC-1 [0,45)` (priority 3 first on CNC-1)
- `JOB-001: CNC-1 [45,135)` (priority 2 second on CNC-1)
- `JOB-003: CNC-2 [0,60)` (alone on CNC-2)

Expected summary (exact `summarize()` output):

```text
{'tasks': 3, 'late_tasks': 0, 'makespan_minutes': 135, 'total_late_minutes': 0, 'utilization': {'CNC-1': 1.0, 'CNC-2': 0.444}}
```

- `makespan_minutes = 135`
- `late_tasks = 0`, `total_late_minutes = 0`
- `utilization = {CNC-1: 1.0, CNC-2: 0.444}` (busy 135 / 135; busy 60 / 135)

---

## Scenario 2 — Urgent order `JOB-004` (new-task arrival)

**Given** baseline plus one urgent synthetic order:

```csv
JOB-004,CNC-1,30,100,5
```

i.e. `Task("JOB-004", "CNC-1", 30, 100, priority=5)` — highest priority, tight due.

**When** the planner builds the proposal in a gitignored temp copy and runs it:

```sh
cp data/sample_tasks.csv /tmp/scenario-urgent.csv
printf 'JOB-004,CNC-1,30,100,5\n' >> /tmp/scenario-urgent.csv
PYTHONPATH=src python -m factory_scheduler.cli /tmp/scenario-urgent.csv
```

(` /tmp/*.csv` is ephemeral preview data. Never commit it. Synthetic only.)

**Then** the plan is (priority order 5, 3, 2, 1):

- `JOB-004: CNC-1 [0,30)`
- `JOB-002: CNC-1 [30,75)`
- `JOB-001: CNC-1 [75,165)`
- `JOB-003: CNC-2 [0,60)`

Expected summary:

```text
{'tasks': 4, 'late_tasks': 0, 'makespan_minutes': 165, 'total_late_minutes': 0, 'utilization': {'CNC-1': 1.0, 'CNC-2': 0.364}}
```

- `makespan_minutes = 165` (baseline 135 + 30 urgent minutes on bottleneck CNC-1)
- `late_tasks = 0`, `total_late_minutes = 0` (urgent order is absorbed; nothing goes late)
- `utilization = {CNC-1: 1.0, CNC-2: 0.364}` (CNC-1 busy 165 / 165; CNC-2 busy 60 / 165)
- Planner read: +30 min makespan vs baseline, no lateness cost. Go/no-go is about
  whether +30 min on CNC-1 is acceptable, per `docs/WORKFLOWS.md` Workflow B.

---

## Scenario 3 — Delay edit: `JOB-001` due `180 -> 60` (changed-task trigger)

**Given** baseline with one field edited: `JOB-001.due_minute` `180 -> 60`
(same id, any field differs = `detect_changed_tasks`, `docs/WORKFLOWS.md` Workflow B).
All durations/priorities unchanged.

**When** the planner builds the edited temp copy and runs it:

```sh
cat > /tmp/scenario-delay.csv <<'EOF'
id,machine,duration_minutes,due_minute,priority
JOB-001,CNC-1,90,60,2
JOB-002,CNC-1,45,120,3
JOB-003,CNC-2,60,150,1
EOF
PYTHONPATH=src python -m factory_scheduler.cli /tmp/scenario-delay.csv
```

**Then** times are identical to baseline (priority order unchanged), but `JOB-001`
is now late:

- `JOB-002: CNC-1 [0,45)` — on time (45 <= 120)
- `JOB-001: CNC-1 [45,135)` — late (135 > 60, late by 75)
- `JOB-003: CNC-2 [0,60)` — on time (60 <= 150)

Expected summary:

```text
{'tasks': 3, 'late_tasks': 1, 'makespan_minutes': 135, 'total_late_minutes': 75, 'utilization': {'CNC-1': 1.0, 'CNC-2': 0.444}}
```

- `makespan_minutes = 135` (unchanged)
- `late_tasks = 1`, `total_late_minutes = 75`
- `utilization = {CNC-1: 1.0, CNC-2: 0.444}` (unchanged)
- Planner read: the due-date pull-in converts a feasible plan into a 1-job /
  75-min late plan with no capacity change. Options (re-prioritize, split,
  overtime) are future work; today the dashboard only surfaces the trade-off
  for human approval. Not modeled: precedence, shifts, setups, downtime
  (`docs/ARCHITECTURE.md:7`).
