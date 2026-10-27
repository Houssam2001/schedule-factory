# Dashboard (prototype stub spec — static, no auth, synthetic only)

Status: spec only. No implementation in this slice. No auth, no server,
no ERP write-back, no optimizer.

## What it is

A static **JSON-in / HTML-out** viewer for planner review. It renders one
`schedule()` + `summarize()` run as read-only cards, Gantt-style bars, and an
exact-records table. Local-only example (gitignored, do not commit):
`temp/schedule-view.html`.

## Viewer contract

### Input (JSON file, built from CLI output — no live polling)

```json
{
  "meta": {"source_csv": "data/sample_tasks.csv", "scenario": "baseline", "generated_utc": "2026-10-27T00:00:00Z"},
  "plan": [
    {"id": "JOB-002", "machine": "CNC-1", "start": 0, "end": 45, "due": 120, "late": false}
  ],
  "summary": {"tasks": 3, "late_tasks": 0, "makespan_minutes": 135, "total_late_minutes": 0, "utilization": {"CNC-1": 1.0, "CNC-2": 0.444}}
}
```

- `plan[]` mirrors `ScheduledTask(task, start, end)` from
  `src/factory_scheduler/scheduler.py:5` plus `due` and derived `late = end > due`.
- `summary` is byte-identical to
  `src/factory_scheduler/agents/decision_support.py:4 summarize()` keys.
- Time unit: minutes from a shared origin.

### Output (single self-contained HTML file, no JS fetch, no backend)

Cards (`tasks`, `late_tasks`, `makespan_minutes`, `total_late_minutes`,
per-machine `utilization`), per-machine bars (`[start,end)`, late in red),
exact-records table, plus the CLI command and source CSV name for traceability.

### Approval gate (human go / no-go, no auto write)

1. Planner opens the static HTML for baseline vs proposal (`docs/SCENARIOS.md`).
2. Planner compares `late_tasks`, `total_late_minutes`, `makespan_minutes`, `utilization`.
3. Planner records **go / no-go** outside the tool (manual ERP entry if go).
4. The viewer never writes to ERP, never mutates the CSV, never re-plans on its own.

## Explicitly out of scope

- Auth, roles, audit logs, multi-user sessions.
- ERP write-back, SQL sync, automatic dispatch.
- Optimizer / solver (OR-Tools etc.), precedence, shifts/calendars, setup times,
  downtime windows, material/workforce constraints.
- Live updates, websockets, polling, persistence, file upload.
- Real or customer data: synthetic `data/sample_tasks.csv`-derived inputs only.
- Any `src/` logic change: the dashboard is a read-only view over existing
  `schedule()` + `summarize()` outputs (stdlib only if a render script is added later).
