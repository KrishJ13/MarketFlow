# Learning plan

The whole V0 is rebuilt and locally verified. CURRENT_STATE.md records the actual
checks; no later version has been implemented here. Learner review is next.

Current activity: V0 review plus user-authorised old-project cleanup. Independence
is verified; old files are archived/removed. The user requested a fresh local Git
history with one V0 starting commit and a theory recap. This is
maintenance, not a new version. V1 remains deferred until learner review.

| Version | Goal | Status |
| --- | --- | --- |
| V0 | Fake JSON → Kafka → Spark Structured Streaming → Parquet → SQL minute counts | Implemented/verified: 2 focused tests + 1 real pipeline/restart test; learner review pending |
| V1 | Add authentic capture and understand its journey through the local pipeline | Wait for V0 learner review; select one concept at a time |
| V2 | Learn managed storage/compute and warehouse modelling | Deferred until the corresponding local concepts are understood |

Next action after verification: explain V0's six small Python files before adding
anything. Future lessons introduce only the next missing concept; no V3+ work.
