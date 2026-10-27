# Factory Scheduling Workflows and Constraints

Status: baseline prototype. This doc defines what the planner can rely on today vs what is planned.
Time unit everywhere: `minutes from a shared origin` (see `src/factory_scheduler/ingestion.py:7`).

## Workflow A — Ingest, validate, schedule, review

| Step | Input | Output | Owner | Failure |
| --- | --- | --- | --- | --- |
| 1. Export | ERP/SQL/CSV orders | `id,machine,duration_minutes,due_minute,priority` CSV | ERP Integration (manual export today) | Missing columns, bad ints, duplicates |
| 2. Validate | CSV rows | `Task` list or `ValueError` | `src/factory_scheduler/ingestion.py:6`, `models.py:12` | Empty id/machine, `duration<=0`, `due<0`, `priority<=0`, duplicate ids |
| 3. Schedule | `Task` list | `ScheduledTask(task,start,end)` list | `src/factory_scheduler/scheduler.py:5` | Never fails today; ignores unmodeled constraints |
| 4. Evaluate | Plan | `tasks, late_tasks, makespan_minutes, total_late_minutes, utilization` | `agents/decision_support.py:4` | Empty plan returns zeros, no div-zero |
| 5. Review | CLI text + summary | Human decision (no auto write-back) | `cli.py:7` | Operator must approve before any ERP action |

## Workflow B — Monitor, propose, approve

| Step | Input | Output | Owner |
| --- | --- | --- | --- |
| 1. Snapshot | previous `Task[]`, current `Task[]` | new / removed / changed lists | `agents/monitoring.py:4,9,14` |
| 2. Propose | current `Task[]` | new plan via `schedule()` | `agents/rescheduling.py:5` (stub: re-runs baseline) |
| 3. Compare | old summary vs new summary | delta in lateness, makespan, utilization | Manual / `cli.py` today; `--compare` planned |
| 4. Approve | proposal + explanation | Human go / no-go, manual ERP entry | Planner (no auto write-back exists) |

`detect_new_tasks`: id in current, not in previous.
`detect_removed_tasks`: id in previous, not in current.
`detect_changed_tasks`: same id, any field differs (`Task` dataclass `!=`).

## Constraint catalog

| Constraint | Hard / Soft | Unit / Semantics | Example | Status today |
| --- | --- | --- | --- | --- |
| Machine capacity: one task at a time per machine | Hard | minutes, `[start,end)` non-overlapping per `machine` | CNC-1: JOB-002 `[0,45)` then JOB-001 `[45,135)` | Enforced in `scheduler.py:12-16` |
| Due date | Soft (reported) | `due_minute`; late if `end > due` | JOB-002 due 120, ends 45 = on time | Reported as `late_tasks`, `total_late_minutes`; not optimized |
| Priority ordering | Soft (heuristic) | int `priority`, higher first, tie-break `(due_minute, id)` | priority 3 JOB-002 before priority 2 JOB-001 | Heuristic sort only, not weighted optimization |
| ID uniqueness | Hard | exact `id` string after `strip()` | two `JOB-001` rows rejected | Enforced in `ingestion.py:14` |
| Field validity | Hard | non-empty id/machine, `duration>0`, `due>=0`, `priority>0` | `duration 0` rejected | Enforced in `models.py:12-16` |
| Precedence (A before B) | Hard (planned) | task id dependency | JOB-002 after JOB-001 | Not modeled; scheduler ignores order except by priority |
| Machine calendars / shifts | Hard (planned) | available windows per machine | night shift closed 22:00-06:00 | Not modeled; `available` starts at 0 in `scheduler.py:10` |
| Setup times | Hard (planned) | minutes between jobs on same machine | 15 min changeover | Not modeled |
| Downtime / breakdowns | Hard (planned) | unavailable `[start,end)` per machine | CNC-1 down `[50,120)` | Not modeled; use removed/changed detection as trigger only |
| Material / workforce | Hard (planned) | stock / headcount per window | 2 operators required | Not modeled |
| Cross-machine moves | Planned | reassign `machine` field | CNC-1 to CNC-2 | Not supported; `machine` fixed per `Task` |

## Walkthrough — `data/sample_tasks.csv`

Input:

```csv
JOB-001,CNC-1,90,180,2
JOB-002,CNC-1,45,120,3
JOB-003,CNC-2,60,150,1
```

Run: `PYTHONPATH=src python -m factory_scheduler.cli data/sample_tasks.csv`

Enforced: CNC-1 serializes by priority (JOB-002 `[0,45)`, JOB-001 `[45,135)`); CNC-2 runs alone (`[0,60)`); summary `{tasks:3, late:0, makespan:135, total_late:0, utilization:{CNC-1:1.0, CNC-2:0.444}}`.

Ignored today: if JOB-001 required JOB-002's material, or CNC-1 had a night break, or a 15 min setup applied, the plan would still show the same times. Do not use for real dispatch.

## Non-goals and privacy

No autonomous Llama actions, no ERP write-back, no dashboard auth/audit yet (see `docs/ARCHITECTURE.md:7`). LLM outputs must never override hard constraints; a future optimizer must enforce them independently. Use synthetic data only; never commit ERP exports, customer, employee, or credential data.
