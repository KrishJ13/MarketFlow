# V0–V2 Implementation Plan

Reconciled 2026-10-14 against implementation revision `21f2e93`; initial audit was at `441ab95`. Endpoint: **V2 only**. No V3+ implementation.

Statuses: DONE means bounded behaviour verified; IN PROGRESS means code exists with a verification or behaviour gap; TODO means remaining work. No whole-version completion is inferred from individual DONE rows. V0 letter labels below are audit planning identifiers introduced here; they are not existing release numbers.

## V0 — finish verification of the existing skeleton

| Slice | Status | Evidence / remaining work |
| --- | --- | --- |
| V0-A: deterministic event fixtures/load | DONE | Four tracked synthetic fixtures; loader and JSON parsing passed. |
| V0-B: local Kafka producer/consumer | DONE | Isolated real-broker test: acknowledgments/coordinates, three initial consumer rows, zero after commit, two backlog deliveries after resume. |
| V0-C: Spark typing and schema flag | DONE (bounded transformation) | Tolerant decimal/time conversion and explicit Boolean flag; 40 real-Spark cases passed; real Kafka/Parquet exit verification completed in V0-G. |
| V0-D: checkpointed Parquet output | DONE | Fresh checkpoint: three initial rows, five after backlog, still five after no-new-data restart; exact Kafka coordinates match. |
| V0-E: stored-data trades-per-minute SQL | DONE | Existing SQL script passed against local Parquet; counts delivery rows. |
| V0-F: schema/typing regression tests | DONE | Converted to pytest at user request: 19 real-Spark cases passed; existing transformation unchanged; both runs preserved. |
| V0-F1: explicit invalid-row typing | DONE | 15 failures reproduced before fix; 40 passed after fix under both ANSI settings; mixed-batch rows/coordinates retained. |
| V0-G: reproducible exit demonstration | DONE | Opt-in real Kafka/Spark exit test passed; actual SQL and written-count scripts verified, including expected-count failure. Logs and runbook preserved. |

All V0 implementation/verification slices are complete. The learner explain-back remains a review checkpoint, not a competence claim inferred from tests. V1.1 through V1.16 have been implemented and verified as recorded below; V2.1 is locally implemented with real AWS checks pending. V1 exit is demonstrated for bounded authentic trades, with continuous/L2/orchestration limits explicit. Existing baselines and historical failed runs are retained.

## Completed slice — V0-F

Existing transformation extracted into `spark/v0/trade_transform.py`; writer uses it. Eight pytest test functions (19 collected cases) assert four valid fixtures, exact decimals/timestamps/coordinates, missing fields, malformed JSON, wrong type/version, null flags, ANSI cast errors and ANSI-off outcomes. Negative inputs are small fixture mutations in tests. Pytest 9.1.1 is pinned in `requirements-dev.txt`; no production dependency added. Command: `.venv/bin/python -B -m pytest -v -p no:cacheprovider`; result: 19 passed. Historical V0-F raw evidence: `docs/verification/v0-f-pytest.log`; earlier unittest evidence retained in `docs/verification/v0-f-unittest.log`. No validation policy, Kafka source, sink or checkpoint behaviour changed.

## Completed slice — V0-F1

`try_cast` retains decimal(20,8) while converting malformed/overflow values to null; `try_to_timestamp` retains the timestamp format and returns null for invalid values. `coalesce(predicate, false)` prevents nullable flags. ANSI is not disabled or changed by the transformation. No filters, deduplication or new domain rules added; output columns/types and Kafka coordinates retained.

Tests run under both ANSI settings: four valid fixtures, missing/explicit-null type/version, other missing fields, malformed JSON, invalid decimal/time, decimal overflow, impossible date, and mixed valid/invalid/duplicate deliveries. Before fix: 15 failed / 25 passed. After fix: 40 passed. Evidence: `docs/verification/v0-f1-before-pytest.log` and `docs/verification/v0-f1-after-pytest.log`. Prior V0-F baseline logs remain unchanged.

## Completed slice — V0-G

Existing scripts gained optional topic/group/storage environment settings with unchanged defaults; streaming writer optionally uses AvailableNow to catch up and terminate. Written-count script optionally asserts an expected count and safely treats the ID as a literal. The opt-in `tests/test_v0_exit.py` executes actual scripts against a unique single-partition topic and fresh Parquet/checkpoint state.

Exit test result: 1 passed. Five synthetic deliveries account for four valid rows and one invalid row; three valid event IDs, with a deliberate repeated publication. Restart resumes checkpointed offsets; no-new-data restart leaves the row count unchanged. Actual SQL aggregates and positive/negative written-count checks passed. First attempt exposed missing connector at spark-submit launch; fixed the runner to pass the existing connector explicitly. Raw evidence: `docs/verification/v0-g/`; runbook and learner explanation: `docs/v0_exit.md`.

## Completed slice — V1.1 (simplified for undergraduate learning)

Simple BTC-USD observer: receive a message with UTC receipt time, flatten its trades, and print each with the exact raw message. Uses ordinary Python exceptions, one source-error check and `finally` cleanup. Five-message default and ten-second socket timeout; detailed validators, duration option and custom error-reporting/counter machinery removed at user request. Existing synthetic example and websocket-client requirement retained.

Current verification: **5 focused tests passed; default suite 45 passed / 1 opt-in skip**. Offline readback reproduced all 104 observations from the earlier authentic capture. Evidence: `docs/verification/v1-1/*-simplified.log`; explanation: `docs/v1_trade_collector.md`. Earlier 40-test collector/80-test suite and live smoke results are retained as historical evidence, not current coverage. No new live run or performance/unique-volume claim.

## Completed slice — V1.2

One small reconnect loop catches only OS/socket connection errors, closed connections and idle timeouts. Close failed socket, report possible ingestion gap, wait one second and resubscribe. Default: initial attempt plus at most three reconnects across the whole run; message count does not reset. Parsing and output remain outside retry handling. UTC status/failure logs go to stderr; raw/receipt JSON observations remain unchanged.

Verification: 9 collector tests passed (5 V1.1 + 4 focused V1.2); full default suite 49 passed / 1 opt-in skip. Deterministic offline failures only, no public provider traffic, new dependency or performance metric. Evidence: `docs/verification/v1-2/`; learning explanation: `docs/v1_reconnect.md`. Reconnection does not recover missed trades or remove duplicates.

## Completed slice — V1.3

`publish_trades.py` reuses the collector via a small optional callback. Versioned JSON trade envelope retains stable venue/product/trade ID, source/receipt/send-attempt times, sequence, untouched trade and exact raw message. Separate default topic `marketflow.coinbase.trades.v1`; UTF-8 product key; wait for each acknowledgment and print coordinates. Kafka errors occur outside WebSocket reconnect handling; producer/socket cleanup retained. V0 and stdout-only collector defaults remain unchanged.

Verification: 12 focused tests passed (9 existing + 3 contract/publish tests); default suite 52 passed / 2 opt-in skips; separately opted-in real Kafka roundtrip 1 passed. Three-partition isolated topic: one earlier authentic observation delivered twice, same BTC-USD key/ID, partition 0 offsets 0 and 1, exact trade/raw/receipt readback and acknowledgment reconciliation. No new source traffic or unique-volume/performance claim. Evidence: `docs/verification/v1-3/`; explanation/contract: `docs/v1_trade_topic.md`.

## Completed slice — V1.4

Separate `publish_l2.py` subscribes to level2 and parses l2_data into one product snapshot/update batch per record. Versioned L2 envelope retains original batch, update strings/times, raw message, source message time, sequence and receipt time. Distinct default topic `marketflow.coinbase.l2.v1`, product key and acknowledged send. Exact raw-message digest plus event index identifies retained observations without treating per-connection sequence as globally unique. A small shared connection loop preserves the original trade wrapper/defaults and bounded retry policy.

Verification: 17 focused tests passed (12 existing + 5 L2 cases); default suite 57 passed / 3 opt-in skips; separate real Kafka L2 test 1 passed. Two synthetic fixture messages (snapshot/update) passed through collector/parser/publisher and read back with matching keys/raw/acknowledged coordinates at partition 0 offsets 0/1. Evidence: `docs/verification/v1-4/`; contract/lesson: `docs/v1_l2_topic.md`. No live L2 smoke, authentic-volume or performance claim. No book state, deduplication or archive added.

## Completed slice — V1.5 (2026-10-15)

`raw_archive.py` captures original text messages and UTC receipt/subscription metadata into new files under ignored `data/raw/<channel>/`. UUID filenames and exclusive-create mode refuse overwrite; repeated deliveries remain distinct captures. A small optional shared-loop `on_message` hook saves before domain parsing, outside WebSocket retry handling. The standalone command skips domain parsing and does not publish to Kafka; existing publisher defaults are unchanged.

Verification: 4 archive tests passed; default suite 61 passed / 3 opt-in skips. Real-filesystem checks cover exact multiline/Unicode readback, repeated capture with prior bytes unchanged, overwrite refusal, preservation before parser failure and visible archive failure. Separate local readback saved one earlier authentic message twice without alteration. No new provider traffic/performance claim. Evidence: `docs/verification/v1-5/`; lesson: `docs/v1_raw_archive.md`. Writer is create-only, not filesystem-enforced immutability or power-loss-safe storage.

## Completed slice — V1.6 (2026-10-15)

`replay_archive.py` loads a frozen archive once, sorts by parsed receipt time/relative filename, repeats at a fixed per-message pause and reuses existing trade/L2 parsing. Separate fixed replay topics and explicit replay run/pass/archive markers preserve original text, receipt/source times and logical IDs without mixing live datasets. Summary distinguishes archive files, processed replay messages and acknowledged Kafka deliveries; none is a unique-source metric. No archive/publisher/collector changes.

Verification: 5 focused replay tests passed; default suite 66 passed / 4 opt-in skips; separate real Kafka replay test 1 passed. One unmodified earlier authentic raw message replayed twice, same event ID/product key and original provenance, partition 0 offsets 0/1. No provider traffic/performance measurement; pacing is test-controlled rather than benchmarked. Evidence: `docs/verification/v1-6/`; lesson: `docs/v1_archive_replay.md`. Determinism covers event content/IDs and send order, not fresh timestamps/run IDs/offsets or original global order.

## Completed slice — V1.7 (2026-10-15)

Separate Spark Bronze source/parse/Delta sink and bounded inspection script. One row per Kafka delivery retains topic/partition/offset, key/value bytes, full envelope JSON, original source raw payload, parsed envelope/version/replay fields, payload JSON and separate Kafka/processing times. Source time strings remain unchanged. No row filtering, domain validation or logical deduplication. Pinned JVM Delta 4.4.1 Spark-4.2 artifact; Python requirements/Spark/V0 unchanged.

Verification: 2 focused Spark/Delta tests; default suite 68 passed / 5 opt-in skips; separately enabled Kafka→Delta test 1 passed. Isolated earlier authentic trade envelope delivered twice plus synthetic malformed record, exact coordinates/provenance, row counts 2 → 3 → 3 with same checkpoint. Actual CLI restart and reader passed after explicit --packages launch fix; initial failed logs retained. Evidence: `docs/verification/v1-7/`; lesson: `docs/v1_bronze.md`. No source traffic/performance claim. Compatible restart is not business deduplication, crash recovery or checkpoint migration.

## Completed slice — V1.8 (2026-10-15)

Bounded full Bronze→Silver trade rebuild with decimal(20,8), explicit-zone event timestamps, Coinbase trade/version/identity/positive-value/side rules and first-failure reasons. Excess decimal precision is rejected, not rounded into acceptance. Canonical source/product/trade key; identical typed trades have one representative selected by Kafka coordinates, while conflicting valid values reject the key's candidates. Writes accepted `trades` plus every-delivery `audit`; independently reconciles accepted+duplicate+rejected against input. Rebuild overwrites rather than appends. Destination is bound to one Bronze input; valid live/replay candidates cannot mix.

Verification: 4 focused real Spark/Delta tests passed; full suite 72 passed / 5 opt-in skips. Actual CLI on prior Bronze check: 3 deliveries = 1 accepted + 1 rejected + 1 duplicate; no source traffic. Tests cover conflicting keys, small invalid set, exact UTC instant, repeatable rebuild and input binding. Initial 2 failures (host-time assertion and malformed replay-marker interpretation) corrected, evidence retained. Local evidence: `docs/verification/v1-8/`, currently Git-ignored by the user's rule; tracked summary/lesson: `docs/v1_silver_trades.md`. No benchmark claim. Two table writes are separate commits, not an atomic multi-table transaction; no incremental pipeline.

## Completed slice — V1.9 (2026-10-15)

Bounded accepted Silver→Delta minute rebuild: count and decimal total size per source/product/replay mode and fixed UTC event-time minute, with inclusive start/exclusive end. Every trade in the input snapshot participates, regardless of arrival order or age; older arrivals revise their original minute on the next full overwrite. No watermark or streaming finality claim. Input remains unchanged; output is bound to one Silver path and cannot overlap it.

Verification: 2 focused real Spark/Delta tests passed; full suite 74 passed / 5 opt-in skips. Tests cover boundaries, equivalent timezone offsets, out-of-order input, product/replay separation, exact totals, older arrivals and repeatable rebuild. Actual CLI exited 0 on earlier Silver verification input: one BTC-USD replay trade, 10:26–10:27 UTC, total size 0.00000012 BTC. Local evidence: `docs/verification/v1-9/`, Git-ignored as before; initial sandbox JVM-start failure retained. Guide: `docs/v1_trade_minutes.md`. No new provider traffic, dependencies, performance claims or prior baseline changes.

## Completed slice — V1.10 (2026-10-15)

Small independent Python `OrderBook`: product → (side, Decimal price) → Decimal quantity. Snapshots replace only their product; updates require a snapshot, replace positive quantities and remove zero levels. Staging prevents partial mutation on a bad batch. Uses the existing L2 parser/payload contract and synthetic fixtures; no publisher or Spark pipeline changes.

Verification: 3 focused tests passed; default suite 77 passed / 5 opt-in skips. Local fixture demo shows snapshot bid 1.5/offer 2.0 → bid absent/offer 1.2 → unchanged on immediate repeat. Tests also cover snapshot reset, product/side isolation, update-before-snapshot refusal and failed-batch preservation. Guide: `docs/v1_l2_state.md`; local Git-ignored evidence: `docs/verification/v1-10/`. No provider/broker traffic, dependencies, authentic-volume or performance metrics. Assumes complete supplied order and isolated input histories; no gap detection, stale-delivery protection, durable state or best bid/ask.

## Completed slice — V1.11 (2026-10-15)

Read-only `OrderBook.best_bid_ask(product)`: maximum Decimal bid and minimum offer from one product's supplied state. Missing sides return None, unknown products require a snapshot, equality is allowed, crossed quotes (bid > ask) raise without mutating state. Existing apply/transition behaviour is unchanged; no timestamp or freshness is inferred.

Verification: 3 new quote tests plus 3 existing transition tests passed; full suite 80 passed / 5 opt-in skips. Existing synthetic fixture/parser demonstration exited 0: snapshot bid 60000/ask 60001 → missing bid/ask 60001 after removal. Tests cover multiple levels, numeric comparison, removal exposing next prices, product isolation, empty/one-sided and locked/crossed books. Guide: `docs/v1_best_bid_ask.md`; local Git-ignored evidence: `docs/verification/v1-11/`. No provider/broker traffic, dependencies or performance measurements. Supplied-history completeness/freshness remain unverified; no integration, persistence or spread.

## Completed slice — V1.12 (2026-10-15)

One manual local Airflow 3.3.2 DAG: inspect_archive → replay. Bash tasks reuse the project Python archive loader and bounded V1.6 replay CLI; inspection retries once, replay has no automatic retry. Separate constrained `.venv-airflow`, ignored local metadata/logs and max one scheduler-active DAG run. No live stream or Compose changes.

Verification: 2 real Airflow tests passed, including synthetic archive → Kafka replay readback and missing archive → failed inspection after two attempts / replay upstream_failed with zero attempts. Default project suite 80 passed / 6 skips; the new skip is the separate-environment Airflow module. No source bytes changed, provider traffic or performance metric. First DagBag API mismatch corrected; failed log retained. Local evidence: `docs/verification/v1-12/`; guide: `docs/v1_airflow_replay.md`. Real local dag.test runs verified, continuous scheduler/UI not exercised. Replay is not exactly-once; manual reruns/partial failure may duplicate deliveries.

## Completed slice — V1.13 (2026-10-15)

Read-only bounded trade-replay reconciliation: archive-derived source/provenance signatures and multiplicities match one declared run/pass workload in Bronze; original Bronze columns match the persisted audit; accepted audit rows match trades. Known statuses, rejection reasons and non-null/unique accepted keys checked. No source writes, parser/domain-policy rewrite or pipeline changes.

Verification: 3 focused Spark/Delta tests passed; full suite 84 passed / 6 skips, exit 0. Actual CLI exit 0: 1 synthetic archive message → 3 expected/Bronze deliveries = 1 accepted + 1 duplicate + 1 rejected. Equal-count missing/extra delivery substitution and changed accepted size both raise. Full-suite Py4J closed-stream logging error occurred after passing summary; raw log retained. Evidence: local Git-ignored `docs/verification/v1-13/`; guide: `docs/v1_reconciliation.md`. No provider/Kafka traffic or performance metric. Scope is one frozen trade replay run, not live/L2/global reconciliation, policy recomputation or source completeness.

## Completed slice — V1.14 (2026-10-15)

Local dbt/DuckDB path: accepted Silver Delta → fresh Parquet export → external source → stg_trades view → dim_product/fct_trade tables. Natural product key; one fact per accepted logical trade, typed event-time/decimal/replay fields retained. Six data tests protect keys and product references. Export refuses overlap/replacement; one export root owns its local database. Separate pinned .venv-dbt leaves Spark/Airflow runtimes unchanged.

Verification: 1 real Spark export test and 2 dbt integration tests passed; duplicate fact keys deliberately fail unique. Actual earlier Silver export/dbt build/query passed: 1 view + 2 tables + 6 tests, one historical BTC-USD replay trade joined to BTC/USD product metadata. Full project suite 85 passed / 7 skips, exit 0; known post-summary Py4J closed-stream logging error retained. No new provider/Kafka traffic or performance claim. Evidence: local Git-ignored docs/verification/v1-14/; guide: docs/v1_local_dbt.md. No Snowflake, incremental models, Airflow chain or full source/freshness validation.

## Completed slice — V1.15 (2026-10-15)

Additive Compose overlay creates isolated marketflow-learning: pinned observed Kafka 4.3.1 digest, dual internal/host listeners, named broker/Airflow/cache volumes, readiness checks, standalone Airflow and an on-demand tools image with existing project/Spark/dbt runtimes. Read-only source and separate host data/compose tree preserve native baselines. Original compose file/broker unchanged. One optional DAG Python-path setting preserves native defaults.

Verification: image built; Kafka/Airflow healthy and UI HTTP 200; 2 opt-in Compose tests passed including host write→broker recreation→container read with matching coordinates. Container Spark export test 1 passed, dbt tests 2 passed, and existing replay DAG succeeded on one synthetic L2 archive. Host DAG parse 1 passed / 1 skip; full project suite 88 passed / 7 skips, exit 0. Final config check 1 passed / 1 skip after Airflow child-process PATH fix. Original broker ID unchanged/running. First startup failure/health diagnostics and known host Py4J shutdown noise retained. No provider traffic, performance metric or V1 exit claim. Guide: docs/v1_local_compose.md; local evidence: docs/verification/v1-15/.

## Completed slice — V1.16 (2026-10-15)

Frozen authentic workload: 4 retained raw messages, 104 distinct trades. Two fresh
Kafka→Delta Bronze→Silver/minutes→Parquet export→dbt/DuckDB query executions,
each with two archive passes: 208 deliveries = 104 accepted + 104 duplicates +
0 rejects. Source values and minute totals match; both 104-row logical query
results have identical hashes. Final opt-in experiment 2 passed; focused check
7 passed/1 skip. Default regression: 90 passed/8 skips, exit 0 (known
post-summary Py4J shutdown logging noise retained). Raw stage logs, progress,
delay samples and dbt artifacts retained.
Baseline timings describe paced backlog replay, not steady-state/live freshness.
Guide/results: docs/v1_exit.md and docs/v1_exit_baseline.json. V1 trade-path exit
criterion demonstrated; continuous/L2/full-orchestration/recovery gaps remain.

## Completed maintenance — V1 repository cleanup (2026-10-15)

User-requested consolidation after V1, not a new processing feature. Added a
README, reset/run guide, learning index and Make commands for the existing
container workflow; documented optional native environments. Moved the four V0
fixtures unchanged into tests/fixtures/v0 so generated data can be reset without
losing inputs. Short inline comments explain the versioned scripts; processing
logic/baselines unchanged. Full pre-cleanup state narrative retained in
`docs/history/CURRENT_STATE_V1.md`; current state condensed.

Verified rebuilt image, authentic Docker demo (two equivalent 104-trade results),
read-only Kafka/database inspection, core/Spark 87 passed/10 skipped, dbt 2 passed,
DAG parse 1 passed/1 skip, isolated V0 producer/consumer smoke, package consistency,
fixture bytes and unchanged executable ASTs for 20 annotated scripts. Historical
records, raw archives, checkpoints, datasets, broker volumes and host venvs were
not deleted; destructive reset commands are documented, not executed. No V2 work.

## Current recommended slice — V2.1 (not started; after learner review)

Goal: S3 raw/landing, preserving original raw input and provenance with a small
readback/access verification. No managed infrastructure introduced in V1.16.

## V1 — authentic local platform

Order follows the handover's feature-sized sequence after V0 exit. Diagnostic probe presence does not waive prerequisites.

| Slice | Status | Behaviour / verification |
| --- | --- | --- |
| V1.1 minimal live trade collector | DONE (simple observer) | 5 focused tests; earlier authentic capture reproduced offline; exact raw/UTC receipt retained. Message-count bound, no durable pipeline guarantee. |
| V1.2 disconnect/bounded reconnect | DONE (bounded retry) | Four offline failure tests; close/resubscribe, whole-run retry limit and possible-gap reporting. No missed-data recovery. |
| V1.3 trade topic contract/key | DONE (bounded publisher) | Versioned raw/provenance envelope and product key; 3 focused unit tests, 1 real Kafka roundtrip using archived authentic input. No live loss/deduplication guarantee. |
| V1.4 separate L2 stream | DONE (batch transport) | Separate product-keyed contract; 5 focused cases and 1 real Kafka check using synthetic snapshot/update fixtures. No book reconstruction. |
| V1.5 immutable raw archive | DONE (local create-only capture) | 4 focused disk tests; original text/receipt readback and overwrite refusal; no storage-enforced immutability/crash durability. |
| V1.6 deterministic replay | DONE (bounded local input) | Stable receipt/file ordering, pacing, replay topics/markers and explicit counts; 5 focused tests plus real Kafka check. No logical deduplication or loss-free recovery. |
| V1.7 Bronze ingestion | DONE (local Delta deliveries) | 2 focused Spark/Delta tests and 1 real Kafka→Delta restart check; exact raw/provenance and 2→3→3 rows. No logical deduplication. |
| V1.8 Silver trade validation | DONE (bounded rebuild) | Typed/validated logical trades, duplicate/conflict policy and every-delivery audit; 4 real Spark/Delta tests plus CLI accounting. No incremental/multi-table atomicity guarantee. |
| V1.9 event-time aggregation | DONE (bounded rebuild) | Fixed UTC source-time minutes, counts/decimal size, product/replay separation; 2 tests and CLI passed. All snapshot trades included; no streaming watermark/finality. |
| V1.10 L2 state model | DONE (in-memory transitions) | Decimal replace/remove, snapshot reset and product/side isolation; 3 tests plus fixture demo. No transport continuity or persistence claim. |
| V1.11 best bid/ask | DONE (in-memory query) | Decimal max bid/min offer, missing-side policy and crossed-result rejection; 3 new tests plus fixture demo. No live freshness/completeness claim. |
| V1.12 local Airflow | DONE (local DAG runner) | Manual inspect→replay, retry/dependency policy; 2 real Airflow tests including Kafka readback/failure blocking. Continuous scheduler/UI unverified. |
| V1.13 quality/reconciliation | DONE (bounded trade replay) | Archive/Bronze/audit/trades content and multiplicity checks; 3 tests plus CLI. Explicit run/pass/frozen-input scope; no live/global guarantee. |
| V1.14 local dbt fundamentals | DONE (local DuckDB) | Silver export → source/staging → product dimension/trade fact; 6 dbt tests, export preservation and duplicate-failure checks. No managed warehouse/incremental path. |
| V1.15 Compose consolidation | DONE (isolated learning overlay) | Kafka/Airflow readiness, named-state persistence, runtime image and synthetic checks verified; native broker/data preserved. No full V1 exit/performance claim. |
| V1.16 baseline/exit | DONE (bounded authentic trade path) | Two isolated executions: each 208 deliveries → 104 accepted/104 duplicate/0 rejected; matching source values, minute totals and analytical results; workload/configuration/raw timing evidence retained. |

## V2 — managed lakehouse and warehouse MVP

V2.1 code exists locally; real AWS verification remains pending. All later implementation below is absent. Proceed sequentially, one bounded behaviour per review.

| Slice | Status | Behaviour / verification |
| --- | --- | --- |
| V2.1 S3 raw/landing | IN PROGRESS | Conditional create-only archive uploader, exact byte readback and scoped IAM/bucket templates; 5 local SDK tests pass. Real S3 readback, replacement/access denial and authentic upload await first AWS account setup; no deployed immutability claim. Guide: docs/v2_s3_landing.md. |
| V2.2 first Databricks job | TODO | Port one understood Spark workload; compare local logical output. |
| V2.3 managed Delta Bronze | TODO | Retain schema/provenance; verify repeat processing. |
| V2.4 managed Delta Silver | TODO | Port validated/deduplicated/event-time logic; equivalence checks. |
| V2.5 checkpoint ownership | TODO | Durable continuous-query checkpoint, owner and restart verification. |
| V2.6 curated publication | TODO | Define lake-to-warehouse contract; reconcile exported rows/totals. |
| V2.7 Snowflake staging load | TODO | Bounded staged-file COPY; row counts and failure verification. |
| V2.8 Snowflake dbt sources/staging | TODO | Standardise names/types; source and data tests. |
| V2.9a dim_product | TODO | Define grain/key and test uniqueness/non-nullness. |
| V2.9b dim_venue | TODO | Same, as a separate slice. |
| V2.9c dim_date | TODO | Same, as a separate slice. |
| V2.10 fct_trade | TODO | One executed trade grain; stable keys and relationship tests. |
| V2.11 fct_market_interval | TODO | One product × interval; justified metrics and domain tests. |
| V2.12 first mart/query | TODO | Analyst-facing output over tested facts/dimensions. |
| V2.13 Airflow managed batch chain | TODO | Historical input → Databricks → publication → Snowflake → dbt/tests → reconciliation; retry/rerun checks. |
| V2.14 cross-layer reconciliation | TODO | Detect deliberate missing/duplicate rows and incorrect totals. |
| V2.15 CI baseline | TODO | Run actual Python/contract/Spark/DAG/dbt checks appropriate to implemented code. |
| V2.16 measurements/exit | TODO | Preserve freshness, lag, micro-batch/load/build/query measurements; real end-to-end path with reproducible orchestration/tests. |

## Next three bounded increments

1. V2.1: finish AWS account/target setup and real S3 readback/access checks after learner review of the local implementation.
2. V2.2: first Databricks job after S3 landing.
3. V2.3: managed Delta Bronze after the first job.

Do not bring CDC, SCD Type 2, broad schema evolution or V4 optimisation forward. Stop for user review after each meaningful slice.

Final V0 regression command: `.venv/bin/python -B -m pytest -v -p no:cacheprovider` — 40 passed, 1 skipped (real-broker exit test is opt-in and passed separately). Raw output: `docs/verification/v0-g/pytest-default-suite.log`.
