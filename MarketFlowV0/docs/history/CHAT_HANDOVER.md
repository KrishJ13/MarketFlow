# CHAT_HANDOVER.md

## 1. Project

- **Project name:** MarketFlow — Real-Time Financial Data Engineering Platform.
- **Repository/project purpose:** Build a production-style financial data platform that ingests public market events through Kafka, processes batch and streaming workloads with Spark/Databricks and Delta Lake, orchestrates bounded workflows with Airflow, publishes curated data into Snowflake, and uses dbt for tested dimensional models and analytical marts. The project is explicitly a data-engineering project rather than an ML or trading project.
- **Current intended stopping point:** **V2 — Managed Lakehouse & Warehouse MVP.**
- **Current approximate version/sub-version reached:** **V0 kickoff / exact implementation point UNKNOWN.** The recoverable project conversation shows that the learner started the V0 Walking Skeleton session, but no subsequent implementation or verification evidence is available in the accessible conversation history.
- **Implementation confidence:** Very low. Do not infer repository state from the project specification.
- The handover request explicitly requires uncertainty to remain visible, prohibits inventing implementation state, and limits the immediate scope to V2.

---

## 2. Authoritative Documents

`PROJECT_SPEC.md` defines **what MarketFlow should become**.

`TEACHING_STYLE.md` defines **how MarketFlow should be taught and built**.

Neither file may be silently overridden, rewritten, shortened, or replaced by this handover. The teaching guide explicitly supplements rather than overrides the project specification and makes learner understanding, incremental implementation, testing, debugging, and explainability part of the objective.

This handover is therefore descriptive, not authoritative over either document.

The uploaded project specification appears under the descriptive filename `MarketFlow — Real-Time Financial Data Engineering Platform — Project Specification.md`, but the canonical repository role referenced throughout this handover is `PROJECT_SPEC.md`.

---

## 3. Conversation History Summary

Only a very small amount of recoverable project-chat history is available. No implementation claims below should be upgraded without inspecting the repository.

### V0 kickoff — Walking Skeleton

**Goal**

Begin MarketFlow at V0 and establish the smallest end-to-end data path.

The V0 specification asks:

> Can one financial event cross the entire data pipeline?

The intended V0 path is checked-in fake events → one local Kafka topic → a tiny PySpark Structured Streaming job → local Delta/Parquet → a simple analytical SQL query. V0 deliberately excludes Airflow and uses only minimal quality and observability.

**What was discussed**

Recoverable conversation evidence only establishes that the learner said, in effect, “Let’s get started” in a project conversation titled around starting the V0 Walking Skeleton, with `PROJECT_SPEC.md` and `TEACHING_STYLE.md` available.

No later V0 lesson, code exchange, test output, command output, design discussion, or learner explanation is recoverable from the available history.

Accordingly, the detailed V0 architecture below comes from `PROJECT_SPEC.md`, not from evidence that it was already implemented or taught.

**What I appear to have implemented**

`UNKNOWN`.

No implementation can be proven from the accessible conversation.

Do not interpret the existence of V0 requirements in the specification as evidence that the repository contains them.

**Tests / verification discussed or performed**

No performed test or command result is recoverable.

The V0 specification requires one schema check and simple received/processed/written observability, but there is no evidence that either was implemented or run.

**Important decisions**

The following are V0 design constraints from the specification rather than verified conversation decisions:

- use checked-in fake events before introducing live Coinbase;
- use one local Kafka broker/topic;
- use a tiny Structured Streaming job rather than building a substantial Spark application;
- use local Delta/Parquet;
- keep orchestration manual;
- do not introduce Airflow yet;
- prove one simple analytical query;
- keep observability intentionally primitive.

**Known limitations / shortcuts**

The V0 design is intentionally naive:

- fake rather than authentic data;
- one broker/topic;
- minimal schema validation;
- local persistence;
- manual orchestration;
- primitive logs/counters;
- no production recovery, replay architecture, dimensional modelling, managed cloud infrastructure, or sophisticated monitoring.

These are learning baselines, not defects to silently “fix” before they have served their purpose.

**Learning context**

No specific V0 concept can be confirmed as already taught in the recoverable conversation.

The intended V0 exit explanation is:

```text
producer
→ Kafka topic
→ partition
→ Spark consumer
→ Delta table
→ SQL
```



The teaching guide requires the project to proceed feature-by-feature, from first principles and naive implementations to incremental improvements, rather than dumping the final architecture into the repository.

---

## 4. Current Functional Behaviour

### Confirmed from conversation

No runtime behaviour is confirmed.

There is no recoverable evidence that:

- Kafka is running;
- a producer exists;
- any event has been published;
- Spark consumes anything;
- Delta or Parquet files have been written;
- SQL has been executed;
- a schema check passes;
- any tests pass;
- Docker is configured;
- CI exists.

The only confirmed project state is that work was intended to begin at V0.

### Likely but not verified from code

No behaviour should be labelled “likely implemented” solely from the specification.

The **intended V0 behaviour**, once implemented, is:

```text
checked-in fake event
→ Kafka
→ tiny Spark Structured Streaming transformation
→ local Delta/Parquet
→ SQL: trades per minute
```

with one schema check and simple received/processed/written logging.

Whether any portion of that path already exists must be established through repository inspection.

---

## 5. Current Architecture

Because implementation is unverified, distinguish the **current intended V0 architecture** from the project's later target architecture.

### Intended architecture at the apparent stopping point

```text
checked-in fake trade/event
        ↓
simple producer
        ↓
one local Kafka broker/topic
        ↓
tiny PySpark Structured Streaming consumer
        ↓
minimal transformation/schema check
        ↓
local Delta or Parquet storage
        ↓
simple SQL analytical query
```

Operationally:

```text
manual command/script
simple received / processed / written output
```

No Airflow is intended at V0.

### Do not describe this later architecture as already present

The full project eventually expands toward:

```text
Coinbase
→ Python collector
→ Kafka
→ raw archive + Spark
→ Delta Bronze/Silver
→ Snowflake
→ dbt facts/dimensions/marts
```

with Airflow orchestrating bounded workflows rather than streaming itself. That is target architecture, not proven repository state.

---

## 6. Important Domain Invariants Already Introduced

The authoritative project specification defines the following system invariants. However, the recoverable conversation does **not** establish which of them had already been explicitly taught to the learner or implemented.

Therefore every invariant below is conservatively marked **UNKNOWN** with respect to implementation.

| Invariant | Rule | Status |
|---|---|---|
| INV-001 | Authentic raw events are never silently overwritten. | UNKNOWN — specified, implementation not verified |
| INV-002 | Every processed event retains source/channel and ingestion provenance. | UNKNOWN — specified, implementation not verified |
| INV-003 | Duplicate deliveries must not create uncontrolled duplicate logical facts. | UNKNOWN — specified, implementation not verified |
| INV-004 | Historical replay must not corrupt live logical datasets. | UNKNOWN — specified, implementation not verified |
| INV-005 | Event-time semantics must be explicit; processing time must not silently substitute for event time. | UNKNOWN — specified, implementation not verified |
| INV-006 | Records beyond a watermark require a defined policy. | UNKNOWN — specified, implementation not verified |
| INV-007 | Kafka ordering assumptions are scoped to partitions, not global. | UNKNOWN — specified, implementation not verified |
| INV-008 | One active compatible streaming query owns a checkpoint. | UNKNOWN — specified, implementation not verified |
| INV-009 | Invalid/quarantined records must not disappear silently. | UNKNOWN — specified, implementation not verified |
| INV-010 | Critical counts/totals must be reconcilable across layers. | UNKNOWN — specified, implementation not verified |
| INV-011 | Warehouse fact grain and dimensional keys must be explicit and stable. | UNKNOWN — specified, implementation not verified |
| INV-012 | Historical dimension relationships must remain reconstructible. | UNKNOWN — specified, implementation not verified |
| INV-013 | Historical backfills must not silently corrupt live data. | UNKNOWN — specified, implementation not verified |
| INV-014 | Rerunning orchestrated work should give equivalent logical results. | UNKNOWN — specified, implementation not verified |
| INV-015 | Stale data must not appear current without an indication. | UNKNOWN — specified, implementation not verified |
| INV-016 | No scale/performance CV claim exists without preserved workload evidence. | UNKNOWN — specified, implementation not verified |

These invariants are defined together in the specification and should remain design guardrails as implementation progresses.

For the earliest V0 work, Codex should particularly avoid accidentally violating the long-term direction around provenance, replayability, duplicate safety, and measurable claims even if the first implementation remains deliberately simple.

---

## 7. Important Architectural Decisions

The following are authoritative **project design decisions**. They are not evidence of implemented repository state.

### Decision: progress through runnable vertical versions

- **Decision:** Every version should preserve an end-to-end path rather than assigning one technology to one version.
- **Reason:** The learner should repeatedly experience source → transport → transform → store → model/query/observe while sophistication increases.
- **Alternatives discussed:** A technology-by-version progression such as “V0 Kafka, V1 Spark, V2 Databricks”.
- **Consequences:** Early implementations will be deliberately small or naive, but remain demonstrable.
- **Appears implemented:** UNKNOWN.

The project specification explicitly rejects a technology-siloed version sequence.

### Decision: Kafka is the event backbone

- **Decision:** Kafka provides durable transport and replayable event distribution.
- **Reason:** MarketFlow needs partitions, ordering scope, offsets, replay, independent consumers, and a durable event boundary.
- **Alternatives discussed:** Not recoverable from conversation.
- **Consequences:** Learner must understand topics, partitions, keys, offsets, consumer groups, and retention rather than treating Kafka as a black box.
- **Appears implemented:** UNKNOWN.

### Decision: partition ordering is not global

- **Decision:** Ordering guarantees apply inside a Kafka partition.
- **Reason:** Correctness depends on knowing which events can actually be assumed ordered.
- **Alternatives discussed:** The incorrect blanket statement “Kafka guarantees ordering”.
- **Consequences:** Topic key design is correctness-sensitive.
- **Appears implemented:** UNKNOWN.

The specification states that the default key is `product_id` or `venue + product_id`, supporting instrument-specific ordering, and explicitly limits Kafka's ordering guarantee to a partition.

### Decision: assume events may be processed more than once

- **Decision:** Do not rely on an unqualified exactly-once architecture.
- **Reason:** Delivery and processing boundaries can retry independently.
- **Alternatives discussed:** Casual “exactly once” claims.
- **Consequences:** Downstream logic must evolve toward deterministic keys, idempotency, and deduplication.
- **Appears implemented:** UNKNOWN.



### Decision: preserve immutable raw inputs

- **Decision:** Raw authentic capture is append-only and retained for reconstruction.
- **Reason:** Parsing or transformation bugs should be repairable through reprocessing.
- **Alternatives discussed:** Mutating historical raw data after downstream logic changes.
- **Consequences:** Storage grows, but reproducibility and repair become possible.
- **Appears implemented:** UNKNOWN.

### Decision: Bronze and Silver have different responsibilities

- **Decision:** Bronze remains minimally transformed/raw-but-queryable; Silver contains validated, typed, deduplicated, event-time-correct domain records.
- **Reason:** Preserve source truth while creating trustworthy domain datasets.
- **Alternatives discussed:** One undifferentiated processed table.
- **Consequences:** Reprocessing and layer-specific quality/reconciliation become explicit.
- **Appears implemented:** UNKNOWN.



### Decision: Airflow orchestrates bounded workflows, not event streaming

- **Decision:** Airflow will schedule/retry/backfill bounded work; it must not process individual market events.
- **Reason:** Streaming processing belongs to Kafka/Spark, while Airflow handles workflow dependencies.
- **Alternatives discussed:** Frequent DAG polling as imitation streaming.
- **Consequences:** The live streaming application runs independently of Airflow.
- **Appears implemented:** UNKNOWN.

The V2 specification explicitly keeps the streaming job continuously/independently operated while Airflow orchestrates historical and downstream bounded work.

### Decision: Databricks and Snowflake have distinct roles

- **Decision:** Databricks/Spark/Delta handle high-volume streaming/lakehouse processing; Snowflake/dbt handle analytical warehouse and dimensional modelling.
- **Reason:** The project deliberately teaches both processing/lakehouse and relational warehouse responsibilities.
- **Alternatives discussed:** Doing everything in one of the two systems.
- **Consequences:** Data needs an explicit lake-to-warehouse publication boundary.
- **Appears implemented:** UNKNOWN.

### Decision: never benchmark the public Coinbase source

- **Decision:** Capture authentic data once, then replay internally for load testing.
- **Reason:** Avoid abusing an external public service and make workloads reproducible.
- **Alternatives discussed:** Driving synthetic benchmark load against Coinbase.
- **Consequences:** Benchmarks must distinguish unique authentic events from replayed deliveries.
- **Appears implemented:** UNKNOWN.



---

## 8. Known Technical Debt / Naive Implementations

No existing technical-debt item can be proven from repository state.

The following are **intentional V0 baselines expected by the specification** and must not be mistaken for repository facts until inspected.

### Checked-in fake events

- **Current approach:** V0 uses deterministic fake input.
- **Why it is limited:** It does not demonstrate reconnect behaviour, real source schemas, late arrival, source irregularities, or continuous authentic data.
- **Intended later improvement:** V1 introduces real Coinbase feeds.

### One local Kafka broker/topic

- **Current approach:** Single minimal Kafka path.
- **Why it is limited:** It hides richer topic separation, partition behaviour, consumer groups, retention tuning, and failure scenarios.
- **Intended later improvement:** V1 separates trade and L2 topics and begins authentic event handling.

### Tiny Spark streaming job

- **Current approach:** Minimal Structured Streaming processing.
- **Why it is limited:** No genuine order-book reconstruction, late-data policy, Bronze/Silver separation, or performance engineering.
- **Intended later improvement:** V1 introduces real parsing, event time, order-book state, and trade aggregation; V2 moves workloads to Databricks.

### Local Delta/Parquet

- **Current approach:** Local table/file storage.
- **Why it is limited:** No managed object-storage/lakehouse infrastructure.
- **Intended later improvement:** V2 uses S3 and managed Databricks/Delta.

### Manual orchestration

- **Current approach:** One script/command.
- **Why it is limited:** No scheduler, bounded retries, backfill workflow, or reconciliation dependencies.
- **Intended later improvement:** V1 introduces Airflow for replay, daily quality, and reconciliation; V2 expands orchestration.

### One schema check

- **Current approach:** Minimal structural-quality validation.
- **Why it is limited:** It is not a complete data-quality strategy.
- **Intended later improvement:** V1/V2 add typed Silver records, quality rules, dbt tests, and reconciliation.

### Basic received/processed/written output

- **Current approach:** Primitive observability.
- **Why it is limited:** It does not measure lag, freshness, throughput, failure rates, state size, or cross-layer correctness.
- **Intended later improvement:** V1 establishes baseline metrics and V2 expands end-to-end operational measurements.

Again, whether any of these naive components actually exists is `UNKNOWN`.

---

## 9. Known Bugs / Failing Tests / Unresolved Problems

`No known unresolved issue was recoverable from conversation history.`

This statement does **not** mean the repository is bug-free. It means no specific failing behaviour or unresolved bug is supported by the available conversation evidence.

---

## 10. Existing Tests and Verification

No executed or implemented test can be verified from the available conversation history.

### Unit

None verified.

### Integration

None verified.

The specification eventually expects Kafka production/consumption, replay, partition-key, Spark, Delta, Airflow, Snowflake/dbt, reconciliation, and failure tests, but those are target requirements rather than confirmed existing tests.

### End-to-end

None verified.

V0 should eventually prove one fake event crosses the whole local pipeline, but there is no evidence this currently passes.

### Concurrency

None verified.

### Data-quality

No implemented test verified.

V0 specifies a single schema check; implementation status is UNKNOWN.

### Performance

None verified.

No benchmark numbers should be assumed.

### Manual verification

No command output or learner-reported manual verification is recoverable.

Repository inspection should locate tests before Codex writes replacements. Existing tests, even incomplete ones, are evidence of the learning progression and should not be silently discarded.

---

## 11. Metrics and Benchmarks

No metric below has recoverable measured evidence.

| Metric / Claim | Status | Existing Evidence | Notes |
|---|---|---|---|
| Authentic unique event count | NOT MEASURED | None recoverable | Must remain distinct from replayed deliveries |
| Replayed event deliveries | NOT MEASURED | None recoverable | Never present as unique authentic events |
| Ingress rate | NOT MEASURED | None recoverable | V1 measurement target |
| Spark processing rate | NOT MEASURED | None recoverable | V1 measurement target |
| General processing/data latency | NOT MEASURED | None recoverable | V1 measurement target |
| Raw event count | NOT MEASURED | None recoverable | V1 reconciliation input |
| Silver event count | NOT MEASURED | None recoverable | V1 reconciliation output |
| End-to-end freshness | NOT MEASURED | None recoverable | V2 headline metric candidate |
| Kafka consumer lag | NOT MEASURED | None recoverable | V2 measurement target |
| Spark micro-batch duration | NOT MEASURED | None recoverable | V2 measurement target |
| Snowflake load time | NOT MEASURED | None recoverable | V2 measurement target |
| dbt build time | NOT MEASURED | None recoverable | V2 measurement target |
| Analytical query latency | NOT MEASURED | None recoverable | V2 measurement target |
| Throughput claim in events/s | NOT MEASURED | None recoverable | Never fabricate |
| p50/p95/p99 freshness | NOT MEASURED | None recoverable | Requires controlled workload |
| Cost/compute efficiency | NOT MEASURED | None recoverable | No cost claim should be inferred |

The specification explicitly leaves freshness SLO values TBD until measured and prohibits fabricated performance claims.

The teaching guide likewise requires a defined workload, baseline, controlled environment, distributions, profiling, repeated trials, and preservation of raw results before making performance claims.

---

## 12. Technologies Already Encountered

### Actually used

**None can be verified from conversation history.**

Do not promote a technology into this category merely because it is named in `PROJECT_SPEC.md`.

Python and SQL are described in the project specification as part of the learner's prior professional experience, but that is learner background rather than evidence they have already been used in the MarketFlow repository.

### Discussed but not yet verified as used

At the V0 design level:

- Python;
- Apache Kafka;
- PySpark / Spark Structured Streaming;
- Delta Lake or Parquet;
- SQL;
- local process execution;
- simple schema validation/logging.

Status for all: **specified / implementation not verified**.

### Planned for V1/V2

#### V1

- Coinbase Advanced Trade public market-data WebSocket;
- separate Kafka trade and L2 topics;
- immutable local/S3-compatible raw archive;
- real Spark parsing;
- event-time processing;
- stateful order-book reconstruction;
- trade aggregation;
- Delta Bronze and Silver;
- Airflow for replay, daily quality, and reconciliation;
- dbt against an inexpensive local analytical database;
- Docker Compose;
- optional PostgreSQL;
- initial operational measurements.

The V1 exit criterion is that a real event reaches a queryable analytical table and can be replayed.

#### V2

- AWS S3;
- Databricks;
- Delta Bronze/Silver on managed infrastructure;
- Snowflake;
- dbt + Snowflake;
- staging/dimensions/facts/marts;
- Airflow orchestration across historical input, Databricks, publication, Snowflake, dbt, and reconciliation;
- CI;
- cross-layer data-quality checks;
- V2 metrics.

The V2 exit criterion is a tested and reproducibly orchestrated path from Coinbase through Kafka, Databricks/Spark, Delta, Snowflake, and a dbt mart.

Do not introduce V3-only capabilities such as Debezium CDC simply because they appear elsewhere in the full specification.

---

## 13. Learning State

### Concepts demonstrably already known from learner background

The project specification states that the learner already has substantial experience/evidence with:

- Python;
- SQL;
- Pandas;
- NumPy;
- PyTorch;
- scikit-learn;
- feature engineering;
- modelling;
- statistics;
- exploratory analysis.



Do not interpret this as permission to skip distributed-systems or production software-engineering fundamentals. `TEACHING_STYLE.md` explicitly forbids making that assumption.

### Concepts confirmed taught in this project

None can be proven from the recoverable conversation.

### Concepts currently being learned / intended current V0 learning target

Assuming repository inspection confirms development is still at the start of V0:

- event producer vs consumer;
- Kafka broker/topic/record;
- partition as an ordering and distribution unit;
- the first notion of a consumer;
- a streaming DataFrame/application at minimal scale;
- the difference between transport, processing, storage, and analytical query;
- simple schema validation;
- observable pipeline stages;
- end-to-end data flow.

The learner should eventually be able to explain the V0 chain without relying on framework magic.

### Concepts not yet confirmed introduced

No concept beyond the kickoff can be claimed to have been taught.

In particular, repository/conversation evidence is required before assuming familiarity from this project with:

- Kafka offsets;
- consumer groups;
- retention;
- replay semantics;
- event time vs processing time;
- watermarks;
- late/out-of-order events;
- Spark lazy execution/stages/tasks/shuffles;
- checkpoints;
- stateful Structured Streaming;
- Delta transaction semantics;
- Bronze/Silver responsibilities;
- order-book reconstruction;
- idempotency/deduplication;
- Airflow DAGs/retries/backfills;
- dbt sources/refs/tests;
- dimensional modelling;
- Snowflake architecture;
- Databricks operations;
- S3/IAM;
- reconciliation;
- data freshness;
- CI for the data platform.

These should be introduced in the order required by V0 → V1 → V2 rather than assumed from the final architecture.

---

## 14. Immediate Next Logical Slice

### Conditional next slice: V0.1 — Establish one deterministic event and its schema boundary

This is the safest next implementation slice **if repository inspection confirms it has not already been completed**.

Do not reimplement it if code/tests show the learner already progressed further.

### Goal

Create the smallest deterministic input that can later be sent through Kafka: one or a handful of checked-in fake market events with an explicit minimal schema.

### Behaviour to add

Given a checked-in fake event:

- the project can load it deterministically;
- required fields are identifiable;
- one deliberately malformed fixture can be rejected by the minimal schema check;
- the event is ready to become the input to the first Kafka producer slice.

The slice should remain bounded Python/data-contract work. It should not introduce Kafka, Spark, Airflow, Docker Compose, cloud infrastructure, or live Coinbase in the same step unless repository inspection proves those foundations already exist and were understood.

### Limitation of the current implementation motivating it

The implementation state is unknown.

At the specification level, V0 needs fake events and a schema check before the end-to-end path can be meaningfully verified. Establishing that boundary first prevents Kafka/Spark plumbing from obscuring what an event actually contains.

### Likely files/components affected

Exact paths must follow the existing repository structure rather than being invented.

Potential areas, subject to repository inspection:

```text
data/ or fixtures/
schemas/
marketflow/.../
tests/
```

Possible artefacts:

- one fake trade/event JSON fixture;
- one minimal schema/validation representation;
- one focused validation test.

Do not create the entire final suggested repository tree merely because the specification contains one.

### Tests that should prove it

At minimum:

1. valid fixture loads successfully;
2. malformed/missing required field is rejected;
3. test output is deterministic.

The test should protect against sending structurally invalid data farther into the pipeline.

### Concepts that should be understood

- What is an event?
- What is a schema?
- What is the boundary between source data and infrastructure?
- Why validate before adding distributed-system complexity?
- What does deterministic test data buy us?

### Explicit non-goals

- no Coinbase;
- no reconnect logic;
- no order book;
- no event-time watermarking;
- no Airflow;
- no Databricks;
- no Snowflake;
- no dbt;
- no cloud deployment;
- no performance claims;
- no “production-grade” abstraction;
- no full V0 implementation in one commit.

`TEACHING_STYLE.md` requires exactly this kind of feature-sized progression: explain the goal and first principles, show a reasonable naive baseline, improve incrementally, let the learner implement, verify, and use explain-back questions before advancing.

---

## 15. V1/V2 Remaining Roadmap

This roadmap assumes V0 is completed and its exit criterion is verified first.

If repository inspection finds V0 incomplete, finish V0 before starting these slices.

Each item should be independently implementable, testable, reviewable, explainable, and committable.

### V1 — Authentic Local Data Platform

#### V1.1 — Minimal live trade collector

- Connect to Coinbase public market data.
- Subscribe to one configured product/channel first.
- Preserve receive timestamp.
- Observe real messages.
- Do not add L2 state yet.

#### V1.2 — Collector disconnect and bounded reconnect

- Detect connection loss.
- Add an explicit bounded reconnect policy.
- Make connection health observable.
- Test/discuss what happens during the gap.

#### V1.3 — Trade topic contract and Kafka key

- Publish real trade events to a versioned trade topic.
- Choose/document the key deliberately.
- Teach partition-level ordering before scaling partitions.

#### V1.4 — L2 topic as a separate stream

- Add Level-2 feed parsing/publication.
- Keep trade and L2 semantics separate.
- Do not build full order-book state in the same change.

#### V1.5 — Immutable raw local archive

- Persist authentic source payloads append-only.
- Retain provenance and receive metadata.
- Prove capture can be read back unchanged.

#### V1.6 — Deterministic replay utility

- Read captured authentic data.
- Replay internally at a controlled rate.
- Preserve the distinction between unique source events and replayed deliveries.
- Do not benchmark Coinbase itself.

#### V1.7 — Bronze ingestion

- Consume Kafka using Structured Streaming.
- Parse the envelope/schema.
- Write raw-but-queryable Bronze records.
- Preserve payload/provenance/version fields.

#### V1.8 — Silver trade validation

- Type and validate trade records.
- Define a canonical logical key.
- Handle duplicates deterministically.
- Make accepted/rejected counts explicit.

#### V1.9 — Event-time trade aggregation

- Introduce source event time explicitly.
- Build the first bounded trade aggregation/window.
- Only then introduce lateness policy as needed.

#### V1.10 — L2 state model

- Teach `(product, side, price) → quantity`.
- Apply replace/remove semantics.
- Test simple state transitions independently before deriving analytics.

#### V1.11 — Best bid/ask or equivalent small order-book product

- Derive one useful stateful output.
- Add domain-quality checks such as bid ≤ ask where appropriate.
- Avoid a large menu of derived metrics.

#### V1.12 — Local Airflow introduction

- Create one bounded batch/replay workflow.
- Teach DAG/task/dependency/retry concepts.
- Keep the live streaming job independent.

#### V1.13 — Daily quality and reconciliation

- Compare raw/Bronze/Silver boundaries.
- Ensure invalid/quarantined records are accounted for.
- Fail visibly on unexplained discrepancies.

#### V1.14 — Local dbt fundamentals

- Introduce one source.
- Create one staging model.
- Create one small analytical fact/dimension path.
- Add `unique`, `not_null`, relationship, or domain tests only where justified.

#### V1.15 — Docker Compose consolidation

- Run the local dependencies reproducibly.
- Do not use Compose to hide Kafka/Spark mechanics the learner has not understood.

#### V1.16 — V1 measurement baseline and exit demo

Measure, without optimisation:

- unique authentic events;
- replay deliveries;
- ingress rate;
- Spark processing rate;
- latency;
- raw/Silver counts.

Exit only when a real event reaches a queryable analytical table and can be replayed reproducibly.

### V2 — Managed Lakehouse & Warehouse MVP

#### V2.1 — S3 landing/raw boundary

- Move durable landing/raw storage to AWS S3.
- Preserve immutable semantics.
- Introduce least-privilege access rather than broad credentials.

#### V2.2 — First Databricks Spark job

- Move one already-understood Spark workload to Databricks.
- Verify behaviour matches the local baseline.
- Use Spark UI/execution information rather than treating Databricks as an abstraction that replaces Spark understanding.

#### V2.3 — Delta Bronze on managed storage

- Establish Bronze table semantics.
- Verify schema, provenance, and repeat processing behaviour.

#### V2.4 — Delta Silver on managed storage

- Port validated/deduplicated/event-time-correct transformations.
- Verify local vs managed logical equivalence where practical.

#### V2.5 — Streaming checkpoint ownership

- Configure an explicit durable checkpoint for the continuous streaming job.
- Document ownership and restart behaviour.
- Keep Airflow away from per-event processing.

#### V2.6 — Curated lake-to-warehouse publication boundary

- Define what Silver/curated data Snowflake receives.
- Avoid dumping every raw Kafka record into analyst-facing warehouse models.

#### V2.7 — Initial Snowflake staging load

- Create the minimum staging path.
- Start with bounded staged-file loading / `COPY INTO`.
- Verify row counts and failure behaviour.

#### V2.8 — dbt source and staging models on Snowflake

- Define warehouse sources.
- Standardise names/types in staging.
- Add source/data tests.

#### V2.9 — Core dimensions

Implement separately:

- `dim_product`;
- `dim_venue`;
- `dim_date`.

Do not introduce SCD Type 2 unless V2 requirements genuinely need it; the more advanced historical CDC path belongs later.

#### V2.10 — `fct_trade`

- Establish the grain: one executed trade.
- Define stable keys.
- Add required quality and relationship tests.

#### V2.11 — `fct_market_interval`

- Establish one product × fixed interval grain.
- Build only metrics justified by available Silver inputs.
- Test interval uniqueness and domain assumptions.

#### V2.12 — First analytical mart/query

- Compose the fact/dimension data into one analyst-facing result.
- Demonstrate why the warehouse model is preferable to raw-event querying.

#### V2.13 — Airflow managed batch chain

Orchestrate the bounded path:

```text
historical input
→ Databricks batch processing
→ curated publication
→ Snowflake load
→ dbt build
→ dbt tests
→ reconciliation
```

The continuously running stream remains independent.

#### V2.14 — Cross-layer reconciliation

Verify at least:

- Silver vs published data;
- published/staged data vs Snowflake;
- fact row counts/totals where meaningful.

Do not accept “job succeeded” as proof that all data arrived.

#### V2.15 — CI baseline

Add checks appropriate to the repository's actual implementation:

- Python tests;
- schema/contract tests;
- Spark tests;
- Airflow DAG import validation;
- dbt compile/tests.

Do not add later-version infrastructure checks prematurely.

#### V2.16 — V2 measurements and exit evidence

Measure:

- end-to-end freshness;
- consumer lag;
- Spark micro-batch time;
- Snowflake load time;
- dbt build time;
- query latency.

Preserve workload/configuration evidence.

V2 is complete only when real data reproducibly traverses:

```text
Coinbase
→ Kafka
→ Databricks/Spark
→ Delta
→ Snowflake
→ dbt mart
```

with orchestration and tests.

---

## 16. Important Warnings for Codex

1. **Do not modify, rewrite, shorten, replace, or silently reinterpret `PROJECT_SPEC.md` or `TEACHING_STYLE.md`.**

2. **Do not assume implementation from design documentation.** Anything not established from repository evidence remains UNKNOWN or `DISCUSSED / IMPLEMENTATION NOT VERIFIED`.

3. **Inspect the repository before coding.** The exact current sub-version is not recoverable from conversation history.

4. **Do not jump directly to V2 architecture.** V0 and V1 naive/local forms are intentional parts of the learning progression.

5. **Do not erase a naive baseline merely because a more sophisticated design is already known.** The teaching model is deliberately:

```text
simple working system
→ discovered limitation
→ improvement
→ new limitation
```



6. **The learner builds; Codex should preserve the teaching role unless explicitly asked to switch into build-for-me mode.** Do not silently fill the repository with finished implementation.

7. **One major systems concept at a time.** Do not introduce Kafka, Spark watermarks, Airflow, Delta internals, Snowflake, and dbt in one implementation dump.

8. **Do not benchmark Coinbase.** Capture authentic events and replay them internally.

9. **Always distinguish unique authentic events from replayed event deliveries.**

10. **Do not fabricate metrics.** Use `NOT MEASURED`, `TBD`, or `UNKNOWN` until evidence exists.

11. **Do not casually claim “exactly once”.** Define exactly once at which boundary. Prefer explicit at-least-once transport plus idempotent logical effects when that is the actual design.

12. **Do not claim Kafka guarantees global ordering.** Ordering is within a partition.

13. **Do not make Airflow the streaming engine.** Airflow is for bounded orchestration, retries, backfills, reconciliation, and dependency management.

14. **Do not let Databricks hide Spark mechanics.** The learner still needs to understand partitions, stages, tasks, shuffles, state, and checkpoints.

15. **Do not let Snowflake hide dimensional design.** Grain, facts, dimensions, and keys must remain explicit.

16. **Do not reduce dbt to “SQL in files”.** Teach sources, refs/dependencies, models, tests, documentation, and lineage.

17. **Do not optimise before a representative baseline exists.**

18. **Preserve failed experiments and naive approaches when they carry learning value.**

19. **Do not introduce V3+ architecture while the immediate implementation scope stops at V2.** In particular, PostgreSQL/Debezium CDC, SCD/CDC reliability exercises, broad schema-evolution work, and later performance programmes should not be pulled forward without a specific V0–V2 requirement.

20. **Do not create every directory in the final suggested repository tree on day one.** The specification explicitly warns against this.

21. **Never weaken tests or exit criteria simply to make a version appear complete.**

22. **If code conflicts with this handover, trust repository evidence about implementation state but trust `PROJECT_SPEC.md` and `TEACHING_STYLE.md` about project intent and teaching rules. Record the conflict rather than silently rewriting history.**

---

## 17. Unknowns Requiring Repository Inspection

This section is mandatory because the accessible conversation history is insufficient to establish implementation state.

Before continuing development, Codex must inspect and establish the following.

### Repository/version-control state

- current Git branch;
- latest relevant commit;
- whether there are uncommitted changes;
- repository tree;
- whether the V0 work lives on another branch;
- commit messages that reveal sub-version progression;
- tags or changelog entries, if any.

### Existing V0 implementation

Verify whether any of the following already exists:

- fake event fixtures;
- event schema;
- producer;
- Kafka configuration;
- Docker/Compose Kafka service;
- Kafka topic creation/configuration;
- PySpark application;
- Structured Streaming Kafka source;
- Delta dependency;
- Parquet fallback;
- local output table;
- SQL analytical query;
- trades-per-minute aggregation;
- received/processed/written logging;
- manual run script.

### Package and dependency state

Inspect:

- `pyproject.toml`, requirements files, lock files, or equivalent;
- Python version;
- Java/JVM requirements;
- Spark/PySpark version;
- Kafka client library;
- Delta packages;
- pytest configuration;
- lint/type-check tooling;
- environment-variable/configuration mechanism.

Do not change dependencies until the existing choices are understood.

### Existing tests

Determine:

- which tests exist;
- whether they are unit, integration, or end-to-end;
- which commands run them;
- whether they currently pass;
- whether any tests are deliberately skipped;
- whether Kafka/Spark dependencies are mocked or real;
- whether the expected V0 schema test exists.

### Actual command/output evidence

Run or inspect documentation for:

- environment setup;
- service startup;
- producer invocation;
- Kafka topic inspection;
- Spark job invocation;
- output table inspection;
- SQL query;
- test suite.

Record actual outcomes. Do not infer success from code presence.

### V0 exit status

Determine whether the learner can currently demonstrate:

```text
producer
→ Kafka topic
→ partition
→ Spark consumer
→ Delta/Parquet table
→ SQL
```

If not, locate the earliest failing or missing boundary and resume there.

### Architecture decisions already recorded

Look for:

- `docs/adr/`;
- topic/key decisions;
- event schema/envelope decisions;
- choice of Delta vs Parquet for V0;
- Kafka deployment choice;
- storage path conventions;
- any deliberate simplifications.

Do not create duplicate ADRs if reasoning already exists.

### Current event model

Establish:

- fixture fields;
- timestamp representation;
- event identifier/key;
- product identifier;
- price/size types;
- envelope vs payload design;
- schema/version field;
- provenance metadata.

Do not silently replace an existing event contract with the later final envelope.

### Kafka state

Verify:

- broker distribution/configuration;
- topic names;
- partition count;
- replication factor;
- key;
- producer serialisation;
- consumer deserialisation;
- offsets/consumer-group configuration;
- retention configuration.

Do not infer V1 topic naming from the specification if V0 intentionally uses something simpler.

### Spark state

Verify:

- whether the code is batch or Structured Streaming;
- Kafka connector configuration;
- schema parsing;
- transformations;
- trigger/output mode;
- checkpoint use, if any;
- storage sink;
- query/test strategy.

### Storage state

Verify:

- whether V0 uses Delta or Parquet;
- output path;
- overwrite vs append semantics;
- whether rerunning produces duplicates;
- whether output is queryable;
- any cleanup scripts.

### Data-quality state

Verify:

- whether a schema check exists;
- what fields it checks;
- how malformed input fails;
- whether invalid records can disappear silently;
- tests associated with validation.

### Observability state

Verify:

- `print` vs logging;
- current received/processed/written counters;
- structured fields, if any;
- whether numbers are genuine measurements or only demonstration output.

### Metrics and benchmarks

Search for:

- benchmark files;
- logs;
- recorded event counts;
- latency measurements;
- throughput measurements;
- charts;
- CV-claim documentation.

Unless preserved evidence exists, continue to mark all quantitative performance claims `NOT MEASURED`.

### Documentation

Inspect:

- `README.md`;
- setup/quick-start instructions;
- architecture diagrams;
- ADRs;
- data contracts;
- changelog/session notes;
- any V0 teaching notes;
- any learner explain-back answers.

These may reveal sub-version history not recoverable from the chat.

### CI

Verify whether:

- GitHub Actions or another CI system exists;
- tests/lint/type checks run remotely;
- current workflows are green;
- CI was intentionally deferred.

Do not introduce or overhaul CI merely because it appears in the eventual project specification.

### V1/V2 work already present

Search before creating anything for:

- Coinbase collector;
- raw capture/replay;
- separate trade/L2 topics;
- Bronze/Silver tables;
- order-book state;
- Airflow;
- dbt;
- Docker Compose;
- S3;
- Databricks;
- Snowflake;
- CI.

If later-version code exists, determine whether it is experimental, partial, abandoned, or active. Do not automatically treat presence as completion.

### Learning progression

Repository evidence should be used to reconstruct, where possible:

- the sequence of commits;
- concepts already taught;
- code written by the learner;
- learner explain-back answers;
- deliberately naive versions;
- limitations intentionally postponed;
- tests used as teaching checkpoints.

Do not discard this progression in favour of a cleaner “final” implementation.

---

The central constraint for the next coding agent is therefore:

> **Inspect first, establish the exact verified V0 state, then continue with the smallest missing learning/implementation slice. Do not infer progress from the final architecture and do not skip directly to V1 or V2.**

The handover itself is intentionally conservative because the available conversation proves only the V0 kickoff, while the handover requirements explicitly prohibit invented implementation state and require uncertainty to be labelled.