# Learning Log

Use one entry per consequential implementation slice.

---

## [Date] — [Slice]

### Concept

### Concrete Problem

### Mental Model

### Implementation

### Guarantee Added

### What It Does Not Guarantee

### Failure Mode

### Tests / Evidence

### Important Files

### Metric, if any

### Explain-Back

In my own words:

`TO BE COMPLETED/REVIEWED BY LEARNER`

### Interview Question

`Why did we use X rather than Y here?`

---

## 2026-10-14 — V0-F: schema/typing regression tests

### Concept and problem

A parsing schema describes data; it does not ensure safe validation. Spark is lazy: a transformation can build successfully and fail only when an action evaluates values. Manual valid-event observations did not protect malformed-input behaviour.

### Mental model and implementation

Separate the existing transformation plan from source/sink ownership. `transform_trades` accepts a Kafka-shaped DataFrame; both the live writer and bounded tests use the same code. Tests run real local Spark and call `collect()` so casts and output columns are evaluated. Python unittest requires no new dependency. Negative cases mutate a copied synthetic fixture, leaving the original unchanged.

### Guarantee added

Regression assertions protect current decimal precision, event-time conversion, row retention, Kafka coordinates and valid/invalid outcomes. Eight tests passed. An AST comparison confirmed all ten schema/transformation assignments and the Kafka source/Parquet sink are unchanged from HEAD.

### What it does not guarantee

These are characterization tests, not a repaired validation policy, streaming recovery test or end-to-end exit. No deduplication, quarantine, positivity/side domain checks or logical exactly-once guarantee was added.

### Important failure mode

With ANSI enabled, invalid price/size/time throws before a flagged row can be returned; with ANSI disabled the tested casts yield null and false. Missing event type/version can produce a null validation flag through SQL three-valued logic. The tests assert these baseline limitations explicitly; V0-F1 should fix them in a separate reviewable slice.

### Tests / evidence / files

Command: `.venv/bin/python -B -m unittest discover -s tests -v`. Result: 8 tests passed (approved outside-sandbox JVM execution; sandbox startup failed). Raw evidence: `docs/verification/v0-f-unittest.log`. Important files: `spark/v0/trade_transform.py`, `spark/v0/read_kafka.py`, `tests/test_v0_trade_transform.py`.

Metrics: none; suite runtime is not a throughput/latency benchmark.

### Explain-back

TO BE COMPLETED/REVIEWED BY LEARNER: why can plan construction succeed but collection fail, and why does a passing expected-exception test not imply safe invalid-record handling?

### Interview question

How do you test the real Spark transformation without starting Kafka or duplicating production logic, and what does SQL `true AND null` imply for a validation flag?

---

## 2026-10-14 — V0-F revision: pytest

Concept: fixtures own test setup/cleanup; parameterization gives each malformed input its own named case. Replaced unittest lifecycle/assertions with one module-scoped Spark yield fixture, a fresh event dictionary per case, ANSI setup/restoration, plain assertions and `pytest.raises`. Pytest 9.1.1 is a development dependency in `requirements-dev.txt`.

Guarantee: same V0 characterization assertions remain covered by real Spark; mutations and ANSI changes are isolated between cases. Production code was unchanged by this conversion. Limitations: strict cast exceptions/null flags remain intentionally asserted; no streaming/recovery/end-to-end guarantee added. Failure mode: passing expected-exception tests still does not mean the stream safely handles malformed input.

Verification: `.venv/bin/python -B -m pytest -v -p no:cacheprovider` — 19 passed. Raw evidence: `docs/verification/v0-f-pytest.log`; earlier unittest evidence retained. No performance metrics. Important files: `tests/test_v0_trade_transform.py`, `requirements-dev.txt`.

Learner review: how does fixture scope control the Spark lifetime, why must each parameterized case get a fresh event dictionary, and why restore ANSI settings after a case?

Explain-back: TO BE COMPLETED/REVIEWED BY LEARNER.

---

## 2026-10-14 — V0-F1: explicit invalid-row typing

### Concept / problem

Strict casts can fail at execution before validation produces a row. Comparisons against missing values use SQL null logic, so a validation predicate can return null. V0-F made these limitations reproducible; V0-F1 corrects them without hiding invalid deliveries.

### Mental model / implementation

Convert tolerantly at the data boundary, then validate explicitly: `try_cast(DecimalType(20, 8))` and `try_to_timestamp` yield null for invalid values; existing presence checks mark those rows invalid. `coalesce(predicate, false)` converts unknown validation to false. The timestamp format and decimal types are unchanged. No global ANSI switch, row filtering or new domain rule.

### Guarantee

Tested malformed decimal/time values retain a row and produce false flags under both ANSI modes; flags are non-null Booleans. Valid fixture values/types, row count and Kafka coordinates are preserved. Mixed-batch assertions account for all six deliveries (two valid, four invalid); duplicate deliveries remain distinct rows.

### What it does not guarantee / failure mode

No end-to-end storage/recovery, quarantine reasons, full raw provenance, deduplication or freshness guarantee. A numerically parseable negative price can still be flagged valid: V0 only checks presence/type, not price positivity. Infrastructure/session/invalid query configuration can still fail; tolerant conversion is not a blanket exception handler.

### Tests / evidence / files

Command: `.venv/bin/python -B -m pytest -v -p no:cacheprovider`.
New expectations against baseline: 15 failed, 25 passed. Corrected transformation: 40 passed. Real Spark, every case under ANSI true and false; includes decimal overflow, impossible date, missing/null type/version, valid fixtures and mixed-batch retention. Initial sandbox JVM startup was unavailable; approved local runs supplied evidence.

Important files: `spark/v0/trade_transform.py`, `tests/test_v0_trade_transform.py`.
Raw evidence: `docs/verification/v0-f1-before-pytest.log`, `docs/verification/v0-f1-after-pytest.log`. Prior baseline logs retained. Metrics: no performance measurements.

### Explain-back

TO BE COMPLETED/REVIEWED BY LEARNER: explain how tolerant conversion, non-null validation and retained coordinates let us account for invalid rows without silently dropping them.

### Interview question

Why use tolerant conversions at this boundary instead of disabling ANSI for the entire Spark session, and why is the validation predicate wrapped in `coalesce`?

---

## 2026-10-14 — V0-G: reproducible exit and restart

Concept/problem: component success is not end-to-end correctness. Acknowledged Kafka coordinates must match stored rows, while consumer-group commits and Spark checkpoint progress are separate mechanisms.

Implementation: optional environment configuration preserves existing script defaults. AvailableNow executes the same real streaming source/transform/Parquet sink as bounded catch-up. Opt-in pytest runs actual producer/consumer/writer/SQL/written-count scripts on a unique topic/group and fresh output/checkpoint. Written-count verification has an optional assertion and literal ID filter. No new dependency or V1 feature.

Guarantee: five synthetic deliveries matched five stored Kafka coordinates; four valid plus one invalid row accounted. Checkpoint restart consumed two backlog records without rewriting prior offsets; a second restart with no input kept the row count unchanged. Actual SQL and written-count positive/negative checks passed. Consumer committed-offset resume verified independently.

Limits/failure: repeated publication still adds a second logical trade delivery. Loss/incompatible reuse of checkpoint can invalidate restart assumptions; do not delete it or change its topic/sink/schema casually. No abrupt-crash injection, exactly-once business guarantee, old-checkpoint migration, live source, late-data policy or production resilience.

Verification: opted-in exit test passed (1 test). First attempt failed on missing Kafka connector at spark-submit launch; explicit --packages corrected the runner, and failed evidence is retained. Logs/manifest: `docs/verification/v0-g/`. Important files: `tests/test_v0_exit.py`, existing root/Spark scripts, `docs/v0_exit.md`. No performance metrics.

Explain-back (learner review pending): producer → Kafka partition/offset → Spark checkpointed transformation → Parquet → bounded SQL. Why does checkpoint progress avoid rewriting old offsets but not deduplicate a republished event? Why does the Python consumer use its own committed position?

Interview question: how would you distinguish a backlog recovered from Kafka from duplicate logical events in the analytical result?

Final default regression suite: 40 passed, 1 intentional opt-in skip; separately executed broker exit: 1 passed. No V1 work started.

---

## 2026-10-14 — End-of-session review (documentation only)

Completed technical work: repository reconciliation; V0-F real-Spark characterization and pytest conversion; V0-F1 tolerant typing/non-null validation; V0-G real Kafka → Spark → Parquet → SQL exit, consumer commit resume and compatible-checkpoint restart. Older entries describe behaviour at their slice's time; their exception/null expectations were replaced in V0-F1, not left as current policy.

Latest preserved results: default suite 40 passed / 1 opt-in skip, separately enabled exit 1 passed. Historical red run: 15 failed / 25 passed before correction. First connector-launch failure was fixed in the exit runner; logs retained. No tests rerun or implementation added during handover. Correctness counts only; no performance metrics.

Learner review remains unverified. Before interview claims, explain:

- producer acknowledgment and partition-scoped topic/offset provenance;
- why Python consumer-group commits and Spark checkpoint progress are separate;
- Spark laziness and why collect/start exposes conversion failures;
- tolerant casts plus explicit Boolean validation without silently dropping rows;
- why republishing a trade creates another delivery despite checkpointed restart;
- why AvailableNow catch-up/same-query restart does not prove crash recovery, checkpoint migration or production durability;
- which technologies and guarantees are still absent (Delta/cloud, authentic archive/replay, deduplication, late-data policy, Airflow/dbt).

Next: V1.1 bounded observable BTC-USD trade collector after V0 review. No reconnect, Kafka wiring or cloud in that slice. Approved endpoint remains V2. Explain-back answers: TO BE COMPLETED/REVIEWED BY LEARNER.

---

## 2026-10-14 — V1.1: bounded observable trade collector

Concept/problem: message grain differs from trade grain. The naive probe printed
whole batches, omitted receipt metadata from output, raised incidental TypeErrors
for malformed shapes and swallowed loop failures. One batch may contain many
trades, and snapshot/update delivery does not establish unique trade volume.

Mental model/implementation: receive an exact text message with UTC receipt time;
validate its nested batch structure; emit one observation per trade with the raw
message and shared receipt metadata. Source `time`/numeric strings remain untouched.
A monotonic deadline controls the observation loop, independently of wall-clock
receipt labels. Positive finite duration and message limits bound diagnostics;
socket timeouts and `finally` cleanup keep failures visible. CLI failures exit 1,
interruptions 130. Existing synthetic flattening example remains test-covered;
websocket-client is declared using the existing requirements convention.

Guarantee: tested batch shapes flatten in order; exact raw text/source fields and
receipt time survive. Invalid batch structure is rejected before any rows from
that batch emit. Connection/send/receive/parse failures and interrupts are visible
and cleanup is tested. Limits: stdout is not durable or atomic, domain fields are
not yet validated, duplicates remain, no Kafka/archive/replay/reconnect. Duration
is a loop bound; DNS, close and blocked stdout can extend process wall time.
Failure mode: disconnect after some output leaves a gap that this slice detects
but cannot recover. Output failure can also partially emit a valid batch.

Verification: 40 offline collector tests; default suite 80 passed / 1 intentional
opt-in broker skip. Live command: `.venv/bin/python -B coinbase_probe.py
--duration-seconds 10 --max-messages 5`, exit 0: five messages, 104 BTC-USD
observations, snapshot/update batches. Readback reconciled each trade to its raw
message. Sandbox Spark sockets/DNS were unavailable; approved local runs passed.
Raw logs, compressed live output and manifest: `docs/verification/v1-1/`.
No performance or unique-volume metric; no provider benchmark.

Important files: `coinbase_probe.py`, `tests/test_coinbase_probe.py`,
`requirements.txt`, `docs/v1_trade_collector.md`.

Explain-back (TO BE COMPLETED/REVIEWED BY LEARNER): why is receipt time shared
across trades in a message, why is monotonic time used for deadlines, and what
happens if a malformed event follows a valid event in the same batch?

Interview question: why do retaining raw payloads in diagnostic output and closing
a WebSocket correctly still not prove durable, unique or loss-free ingestion?
Next slice: V1.2 bounded reconnect and visible gaps, after review; not implemented.

---

## 2026-10-14 — V1.1 simplification for undergraduate learning

The user clarified that this is a learning project and defensive machinery was
obscuring the slice. `AGENTS.md` now prioritizes simple code and focused tests.
The earlier V1.1 entry describes the previous implementation, not current coverage.

Core idea: one message contains several trades. A short loop flattens them; each
observation keeps the original message and shared UTC receipt time. Source fields
remain untouched. Removed detailed shape checks, duration handling, counters and
custom CLI error handling. Kept a message-count limit, socket timeout, explicit
source-error check and `finally` cleanup. Ordinary Python exceptions stay visible.

Five focused tests passed; full suite 45 passed / 1 opt-in skip. Offline readback
reproduced the earlier 104 authentic observations exactly. Evidence:
`docs/verification/v1-1/*-simplified.log`; no new live traffic or metrics.
Important files: `AGENTS.md`, `coinbase_probe.py`, `tests/test_coinbase_probe.py`,
`docs/v1_trade_collector.md`. V0 code and previous evidence remain unchanged.

Assumption/failure: unexpected source shapes may raise KeyError/TypeError; the
script stops visibly rather than attempting recovery. No durable storage,
deduplication, reconnect or total elapsed-time bound. These remain later lessons.

Explain back: why do several trades share one receipt timestamp, and what does
`finally` do if parsing fails? Interview question: what does one output row mean?
V1.2 remains unstarted.

---

## 2026-10-14 — V1.2: bounded reconnect

Problem/concept: a WebSocket connection can close or time out. A new connection
lets us continue observing, but cannot recover trades that happened while absent.

Implementation: one retry loop around connection/send/receive only. Close the
failed socket, report a possible gap with UTC detection time, pause one second,
and reconnect/resubscribe. Three reconnects by default after the first attempt;
the counter is never reset on success. The message limit spans connections.
Parsing/output errors remain ordinary exceptions outside the retry block.

Guarantee: deterministic tests prove close/resubscribe, preserved message limit,
retry exhaustion and visible idle-timeout handling. Existing trade/raw/receipt
parsing is unchanged. Limits: no missed-trade recovery, duplicate removal, exact
gap/loss measurement or silent sequence-gap detection. Failure mode: after all
retries fail the script stops with an exception; already printed observations
remain and missing trades are not fetched.

Verification: 9 collector tests passed (5 existing + 4 new); full default suite
49 passed / 1 opt-in skip. No Coinbase traffic, new dependency or performance
metrics. Logs: `docs/verification/v1-2/`. Files: `coinbase_probe.py`,
`tests/test_coinbase_reconnect.py`, `docs/v1_reconnect.md` and state/plan notes.

Explain-back: why keep separate message and reconnect counters, and why does
parsing sit outside the retry block? Interview question: why is “reconnected”
insufficient evidence of zero lost trades? Learner answers remain pending.
Next: V1.3 trade topic contract/key; not implemented.

---

## 2026-10-14 — V1.3: trade envelope and Kafka product key

Problem/concept: stdout observations do not define a Kafka record contract or
routing key. A record has a key for partition routing and a value containing data.

Implementation: `publish_trades.py` wraps the trade in versioned JSON with its
stable venue/product/trade ID, source time, receipt time, send-attempt time,
sequence and original raw text. UTF-8 product key routes the same product under
a fixed partition count. `send().get(timeout=10)` waits for acknowledgment;
coordinates print to stderr. A small optional collector callback connects these
steps without changing the diagnostic command or WebSocket retry policy.

Guarantee: tests preserve contract/provenance, product key and acknowledged
coordinates. Real Kafka roundtrip on three partitions reconciled two repeated
deliveries of one earlier authentic observation, same ID/key and partition 0
offsets 0/1. Ordering is partition-scoped; event time is not sorted by Kafka.
Limitations: no deduplication, archive, gap recovery or production durability.
Failure: an acknowledgment timeout can follow a successful write; another send
may duplicate the logical trade. Kafka failure stops the collector rather than
triggering a Coinbase reconnect. Waiting per trade trades throughput for clarity.

Verification: 12 focused tests; default suite 52 passed / 2 opt-in skips; separate
real Kafka test 1 passed. Earlier authentic input was replayed, no new Coinbase
traffic or performance metrics. Evidence: `docs/verification/v1-3/`. Files:
`publish_trades.py`, collector callback, `tests/test_trade_publish.py`,
`tests/test_trade_kafka.py`, `docs/v1_trade_topic.md`, state/plan/metrics notes.
V0 code, previous evidence and dependencies unchanged.

Explain-back: what belongs in the key/value, why retain both source and receipt
times, and why keep the event ID stable? Interview question: why does an
acknowledged repeated delivery still need downstream logical deduplication?
Next: V1.4 separate L2 stream; not implemented.

---

## 2026-10-14 — V1.4: L2 as a separate stream

Problem/concept: executed trades and price-level quantities have different
meanings. L2 transport must preserve snapshot/update batches separately from
trade records. Subscribe with level2; parse received l2_data.

Implementation: `publish_l2.py` retains one source product event per Kafka record,
including all price-level updates, source times/strings, raw message and UTC
receipt metadata. Its separate topic uses product key and acknowledged sends.
The existing reconnect loop is shared through a small `collect_messages` function;
the trade wrapper/defaults remain. An exact-message digest and event index identify
observations without assuming connection-local sequences are globally unique.
Digest here means a repeatable identifier for bytes, not price-level identity.

Guarantee: fixtures prove snapshot/update boundaries, zero quantities, provenance,
stream separation and publication key. Real Kafka check passed collector/parser/
publisher-to-consumer reconciliation. Limits: no level-state changes, bid/ask,
deduplication, continuity enforcement, archive or live L2 verification. Failure:
a disconnect may leave missing updates; reconnect cannot prove a correct book.
Keeping batches together is easy to inspect but large snapshots may exceed Kafka
record-size limits; this slice does not tune or split them.

Verification: 17 focused tests; default suite 57 passed / 3 opt-in skips; separate
real Kafka test 1 passed. Two explicitly synthetic fixture messages, no authentic
L2/provider traffic or performance metrics. Logs: `docs/verification/v1-4/`.
Files: collector shared loop, `publish_l2.py`, `tests/fixtures/l2_*.json`,
`tests/test_l2_publish.py`, `tests/test_l2_kafka.py`, `docs/v1_l2_topic.md` and
state/plan/metrics notes. Earlier baselines and user comments preserved.

Explain-back: why distinguish snapshot/update, why keep zero quantity, and why
is source message time different from each update's event time?
Interview question: why does publishing L2 batches not establish a correct order
book? Next: V1.5 immutable archive; not implemented.

---

## 2026-10-15 — V1.5: save the original before parsing

Problem/concept: parser output is not a substitute for original input. Keep a
receipt: exact source text plus when/which subscription received it.

Implementation: `raw_archive.py` creates one JSON wrapper per received message.
Fresh UUID filenames and file mode `"x"` add captures without replacing earlier
ones. `raw_payload` stays a string, preserving source whitespace/newlines and
characters on readback. An optional shared-loop `on_message` hook runs before
domain parsing. Standalone capture skips parsing and saves control/error text too;
existing publishers do not automatically archive. No new dependency.

Guarantee: four real-disk tests prove exact readback/repeated capture, overwrite
refusal, raw preservation before parser failure and visible disk failure with
socket cleanup. Default suite 61 passed / 3 opt-in skips. One earlier authentic
message was saved twice locally and read back unchanged; no new live source run.
Evidence: `docs/verification/v1-5/`. No performance or unique-volume measurement.

Limits/failure: another program can modify local files; a crash or disk-full
error during writing may leave an incomplete new file. This is create-only writer
behaviour, not filesystem retention or power-loss-safe storage. No replay,
deduplication, gap recovery or Kafka/archive transaction.

Important files: `raw_archive.py`, collector message hook,
`tests/test_raw_archive.py`, `docs/v1_raw_archive.md` and state/plan/metrics notes.
Explain back: why archive once per message rather than once per trade, and why
use `"x"` instead of `"w"`? Interview question: what can the raw archive preserve
when a parser fails, and what can it not recover? V1.6 remains unstarted.

---

## 2026-10-15 — V1.6: replay saved inputs internally

Problem/concept: an archive is useful only if we can reuse its input. Replay
substitutes saved text/original receipt times for a live connection, keeping
new deliveries distinct from the original observations.

Implementation: `replay_archive.py` loads the chosen frozen archive, sorts by
receipt time then relative filename, and repeats the list with a fixed pause per
raw message. Existing parsers build trade/L2 events. Separate replay topics and
run/pass/archive markers preserve logical IDs/source times while distinguishing
fresh publication timestamps and Kafka offsets. Archive/control-message counts
are reported separately from acknowledged domain deliveries; no unique-volume
inference. Existing archive/live code is unchanged.

Guarantee: five focused tests prove stable event order/IDs, filename ties,
pacing/provenance, unchanged source files, control accounting and visible input/
ack failure. Default suite 66 passed / 4 opt-in skips; separate real Kafka test
1 passed. Earlier authentic raw message replayed twice: one input message, two
replay messages, two deliveries, same ID/key/provenance, partition 0 offsets 0/1.
No Coinbase traffic, new dependency, achieved-rate or performance measurement.
Evidence: `docs/verification/v1-6/`; code/tests: `replay_archive.py`,
`tests/test_archive_replay.py`, `tests/test_replay_kafka.py`; explanation:
`docs/v1_archive_replay.md`.

Trade-off/limits: loading input into memory makes deterministic repeats simple
but is bounded by memory. Receipt/file order is a chosen replay rule, not original
global source order. Failure after some sends leaves those deliveries in Kafka;
no rollback/resume/deduplication. Fresh times/run IDs/offsets prevent byte-identical
records even though original domain content and order repeat.

Explain back: why keep the old receipt time, why distinguish message/delivery
counts, and why use replay topics? Interview question: what exactly is deterministic
when the same archive is replayed twice? V1.7 remains unstarted.

---

## 2026-10-15 — V1.7: a raw-but-queryable Delta Bronze table

Problem/concept: Kafka is a log, not the lake table we query. Bronze retains one
row per received delivery with enough raw/source/transport metadata to inspect
and reconcile it. Silver will validate and deduplicate logical trades later.

Implementation: separate `spark/bronze/ingest.py` reads Kafka, parses only envelope
fields and appends to Delta. Original value/key bytes, envelope text, source raw
message/payload, version/replay fields and topic/partition/offset remain. Source
and receipt strings are distinct from Kafka timestamp and Spark ingested_at.
Malformed data remains a row. `query.py` inspects schema/counts/provenance. Delta
adds a transaction log over data files; the stream checkpoint separately tracks
query progress. Neither removes a republished logical trade.

Dependency decision: pin the JVM Delta 4.4.1 Spark-4.2 build beside the existing
Kafka connector. No Python Delta API, Spark upgrade or V0 migration. spark-submit
must receive --packages at launch; initial missing-package CLI failures were
reproduced, documented and retained before corrected CLI restart/reader passed.

Verification: 2 focused tests; default suite 68 passed / 5 opt-in skips; separate
real Kafka→Delta test 1 passed. One earlier authentic envelope delivered twice
plus synthetic malformed row: exact coordinates/raw/source fields, row counts
2→3→3 across compatible restart. CLI reader confirms three rows. Evidence:
`docs/verification/v1-7/`. No new provider traffic or performance metrics.
Files: `spark/bronze/ingest.py`, `query.py`, `tests/test_bronze.py`,
`tests/test_bronze_kafka.py`, `docs/v1_bronze.md` and state/plan/metrics notes.

Guarantee/limits: tested raw retention, Delta table read/write and compatible
checkpoint restart; no domain validity, logical deduplication, late-data policy
or production/crash recovery guarantee. Failure: losing/reusing an incompatible
checkpoint can break progress assumptions. Raw retention costs storage but allows
later interpretation/repair without hiding unknown fields.

Explain back: why keep raw bytes after parsing, what does one Bronze row mean,
and how do checkpoint progress and Delta commits differ? Interview question:
why can a repeated trade have two Bronze rows despite checkpointed restart?
Next: V1.8 Silver trade validation; not implemented.

---

## 2026-10-15 — V1.8: type, validate and deduplicate trades

Concept/problem: Bronze deliveries can be malformed or repeat the same trade.
Typing answers “can this become a decimal/time?”; validation adds domain rules;
deduplication identifies repeated logical trades using source/product/trade ID.

Implementation: bounded full rebuild in `spark/silver/trades.py`. Positive
exact-scale decimal(20,8), BUY/SELL and explicit-zone event time; supported
Coinbase envelope/product/ID checks. First-failure rejection reason, explicit
false for unknown SQL predicates. Grouped typed-value signatures detect conflicts;
a window ranks identical candidates by transport coordinates. One accepted row
per valid identical key, extra rows duplicate, conflicting candidates rejected.
Accepted `trades` and every-delivery `audit` are separate Delta tables. Rebuild
replaces rather than appends; independent count reconciliation and source-path
binding protect accounting and avoid replacing another input's output. Valid live
and replay candidates cannot mix.

Verification: 4 focused real Spark/Delta tests; full suite 72 passed / 5 opt-in
skips. Actual CLI: prior 3 Bronze deliveries → 1 accepted, 1 rejected, 1 duplicate.
Initial focused failures taught that collected Python naive timestamps use host
timezone (test now checks UTC instant) and malformed missing replay markers must
not be mistaken for live candidates. Raw failed/final logs retained under
`docs/verification/v1-8/`, currently ignored/local. No new provider/dependency or
performance claim. Existing Bronze and prior code unchanged.

Guarantee/limits: tested bounded typing/domain/deduplication/accounting and same
input rebuild. Typed timestamps have microsecond resolution; original text remains.
Not a streaming/incremental pipeline or full exchange contract. Two table commits
are not atomic: failure between writes leaves different output generations;
rerun same input after resolving the failure. New conflicts reject a previously
accepted key rather than pretending to resolve market corrections.

Files: `spark/silver/trades.py`, `tests/test_silver_trades.py`,
`docs/v1_silver_trades.md`, state/plan/metrics notes. Explain back: why can a typed
price still be invalid, why distinguish duplicate from conflict, and how does
input = accepted+duplicate+rejected help? Interview question: why does a full
rebuild avoid accumulating repeated logical trades without needing MERGE yet?
V1.9 remains unstarted.

## V1.9 — source-event-time minute aggregation (2026-10-15)

Problem: accepted Silver trades were individual facts, without per-minute totals.
Concept: fixed, non-overlapping event-time windows. `window(event_time, '1 minute')`
groups `[start, end)`; groupBy/count/sum produces one source/product/replay/minute
row. UTC instants determine membership, not arrival order or receipt time. Size
is summed as decimal in base-asset units; absent minutes have no row.

Implementation: `spark/silver/trade_minutes.py` reads accepted Silver Delta,
fully rebuilds a separate Delta minutes table and prints sorted results. Output
binding/path checks preserve the source boundary. No new dependency or V0 change.
Guarantee: all snapshot trades participate, product/replay totals stay separate,
and repeating unchanged input adds no copies. Lateness policy: older arrivals
revise their original minute on the next rebuild; no age cutoff. Not a watermark,
continuous stream, finalised window, new deduplication or freshness mechanism.
Failure: a failed rebuild can leave the previous minute table queryable but stale;
upstream Silver and minute publication are not one transaction.

Evidence: 2 focused real Spark/Delta tests; full suite 74 passed / 5 opt-in skips.
CLI on prior Silver: one replay BTC-USD trade, 10:26–10:27 UTC, size 0.00000012 BTC.
No provider traffic/performance metrics. Sandbox JVM-start failure retained;
local execution passed. Local raw evidence: `docs/verification/v1-9/`; guide:
`docs/v1_trade_minutes.md`; tests: `tests/test_trade_minutes.py`.

Explain back: why does 12:01:00 belong to the next minute, why does arrival order
not matter, and when will an older trade change the output? Interview question:
what changes if we group by ingestion time instead of event time?
V1.10 remains unstarted; stop for learner review.

## V1.10 — L2 state transitions (2026-10-15)

Problem: L2 snapshots/updates were transported without being interpreted as state.
Concept: (product, side, price) → quantity. In `l2_state.OrderBook`, a snapshot
replaces that product's dictionary; an update assigns absolute new quantities,
and zero removes a level. Decimal keys/values avoid binary floating-point
approximation. Bid/offer and products stay separate. Updates require a snapshot.
A temporary dictionary stages each batch before assignment, preventing partial
state changes when a later entry raises; input payloads remain unchanged.

Guarantee: tested in-memory transitions for a supplied ordered history. Immediate
repeat of the same update does not add quantities. This is not general duplicate
handling: stale redelivery after a newer update can restore stale state. Missing
updates are undetected, so a plausible book can be wrong; obtain a fresh snapshot
and start a new isolated history after a gap. No Kafka/Spark integration, durable
state, live/replay mixing protection inside this payload-only API, best bid/ask,
or proof of complete live exchange state. Copying each product's levels keeps
the example clear at the cost of per-batch copying work.

Verification: 3 focused tests; default suite 77 passed / 5 opt-in skips; fixture
demo exit 0. Synthetic snapshot bid 1.5/offer 2.0 becomes bid absent/offer 1.2,
and immediate repeat is unchanged. Tests cover replacement/removal, snapshot
reset, product/side isolation and failure preservation. No provider/broker traffic
or performance metrics. Files: `l2_state.py`, `tests/test_l2_state.py`,
`docs/v1_l2_state.md`; local evidence `docs/verification/v1-10/`.

Explain back: why is new_quantity assigned rather than added, why must a snapshot
clear old levels, and how can a lost update leave a believable but wrong book?
Interview question: why does immediate repeat safety not protect against stale
out-of-order delivery? V1.11 remains unstarted; stop for learner review.

## V1.11 — best bid/ask (2026-10-15)

Problem: the L2 model stored levels without a small queryable price summary.
Concept: best bid = highest buying price; best ask = lowest selling price.
`OrderBook.best_bid_ask(product)` scans Decimal keys with an explicit loop,
keeping maxima/minima. Removing a best level exposes the next price on query.
None represents a missing side; no snapshot differs from a known empty book.
Equal bid/ask is allowed; a crossed result (bid > ask) raises ValueError. The
query is read-only and does not change apply's transition or rollback behaviour.

Guarantee: exact extrema of that product's supplied valid model state and visible
crossed-result failure. Not a complete/fresh live quote, timestamped observation,
transport integration or gap recovery. A lost update can leave an incorrect
quote that still passes bid <= ask. Ordered isolated-history assumptions remain.
Trade-off: each query scans all product levels rather than maintaining a more
complex cached top price. No performance measurement was made.

Verification: 6 focused tests (3 new + 3 existing); full suite 80 passed / 5 skips.
Fixture/parser demo exit 0: bid 60000/ask 60001 → missing bid/ask 60001. No provider
or broker traffic. Files: `l2_state.py`, `tests/test_best_bid_ask.py`,
`docs/v1_best_bid_ask.md`; local evidence: `docs/verification/v1-11/`.
Explain back: why max/min, why missing is None rather than zero, and why is a
non-crossed quote not proof of freshness? Interview question: what happens when
the current best bid is removed? V1.12 remains unstarted; stop for learner review.

## V1.12 — local Airflow bounded replay (2026-10-15)

Problem: replay was a manual command without recorded workflow dependencies.
Concept: a DAG describes tasks and their dependency arrows; a DAG run records
one execution, task instances record attempts/outcomes. Two BashOperators in
`dags/archive_replay.py` run inspect_archive → replay using the existing project
Python. Airflow orchestrates commands; it is not the live stream processor.
Manual schedule, no catchup, max one scheduler-active run. archive_dir is a Param.
Inspection retries once; replay has no automatic retry because partial failure
may follow acknowledged Kafka writes. Manual reruns can still duplicate data.

Guarantee: tested task dependency blocking, bounded replay and visible failure.
Inspection only loads archive wrappers, not every source-payload rule. The input
must remain frozen. No Spark chain, reconciliation, exactly-once, live recovery
or cross-process lock. Separate constrained .venv-airflow avoids changing the
project runtime; it adds an extra environment to maintain. Source timestamps
and replay topics remain the existing command's responsibility.

Verification: 2 real Airflow tests passed using SQLite/local Kafka, including one
synthetic replay readback and unchanged archive; missing archive failed inspection
after two attempts and blocked replay. Project suite 80 passed / 6 skips. First
DagBag API mismatch fixed; two framework dependency deprecation warnings remain.
No provider/performance/authentic-volume claim. Continuous scheduler/UI not tested.
Files: `dags/archive_replay.py`, `requirements-airflow.txt`,
`tests/test_airflow_replay.py`, `docs/v1_airflow_replay.md`; raw local evidence:
`docs/verification/v1-12/`. Interview question: why is read-only inspection safe
to retry while replay is not automatically retried? Explain back the dependency
arrow, task states and distinction between orchestration and stream processing.
V1.13 remains unstarted; stop for learner review.

## V1.13 — bounded layer reconciliation (2026-10-15)

Problem: successful writes do not prove every expected delivery survived or
persisted values still agree. Concept: reconcile a precisely declared workload
across layers, preserving occurrence counts. A Counter maps each canonical JSON
signature to its multiplicity; Spark exceptAll compares persisted rows without
discarding duplicates. Both directions find missing and extra rows. Archive
files are not trade counts: messages can contain several trades; replay passes
and repeated observations are deliveries, not unique source events.

Implementation: `spark/silver/reconcile.py` compares a frozen trade archive plus
run ID/pass count to Bronze, Bronze to audit, and accepted audit to trades. It
also checks known statuses/reasons and accepted key uniqueness. Read-only with
nonzero failure on mismatch. Invalid trades are accounted as deliveries, not
silently omitted. It does not independently revalidate Silver's policy or prove
source capture completeness; expectations reuse the current parser. Only the
selected replay run is in scope, with small driver-memory inputs. Concurrent
writes can cause a transient mismatch; freeze layers and rerun before diagnosing
loss. No auto-repair, Airflow scheduling, L2 or dbt work.

Evidence: 3 focused Spark/Delta tests; full suite 84 passed / 6 skips (exit 0),
with a retained post-summary Py4J closed-stream logging error. CLI 1 raw message
→ 3 deliveries = 1 accepted + 1 duplicate + 1 rejected. Same-count delivery
substitution and changed accepted size both fail. No provider/Kafka traffic or
performance measurement. Tests: `tests/test_reconcile.py`; guide:
`docs/v1_reconciliation.md`; local logs: `docs/verification/v1-13/`.
Explain back: why are equal counts insufficient, why preserve rejected rows, and
why must run ID/pass count be explicit? Interview question: how can a missing row
and a duplicate cancel in a count comparison? V1.14 remains unstarted.

## V1.14 — local dbt source, staging and fact/dimension (2026-10-15)

Problem: accepted Silver lacked a declared SQL modelling path. Concept: dbt
compiles SELECT models, resolves source/ref dependencies and builds/tests
relations inside an analytical database. DuckDB executes SQL; dbt coordinates
model creation. Source is a frozen accepted-Silver Parquet export read from a
Delta snapshot. stg_trades is a view that renames keys/size, dim_product a table
with one observed product, fct_trade a table with one accepted logical trade.
Natural product_id links them; Decimal, UTC event time and replay identity remain.
Six small data tests assert keys/nulls/relationships. A test returns violating
rows; zero violations is success. No extra Silver domain rules are introduced.

Guarantee: tested value/grain preservation, natural-key relationship and visible
duplicate-fact failure for supplied input. Each fresh export has its own local
database; export refuses replacement/overlap. Not source completeness, freshness,
SCD history, incremental processing, Snowflake or automatic orchestration. A dbt
test can fail after model tables were created, so failure does not roll back the
build. Use only successful builds. The Parquet bridge adds a stored copy/manual
step but avoids Delta extension setup in the first dbt lesson.

Verification: 1 export test, 2 real dbt integration tests; smoke build 1 view +
2 tables + 6 data tests passed. Earlier replay trade query retained BTC/USD,
quantity 0.00000012 and source time. Project suite 85 passed / 7 skips (separate
dbt env tested independently); known Py4J shutdown logging issue retained. No
provider/Kafka traffic or performance claim. Files: dbt/, spark/silver/export_dbt.py,
requirements-dbt.txt, tests/test_export_dbt.py, tests/test_dbt_local.py,
docs/v1_local_dbt.md; raw evidence docs/verification/v1-14/.
Explain back: source versus ref, view versus table, fact versus dimension grain,
and why failed tests do not imply absent tables. Interview question: what does
the fact-to-product relationship test check that unique trade keys do not?
V1.15 remains unstarted; stop for learner review.

## V1.15 — Compose runtime consolidation (2026-10-15)

Problem: several learned runtimes/startup commands depended on host setup.
Concept: an image defines runtime contents; containers run it; Compose declares
services, connections and mounts. Kafka/Airflow are long-running; tools runs
finite Python/Spark/dbt commands. Existing base Compose is extended in a separate
learning project, preserving the historical broker and native data.

Two Kafka listeners are necessary because clients receive advertised broker
addresses: host localhost:19092 versus container kafka:9092. Container localhost
means that container. Named Kafka/Airflow volumes survive container recreation;
read-only source plus separate data/compose bind mount keeps learning output
apart. Health dependencies wait for readiness, not ongoing recovery. Airflow
health checks JSON component states, not only HTTP 200. Container DAG Python
is selected through one optional env setting; host default is unchanged.

Failure learned: invoking Airflow by absolute path was insufficient because
standalone launches child 'airflow' commands via PATH. Adding its venv bin to
service PATH fixed startup; final config and real runtime checks passed. Volume
deletion can still remove data. One broker/SQLite/local Spark are learning
shortcuts, not HA/production claims. Shared image is larger but keeps three
runtime environments explicit; no new processing semantics or hidden pipeline.

Evidence: Compose tests 2 passed (including recreation/persistence), container
Spark 1 passed, dbt 2 passed, manual synthetic Airflow DAG success and healthy
API/scheduler/DAG processor. Native DAG parse 1 passed/1 skip; host suite 88
passed/7 skips, then final PATH config 1 passed/1 skip and startup/DAG verified.
Original broker ID unchanged/running. Two synthetic deliveries; no provider or
performance measurement. Files: compose.local.yml, docker/Dockerfile.local,
.dockerignore, dags/archive_replay.py, tests/test_local_compose.py,
docs/v1_local_compose.md. Local evidence docs/verification/v1-15/.
Explain back: image vs container vs volume, host vs container Kafka addresses,
and why startup health is not stream correctness. Interview question: why does
container recreation preserve a message, while volume deletion would not?
V1.16 remains unstarted; stop for learner review.

## V1.16 — reproducible authentic trade exit (2026-10-15)

Problem: separate component tests did not demonstrate the whole learned trade
path. Concept: freeze the input, run the real components with fresh state, then
compare logical results rather than changing transport metadata.

Implementation: four original V1.1 raw messages contain 104 distinct trades.
Two passes produce 208 Kafka/Bronze deliveries; Silver retains 104 logical trades
and marks 104 duplicate audit rows. Minutes total 104 trades / 1.24180961 BTC.
Export/dbt builds an analytical fact/product join with 104 rows. Run twice with
fresh topics/checkpoints/tables/databases: direct source values match and sorted
query hashes agree. The original raw/receipt strings and hashes remain frozen.
Historical capture reported five messages but only four trade-bearing messages
survive in its observation artifact; nothing is reconstructed without evidence.

Guarantee: this retained authentic workload is replayable through the bounded
trade path into equivalent queryable data. No live completeness, continuous
pipeline, L2 integration, atomic multi-stage publication or crash recovery claim.
Failure: Kafka replay may succeed before a later dbt stage fails; partial tables
remain. FAILED manifest/raised exception must not be read as successful output.

Trade-off: a real integration experiment is slower and needs Kafka/Spark/dbt,
so it is opt-in; ordinary tests check the fixed workload and percentile rule.
No framework or new production dependency is needed. The runner connects the
existing scripts rather than reimplementing their processing policies.

Measurement lesson: acknowledged replay rate includes intentional per-message
pacing; a source message can contain many trades. Bronze drain rate includes
startup/termination. Publication→processing delay includes backlog waiting,
not original event freshness or committed/queryable output time. Nearest-rank
p95 means the value at ceil(0.95*n) in sorted delay samples. Both executions share
one JVM; the faster warmed second run proves no optimisation. The unchanged
200 shuffle partitions produced many small Silver Parquet files; recorded,
not tuned here. Delta still stores Parquet plus its transaction log.

Evidence: focused 7 passed/1 skip; final real exit experiment 2 passed (73.02s);
full regression 90 passed/8 skips, exit 0 (known Py4J shutdown logging retained).
Final baseline: 416 replay deliveries; earlier preliminary run adds another 416.
These 832 deliveries still represent the same 104 authentic historical trade IDs.
No provider traffic. Files: verify_v1_exit.py, tests/test_v1_exit.py,
tests/fixtures/v1_exit/, replay_archive.py, tests/test_archive_replay.py,
docs/v1_exit.md, docs/v1_exit_baseline.json. Raw evidence: ignored
`docs/verification/v1-16/` and recorded `data/v1/v1-16-final-20261015/` output.

Explain back: delivery versus logical trade; why fresh checkpoints/topics matter;
what the result hash excludes; why processing delay is not source freshness.
Interview question: how can two executions have different Kafka offsets/run IDs
but still produce equivalent analytical data?
V2.1 remains unstarted; stop for learner review.

## V1 cleanup — a single runnable workflow (2026-10-15)

Problem: multiple environment commands, machine-local walkthrough input and a
long historical state document hid the learned pipeline. Concept: distinguish
source/test fixtures, generated runtime state, dependency environments and
historical evidence. A fresh experiment does not require erasing all old data.

Implementation: README → docs/use.md → Make targets for the existing container
workflow. Docker owns core/Spark, dbt and Airflow environments; host venvs become
optional. Separate dependency trees remain explicit rather than forced together;
PySpark owns its transitive Py4J requirement. Original V0 fixture bytes moved to
tests/fixtures/v0 so a writable data mount cannot hide them. A read-only inspector
shows Kafka samples and queries actual analytical tables. Inline comments explain
processing steps, while long standalone tutorial strings were shortened. The
current-state page is concise; its original full narrative is archived unchanged.
All per-slice lesson records remain indexed in docs/README.md.

Guarantee: the documented Docker path reproduces V1's authentic bounded results;
fixture/output separation supports repeatable practice without overwriting
baselines. Reset levels are explicit: new run name, archive files, stop services,
or intentionally delete named volumes. No existing data/venvs/volumes were deleted.
Not a new recovery guarantee or a V2 implementation. A failed stage can leave
partial tables; inspect_run refuses non-PASS manifests. Resetting Kafka alone can
leave old tables whose transport records no longer exist. Checkpoints and their
output tables must be treated as a pair.

Verification: Docker build/demo/inspection passed; each demo execution has 208
rows→104 accepted/104 duplicates/0 rejected, source values and query hashes match.
Core/Spark 87 passed/10 skipped, dbt 2 passed, DAG 1 passed/1 skip; pip checks pass.
V0 CLI smoke reads 1 then 0 after commit. Original fixtures/history preserve bytes;
20 script executable ASTs unchanged, excluding explanatory strings/comments.
Local logs docs/verification/v1-tidy/; runtime data/compose/runs/tidy-verification-20261015/.
416 historical replay deliveries plus 1 synthetic, no provider traffic/performance
claim. Files: README.md, Makefile, docs/use.md, docs/README.md, inspect_run.py,
tests/test_inspect_run.py, tests/fixtures/v0/, requirements*, Dockerfile and annotated
scripts. Existing spec, teaching guide and CV bank were not rewritten.

Explain back: why raw inputs and test fixtures survive a reset; why a new Kafka
topic/checkpoint gives fresh logical state; why stopping services preserves data;
why Docker can hide environment switching without merging package dependencies.
Interview question: why can deleting only a checkpoint cause repeated delivery
rows, while deleting only output can lose already-checkpointed records?
V2.1 remains unstarted; stop for learner review.

## V2.1 — conditional S3 landing (2026-10-15, in progress)

Problem: V1 raw archives are local; ordinary S3 PUT can replace an existing key.
Concept: a bucket holds objects addressed by keys; conditional creation checks
absence and writes together. A separate HEAD followed by PUT would leave a race.
An identity policy grants scoped actions; a bucket policy enforces restrictions.

Implementation: `s3_landing.py` reads archive bytes, PUTs with IfNoneMatch="*",
GETs and compares exact bytes, then records key/size/SHA-256. A small explicit
loop preserves relative capture filenames and stops on errors. `closing` closes
the SDK client on block exit; response bodies use finally cleanup. No archive
parsing, timestamp rewrite, live capture or V1 pipeline change. `aws/` templates
grant only conditional creation/readback under raw/ and deny unconditional
replacement, deletion and insecure transport. Credentials stay outside source.

Guarantee: local tests protect request construction, byte preservation and visible
failures. They do not prove AWS service behaviour or IAM enforcement. Policies
are not deployed; real cloud immutability/readback are unverified. Append-only
policy is not Object Lock: administrators/lifecycle configuration can undermine
retention. Failure: PUT can succeed before a failed readback/timeout; the object
remains and retry refuses replacement. Partial batches are not rolled back.

Evidence: five Stubber tests passed; focused with archive/replay 15 passed/1 AWS
skip. First setup failure retained and corrected. Rebuilt Docker image, CLI help,
native pip check and policy JSON parsing passed. Logs: docs/verification/v2-1/.
No cloud/provider traffic, event count or performance metric produced.

Important files: s3_landing.py, aws/landing-*-policy.json,
tests/test_s3_landing.py, tests/test_s3_landing_live.py, docs/v2_s3_landing.md.
The learner is new to AWS: account/MFA, private bucket and restricted identity
setup are documented but unperformed. V2.1 remains IN PROGRESS; do not advance.

Interview question: why is a successful conditional PUT followed by a failed GET
an ambiguous completion, and why does retrying without the condition risk raw data?

Final container regression: `make test` exited 0, core/Spark 92 passed/11 skipped,
dbt 2 passed, DAG 1 passed/1 opt-in skip. Real AWS remains untested. Historical
fixtures/baseline and protected spec/teaching/handover files have no diff.
