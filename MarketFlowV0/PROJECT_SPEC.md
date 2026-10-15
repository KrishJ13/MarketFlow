# MarketFlow — Real-Time Financial Data Engineering Platform

## Technology Stack Checklist

### Required — Core Languages & Data Engineering

- [ ] Python 3.12+
- [ ] SQL
- [ ] Apache Kafka
- [ ] Apache Spark
- [ ] PySpark
- [ ] Spark Structured Streaming
- [ ] Apache Airflow
- [ ] Databricks
- [ ] Delta Lake
- [ ] Snowflake
- [ ] dbt
- [ ] AWS S3
- [ ] PostgreSQL
- [ ] Debezium / Change Data Capture
- [ ] Docker / Docker Compose
- [ ] Git
- [ ] GitHub Actions / CI/CD

### Required — Data Engineering Concepts

- [ ] Batch processing
- [ ] Stream processing
- [ ] ETL vs ELT
- [ ] Data lake
- [ ] Data warehouse
- [ ] Lakehouse architecture
- [ ] Bronze / Silver / Gold data layers
- [ ] Dimensional modelling
- [ ] Fact tables
- [ ] Dimension tables
- [ ] Slowly Changing Dimensions
- [ ] CDC
- [ ] Event time vs processing time
- [ ] Watermarks
- [ ] Late-arriving data
- [ ] Out-of-order data
- [ ] Idempotency
- [ ] Deduplication
- [ ] Kafka partitions / offsets / consumer groups
- [ ] Replay
- [ ] Schema evolution
- [ ] Data contracts
- [ ] Data quality
- [ ] Data lineage
- [ ] Backfills
- [ ] Reconciliation
- [ ] Incremental processing
- [ ] Partitioning
- [ ] Shuffle
- [ ] Data skew
- [ ] File sizing / small-file problems
- [ ] Query optimisation
- [ ] Data freshness
- [ ] Data-platform observability
- [ ] Cost/performance engineering
- [ ] Cloud IAM / secrets / RBAC

### Required — Testing & Operations

- [ ] pytest
- [ ] dbt data tests
- [ ] dbt unit tests where valuable
- [ ] Pipeline integration tests
- [ ] Contract/schema tests
- [ ] Reconciliation tests
- [ ] Failure injection
- [ ] Structured logging
- [ ] Pipeline metrics
- [ ] Freshness monitoring
- [ ] Runbooks
- [ ] Incident reviews

### Later-Version Required

- [ ] Terraform
- [ ] Snowflake RBAC
- [ ] Databricks governance/Unity Catalog concepts
- [ ] dbt incremental models
- [ ] dbt snapshots
- [ ] Spark performance profiling
- [ ] Snowflake query profiling
- [ ] Airflow backfill/recovery workflows

### Optional / Comparative Learning

- [ ] Avro
- [ ] Schema Registry
- [ ] OpenLineage
- [ ] Great Expectations / equivalent quality framework
- [ ] Iceberg concepts
- [ ] Snowpipe
- [ ] Databricks Auto Loader
- [ ] Spark Adaptive Query Execution
- [ ] Metabase / lightweight BI dashboard
- [ ] AWS Glue concepts
- [ ] Kinesis comparison
- [ ] Airflow managed-service comparison

### Explicitly Not Required

- [ ] Machine-learning model development
- [ ] PyTorch
- [ ] Kubernetes
- [ ] LLMs
- [ ] Microservices
- [ ] Trading execution
- [ ] Automated investment decisions

---

# 1. Project Identity

| Field                     | Definition                                                                                                                                                                                                                                                                                                                                                         |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Project name              | **MarketFlow**                                                                                                                                                                                                                                                                                                                                                     |
| Full title                | **MarketFlow — Real-Time Financial Data Engineering Platform**                                                                                                                                                                                                                                                                                                     |
| One-sentence description  | Build a production-style financial data platform that captures live public market events through Kafka, processes batch and streaming workloads with Spark/Databricks and Delta Lake, orchestrates backfills and reconciliation with Airflow, publishes warehouse-ready data into Snowflake, and uses dbt to build tested dimensional models and analytical marts. |
| Primary language          | Python                                                                                                                                                                                                                                                                                                                                                             |
| Primary query language    | SQL                                                                                                                                                                                                                                                                                                                                                                |
| Event backbone            | Apache Kafka                                                                                                                                                                                                                                                                                                                                                       |
| Distributed compute       | Apache Spark / PySpark                                                                                                                                                                                                                                                                                                                                             |
| Streaming engine          | Spark Structured Streaming                                                                                                                                                                                                                                                                                                                                         |
| Lakehouse                 | Databricks + Delta Lake                                                                                                                                                                                                                                                                                                                                            |
| Cloud object storage      | AWS S3                                                                                                                                                                                                                                                                                                                                                             |
| Orchestration             | Apache Airflow                                                                                                                                                                                                                                                                                                                                                     |
| Analytical warehouse      | Snowflake                                                                                                                                                                                                                                                                                                                                                          |
| Analytics transformation  | dbt                                                                                                                                                                                                                                                                                                                                                                |
| CDC                       | PostgreSQL + Debezium                                                                                                                                                                                                                                                                                                                                              |
| Portfolio archetype       | Data Engineering / Streaming / Lakehouse / Warehouse                                                                                                                                                                                                                                                                                                               |
| Engineering thesis        | Can continuously arriving, duplicated, late and evolving financial data be transformed into trusted analytical datasets that remain reproducible, replayable and reconcilable at increasing scale?                                                                                                                                                                 |
| Target roles              | Data Engineer, Software Engineer — Data, Data Platform Engineer, Analytics Engineer, Data & AI Engineer                                                                                                                                                                                                                                                            |
| Expected difficulty       | Advanced; V2 should be CV-ready, V4 should provide strong production-style evidence.                                                                                                                                                                                                                                                                               |
| Primary portfolio purpose | Demonstrate industrial data-engineering fundamentals that are not already strongly represented by the learner's data-science experience.                                                                                                                                                                                                                           |

---

# 2. Portfolio Role

MarketFlow is **not an ML project**.

Its purpose is to prove:

> I can build the data systems that analysts, data scientists, ML engineers and business applications depend upon.

The project therefore focuses on:

```text
data arrival
→ durable ingestion
→ distributed processing
→ quality
→ modelling
→ orchestration
→ warehousing
→ serving
→ governance
→ operations
```

rather than:

```text
features
→ model
→ prediction
```

The learner's existing professional experience already provides extensive evidence for:

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

MarketFlow should deliberately build the missing complementary evidence:

- Kafka;
- Spark;
- distributed execution;
- streaming;
- Databricks;
- Delta Lake;
- Airflow;
- Snowflake;
- dbt;
- dimensional modelling;
- cloud data architecture;
- CDC;
- lineage;
- data quality;
- pipeline reliability;
- backfills;
- performance engineering.

---

# 3. Product Thesis

Financial markets produce continuously changing data.

Examples include:

```text
trades
order-book updates
best bid/ask
volume
instrument reference data
```

A simple project might:

```text
connect to WebSocket
→ write CSV
→ analyse later
```

MarketFlow asks the much harder questions:

> What happens if the process crashes?

> Can the events be replayed?

> Which event occurred first?

> What if messages arrive late?

> What if the source schema changes?

> What happens if the same event is processed twice?

> How do we reconstruct the current order book?

> What does "exactly once" actually mean?

> What belongs in the lake versus the warehouse?

> How do we backfill three months without breaking the live pipeline?

> How do we know the warehouse matches the lake?

> What if the Spark job falls six hours behind?

> What happens when one Kafka partition becomes hot?

> Which dimensional model should an analyst query?

> How does a fact table differ from a stream of source messages?

> What is the cost of recomputing all history rather than incrementally processing it?

Those questions define the project.

---

# 4. Financial Scope

MarketFlow is a **market-data engineering platform**.

It is not:

- a trading algorithm;
- a brokerage;
- an execution engine;
- a portfolio-management system;
- an investment recommendation system.

The financial domain is useful because it naturally provides:

- continuous events;
- high event volume;
- ordering;
- timestamps;
- changing state;
- streaming aggregation;
- batch reconstruction;
- dimensional analytics.

---

# 5. Primary Public Data Source

Default source:

**Coinbase Advanced Trade public market-data WebSocket**

Relevant channels include:

```text
Level 2 order book
Market trades
Heartbeat
Ticker
```

Coinbase currently documents its Level 2 channel as delivering all updates needed to keep an order-book snapshot synchronised; updates provide the new quantity at a price level, and zero removes the level.

This gives MarketFlow a genuine event stream rather than fabricated CSV data.

---

# 6. Initial Instruments

Start with:

```text
BTC-USD
ETH-USD
```

Later add a small curated set such as:

```text
SOL-USD
LTC-USD
```

Do not subscribe to dozens of products merely to inflate event counts.

The project should scale primarily through:

> controlled replay of captured authentic events

rather than abuse of the external source.

---

# 7. External-Source Load Principle

Never benchmark Coinbase.

Use:

```text
public WebSocket
↓
capture once
↓
durable local/cloud raw archive
↓
replay internally at controlled rates
```

Performance experiments may replay:

```text
1×
10×
100×
```

the captured source rate.

Every benchmark must distinguish:

```text
unique authentic events
```

from:

```text
replayed event deliveries
```

---

# 8. High-Level Architecture

```text
Coinbase WebSocket
        ↓
Python Market Collector
        ↓
      Kafka
        ↓
   ┌────┴─────┐
   ↓          ↓
Raw S3      Spark Structured Streaming
Archive           ↓
             Delta Bronze
                  ↓
             Delta Silver
                  ↓
         Published lake datasets
                  ↓
             Snowflake
                  ↓
                dbt
                  ↓
        Facts / Dimensions / Marts
                  ↓
        SQL / BI / Analysts
```

Airflow orchestrates:

```text
batch ingestion
historical backfills
reconciliation
Databricks jobs
Snowflake loading
dbt builds/tests
quality checks
```

Airflow is **not** the streaming engine.

---

# 9. Responsibility of Each Major Technology

## Kafka

Responsible for:

> durable transport and replayable event distribution.

Learner should understand:

- records;
- topics;
- partitions;
- keys;
- brokers;
- offsets;
- consumer groups;
- retention.

---

## Spark

Responsible for:

> distributed transformation and stateful stream processing.

Learner should understand:

- DataFrames;
- lazy evaluation;
- stages;
- tasks;
- partitions;
- shuffle;
- joins;
- state;
- checkpoints;
- watermarks.

---

## Databricks

Responsible for:

> managed execution and governance around the Spark/Delta lakehouse.

Not:

> "Spark, but with a nice notebook."

---

## Delta Lake

Responsible for:

> reliable lakehouse tables over object storage, including transaction-log-based table semantics and support for batch/streaming processing.

Delta Lake extends Parquet with a transaction log and integrates directly with Spark/Structured Streaming.

---

## Airflow

Responsible for:

> orchestration of bounded workflows and dependencies.

A DAG defines tasks, their dependencies, and scheduling/retry behaviour; it does not replace the processing logic inside those tasks.

---

## Snowflake

Responsible for:

> analytical warehouse workloads.

It is where analysts should query curated relational models rather than reconstruct raw order-book events themselves.

Snowflake's virtual warehouses provide compute separately from stored data, allowing workload-specific compute sizing.

---

## dbt

Responsible for:

> SQL transformations, analytics modelling, documentation and warehouse-level tests.

dbt incremental models process selected new/updated source records after their initial build rather than recomputing an entire model every time.

---

# 10. Why Both Databricks and Snowflake?

This is a deliberate architecture decision.

Databricks provides the project's:

```text
high-volume streaming
Spark
lakehouse
Delta
distributed transformation
```

experience.

Snowflake provides the project's:

```text
warehouse
dimensional modelling
SQL serving
workload isolation
analytics engineering
```

experience.

The project should be able to explain:

> Why are we not simply doing everything in either system?

The answer should include trade-offs, not brand preference.

---

# 11. Layer Architecture

The platform uses four conceptual layers.

## Landing

Immutable source payloads.

```text
S3 / raw capture
```

## Bronze

Raw-but-queryable source events.

```text
Delta
```

## Silver

Validated, typed, deduplicated, event-time-correct domain records.

```text
Delta
```

## Warehouse

Dimensional analytical models.

```text
Snowflake + dbt
```

Databricks recommends progressively improving data quality through Bronze, Silver and Gold-style layers, with raw data preserved as a reproducible source of truth.

For MarketFlow, the final business-facing "Gold" semantics primarily live in the Snowflake/dbt warehouse layer.

---

# 12. Core Data Streams

## Level-2 Updates

Logical fields:

```text
venue
product_id
side
price
new_quantity
source_event_time
source_sequence
received_at
```

---

## Trades

```text
venue
product_id
trade_id
price
size
side
source_event_time
received_at
```

---

## Heartbeats

Used for:

- connection health;
- missed-message detection;
- feed monitoring.

---

# 13. Event Envelope

Internal Kafka message:

```text
event_id
event_type
schema_version

source
product_id

source_event_time
received_at
published_at

source_sequence

payload
```

---

# 14. Time Semantics

The learner must distinguish:

## Event time

When the market event occurred according to the source.

## Ingestion time

When MarketFlow received the event.

## Kafka time

When the event was written to Kafka.

## Processing time

When Spark processed it.

## Warehouse availability time

When the event became queryable through the analytical model.

These are different clocks.

---

# 15. Data-Latency Metrics

Track:

```text
source → collector
collector → Kafka
Kafka → Silver
Silver → warehouse
source → warehouse
```

The last one is:

> **end-to-end data freshness latency**

and should become a headline data-platform metric.

---

# 16. Kafka Topic Design

Initial topics:

```text
marketflow.l2.v1
marketflow.trades.v1
marketflow.heartbeat.v1
```

Later:

```text
marketflow.reference.v1
marketflow.dlq.v1
```

Do not create separate topics for every instrument.

---

# 17. Kafka Key

Default:

```text
product_id
```

or:

```text
venue + product_id
```

This provides stable partitioning for instrument-specific event ordering.

---

# 18. Kafka Ordering Guarantee

Do not say:

> Kafka guarantees ordering.

Correct:

> Kafka preserves record order within one partition.

Therefore the partition key determines which events can be assumed ordered relative to each other.

---

# 19. Consumer Groups

Examples:

```text
spark-market-processing
raw-archive-consumer
quality-monitor
```

Within one consumer group:

```text
partitions are divided between consumers
```

Different groups independently consume the same events.

---

# 20. Offset Semantics

The learner must understand:

```text
Kafka log
      ↓
consumer position
      ↓
committed offset
```

A processed message and a committed offset are not necessarily the same thing.

---

# 21. Delivery Semantics

Project-wide default assumption:

> **events may be processed more than once.**

Therefore downstream transformations must be designed for:

- idempotency;
- deduplication;
- deterministic keys.

Avoid unqualified claims of:

```text
exactly-once architecture
```

---

# 22. Raw Archive

Every received authentic event should eventually be recoverable from durable storage.

Canonical raw archive hierarchy might be:

```text
s3://marketflow/raw/
    source=coinbase/
    event_type=l2/
    date=2026-09-27/
    hour=13/
```

Exact partition layout requires measurement.

---

# 23. Immutable Raw Principle

Bronze/Silver bugs should be recoverable by reprocessing raw data.

Therefore:

> raw capture is append-only.

Do not rewrite history because parsing logic changed.

---

# 24. Bronze Tables

Example:

```text
bronze_l2_events
bronze_trade_events
```

Bronze retains:

- original payload;
- source metadata;
- ingestion metadata;
- schema/version.

Minimal transformation.

---

# 25. Silver Tables

Examples:

```text
silver_l2_updates
silver_trades
silver_best_bid_ask
silver_order_book_snapshots
silver_market_intervals
```

Silver handles:

- typing;
- validation;
- deduplication;
- malformed records;
- event-time logic;
- late data;
- canonical IDs.

---

# 26. Order-Book Reconstruction

Level-2 updates represent changing price-level state.

State:

```text
(product, side, price)
→ quantity
```

Incoming update:

```text
new_quantity > 0
→ replace level quantity

new_quantity = 0
→ remove level
```

This makes order-book reconstruction an authentic **stateful streaming** problem.

---

# 27. Derived Market Data Products

Potential Silver outputs:

### Best Bid / Ask

```text
timestamp
product
best_bid
best_ask
mid_price
spread
```

### Order Book Depth

```text
depth_5bps
depth_10bps
```

### Order Book Imbalance

A descriptive market metric.

### Trade Aggregations

```text
trade_count
volume
VWAP
```

over:

```text
1 sec
1 min
5 min
```

These are data products, not trading signals.

---

# 28. Spark Structured Streaming

MarketFlow must learn Structured Streaming genuinely.

Relevant concepts:

- streaming DataFrames;
- micro-batches;
- checkpoints;
- stateful operators;
- watermarking;
- Kafka integration;
- output modes.

---

# 29. Watermarks

Suppose:

```text
12:00 event
```

arrives at:

```text
12:03
```

A streaming window needs policy for how long late events remain acceptable.

A watermark expresses:

> how late event-time state is retained before old state may be finalised/evicted.

The learner must understand its correctness consequences.

---

# 30. Late Data

Late records must not simply be discarded without measurement.

Track:

```text
event_lateness_seconds
late_events_total
events_beyond_watermark_total
```

---

# 31. Out-of-Order Events

Event streams can arrive:

```text
E10
E12
E11
```

even if the source provides logical ordering.

Silver processing must define whether it:

- reorders;
- deduplicates;
- quarantines;
- rejects stale state.

---

# 32. Checkpointing

Spark streaming checkpoints capture progress/state needed for recovery.

Checkpoint location is part of the application's state.

It is not:

```text
a cache directory that can be deleted whenever convenient
```

Changing incompatible stateful query logic may require an explicit migration/new checkpoint.

---

# 33. Batch and Streaming Unification

The same transformation logic should be shared where practical between:

```text
historical backfill
```

and:

```text
live incremental stream
```

This is a major reason for using Spark + Delta.

Do not create separate transformation definitions that silently diverge.

---

# 34. Airflow Responsibility

Airflow workflows include:

```text
capture-health check
historical import
batch reprocessing
Databricks job trigger
Silver reconciliation
Snowflake load
dbt build
dbt tests
freshness validation
```

Airflow should **not** process each market event.

---

# 35. Airflow Backfills

Backfill is a first-class capability.

Example:

```text
rebuild 2026-08-01 → 2026-08-07
```

without corrupting:

```text
today's live pipeline
```

Required controls:

- bounded date range;
- idempotent output;
- separate run identity;
- reconciliation after completion.

---

# 36. Airflow Idempotency

Rerunning:

```text
silver_backfill(date=2026-08-01)
```

should produce the same logical result.

Avoid tasks whose correctness depends on:

```text
"hope this task only runs once"
```

---

# 37. Snowflake Ingestion Boundary

Snowflake receives curated warehouse-source data.

Do not directly dump every raw Kafka record into analyst-facing marts.

Possible:

```text
Silver Delta
→ S3 publication files
→ Snowflake staging
→ dbt
```

---

# 38. Snowflake Load Strategy

Initial:

```text
COPY INTO
```

from staged S3 files.

Later compare with:

```text
Snowpipe / continuous loading
```

conceptually or experimentally if cost permits.

Snowflake recommends treating loading/query compute intentionally; separate warehouses can isolate loading from analytical query workloads.

---

# 39. Snowflake Warehouses

Suggested logical compute:

```text
INGEST_WH
ANALYTICS_WH
DBT_WH
```

These may map to fewer physical configurations in cost-controlled development.

The important learning point is:

> compute workload isolation.

---

# 40. Dimensional Modelling

MarketFlow must learn classical warehouse modelling explicitly.

Not every analytical table should simply mirror source events.

---

# 41. Fact Tables

## `fct_trade`

Grain:

> one executed trade.

Possible columns:

```text
trade_key
product_key
venue_key
time_key

price
quantity
notional
side
event_timestamp
```

---

## `fct_market_interval`

Grain:

> one product × one fixed time interval.

Example:

```text
product
minute

open
high
low
close
volume
trade_count
VWAP
average_spread
average_depth
```

---

## `fct_order_book_snapshot`

Potential grain:

> one product × one selected snapshot timestamp.

Do not store an enormous full snapshot at every event unless justified.

---

# 42. Dimensions

## `dim_product`

```text
product_key
product_id
base_asset
quote_asset
status
valid_from
valid_to
```

## `dim_venue`

## `dim_date`

## `dim_time`

Potential later:

```text
dim_product SCD Type 2
```

---

# 43. Slowly Changing Dimensions

Suppose product metadata changes:

```text
trading status
tick size
display name
```

The warehouse may need historical truth.

SCD Type 2:

```text
same natural key
multiple dimension rows
valid_from
valid_to
is_current
```

The project must explain why historical facts join to the version valid at fact time.

---

# 44. dbt Project Structure

Example:

```text
models/
    staging/
    intermediate/
    marts/
        market/
```

Staging:

> rename/type/standardise.

Intermediate:

> reusable analytical transformations.

Marts:

> final dimensional/business models.

---

# 45. dbt Data Tests

Required:

```text
unique
not_null
relationships
accepted_values
```

plus custom tests.

dbt currently describes data tests as SQL assertions over models/sources and recommends testing primary-key uniqueness/non-nullness and source assumptions.

---

# 46. Example Custom Data Tests

Examples:

```text
best_bid <= best_ask

trade_size > 0

spread >= 0

interval_start < interval_end
```

Quality rules must encode real domain assumptions.

---

# 47. dbt Incremental Models

Large fact tables should not always full-refresh.

Compare:

```text
full refresh
```

against:

```text
incremental merge
```

Measure:

- runtime;
- compute;
- correctness.

---

# 48. dbt Snapshots

Use snapshots to learn historical record changes.

Candidate:

```text
product reference data
```

Use this to teach:

- source freshness;
- mutable source;
- SCD Type 2.

---

# 49. CDC Extension

Introduce one simulated operational database.

Example PostgreSQL tables:

```text
instrument
venue
account_reference
```

Changes are emitted by:

```text
Debezium
→ Kafka
```

This teaches:

> Change Data Capture is different from polling or normal application events.

---

# 50. CDC Semantics

Example:

```text
UPDATE instrument
SET status = 'SUSPENDED'
```

becomes a change event.

The downstream warehouse can then maintain historical dimension state.

---

# 51. ETL vs ELT

MarketFlow deliberately contains both.

## ETL-like

```text
Kafka
→ Spark transformation
→ Delta
```

## ELT-like

```text
load curated source into Snowflake
→ dbt SQL transformations inside warehouse
```

The learner should be able to explain when either pattern is appropriate.

---

# 52. Data Contracts

Every important dataset gets a contract.

Example:

```text
silver_trades

primary key:
venue + trade_id

required:
product_id
price
size
event_time

constraints:
price > 0
size > 0
```

---

# 53. Schema Evolution

Possible source change:

```text
new optional field
```

should not automatically break every pipeline.

Possible breaking change:

```text
price changes numeric representation
```

requires controlled migration.

Track:

```text
schema_version
```

where necessary.

---

# 54. Data Quality Categories

Distinguish:

## Structural quality

Schema/type valid.

## Completeness

Required data present.

## Uniqueness

Logical key not duplicated.

## Referential integrity

Fact references valid dimension.

## Temporal quality

Timestamp/order expectations.

## Business-domain quality

Example:

```text
best_bid <= best_ask
```

## Reconciliation quality

Counts/totals agree between layers.

---

# 55. Reconciliation

A pipeline can "succeed" and still lose data.

Therefore reconcile.

Example:

```text
Kafka input count
vs
Bronze count
vs
Silver accepted + quarantined count
```

Expected relationship:

```text
input
=
accepted
+
known rejected/quarantined
```

subject to precisely documented boundaries.

---

# 56. Lake-to-Warehouse Reconciliation

Compare:

```text
Silver trade count by product/hour
```

against:

```text
Snowflake fct_trade count
```

Also compare:

```text
volume
notional
min/max event time
```

Discrepancy should fail/alert.

---

# 57. Data Lineage

The learner should trace:

```text
Snowflake mart row
↓
dbt model
↓
Snowflake staging data
↓
Delta Silver
↓
Delta Bronze
↓
Kafka topic/partition/offset
↓
raw source capture
```

This is data lineage.

---

# 58. Data Freshness

For each dataset record:

```text
MAX(source_event_time)
```

and compare with current processing time.

Expose:

```text
freshness_seconds
```

per layer.

---

# 59. Data Freshness SLO

Do not invent final SLO initially.

Later define something like:

```text
under workload W:
99% of eligible market events reach Silver within X seconds
and warehouse marts within Y minutes
```

`X` and `Y` remain:

```text
TBD
```

until measured.

---

# 60. Data Platform Observability

Required metrics eventually include:

## Kafka

- input records/s;
- bytes/s;
- consumer lag;
- partition distribution.

## Spark

- input rows/s;
- processed rows/s;
- micro-batch duration;
- state-store size;
- shuffle read/write;
- failed batches.

## Airflow

- DAG success;
- task duration;
- retry count;
- backfill state.

## Snowflake

- load duration;
- query duration;
- warehouse usage;
- queued queries.

## dbt

- model runtime;
- test failures;
- freshness failures.

---

# 61. Distributed Processing Fundamentals

The learner must understand why Spark exists.

Start with:

```text
single Python process
```

then create a workload where:

- data exceed convenient single-process processing;
- partitioned parallel execution becomes useful;
- joins/shuffles become visible.

Do not begin by writing PySpark because "data engineering uses Spark."

---

# 62. Spark Lazy Evaluation

Transformations build a logical plan.

Execution occurs on an action.

Teach:

```text
logical plan
→ physical plan
→ stages
→ tasks
```

---

# 63. Spark Partitioning

A Spark partition is a unit of distributed work.

Too few:

```text
underutilised compute
```

Too many:

```text
scheduler overhead / tiny tasks / small files
```

Measure.

---

# 64. Spark Shuffle

Operations such as:

```text
groupBy
join
repartition
```

may require data movement between executors.

Shuffle often dominates distributed workloads.

The learner should inspect Spark UI before optimisation.

---

# 65. Data Skew

Example:

```text
BTC-USD
=
80% of events
```

If partitioning/grouping is poorly selected, one task may receive dramatically more work.

Required experiment:

> deliberately create a skewed replay.

Observe:

- task duration;
- partition size;
- stage completion.

---

# 66. Spark Join Strategies

Teach:

- shuffle join;
- broadcast join;
- partition-aware joins.

Do not configure hints without understanding.

Potential reference-data join:

```text
huge trade table
+
tiny product dimension
```

is a natural broadcast example.

---

# 67. Spark Performance Contract

Before optimisation:

1. freeze data;
2. record Spark config;
3. run baseline;
4. inspect Spark UI;
5. identify stage/task bottleneck.

Then optimise one factor.

---

# 68. Delta Table Design

Consider:

- table partitioning;
- file size;
- compaction;
- data skipping;
- update frequency.

Do not partition by extremely high-cardinality columns such as:

```text
trade_id
```

---

# 69. Small-File Problem

Streaming can generate many small files.

Consequences:

- metadata overhead;
- inefficient scans;
- slower downstream reads.

Required experiment:

```text
small frequent output
vs
compacted/optimised layout
```

---

# 70. Snowflake Performance Engineering

Potential experiments:

- warehouse sizing;
- query shape;
- materialised aggregations;
- clustering only if justified;
- incremental dbt models.

Snowflake explicitly notes that making a warehouse larger does not guarantee improved performance for every workload.

---

# 71. Cost Engineering

The project must make cost visible.

Metrics may include:

```text
Databricks compute duration / DBUs where available
Snowflake credits
S3 storage
warehouse runtime
```

Do not chase absolute cheapness.

Optimise:

```text
useful work / cost
```

---

# 72. Security

Although market data are public, infrastructure is not.

Required:

- secrets outside source control;
- AWS IAM least privilege;
- Snowflake RBAC;
- Databricks access controls;
- credential rotation concepts;
- encrypted transport;
- dependency pinning/scanning.

---

# 73. Snowflake RBAC

Suggested conceptual roles:

```text
MARKETFLOW_LOADER
MARKETFLOW_TRANSFORMER
MARKETFLOW_ANALYST
MARKETFLOW_ADMIN
```

`MARKETFLOW_ANALYST` should not require ingestion/write permissions.

---

# 74. AWS IAM

Spark/Databricks loading S3 should receive only necessary paths/actions.

Avoid:

```text
AdministratorAccess
s3:*
```

---

# 75. CI/CD

Pull request pipeline should eventually run:

```text
Python tests
schema/contract tests
Spark unit/integration tests
Airflow DAG import validation
dbt compile
dbt unit/data tests where possible
Terraform validate
```

Do not deploy broken transformations because the Python unit tests passed.

---

# 76. System Invariants — Ingestion

**INV-001 — Raw preservation**\
Captured authentic events are never silently overwritten.

**INV-002 — Event provenance**\
Every processed event traces to source/channel and ingestion metadata.

**INV-003 — Duplicate safety**\
Duplicate deliveries cannot create uncontrolled duplicate logical facts.

**INV-004 — Replay safety**\
Historical replay does not corrupt live logical datasets.

---

# 77. System Invariants — Streaming

**INV-005 — Event-time semantics explicit**\
Processing-time assumptions are never substituted silently for event time.

**INV-006 — Late-data policy explicit**\
Records beyond watermark follow defined policy.

**INV-007 — Partition ordering scoped**\
No global ordering assumption across Kafka partitions.

**INV-008 — Checkpoint ownership**\
One active streaming query owns a compatible checkpoint.

---

# 78. System Invariants — Data Quality

**INV-009 — Quarantine accounted**\
Invalid records do not disappear silently.

**INV-010 — Layer reconciliation**\
Critical counts/totals can be reconciled across pipeline boundaries.

**INV-011 — Warehouse keys stable**\
Fact grain and dimensional keys are defined explicitly.

**INV-012 — SCD history preserved**\
Historical dimension relationships remain reconstructible.

---

# 79. System Invariants — Operations

**INV-013 — Backfills isolated**\
Historical repair cannot silently corrupt live data.

**INV-014 — Idempotent orchestrated work**\
Safe reruns produce equivalent logical outputs.

**INV-015 — Data freshness visible**\
Stale data cannot appear current without indication.

**INV-016 — CV claims measured**\
No scale/performance metric exists without preserved workload evidence.

---

# 80. Functional Requirements — Ingestion

- **FR-001:** Connect to public market-data WebSocket.
- **FR-002:** Subscribe to configured products/channels.
- **FR-003:** Detect disconnect.
- **FR-004:** Reconnect boundedly.
- **FR-005:** Preserve receive timestamp.
- **FR-006:** Publish Kafka event.
- **FR-007:** Persist raw source event.
- **FR-008:** Expose feed health.
- **FR-009:** Support deterministic replay.

---

# 81. Functional Requirements — Kafka

- **FR-010:** Version topic contracts.
- **FR-011:** Use meaningful keys.
- **FR-012:** Configure retention.
- **FR-013:** Track consumer lag.
- **FR-014:** Support multiple consumer groups.
- **FR-015:** Handle duplicate records.
- **FR-016:** Quarantine poison messages where necessary.

---

# 82. Functional Requirements — Spark

- **FR-017:** Read Kafka via Structured Streaming.
- **FR-018:** Parse schemas.
- **FR-019:** Write Bronze Delta.
- **FR-020:** Build Silver tables.
- **FR-021:** Reconstruct order-book state.
- **FR-022:** Handle event time.
- **FR-023:** Handle late data.
- **FR-024:** Checkpoint streaming state.
- **FR-025:** Support historical batch input.
- **FR-026:** Expose streaming metrics.

---

# 83. Functional Requirements — Airflow

- **FR-027:** Orchestrate historical ingestion.
- **FR-028:** Trigger batch Spark/Databricks jobs.
- **FR-029:** Trigger Snowflake loading.
- **FR-030:** Trigger dbt.
- **FR-031:** Run reconciliation.
- **FR-032:** Support backfill.
- **FR-033:** Apply bounded retries.
- **FR-034:** Surface failures.

---

# 84. Functional Requirements — Snowflake/dbt

- **FR-035:** Load curated lake data.
- **FR-036:** Define dbt sources.
- **FR-037:** Build staging models.
- **FR-038:** Build dimensions.
- **FR-039:** Build fact tables.
- **FR-040:** Build analytical marts.
- **FR-041:** Add data tests.
- **FR-042:** Add incremental models.
- **FR-043:** Implement one SCD.
- **FR-044:** Document lineage/models.

---

# 85. Functional Requirements — CDC

- **FR-045:** Capture PostgreSQL changes.
- **FR-046:** Publish CDC through Kafka.
- **FR-047:** Distinguish insert/update/delete.
- **FR-048:** Apply changes downstream idempotently.
- **FR-049:** Maintain historical warehouse state.

---

# 86. Functional Requirements — Operations

- **FR-050:** Monitor freshness.
- **FR-051:** Monitor Kafka lag.
- **FR-052:** Monitor Spark throughput.
- **FR-053:** Monitor failed/quarantined records.
- **FR-054:** Monitor Airflow workflows.
- **FR-055:** Monitor warehouse build state.
- **FR-056:** Produce operator runbooks.
- **FR-057:** Support failure/recovery exercises.

---

# 87. Failure Model

| Failure                        | Required behaviour                                      |
| ------------------------------ | ------------------------------------------------------- |
| Coinbase disconnected          | bounded reconnect; visible ingestion gap                |
| Feed event malformed           | quarantine/metric; pipeline continues safely            |
| Collector crashes              | Kafka/raw replay allows recovery                        |
| Kafka unavailable              | ingestion follows bounded buffering/failure policy      |
| Duplicate Kafka event          | no duplicate logical fact                               |
| Consumer restarted             | resumes from committed/checkpointed position            |
| Spark job crashes              | restart from compatible checkpoint                      |
| Checkpoint lost                | controlled rebuild/replay procedure                     |
| Late event                     | watermark policy applied and measured                   |
| Very late event                | quarantine/correction path                              |
| Hot Kafka partition            | lag/skew becomes visible                                |
| Spark executor failure         | task retry/recovery                                     |
| Spark transform schema changes | contract failure/migration                              |
| Delta malformed state          | fail visibly; raw archive retained                      |
| Airflow task fails             | bounded retry / failure                                 |
| Backfill rerun                 | equivalent logical result                               |
| Snowflake unavailable          | lake remains authoritative upstream; load retries later |
| Snowflake load partially fails | reconciliation detects discrepancy                      |
| dbt test fails                 | affected mart not considered healthy                    |
| CDC duplicate                  | idempotent downstream application                       |
| CDC delete                     | historical semantics preserved                          |
| S3 unavailable                 | pipeline fails visibly; no fabricated success           |
| Credentials expire             | failure visible; no secret fallback in code             |
| Warehouse query overload       | compute isolation/tuning                                |
| Pipeline falls behind          | freshness/lag alert                                     |
| Observability service fails    | processing continues where safe                         |

---

# 88. Versioned Development Philosophy

Every version is runnable end-to-end.

The project must not become:

```text
V0 Kafka
V1 Spark
V2 Databricks
V3 Snowflake
V4 dbt
```

Instead:

```text
source
→ transport
→ transform
→ store
→ model
→ query
→ observe
```

exists from the beginning.

Sophistication evolves.

---

# 89. V0 — Walking Skeleton

## Purpose

> Can one financial event cross the entire data pipeline?

### Source

Use checked-in fake events.

### Kafka

One local broker/topic.

### Spark

Tiny PySpark Structured Streaming job.

### Storage

Local Delta/Parquet.

### Analytical output

Simple SQL query:

```text
trades per minute
```

### Orchestration

One manual command/script.

No Airflow yet.

### Quality

One schema check.

### Observability

Print/log:

```text
received
processed
written
```

### Exit

Learner explains:

```text
producer
→ Kafka topic
→ partition
→ Spark consumer
→ Delta table
→ SQL
```

---

# 90. V1 — Authentic Local Data Platform

## Purpose

> Can real continuously arriving market data be captured and reconstructed reliably?

### Source

Real Coinbase feeds.

### Kafka

Separate trade/L2 topics.

### Raw archive

Immutable local/S3-compatible files.

### Spark

Real:

- parsing;
- event time;
- order-book state;
- trade aggregation.

### Delta

Bronze + Silver.

### Airflow

Introduce for:

- batch replay;
- daily quality;
- reconciliation.

### dbt

Introduce locally using an inexpensive local analytical database where appropriate to learn:

- models;
- refs;
- sources;
- tests;
- facts/dimensions.

Snowflake comes next.

### Docker Compose

Run:

- Kafka;
- Spark/local services;
- Airflow;
- optional PostgreSQL.

### Measurements

Establish:

- unique events;
- ingress rate;
- Spark processing rate;
- latency;
- raw/Silver counts.

### Exit

A real event reaches a queryable analytical table and can be replayed.

---

# 91. V2 — Managed Lakehouse & Warehouse MVP

## Purpose

> Can the local architecture become a credible cloud-style data platform?

This is the first strongly CV-worthy version.

### AWS S3

Raw/landing storage.

### Databricks

Run Spark workloads on Databricks.

### Delta Lake

Bronze/Silver tables.

### Snowflake

Introduce warehouse.

### dbt + Snowflake

Rebuild warehouse modelling properly:

```text
staging
dimensions
facts
marts
```

### Airflow

Orchestrate:

```text
historical input
→ Databricks batch processing
→ publish curated files
→ Snowflake load
→ dbt build
→ dbt tests
→ reconciliation
```

The streaming job remains continuously/independently operated rather than being restarted every few minutes by Airflow.

### Dimensional Model

Required:

```text
dim_product
dim_venue
dim_date
fct_trade
fct_market_interval
```

### Data Quality

Required across:

- ingestion;
- Silver;
- warehouse.

### CI

Introduce.

### Measurements

- end-to-end freshness;
- consumer lag;
- micro-batch time;
- Snowflake load time;
- dbt build time;
- query latency.

### Exit

Real data reaches:

```text
Coinbase
→ Kafka
→ Databricks/Spark
→ Delta
→ Snowflake
→ dbt mart
```

with reproducible orchestration and tests.

---

# 92. V3 — Reliability, CDC & Schema Evolution

## Purpose

> Can MarketFlow remain trustworthy when inputs, schemas and processing fail?

### CDC

Introduce:

```text
PostgreSQL
→ Debezium
→ Kafka
```

for reference data.

### SCD Type 2

Use CDC/reference changes to maintain historical `dim_product`.

### dbt Snapshots

Learn/compare snapshot approach where suitable.

### Schema Evolution

Rehearse:

```text
additive change
breaking change
```

### Late Data

Inject late events.

### Out-of-Order Data

Inject controlled reordering.

### DLQ/Quarantine

Introduce explicit operator path.

### Reconciliation

Automate comparisons:

```text
raw ↔ Bronze
Bronze ↔ Silver
Silver ↔ Snowflake
```

### Backfill

Run multi-day historical repair while live pipeline remains active.

### Failure Exercises

- kill collector;
- kill Spark job;
- restart consumer;
- Snowflake outage;
- dbt failure.

### Exit

Every important failure has:

```text
detection
authoritative state
recovery
verification
```

---

# 93. V4 — Portfolio-Grade Scale & Performance Engineering

## Purpose

> Where does the platform saturate, what costs dominate, and what engineering improvements actually matter?

### Freeze benchmark

Record:

- source replay;
- Kafka partitions;
- Spark config;
- cluster size;
- table versions;
- Snowflake warehouse;
- dbt project revision.

### Replay Scale

Run controlled:

```text
1×
10×
100×
```

or whatever the hardware can honestly support.

### Kafka Experiments

Compare partition counts.

Measure:

- throughput;
- consumer lag;
- skew.

### Spark Experiments

Required:

#### Partition count

#### Shuffle partitions

#### Join strategy

#### Data skew

#### Small-file behaviour

#### Incremental vs full batch

### Databricks

Use Spark UI/job metrics to identify the bottleneck.

### Delta

Measure:

```text
unoptimised files
vs
compacted/optimised
```

### Snowflake

Benchmark:

- warehouse size;
- load/query separation;
- dbt incremental model.

### dbt

Compare:

```text
full refresh
vs
incremental
```

### Backfill

Measure:

```text
N hours/days
→ complete rebuild duration
```

### Data-Freshness SLO

Freeze final measured target.

### Incident

Example:

> BTC-USD traffic concentrated most data into one key range, causing Spark task skew and growing downstream freshness lag despite apparently healthy aggregate throughput.

### Exit

Publish final:

- capacity envelope;
- latency;
- throughput;
- cost;
- bottleneck;
- recovery behaviour.

---

# 94. V5 — Optional Advanced Extension

Choose one.

## Option A — Multi-Venue Platform

Add a second market-data source.

Challenges:

- differing schemas;
- symbol mapping;
- timestamps;
- canonical contracts;
- venue dimension;
- cross-venue reconciliation.

## Option B — Advanced Stream Processing

Add more complex stateful operations:

- stream-stream joins;
- session windows;
- deeper watermark experiments.

## Option C — Table-Format Interoperability

Compare:

```text
Delta
vs
Iceberg concepts/implementation
```

Preferred:

> **Multi-Venue Platform**

because it adds authentic data integration complexity without introducing another unrelated framework.

---

# 95. Required Experiment Programme

## EXP-001 — Single-process baseline

Python parses captured events.

---

## EXP-002 — Kafka ingestion

Measure transport/lag.

---

## EXP-003 — Spark vs naive processing

Show why distributed processing becomes valuable.

---

## EXP-004 — Partition count

---

## EXP-005 — Event-time watermark

Compare late-event policies.

---

## EXP-006 — Skew

Create hot product distribution.

---

## EXP-007 — Join strategy

Broadcast vs shuffle where applicable.

---

## EXP-008 — Delta file layout

Small files vs optimised layout.

---

## EXP-009 — Full vs incremental Spark processing

---

## EXP-010 — dbt full refresh vs incremental

---

## EXP-011 — Snowflake compute sizing

---

## EXP-012 — Batch backfill

---

## EXP-013 — CDC duplicate/replay

---

## EXP-014 — Consumer failure recovery

---

## EXP-015 — End-to-end freshness under rising load

---

# 96. Portfolio Measurement Contract

## Event Scale

Candidate:

> Ingested and processed **N authentic/replayed market events**.

Always distinguish:

```text
unique
vs
replayed
```

---

## Streaming Performance

Candidate:

> Sustained **X events/s** through Kafka/Spark while maintaining **Y-second p95 Silver freshness**.

---

## Spark Optimisation

Candidate:

> Reduced Spark processing/backfill runtime from **X to Y** through partition, join and file-layout optimisation.

---

## Warehouse

Candidate:

> Reduced analytical query p95 from **X to Y** through dimensional modelling and warehouse/query optimisation.

---

## dbt

Candidate:

> Reduced dbt transformation runtime by **X%** using incremental fact models while preserving reconciliation tests.

---

## Reliability

Candidate:

> Recovered **N-event** processing backlog in **T minutes** following injected Spark/warehouse failure with zero unexplained reconciliation discrepancy.

---

## Data Quality

Candidate:

> Enforced **N data contracts/tests** across ingestion, lakehouse and warehouse layers.

Do not use test count alone as a headline accomplishment.

---

# 97. CV Claims Ledger

Maintain:

```text
docs/cv_claims.md
```

## MF-001 — Platform

Candidate:

> Built MarketFlow, a real-time financial data platform ingesting public market events through Kafka and processing batch/streaming workloads using PySpark, Databricks/Delta Lake, Airflow, Snowflake and dbt.

---

## MF-002 — Scale

Candidate:

> Processed **X events/s** across **N Kafka partitions** while maintaining **Y-second p95** end-to-end lakehouse freshness.

Status:

```text
NOT MEASURED
```

---

## MF-003 — Spark optimisation

Candidate:

> Reduced Spark backfill runtime **X×** by profiling shuffle/skew and optimising partitioning, joins and Delta file layout.

Status:

```text
NOT MEASURED
```

---

## MF-004 — Warehouse

Candidate:

> Designed Snowflake dimensional models with dbt, including incremental fact tables and Type-2 dimensions, reducing analytical query/build runtime by **X%**.

Status:

```text
NOT MEASURED
```

---

## MF-005 — Reliability

Candidate:

> Implemented idempotent replay, late-data handling and cross-layer reconciliation, recovering **N events** after injected consumer/warehouse failures without unexplained loss.

Status:

```text
NOT MEASURED
```

---

## MF-006 — CDC

Candidate:

> Built PostgreSQL→Debezium→Kafka CDC pipelines to maintain historical warehouse dimensions under changing reference data.

Evidence may be qualitative.

---

# 98. Benchmark Manifest

Every performance claim records:

```text
benchmark_id
timestamp
git_revision

machine / cluster
CPU
RAM

Kafka version
partition count

Spark version
executor count
executor CPU
executor memory
shuffle partitions

Databricks runtime where relevant

Delta table/version
input event count
unique event count
replay multiplier

Snowflake warehouse

dbt version

duration
warmup

throughput
p50/p95/p99 freshness
consumer lag
Spark task metrics
shuffle bytes
files written

raw results path
```

---

# 99. Security & Governance Evidence

By V4 produce:

```text
docs/security/
docs/governance/
```

Cover:

- AWS IAM;
- secrets;
- Snowflake RBAC;
- Databricks access;
- lineage;
- retention;
- data contracts;
- dependency scanning.

No personal/customer data are required.

---

# 100. Required ADRs

Likely:

### ADR-001 — Public market source

### ADR-002 — Kafka topic/key design

### ADR-003 — Raw archive layout

### ADR-004 — Bronze/Silver semantics

### ADR-005 — Watermark policy

### ADR-006 — Order-book reconstruction

### ADR-007 — Delta partition strategy

### ADR-008 — Databricks vs Snowflake responsibilities

### ADR-009 — Warehouse dimensional grain

### ADR-010 — dbt incremental strategy

### ADR-011 — CDC architecture

### ADR-012 — SCD implementation

### ADR-013 — Airflow orchestration boundary

### ADR-014 — Backfill isolation

### ADR-015 — Final freshness SLO

---

# 101. Required Test Portfolio

## Unit

- parsers;
- keys;
- transformations;
- quality rules.

## Kafka integration

- produce;
- consume;
- duplicate;
- replay;
- partition key.

## Spark

- batch transformations;
- streaming transformations;
- watermark;
- late records;
- deduplication.

## Delta

- repeat writes;
- schema evolution;
- partition outputs.

## Airflow

- DAG import;
- task dependencies;
- retry;
- backfill parameters.

## Snowflake/dbt

- model keys;
- relationships;
- accepted values;
- incremental behaviour;
- SCD semantics.

## CDC

- insert;
- update;
- delete;
- duplicate replay.

## Reconciliation

- deliberate missing rows;
- duplicate rows;
- incorrect totals.

## Failure

- source disconnect;
- Kafka restart;
- Spark failure;
- warehouse outage.

---

# 102. Required Demo

A strong final demo:

1. start live market collector;
2. inspect Kafka events;
3. show Bronze ingestion;
4. show Silver transformed records;
5. show reconstructed best bid/ask;
6. open Spark UI;
7. show Snowflake staging;
8. show dbt lineage;
9. query `fct_trade`;
10. query analytical mart;
11. inject a duplicate;
12. show deduplication;
13. inject late data;
14. show watermark handling;
15. change PostgreSQL reference row;
16. show Debezium CDC;
17. show SCD dimension history;
18. stop Spark consumer;
19. show Kafka lag increasing;
20. restart;
21. show backlog draining;
22. run Airflow historical backfill;
23. show reconciliation passing;
24. show before/after Spark benchmark.

---

# 103. Required Portfolio Artefacts

```text
README.md
PROJECT_SPEC.md

docs/
    architecture/
    adr/
    data_contracts/
    dimensional_model/
    quality/
    lineage/
    benchmarks/
    incidents/
    runbooks/
    security/
    cost/
    cv_claims.md

schemas/
airflow/
dbt/
spark/
infra/
tests/
```

---

# 104. Suggested Repository Boundaries

```text
marketflow/
    ingestion/
        collector/

    schemas/

    spark/
        bronze/
        silver/
        batch/
        streaming/

    airflow/
        dags/

    dbt/
        models/
        tests/
        snapshots/

    cdc/

    infra/
        docker/
        terraform/

    tests/

    benchmarks/

    docs/
```

Do not create every directory on day one.

---

# 105. Instructions to the Teaching AI

`PROJECT_SPEC.md` defines:

> **what MarketFlow becomes.**

`TEACHING_STYLE.md` defines:

> **how the learner builds it.**

Both are binding.

---

# 105.1 Start Small

Do not begin with:

```text
Kafka
+
Spark
+
Airflow
+
Databricks
+
Snowflake
+
dbt
```

all at once.

Start with:

```text
one event
→ one Kafka topic
→ one Spark transformation
→ one table
```

Then evolve.

---

# 105.2 One Major Systems Concept at a Time

When first teaching Kafka:

do not simultaneously introduce:

- Spark watermarks;
- Airflow DAGs;
- Delta internals.

When first teaching Spark shuffle:

do not hide it behind Databricks optimisation buttons.

---

# 105.3 Naive Before Scalable

Before Spark:

build a bounded Python baseline.

Before incremental dbt:

build full refresh.

Before partition optimisation:

run poor/default partitioning.

Before reconciliation:

demonstrate silent discrepancy.

---

# 105.4 Teach Kafka Mechanically

Learner must explain:

```text
producer
topic
partition
offset
consumer
consumer group
```

without Spring/Databricks abstractions.

---

# 105.5 Teach Spark Mechanically

Learner must explain:

```text
driver
executor
partition
task
stage
shuffle
```

before performance optimisation.

---

# 105.6 Do Not Say Exactly Once Casually

Always ask:

> Exactly once where?

Kafka delivery?

Spark state?

Delta commit?

Snowflake load?

Warehouse fact?

Prefer:

> at-least-once transport + idempotent logical effects

where that describes the implementation.

---

# 105.7 Event Time Before Watermarks

Do not teach watermark syntax until the learner understands why processing time is insufficient.

---

# 105.8 Airflow Is Not the Stream Processor

Do not implement:

```text
Airflow DAG every second
→ pull market events
```

to imitate streaming.

---

# 105.9 Databricks Must Not Hide Spark

The learner must use:

- Spark UI;
- plans;
- stage/task metrics;
- partition counts.

Managed tooling cannot replace understanding.

---

# 105.10 Snowflake Must Not Hide SQL Design

The learner must understand:

- grain;
- fact;
- dimension;
- key;
- historical dimension;
- warehouse compute.

---

# 105.11 dbt Must Not Become "SQL in Files"

Teach:

```text
source
→ ref dependency graph
→ model
→ test
→ documentation
→ lineage
```

---

# 105.12 Testing Is Part of Pipeline Design

A data-quality check is not a final polish item.

When introducing a transformation, define:

> what incorrect data would this allow if we do not test it?

---

# 105.13 Backfills Must Be Designed Early

Do not wait for V4 to discover the pipeline cannot reproduce history.

---

# 105.14 Preserve Raw Inputs

If a transformation is wrong:

> rebuild.

Do not manually repair every downstream output.

---

# 105.15 Profile Before Spark Optimisation

Do not randomly:

```text
repartition(200)
cache()
broadcast()
```

Profile first.

---

# 105.16 One Optimisation at a Time

Do not simultaneously change:

```text
partitions
executor count
join strategy
file size
```

and claim one caused the improvement.

---

# 105.17 Distinguish Unique and Replayed Events

Never write:

> processed 100M market events

if this means:

```text
1M authentic events replayed 100 times.
```

Correct:

> benchmarked 100M event deliveries using controlled replay of a 1M-event authentic capture.

---

# 105.18 Cost Matters

Cloud optimisation is not solely:

> fastest possible.

Compare:

```text
runtime
freshness
cost
```

---

# 105.19 Preserve Failed Approaches

If:

```text
more Spark partitions
```

makes runtime worse:

keep the experiment.

If a larger Snowflake warehouse does not help:

keep it.

Those are strong engineering lessons.

---

# 105.20 No Invented Metrics

Until measured:

```text
TBD
NOT MEASURED
```

applies to:

- event count;
- throughput;
- latency;
- lag;
- cost;
- query improvement;
- backfill improvement.

---

# 106. Final Completion Standard

MarketFlow is complete when the learner can explain and demonstrate:

## Python / SQL

- collectors;
- transformations;
- analytical SQL.

## Kafka

- topics;
- partitions;
- keys;
- offsets;
- groups;
- retention;
- replay.

## Spark

- DataFrames;
- lazy execution;
- tasks;
- stages;
- partitions;
- shuffles;
- joins;
- Structured Streaming;
- checkpoints;
- watermarks.

## Databricks

- Spark execution;
- Delta;
- lakehouse;
- jobs;
- governance concepts.

## Delta Lake

- Bronze/Silver;
- transactional tables;
- schema evolution;
- batch + streaming;
- file optimisation.

## Airflow

- DAGs;
- dependencies;
- scheduling;
- retries;
- backfills;
- orchestration.

## Snowflake

- warehouses;
- staging;
- loading;
- dimensional data;
- query profiling;
- workload separation.

## dbt

- sources;
- refs;
- staging;
- facts;
- dimensions;
- incremental models;
- snapshots;
- tests;
- documentation.

## Data Warehousing

- fact grain;
- dimensions;
- star schema;
- SCD Type 2.

## CDC

- PostgreSQL WAL/change events;
- Debezium;
- insert/update/delete;
- idempotent application.

## Reliability

- duplicates;
- late events;
- consumer failure;
- replay;
- warehouse outage;
- backfills;
- reconciliation.

## Cloud

- S3;
- IAM;
- Databricks;
- Snowflake;
- Terraform.

## Performance

- Kafka lag;
- Spark throughput;
- shuffle;
- skew;
- partitioning;
- file sizing;
- warehouse query performance;
- cost.

---

# 107. Expected Final CV Story

A mature CV entry might eventually resemble:

> **Built MarketFlow, a real-time financial data platform ingesting public Level-2/trade events through Kafka and processing batch/streaming workloads using PySpark, Databricks/Delta Lake, Airflow, Snowflake and dbt.**

> **Sustained X events/s at Y-second p95 end-to-end freshness across N Kafka partitions, with event-time watermarking, idempotent replay, schema evolution and cross-layer reconciliation under injected consumer/warehouse failures.**

> **Reduced Spark backfill runtime X× by profiling shuffle/skew and optimising partitioning, joins and Delta file layout across an N-million-event controlled replay workload.**

> **Designed Snowflake star-schema marts with dbt incremental fact models and Type-2 dimensions fed by PostgreSQL/Debezium CDC, reducing analytical query/build runtime by X%.**

Only measured claims may be used.

---

# 108. Final Project Principle

MarketFlow is not successful because its README contains:

```text
Kafka
Spark
Airflow
Databricks
Snowflake
dbt
```

It is successful if the learner can say:

> I know where a market event enters the system, how Kafka partitions and orders it, how Spark reasons about event time and late data, why a shuffle happened, how Delta lets me rebuild curated datasets, why Airflow orchestrates a backfill rather than serving as a stream processor, why the warehouse has facts and dimensions rather than copies of raw events, how dbt incrementally transforms them, how CDC changes historical dimensions, how I detect missing data between layers, where the platform falls behind, and which measured engineering change improved that bottleneck.

The central principle is:

> **A trustworthy data platform is not defined by how much data it stores; it is defined by whether data can be traced, reproduced, validated, recovered and served efficiently as it changes.**
