# Current state — simplified V0

Implemented and locally verified: three synthetic trades, producer, independent
Kafka inspector, one Spark parse/type/schema-flag function, a bounded streaming
Parquet writer, and a SQL minute-count reader. Docker/Make provide one runtime.
V0 implementation is ready for learner review; understanding remains a checkpoint.

Boundary: fake data, one broker, local Spark, delivery counts, no business
deduplication, no continuous running service and no production recovery claim.
No Airflow, cloud services, Delta, Snowflake or dbt implementation in this folder.

Copied guidance and history are self-contained references. No script imports
the parent project. The old files/data were archived and removed with the user's
explicit approval. The parent holds a fresh Git repository for this V0 baseline;
the previous local Git history was reset at the user's request. V0 is the only
active project. No remote history was changed or pushed.

## Verification — 2026-10-15

- `make build`: passed (Python 3.13.7, Java 21, PySpark 4.2.0,
  kafka-python 3.0.11, pytest 9.1.1; separate pinned Kafka 4.3.1 image).
- `make test`: 2 passed. Valid bytes become typed decimal/time columns and
  correct minute counts; one bad price remains visible and is excluded from SQL.
- `make verify`: 1 passed. Actual producer/inspector/stream/query scripts:
  3 acknowledged deliveries at partition 0 offsets 0–2 → 3 saved rows;
  BTC 12:00 UTC count 2, ETH 12:01 UTC count 1. Same-checkpoint restart processes
  0 new rows and the subsequent actual SQL CLI still reports 3 written rows.
- Logs/tables/checkpoint: `data/verification-20261015T191704Z/test_pipeline_and_checkpoint_r0/`.
  Build/test/verification logs are at `data/`. These ignored files remain local.
- No default practice-topic deliveries or practice output were created; follow
  README from its first command. This project does not publish a host Kafka port.

These are synthetic correctness observations, not a throughput/recovery benchmark.
There is no abrupt-crash or data-loss test. Do not delete a checkpoint separately
from its output or point it at a different topic. Next: inspect the six source
files with docs/flow.md; explain the pipeline before advancing to V1.

## Independence and cleanup — 2026-10-15

An external temporary copy (without parent code/data/environments) successfully
built, passed 2 Spark tests and passed the real pipeline/restart test: 3 synthetic
deliveries → 3 saved rows, then 0 new rows on restart. Its logs/output are retained
under `data/independence-verification-20261015/`.

Before removal, `data/legacy-backup-20261015/old-project.tar.gz` was verified
against 3,012 old files by SHA-256, including uncommitted source, authentic captures
and verification evidence. The adjacent manifest records hashes; old environment
package lists are retained. Re-creatable venv/cache directories were excluded.
Root now contains only .git and MarketFlowV0. Old services were stopped without
deleting their volumes. Nothing in V0's processing code changed.

The archive preserves old bytes, not a promise that relocated Spark checkpoints
or old absolute-path manifests can be resumed directly.
Current lesson remains V0 review, starting with JSON → bytes → acknowledged send.

After removal, verification from this retained folder also passed: `make test`
2 passed; `make verify` 1 passed (3 deliveries → 3 rows; restart adds 0).
Logs: `data/cleanup-tests.log`, `data/cleanup-verify.log` and
`data/verification-20261015T193149Z/`. No default practice data was published.

## Fresh starting commit — 2026-10-15

The user explicitly authorised replacing the previous local Git history with one
V0 starting commit. Tracked content is the retained source, fixtures, build files,
guidance and documentation. Generated data, logs and the old-project archive stay
ignored. The origin URL is retained for convenience; no push is performed.
Processing code is unchanged from the successful post-removal verification above.
Current work is a theory recap and learner review, not the next implementation.
