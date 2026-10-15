# Evidence

Only synthetic fixture correctness is being checked. No authentic source traffic,
benchmark, throughput, latency or scale claim. Test/build durations are diagnostic.
The old project's evidence ledger is preserved in docs/history/METRICS.md and its
underlying datasets/logs remain in the parent project.

2026-10-15: `make test` 2 passed; `make verify` 1 passed. Real local Kafka/Spark:
3 new synthetic deliveries = 3 Parquet rows. SQL groups those as BTC 2 / ETH 1;
same-checkpoint restart adds 0, saved total remains 3. No new authentic events.
Logs: data/tests-first.log, data/verify-first.log and
data/verification-20261015T191704Z/test_pipeline_and_checkpoint_r0/.

2026-10-15 independence check: external standalone copy build passed; 2 focused
tests and 1 real pipeline/restart test passed. It emitted 3 synthetic deliveries,
not authentic events. Logs retained at data/independence-verification-20261015/.
Cleanup archive hashes verify byte preservation, not pipeline performance/recovery.

Post-removal check from retained folder: `make test` 2 passed; `make verify`
1 passed, another 3 synthetic deliveries → 3 rows with no-new-data restart at 3.
Total new transport deliveries during cleanup: 6 synthetic (two isolated checks).
No benchmark. Logs: data/cleanup-tests.log, data/cleanup-verify.log and
data/verification-20261015T193149Z/.
