# Architecture (prototype)

CSV input -> validated Task model -> deterministic baseline scheduler -> monitoring/rescheduling agent stubs -> decision summary -> human review.

## Limitations

This baseline does not handle precedence, machine calendars, shifts, setup times, downtime, material constraints or actual ERP synchronization. The agent modules are Python interfaces, **not** autonomous or Meta Llama-connected agents. No production write-back exists. A future optimizer should enforce hard constraints independently of LLM outputs.

## Privacy

Use synthetic data. Do not commit company ERP exports, credentials, customer data or proprietary schedules.
