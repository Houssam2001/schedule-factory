# Factory Scheduler — AI-Powered Multi-Agent Production Scheduling

> Project status: Concept and early development. Features below are planned, not yet implemented.

## Overview

Factory Scheduler is a proposed intelligent production planning and dynamic rescheduling platform for manufacturing environments. It explores using **Meta Llama models**, specialized AI agents, and constraint-based scheduling algorithms to respond to changing production conditions while keeping factory planners in control.

## The Problem

Factories face machine breakdowns, urgent orders, delayed operations, limited machine and workforce capacity, task dependencies, and disconnected ERP and task-management systems. Manual rescheduling can be slow and make downstream impacts difficult to understand.

## Proposed Solution

- Import and validate production orders, tasks, resources, dependencies, and due dates from ERP data (including SQL or CSV exports).
- Generate feasible production schedules using a constraint-aware optimization engine.
- Detect new tasks, downtime, and delays through monitoring workflows.
- Coordinate AI agents to analyze disruptions and recommend alternative schedules.
- Explain trade-offs and require planner approval before operational changes.
- Evaluate performance through lateness, resource utilization, scheduling stability, and replanning time.

## Proposed Agents

| Component | Responsibility |
| --- | --- |
| ERP Integration Agent | Ingest and normalize manufacturing data |
| Monitoring Agent | Detect new tasks and disruptions |
| Planning Agent | Analyze priorities, dependencies, and objectives |
| Scheduling Engine | Produce and validate constraint-feasible schedules |
| Rescheduling Agent | Evaluate alternative schedules |
| Decision Support Agent | Explain recommendations and support human approval |

## High-Level Architecture

```text
ERP / SQL / CSV exports
         |
         v
Data ingestion & validation
         |
         v
Canonical production task model
         |
         v
Monitoring + Planning Agents
         |
         v
Constraint-Based Scheduling Engine
         |
         v
Rescheduling + Decision Support Agents
         |
         v
Planner Approval & Scheduling Dashboard
```

## Technology Direction

Candidate technologies include **Python**, **Meta Llama**, **SQL/CSV data pipelines**, **OR-Tools or another constraint solver**, and a web-based production scheduling dashboard. The final stack is not yet selected. AI agents will support reasoning and explanations; hard production constraints should be enforced by the scheduling engine.

## Development Roadmap

- [ ] Document factory scheduling workflows and constraints.
- [ ] Build an ERP data ingestion and validation pipeline.
- [ ] Implement a baseline production scheduler.
- [ ] Detect newly added tasks and production disruptions.
- [ ] Develop monitoring, planning, and rescheduling agents.
- [ ] Create a dashboard with planner review and approval.
- [ ] Test against representative manufacturing scenarios and baseline schedules.

## Example Scenario

When an urgent production order arrives while a machine is unavailable, the system would detect the change, calculate feasible alternatives, explain their impacts, and present a proposed reschedule for human approval.

## Privacy and Safety

Use synthetic or properly anonymized sample data. Do not commit proprietary ERP exports, customer information, employee records, commercial details, credentials, or other confidential factory data. Production integration should include access controls, audit logs, validation, and human oversight.

## Vision

**From static task lists to intelligent, adaptive, human-supervised factory scheduling.**

## License

No license has been selected yet.
