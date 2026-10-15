# Current Repository State

Reconciled 2026-10-15. Implementation baseline: `cf6c9b4` (V1 cleanup), followed
by the V2.1 working changes below. Approved implementation endpoint: V2.
V2.1 has locally tested S3 transfer code and policy templates; real AWS storage
and access verification await the learner's first AWS account. It is IN PROGRESS.

## What is complete

**V0 and V1 are implemented and verified within their documented local scope.**
The V1 exit criterion is demonstrated for bounded authentic historical trades:

```text
raw archive → replay → Kafka → Spark / Delta Bronze
→ Silver accepted trades + every-delivery audit
→ event-time minutes and Parquet export → dbt / DuckDB → analytical query
```

Four retained source messages contain 104 distinct trades. Each of two independent
executions replays two passes: 208 deliveries = 104 accepted + 104 duplicate +
0 rejected. Source values, minute totals and sorted analytical results agree.
The original capture reported five messages; only four trade-bearing messages
survive in its observation artifact. No fifth is reconstructed.

## Current capabilities and boundaries

| Component | Implemented behaviour | Boundary |
| --- | --- | --- |
| V0 baseline | Synthetic producer/consumer, typed Parquet, schema flag, SQL and compatible checkpoint restart | Counts deliveries; no business deduplication |
| Collector / publishers | Bounded trade observation/reconnect, separate versioned keyed trade/L2 envelopes, acknowledged sends | Reconnect does not recover missed events |
| Raw / replay | Create-only raw files, exact text/receipt provenance, sorted paced repeats, explicit replay markers/topics | Not enforced immutable retention or new unique event volume |
| Bronze | Kafka bytes/coordinates + parsed envelope fields, Delta append with checkpoint | One row per delivery, no domain validation/deduplication |
| Silver | Decimal/time/domain validation, stable trade key, identical duplicates, conflict rejection, trades/audit rebuild | Bounded full rebuild; two separate table commits |
| Minutes | UTC event-time minute counts/decimal quantities, includes older arrivals on rebuild | No streaming watermark/finality |
| Reconciliation | Archive content/multiplicity → Bronze → audit → accepted trades | Selected frozen trade replay, not source completeness/global reconciliation |
| dbt / DuckDB | Parquet source, staging view, product dimension, trade fact; six data tests | Local, snapshot-based; no Snowflake or incremental models |
| L2 model | In-memory snapshot/update transitions, deletion, best bid/ask | Synthetic supplied history; not integrated with the trade pipeline/live feed |
| Airflow | Inspect → replay DAG, dependency/retry tests; standalone Compose service | Separate bounded lesson, not full-path orchestration |
| Compose | Kafka, tooling and optional Airflow; host/container listeners and named state | Single broker, local Spark, no HA/production guarantee |
| S3 landing (V2.1 in progress) | Bounded archive transfer, conditional PUT, exact readback, scoped policy templates | SDK request tests only; AWS account/policies/storage not yet verified |

## Current workflow and layout

Start with `README.md` and `docs/use.md`. `make build`, `make demo RUN=<new-name>`
and `make inspect RUN=<same-name>` provide the recommended container workflow;
`make test` runs the core, dbt and DAG checks in their own runtimes. Host virtual
environments are optional and have not been deleted. Requirements remain split
by actual runtime; redundant direct Py4J pin removed because pinned PySpark owns it.

- `tests/fixtures/v0/`: original four synthetic inputs, moved byte-for-byte from
  `data/v0/` so the writable data mount cannot hide them. Tests/reader use new paths.
- `tests/fixtures/v1_exit/`: frozen authentic workload and hashes, unchanged.
- `data/compose/runs/<name>/`: new demo output on the host; container path is
  `/workspace/data/runs/<name>/`. Each execution owns its checkpoint/tables/database.
- Root scripts and `spark/`: existing script conventions retained; short comments
  mark the main slice concepts. Twenty annotated scripts retain executable ASTs
  (excluding comments/docstrings); processing policies are unchanged.
- `inspect_run.py`: read-only Kafka samples and actual analytical query; rejects
  a non-PASS manifest rather than displaying partial tables as successful output.

The reset guide distinguishes a fresh isolated experiment, archiving generated
files, stopping services and destructive named-volume deletion. No existing data,
virtual environment, broker volume or historical evidence was reset during cleanup.
Deleting Kafka state leaves stored table snapshots behind; use a new demo afterward.

## Verification and evidence

Historical V1.16: final opt-in experiment 2 passed; native default suite 90 passed /
8 skipped, exit 0. Full scope/results: `docs/v1_exit.md`,
`docs/v1_exit_baseline.json`, dated `METRICS.md` sections. Historical Py4J shutdown
logging after the passing summary remains recorded. Tiny paced backlog timings
do not establish live freshness, sustained capacity or optimisation.

Cleanup verification (Docker image rebuilt successfully):

- `make demo RUN=tidy-verification-20261015`: PASS; two independent executions,
  each 208→104 accepted/104 duplicate/0 rejected; identical analytical hashes and
  source-aligned values/minute totals. No prior output replaced.
- `make inspect RUN=tidy-verification-20261015`: exit 0; three actual Kafka rows
  displayed; database query returns 104 rows/104 keys/1.24180961 BTC.
- Documented Bronze inspection CLI: exit 0; committed Delta schema, 208-delivery
  group and source/Kafka/processing provenance displayed.
- `make test`: core/Spark **87 passed, 10 skipped**; separate dbt **2 passed**;
  DAG checks **1 passed, 1 opt-in skip**; exit 0. Core skips include unavailable
  Airflow/dbt modules, host-only Compose check and explicit integration opt-ins.
- Isolated V0 producer/consumer smoke: 1 synthetic publication/read, then 0 after
  committed-offset resume. Relocated fixtures preserve original bytes.
- All three runtime `pip check` commands passed; transitive Py4J is 0.10.9.9.
- Existing-output retry refuses overwrite; prior PASS manifest unchanged.
- AST comparison preserves executable logic in 20 annotated scripts; archived
  state document preserves original bytes; new entry-point links resolve.

Local raw cleanup logs: `docs/verification/v1-tidy/` (ignored).
New runtime output: `data/compose/runs/tidy-verification-20261015/`.
This check adds 416 replay deliveries of the same historical 104 trade IDs and
one synthetic V0 delivery. No provider traffic or new performance claim.

## Learning history

`LEARNING_LOG.md` preserves the cumulative record. `docs/README.md` indexes every
V0/V1 lesson and the early `buildLog.md`/`learningLog.md`. The exact pre-cleanup
state narrative is retained in `docs/history/CURRENT_STATE_V1.md`; historical
claims there describe their dated verification, not the current recommended setup.
`METRICS.md` remains the evidence ledger. Original raw data, failed experiments,
V0 outputs/checkpoints, broker state and the V1.16 baseline remain intact.
`PROJECT_SPEC.md`, `TEACHING_STYLE.md` and `CHAT_HANDOVER.md` are unchanged.

## Next implementation slice

**Finish V2.1 — real AWS setup and verification**, after learner review. The user
has never used AWS and has no selected target. `docs/v2_s3_landing.md` explains
account/MFA, a private eu-west-2 bucket, scoped runtime identity, credential handling
and explicit Docker credential mounting. No account/resource/policy was created.

`s3_landing.py` copies existing JSON archive wrappers byte-for-byte under a chosen
prefix, preserving relative capture names. Each PUT uses `IfNoneMatch="*"`, then
GET compares exact bytes; output records key/size/SHA-256. Existing keys, SDK
errors and readback mismatch fail visibly. A partial batch or ambiguous PUT leaves
objects behind; there is no resume/rollback. `aws/` supplies scoped GetObject/
conditional PutObject grants plus bucket denies for unconditional writes, deletes
and insecure object transport. These are templates, not applied AWS controls.

Five local Stubber tests verify the request/error contract, not actual S3 or IAM.
The opt-in `tests/test_s3_landing_live.py` requires real readback, duplicate refusal
and denied unconditional overwrite/delete/list/out-of-prefix PUT using one fresh
synthetic probe. It has not run. A later four-file authentic upload/readback is
also required before marking V2.1 DONE. Boto3 1.40.50 is added to the core runtime;
the existing Make/Docker build path is retained. No Databricks or later slice work.

V2.1 verification: `make build` succeeded; `make test` exited 0 with core/Spark
**92 passed / 11 skipped**, dbt **2 passed**, DAG **1 passed / 1 opt-in skip**.
Focused native archive/replay/S3 checks: **15 passed / 1 real-AWS skip**.
CLI help, native `pip check`, both policy JSON parses and `git diff --check` pass.
First SDK cleanup failure and sandbox build denial logs are preserved alongside
successful runs in ignored `docs/verification/v2-1/`. No authentic fixture,
tracked V1 benchmark, provider/Kafka data or cloud resource was changed.
