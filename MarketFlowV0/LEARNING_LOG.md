# Learning log

## V0 restart — 2026-10-15

Goal: understand the complete data path through a few plain scripts before
expanding the stack. JSON becomes bytes in producer.py; Kafka stores them;
transform.py makes typed Spark columns; stream.py writes Parquet and a checkpoint;
query.py reads files and counts event-time minutes. Docker supplies the runtime.

The schema flag demonstrates one bad-price failure without silently losing its
row. A checkpoint is a processing bookmark, not business deduplication. Repeating
publication adds deliveries. No real market-data or performance claim is made.

Explain back: why can inspect_kafka.py read records without consuming them away
from Spark, and why does re-running Spark differ from re-running the producer?
Read docs/flow.md with the source. Verification: Docker build passed; `make test`
2 passed; `make verify` 1 passed using actual scripts. Three synthetic deliveries
became 3 Parquet rows; SQL counts BTC 2 / ETH 1; no-new-data restart adds 0 and
keeps 3 rows. Logs/tables remain in data/. Implementation is verified; learner
explain-back is still pending. Stop here before V1.

## V0 review and independent-project cleanup — 2026-10-15

An external copy without parent files/environments built and passed the two Spark
tests and actual pipeline/restart check. The user authorised deletion of the old
project files. Source/data/evidence were first archived and verified by SHA-256
(3,012 files); .git remains at the parent. Old virtual environments were disposable
because Docker supplies the runtime; old package lists were preserved anyway.

Review starts with producer.py: JSON file → Python dictionaries → JSON text →
UTF-8 bytes → Kafka send/acknowledgement. stream.py calls parse_trades and starts
the write; query.py later reads the resulting files. Kafka holds messages between
these separate programs. Re-running the writer resumes offsets; re-running the
producer publishes new deliveries. Learner explain-back remains pending.

Post-removal verification in the retained folder passed: 2 focused tests and
1 real pipeline/restart test. Two checks together emitted 6 synthetic deliveries
on separate test topics, with no default practice data. Logs: data/cleanup-*.log.

## Fresh Git baseline and theory recap — 2026-10-15

User-authorised local history reset makes the retained V0 one starting commit;
no push or remote history change. No processing changes or new metrics/tests.
Existing post-cleanup verification remains the evidence for this exact code.

Concepts to connect: Python serialises a synthetic trade; Kafka stores its delivery
as bytes with partition/offset; Spark parses and types it; Parquet stores the
resulting columns; SQL groups valid rows by product and event-time minute. Docker
supplies the runtime and network; Make launches these separate programs. The
checkpoint resumes processing positions; it does not remove repeated publications.
Explain-back is still pending. No V1 feature is introduced.
