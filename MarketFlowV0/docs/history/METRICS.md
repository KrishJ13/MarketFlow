# Metrics and CV Evidence Ledger

Audit date: 2026-10-14. Revision: `441ab95cb3314468cecfd2c293936f1a63d2984b`.

## Evidence rules

No performance claim without preserved workload, environment/configuration and raw output. Preserve baselines. Distinguish synthetic records, authentic unique events and replay deliveries. Local correctness observations do not establish production capacity. Never benchmark Coinbase; use archived/local replay.

## Claims

| ID | Candidate claim | Status | Evidence / limitation |
| --- | --- | --- | --- |
| MF-001 | Full Kafka/Spark/Databricks/Delta/Airflow/Snowflake/dbt platform | NOT MEASURED / not implemented in full | Local Kafka/PySpark/Parquet/SQL, archive/replay and Delta Bronze now exist; bounded Silver validation/deduplication and event-time minute aggregation now exist; managed/cloud and warehouse path remain absent. Qualitative description must be limited to those components. |
| MF-002 | Sustained events/s and p95 freshness across partitions | NOT MEASURED | V1.16 now freezes a workload and measures paced bounded backlog replay/drain and publication-to-processing delay; these are not sustained capacity or source freshness. |
| MF-003 | Spark backfill optimisation | NOT MEASURED | No before/after workload or profiling evidence. |
| MF-004 | Snowflake/dbt query or build improvement | NOT MEASURED | Snowflake absent; local dbt/DuckDB now builds, with no comparative performance measurements. |
| MF-005 | Idempotent replay / loss-free recovery | NOT MEASURED | Bounded V0-G same-query restart/coordinate reconciliation is recorded; V1.16 verifies equivalent fresh bounded replays with logical duplicate handling, but no incremental idempotency, abrupt-crash injection or production loss-free recovery evidence. |
| MF-006 | PostgreSQL/Debezium CDC | NOT MEASURED / absent | Outside current V2 scope. |

## Required measurements remaining

V1.16 now measures the retained authentic workload (104 unique trade keys), raw/
Bronze/Silver/replay accounting, bounded paced replay/drain wall rates, selected
stage wall durations and publication-attempt→Bronze-processing p50/p95. Preserved
Spark progress includes micro-batch diagnostics. See the dated baseline below.

Still **NOT MEASURED**: sustained ingress/processing capacity; source-to-query
freshness and p99/SLOs; consumer lag baseline; Spark task/shuffle profiling;
Snowflake load/query time; analytical query latency; comparative optimisation;
backfill capacity and compute/cloud-cost efficiency. Stage wall times and Spark
progress diagnostics must not be promoted to those broader claims.

## Audit observation AUDIT-2026-10-14 — correctness only

Question: can the existing bounded SQL reader query the already stored local dataset?

Environment observed: macOS 26.6.2/aarch64; Python 3.13.7; Java 21.0.12.1; PySpark 4.2.0; local driver execution. No cluster/CPU/RAM benchmark manifest was collected. Kafka container uses `apache/kafka:latest`; actual server version/digest not verified. Topic describe reports one partition and replication factor one.

Workload: four tracked **fake** fixture definitions; existing ignored Parquet includes historical delivery rows. Number of previous publish/replay runs and original run configuration are unknown. No authentic source capture was audited and no messages were published during this audit.

Executed command:

```sh
source .venv/bin/activate
spark-submit spark/v0/query_trades.py
```

Result: exit 0. Raw SQL result excerpt preserved here:

```text
+----------+-------------------+-----------+
|product_id|minute             |trade_count|
+----------+-------------------+-----------+
|BTC-USD   |2026-09-28 12:00:00|4          |
|ETH-USD   |2026-09-28 12:01:00|2          |
|ETH-USD   |2026-09-28 12:04:00|1          |
|BTC-USD   |2026-09-28 12:05:00|4          |
+----------+-------------------+-----------+
```

Interpretation: SQL returned 11 valid **stored delivery rows**, not 11 authentic or unique trades. There is no logical deduplication in the query. This result establishes current stored-data queryability, not a freshly verified end-to-end path or scale result.

Additional raw correctness excerpts:

```text
Event type: trade
Product Id: BTC-USD
Trade Id: T001

PartitionCount: 1    ReplicationFactor: 1
Partition: 0    Leader: 1    Replicas: 1    Isr: 1

synthetic flatten: [{'trade_id': '100'}, {'trade_id': '101'}, {'trade_id': '102'}]
other channel: []
malformed probe input: TypeError 'NoneType' object is not iterable
malformed probe input: TypeError 'NoneType' object is not iterable

/Users/krish/Projects/MarketFlow/.venv/bin/python: No module named pytest
```

Evidence locations: this committed-text result excerpt; `docs/learningLog.md` (learner-reported prior restart observation); machine-local ignored `data/v0/output/trades` and `data/v0/checkpoints/trades` (not portable evidence). Full Spark runtime log is not archived as a benchmark. No benchmark was performed, no baseline changed, and no performance claim is unlocked.

## V0-F verification — 2026-10-14

Correctness evidence only: eight unittest tests passed on local Spark 4.2.0 / Python 3.13.7 / Java 21, using synthetic checked-in fixtures and deterministic malformed mutations. Command: `.venv/bin/python -B -m unittest discover -s tests -v`. Raw output: `docs/verification/v0-f-unittest.log` (includes expected cast error logs). No broker/source traffic or persisted dataset changes. The sandbox attempt could not start the JVM; approved local execution passed.

Tests characterize existing outcomes, including strict-cast exceptions and nullable flags; they do not establish safe poison-message handling or full V0 completion. Test elapsed time is not a pipeline-performance measurement. All performance/CV metrics remain NOT MEASURED.

## V0-F pytest conversion — 2026-10-14

At user request, the same eight characterization groups now use pytest fixtures, plain assertions, `pytest.raises` and parameterization: 19 collected cases passed. Command: `.venv/bin/python -B -m pytest -v -p no:cacheprovider`. Pytest 9.1.1 / Python 3.13.7; same local Spark 4.2.0 and synthetic workload. Raw evidence: `docs/verification/v0-f-pytest.log`; the prior unittest log is preserved. The count increased because parameterized subcases are reported separately, not because production functionality expanded. No performance claim or baseline dataset changed.

## V0-F1 invalid-row correction — 2026-10-14

Revision/environment: working tree based on `32126cd`; Python 3.13.7, pytest 9.1.1, local Spark 4.2.0 and Java 21. Synthetic fixture mutations only; no source/provider or Kafka traffic, no existing Parquet/checkpoint changes.

Command: `.venv/bin/python -B -m pytest -v -p no:cacheprovider`.
Before changing the transformation, the new safe-outcome expectations reproduced **15 failures / 25 passes**. After tolerant typing and Boolean validation, **40 cases passed** under both ANSI settings. The six-delivery mixed batch retained all rows and coordinates, with two valid and four invalid flags, including repeated delivery of the same valid event. These are fixture correctness counts, not authentic event volume or throughput.

Raw evidence: `docs/verification/v0-f1-before-pytest.log`, `docs/verification/v0-f1-after-pytest.log`. Earlier V0-F logs remain unchanged. Initial sandbox execution failed to start the JVM; approved outside-sandbox runs supplied the before/after evidence. No pipeline performance metrics were produced; all performance/CV claims remain NOT MEASURED.

## V0-G exit evidence — 2026-10-14

Correctness only: real local Kafka and Spark 4.2.0 / Python 3.13.7 / Java 21; existing Kafka container, fresh one-partition/replication-one topic. No public source/provider contact. Opt-in integration test: 1 passed. Raw successful/failed attempts, per-command logs and manifest: `docs/verification/v0-g/`.

Workload: five synthetic acknowledged deliveries (offsets 0–4): four valid and one malformed-price delivery. Valid deliveries represent three event IDs; trade_001 was deliberately published twice. Initial output 3 rows; backlog restart 5; no-new-data restart still 5. Consumer reads 3, then 0, then 2 after committed-offset resume. SQL counts valid deliveries as 2/1/1 across three minute/product groups. These are reconciliation assertions, not authentic unique volume, throughput or loss-free production claims. No latency/capacity/cost metric; all performance claims remain NOT MEASURED.

## End-of-session reconciliation — 2026-10-14

Evidence reviewed at implementation revision `21f2e93`; no new measurement or test run in this documentation-only handover. Final default suite: 40 passed, 1 opt-in skip (`docs/verification/v0-g/pytest-default-suite.log`); separate real-broker exit: 1 passed (`docs/verification/v0-g/pytest-exit.log`). Manifest confirms 5 synthetic deliveries = 4 valid + 1 invalid, with 3 valid event IDs. Restart row counts 3 → 5 → 5 and consumer reads 3 → 0 → 2 are correctness observations only.

No measured events/s, freshness distribution, consumer lag baseline, micro-batch performance, analytical latency, cloud cost or authentic unique volume was collected. Suite elapsed times are runner observations, not pipeline benchmarks. Historic failures remain evidence of fixes, not current failing tests. Scope remains V2; advanced optimisation/CDC claims remain unavailable.

## V1.1 bounded observation evidence — 2026-10-14

Correctness only, working tree based on `21f2e93`; Python 3.13.7,
websocket-client 1.9.2. One public BTC-USD market_trades subscription, bounded to
10 seconds / 5 messages; exit 0. Observed 5 source messages and 104 trade
observations across snapshot/update batches. Each observation retains exact raw
text and receipt time; readback confirms all BTC-USD and every trade appears in
its raw message. These are authentic observations, not a measured unique-event
count, replay deliveries, durable ingestion volume or provider benchmark.

Offline collector: 40 passed. Default regression: 80 passed, 1 opt-in skip.
Sandbox Spark startup/DNS failures retained; approved local runs passed.
Raw evidence/manifest: `docs/verification/v1-1/` (live stdout compressed losslessly;
manifest records uncompressed SHA-256). No throughput, latency, freshness, gap
recovery or capacity metric produced; performance/CV claims remain NOT MEASURED.

## V1.1 learning simplification — 2026-10-14

User-requested simplification replaces the 40-case collector suite with five
focused tests. Current results: **5 collector tests passed; full suite 45 passed,
1 opt-in skip**. Previous counts are historical, not current coverage.
Offline readback reproduced all 104 earlier authentic observations exactly;
no new source traffic, unique-volume or performance measurement.
Evidence: `docs/verification/v1-1/*-simplified.log`. Earlier evidence is preserved.

## V1.2 reconnect correctness — 2026-10-14

Working tree based on `bbed98e`. Deterministic scripted sockets only: 9 collector
tests passed (5 existing, 4 new); default suite 49 passed / 1 opt-in skip.
Tests force close/resubscribe, retry exhaustion, idle timeout and parse failure.
Evidence: `docs/verification/v1-2/`. No public provider traffic, authentic/replay
volume, gap-loss measurement or performance metrics. Reconnect is not loss-free
recovery evidence; MF-005 and performance claims remain NOT MEASURED.

## V1.3 trade transport correctness — 2026-10-14

Working tree based on `5293be8`, existing kafka-python 3.0.11 and local broker.
12 focused tests passed; default suite 52 passed / 2 opt-in skips. Separately
opted-in Kafka roundtrip: 1 passed. Fresh three-partition/replication-one topic;
one earlier authentic observation intentionally delivered twice with BTC-USD
key and stable ID. Consumer readback matched both acknowledgments (partition 0,
offsets 0/1), original trade/raw text and receipt/source time. Evidence and topic:
`docs/verification/v1-3/pytest-kafka.log`, `kafka-roundtrip.json`.

These are two replayed deliveries of one archived observation, not two unique
live trades. No new provider traffic, live end-to-end run, performance, capacity
or loss-free recovery measurement. Acknowledgment/IDs do not prove logical
deduplication; performance claims and MF-005 remain NOT MEASURED.

## V1.4 L2 transport correctness — 2026-10-14

Working tree based on `251f8fb`. 17 focused tests passed; default suite 57 passed /
3 opt-in skips. Separate L2 Kafka integration: 1 passed. Two synthetic snapshot/
update fixture messages (two price-level entries each), no authentic L2 capture
or provider traffic. Shared collector/parser/publisher and real consumer readback
matched product key, original batch/raw payload and acknowledgment coordinates
at partition 0 offsets 0/1 on a fresh three-partition/replication-one topic.
Evidence: `docs/verification/v1-4/pytest-kafka.log`, `kafka-roundtrip.json`.
No book-state correctness, continuity, loss-free recovery or performance claim;
no new throughput/latency/unique-volume metric. Existing claims remain NOT MEASURED.

## V1.5 raw archive correctness — 2026-10-15

Working tree based on `630907d`. Four real-filesystem archive tests passed;
default suite 61 passed / 3 opt-in skips. Checks cover exact source-text/receipt
readback, adding repeated captures without altering earlier bytes, overwrite
refusal, saving before parser failure and visible disk failure.

One earlier authentic source message was saved twice to new local files and
read back exactly. These are repeated local captures of historical input, not
new/unique authentic volume or a replay pipeline. Evidence:
`docs/verification/v1-5/` (including readback manifest with machine-local paths).
No provider traffic, performance, crash-durability or loss-free recovery metric;
existing performance/CV claims remain NOT MEASURED.

## V1.6 internal replay correctness — 2026-10-15

Working tree based on `4ee71e3`. Five focused tests passed; default suite 66 passed /
4 opt-in skips. Separate real Kafka replay test 1 passed: one unmodified earlier
authentic raw message containing one trade replayed for two passes. Summary:
1 archive message, 2 replayed messages, 2 acknowledged deliveries, same logical
ID/product key and original raw/receipt provenance, partition 0 offsets 0/1 on
an isolated three-partition replay topic. Original archive bytes unchanged.

No new provider traffic or unique authentic-volume measurement. Rate is a simple
per-message pause; the integration test replaces waits and measures no throughput.
Evidence: `docs/verification/v1-6/` (logs and run/topic/count manifest). No latency,
capacity, loss-free recovery or logical-deduplication claim; MF-005 and performance
claims remain NOT MEASURED. New deliveries are explicitly marked as replay.

## V1.7 Delta Bronze correctness — 2026-10-15

Base `4ee71e3` plus preserved V1.6 working tree. Spark 4.2.0 / Delta JVM 4.4.1
(Spark-4.2/Scala-2.13 artifact), Python 3.13.7 / Java 21. Two focused Spark/Delta
tests passed; default suite 68 passed / 5 opt-in skips. Separate real Kafka→Delta
check 1 passed: earlier authentic trade envelope delivered twice plus synthetic
malformed record, three acknowledged coordinates retained, row counts 2→3→3
across backlog/no-new-data compatible restart. Repeated logical ID remains two
rows. Actual CLI restart/reader passed after explicit package launch; first
failed attempts retained. Evidence: `docs/verification/v1-7/`.

These are local correctness counts, not unique authentic volume, throughput,
latency, benchmark or loss-free recovery figures. No provider traffic. MF-005
still lacks logical idempotency/abrupt-crash/production recovery evidence;
performance claims remain NOT MEASURED. Existing V0 baselines remain unchanged.

## V1.8 Silver correctness — 2026-10-15

Working tree based on `e08911b`; existing Spark 4.2.0 / Delta JVM 4.4.1. Four
focused tests passed; default suite 72 passed / 5 opt-in skips. Synthetic tests
cover typing/domain rejection, identical duplicates, conflicting valid values,
repeatable Delta overwrite/accounting, input binding and live/replay separation.
Actual CLI on earlier Bronze verification data exited 0: 3 deliveries = 1 accepted
+ 1 rejected + 1 duplicate (one earlier authentic trade delivered twice plus a
synthetic malformed record). No new provider traffic or unique-volume metric.

Evidence: `docs/verification/v1-8/` (currently Git-ignored/local). Initial focused
2 failed / 2 passed run retained; UTC instant assertion and malformed replay-mode
handling corrected before final runs. No performance metrics. This establishes
bounded snapshot logical duplicate handling, not incremental idempotency, atomic
multi-table publication or loss-free recovery; broader MF-005 remains unmeasured.

## V1.9 event-time minute correctness — 2026-10-15

Working tree based on `040dcdc`; existing Spark 4.2.0 / Delta JVM 4.4.1,
Python 3.13.7 / Java 21. Two focused real Spark/Delta tests passed; default
suite 74 passed / 5 opt-in skips. Synthetic examples verify UTC fixed-window
boundaries, out-of-order input, product/replay separation, decimal totals and
repeatable rebuild after an older arrival. Initial sandbox JVM-start failure
preserved; approved local execution passed.

Actual CLI exited 0 on the existing accepted Silver verification input: one
BTC-USD replay trade in 2026-10-14 10:26–10:27 UTC, total size 0.00000012 BTC.
This is a historical authentic observation marked replay, not new source volume.
No provider traffic, throughput, latency, streaming-lateness or capacity metric.
All performance claims remain NOT MEASURED. Evidence/paths: Git-ignored local
`docs/verification/v1-9/` (logs and `minute-run.json`); tracked policy and commands
in `docs/v1_trade_minutes.md`. Baselines and earlier evidence unchanged.

## V1.10 L2 state transitions — 2026-10-15

Working tree based on `a903a91`, Python 3.13.7 / pytest 9.1.1. Three focused
state-model tests passed; default suite 77 passed / 5 opt-in skips (existing
Spark/Delta environment unchanged). Local fixture demonstration exited 0:
snapshot bid 1.5/offer 2.0 → bid absent/offer 1.2 → same after immediate repeat.
Existing synthetic V1.4 fixtures/parser; no authentic L2 capture, provider/broker
traffic, throughput/latency measurement or complete-book claim. No CV/performance
claim unlocked. Local evidence: `docs/verification/v1-10/` (Git-ignored); tracked
commands/assumptions: `docs/v1_l2_state.md`. Prior baselines/evidence unchanged.

## V1.11 best bid/ask correctness — 2026-10-15

Working tree based on `aa95b30`, existing Python 3.13.7 / pytest 9.1.1 and
Spark/Delta environment. Six focused tests passed (3 new quotes + 3 existing
transitions); full suite 80 passed / 5 opt-in skips. Synthetic fixture/parser
demo exited 0: bid 60000/ask 60001 → bid None/ask 60001 after removal. Tests
establish supplied-state extrema and domain/missing-side policy, not complete or
fresh live quotes. No provider/broker traffic, authentic volume or performance
measurement; no CV/performance claim unlocked. Local Git-ignored evidence:
`docs/verification/v1-11/`; guide: `docs/v1_best_bid_ask.md`. Baselines preserved.

## V1.12 Airflow orchestration correctness — 2026-10-15

Baseline aa95b30 plus preserved V1.11 working changes. Airflow 3.3.2 / pytest
9.1.1, Python 3.13.7, separate constrained .venv-airflow and SQLite metadata.
Two Airflow tests passed (2 dependency deprecation warnings): real local DAG
success with one synthetic L2 archive snapshot delivered/read back at
marketflow.replay.l2.v1 partition 0 offset 0; missing archive inspection failed
after 2 attempts, replay upstream_failed with 0 attempts. Original archive bytes
unchanged. Project regression: 80 passed / 6 skips, including separate Airflow
module skip. First DagBag API mismatch corrected, failed log retained.

Only local DAG test execution verified; continuous scheduler/UI unverified.
No provider traffic, authentic L2/unique volume, scale or performance metric.
The one replay delivery is synthetic. Airflow success does not establish
exactly-once replay or downstream catchup. Evidence: Git-ignored local
`docs/verification/v1-12/` logs and run-summary.json; tracked runbook:
`docs/v1_airflow_replay.md`. Prior baselines and project dependencies preserved.

## V1.13 bounded reconciliation correctness — 2026-10-15

Baseline 90c95da; existing Python 3.13.7 / pytest 9.1.1 / Spark 4.2.0 / Delta
JVM 4.4.1. Three focused tests passed; full suite 84 passed / 6 skips, exit 0.
Post-summary Py4J logging to a closed stream is retained in the full raw log.
CLI exited 0: 1 synthetic archive message produces 3 expected/Bronze deliveries,
accounted as 1 accepted + 1 duplicate + 1 rejected. Equal-count delivery
substitution and changed Silver size raise as expected. These are fixture
correctness counts, not authentic unique volume, throughput or benchmark results.
No provider/Kafka traffic; no performance/CV claim unlocked. Evidence: local
Git-ignored `docs/verification/v1-13/` logs/run-summary.json; tracked command and
limitations: `docs/v1_reconciliation.md`. Earlier baselines unchanged.

## V1.14 local dbt correctness — 2026-10-15

Baseline a1eef3a; separate dbt-core 1.12.3 / dbt-duckdb 1.11.0 / DuckDB 1.5.0 /
pytest 9.1.1 environment on Python 3.13.7. One Spark export test and two actual
dbt integration tests passed; duplicate fact key intentionally fails unique.
Actual earlier Silver snapshot exported and built: 1 view + 2 tables + 6 data
tests passed (9 successful dbt nodes). Joined query returned one historical
BTC-USD observation marked replay, quantity 0.00000012 BTC, preserving its event
time/identity. Not a new authentic-volume measurement. Project suite 85 passed /
7 skips, exit 0; known post-summary Py4J closed-stream logging error retained.

No provider/Kafka traffic, throughput, latency, comparative query/build benchmark
or cloud-cost measurement. dbt's printed execution durations are diagnostic
output, not a performance claim. Evidence: local Git-ignored
`docs/verification/v1-14/` logs/build artifacts/query.json/run-summary.json;
tracked guide `docs/v1_local_dbt.md`. Existing environments/baselines unchanged.

## V1.15 Compose runtime correctness — 2026-10-15

Baseline 5085299; Docker Compose 5.3.1 on macOS/aarch64, Linux containers.
Image: Python 3.13.7 / Java21, Spark 4.2.0 / existing Delta packages, pinned
Airflow/dbt environments. Original running Kafka observed as 4.3.1; learning
broker pins that exact cached image digest. Original container ID unchanged.

Compose opt-in tests 2 passed: one synthetic host write survives learning broker
recreation and container read, exact coordinates reconciled. Container Spark
export 1 passed, container dbt 2 passed, native DAG parse 1 passed/1 skip.
Learning Airflow health/API and manual synthetic replay DAG succeeded after
fixing child-executable PATH. Final config test 1 passed/1 skip. Host full suite
88 passed/7 skips before final PATH config correction; targeted config/startup/
DAG verification passed afterward. First startup failure and known host Py4J
shutdown logging noise retained. Total new synthetic verification deliveries: 2
(one plain Kafka check and one L2 replay batch), not authentic source volume.

No provider traffic, throughput/freshness/latency/scale/cost benchmark or full V1
exit claim. Build/test/run durations are diagnostic only. Evidence: local ignored
`docs/verification/v1-15/`; guide `docs/v1_local_compose.md`. Historical broker,
data and prior evidence preserved. Runtime readiness is not a recovery guarantee.

## V1.16 bounded authentic trade exit/baseline — 2026-10-15

Working tree based on `1ca0545` (not a committed V1.16 revision). Frozen tracked
input/provenance: `tests/fixtures/v1_exit/`, four retained original messages,
104 observations = 104 distinct source/product/trade keys. Reconstructed only
from the retained historical authentic V1.1 artifact; no new provider traffic.
Exact file hashes and original artifact hashes: `provenance.json` and tracked
`docs/v1_exit_baseline.json`. Four archive wrappers total 17,910 bytes.

Final experiment command:

```sh
MARKETFLOW_RUN_V1_EXIT=1 .venv/bin/python -B -m pytest tests/test_v1_exit.py -v -s -p no:cacheprovider --basetemp data/v1/v1-16-final-20261015
```

Result: **2 passed in 73.02s**, exit 0. Two sequential fresh-state executions;
each repeats the archive twice, uses a new 1-partition/replication-1 replay topic,
checkpoint, Delta tables and database. Each reconciles **208 acknowledged/Bronze
deliveries = 104 accepted + 104 duplicate + 0 rejected**; 104 joined fact rows,
matching source values and minute totals (104 trades, 1.24180961 BTC). Equal
logical-result SHA-256:
`018aeafd59a8185c8728d237ed45e44d822b63fd14f65fd464b60d20607f0429`.
The final baseline contains 416 deliveries, not 416 authentic unique events.
Preliminary experiment also passed (2 tests, 71.48s) and emitted another 416;
total new verification deliveries this slice: 832 of the same 104 source IDs.

Environment: macOS 26.6.2 arm64, 10 logical host CPUs, 34,359,738,368 host RAM
bytes; Python 3.13.7 / Java 21.0.12.1; Spark 4.2.0 local[1] with 200 shuffle
partitions, driver memory not explicitly configured, no separate executor cluster.
Delta JVM 4.4.1 (Spark-4.2/Scala-2.13 artifact); each fresh table commits version0.
Learning Kafka 4.3.1, pinned image digest recorded in tracked baseline; Docker VM
allocation observed as 10 CPUs / 8,321,515,520 RAM bytes. dbt-core 1.12.3 /
dbt-duckdb 1.11.0 / DuckDB 1.5.0. Native Spark, container Kafka; other local
services remain running, no machine isolation. No managed runtime/warehouse.

No discarded warmup; both executions share one JVM. Startup: 3.652169s separately.
All replay finishes **before** Bronze starts. Pacing: 5 archive messages/s; each
message may contain many trades. These are deliberately small baseline observations:

| Actual observation | Execution 1 | Execution 2 |
| --- | ---: | ---: |
| Replay wall seconds | 2.163359 | 2.121191 |
| Acknowledged deliveries / replay wall second | 96.146761 | 98.058133 |
| Bronze query wall seconds | 6.824014 | 2.638490 |
| Bronze rows / query wall second | 30.480592 | 78.832961 |
| Publication→Bronze processing p50 ms | 1968.880 | 1071.488 |
| Publication→Bronze processing p95 ms | 3037.133 | 2131.743 |
| Silver rebuild wall seconds | 12.351583 | 10.567367 |
| dbt build wall seconds (subprocess, incl tests) | 2.030706 | 1.765881 |

Delay uses `ingested_at - published_at` over all 208 deliveries per execution,
nearest-rank `ceil(p*n)` percentiles. It includes backlog waiting and stops at
Spark processing time, **not** Delta commit visibility, original event time or
query readiness. Bronze wall rate includes startup/drain/termination. Replay
wall rate includes acknowledgments and intentional pacing. Second execution is
warmed; differences are not an optimisation result or a reliable capacity estimate.

Physical Parquet files per execution: Bronze1, accepted Silver86, audit86,
minutes1, export3. No compaction/tuning performed. Raw progress, all per-delivery
delay samples, stage logs, Delta tables, dbt run results and query rows remain at
`data/v1/v1-16-final-20261015/test_authentic_trade_exit_and_0/v1-exit/`.
Preliminary output remains under `data/v1/v1-16-baseline-20261015/`.
Test logs: `docs/verification/v1-16/`. Those paths remain intentionally ignored;
tracked baseline and guide preserve summary/configuration, not all raw files.

This establishes the bounded historical trade exit path and fresh replay
equivalence. It does not upgrade MF-002–MF-005 to sustained performance,
optimisation or production recovery claims. Prior baselines remain unchanged.

Regression verification: `.venv/bin/python -B -m pytest -v -p no:cacheprovider`
reported **90 passed, 8 skips in 114.41s**, exit 0. Known Py4J closed-stream
shutdown logging follows the passing summary. Test duration is not a pipeline
throughput measurement. Focused replay/workload verification: 7 passed/1 opt-in
skip. Both CLI help commands and `git diff --check` passed.

## V1 cleanup verification — 2026-10-15

Documentation/workflow maintenance based on `8ab3a11`, with uncommitted cleanup
changes. No optimisation or new performance claim. Prior V1.16 baseline and all
raw historical records preserved. The same pinned runtimes now run through Make;
PySpark supplies its matching Py4J 0.10.9.9 without a redundant direct pin.

`make demo RUN=tidy-verification-20261015` exited 0 inside the rebuilt Linux
container runtime: two isolated executions of the same frozen authentic archive,
each 208 acknowledged/Bronze deliveries = 104 accepted + 104 duplicate + 0 rejected.
Both analytical queries return 104 rows with identical logical hashes and original
source values; minute totals remain 104 trades / 1.24180961 BTC. This creates
416 replay deliveries of the existing 104 source IDs, not new source events.
`make inspect` independently reads three Kafka samples without committing group
offsets and queries the actual database (104 rows/104 keys/1.24180961 BTC).

An isolated V0 CLI smoke adds one synthetic delivery: first consumer read 1,
after committed-offset resume 0. Total new transport deliveries in this cleanup:
417 (416 historical replay + 1 synthetic). No provider traffic. Runner timings
remain incidental bounded observations, not a replacement benchmark or capacity
claim; the earlier tracked baseline JSON is unchanged.

Verification: image build succeeded; `make test` core/Spark 87 passed/10 skipped,
dbt 2 passed, DAG parse 1 passed/1 opt-in skip, exit 0. Environment-dependent skips
explain differences from the earlier native 90-pass suite; this is not a coverage
percentage. `pip check` passes in all three environments. Fixture byte comparison,
comment-only executable AST comparison (20 scripts), existing-output refusal and
new documentation link checks passed. No destructive data/volume reset executed.

Raw logs: `docs/verification/v1-tidy/` (ignored). Runtime manifest/tables/dbt
artifacts: `data/compose/runs/tidy-verification-20261015/` on the host; the recorded
manifest directory `/workspace/data/runs/...` is its container path. V0 smoke topic
and exact counts: `docs/verification/v1-tidy/v0-smoke.json`.

## V2.1 local S3 contract verification — 2026-10-15 (in progress)

Baseline `cf6c9b4` plus V2.1 working changes. Boto3 1.40.50 / botocore 1.40.76,
native Python 3.13.7 / pytest 9.1.1. Five SDK Stubber tests passed; with existing
archive/replay tests, focused result **15 passed / 1 real-AWS opt-in skip**.
One retained authentic archive wrapper is read locally and compared byte-for-byte
through scripted SDK responses. This is neither an AWS upload nor a source-volume
measurement. First run: 11 passed / 1 skipped / 4 setup errors; SDK-client context
cleanup corrected using contextlib.closing, first log preserved.

Docker image rebuild, CLI help, native pip check and policy JSON parsing passed.
Local raw logs: ignored `docs/verification/v2-1/`. No AWS account/target exists yet;
IAM/bucket policies are unapplied templates. Real readback, replacement refusal,
negative access checks and authentic archive upload remain UNVERIFIED. No provider,
Kafka or AWS traffic from these checks; no performance/cost/recovery/CV claim.
Prior V0/V1 baselines and authentic fixtures are unchanged. V2.1 stays IN PROGRESS.

Rebuilt-container `make test` exited 0: core/Spark **92 passed / 11 skipped**;
dbt **2 passed**; DAG **1 passed / 1 opt-in skip**. Core adds the real-AWS opt-in
skip to the prior skip set. Raw output: `docs/verification/v2-1/make-test.log`.
Test elapsed times are diagnostics, not S3/pipeline performance measurements.
