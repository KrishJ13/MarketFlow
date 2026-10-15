# MarketFlow — simplified V0 learning instructions

This repository root is the standalone learning project. Its contents were moved
from MarketFlowV0/ at the user's request. Run commands from this directory.

PROJECT_SPEC.md is the unchanged eventual destination. TEACHING_STYLE.md is the
unchanged original teaching reference. The explicit user direction below takes
precedence where it asks for a simpler approach. CURRENT_STATE.md records verified
behaviour, VERSION_PLAN.md records the next lesson, and CODEX_WORKFLOW.md describes
the short working procedure. LEARNING_LOG.md and METRICS.md contain only this new
baseline's evidence. docs/history/ contains reference history, not current claims.

## Fundamentals-first restart — explicit user direction (2026-10-15)

This section governs how to apply the broader rules above. The learner reports
that much of V1 was too complex to understand. Prior completed tests do not mean
the learner understands the code. Optimise for a small program they can explain.

- The active starting point is the simplified V0 in this repository root
  (formerly `MarketFlowV0/`). The user authorises building its whole V0 at once.
  Stop after V0 for review; later versions still progress in order towards V2.
  Pause the old project's V2.1 work. Preserve old files/evidence until deletion
  is separately requested; do not assume this request authorises deletion now.
- Show the complete data flow first, then where each file/function belongs.
  Explain each function as input → operation → output, with one concrete record.
  Teach the direct library calls before introducing wrappers or abstractions.
- Prefer a few plain scripts, small functions and ordinary Python data structures.
  A helper should name a clear step or share meaningful logic with a test.
  Do not add classes, frameworks, factories, generic configuration, custom error
  types, reporting systems or orchestration just to organise a tiny example.
- Introduce one technology because its role is needed: Python sends records;
  Kafka retains them; Spark transforms them; files store results; SQL queries
  those files. Later, Airflow schedules existing scripts, S3 stores objects,
  Delta adds table transactions, and dbt builds SQL models. Do not add them to V0.
- Use only a few focused tests: normal transformation, one important invalid
  example, and a real end-to-end check when practical. Avoid elaborate test
  runners, malformed-input matrices and benchmark harnesses in the learning code.
- Keep required credentials private, close resources, isolate local experiments
  and do not silently lose data. For cloud services, explain the minimum access
  permission needed to connect. Defer additional IAM policy layers, retention
  controls, security automation and hardening until their own lesson or actual need.
  Do not equate a learning prototype with a deployment-ready system.
- Document limitations in a few sentences instead of implementing all safeguards.
  V0 may count repeated deliveries and use a single broker. Label synthetic data
  honestly; keep event time distinct from processing time. These are deliberate
  baselines, not hidden correctness or performance guarantees.
- Keep the README runnable and explanations concrete. Minimal formatting and
  short state/learning notes are enough. No new dashboards, metric ledgers full
  of hypothetical claims or large operational checklists for a small lesson.
- Treat the copied full specification as the eventual destination, not a request
  to implement its final architecture immediately. Keep specification and teaching
  source files intact; this explicit user direction controls the simpler approach.

### Examples of the expected teaching style

For Kafka, show `producer.send(topic, value=payload).get(timeout=10)` and explain:
“The input is bytes containing one JSON trade. send asks Kafka to store them;
get waits for Kafka's reply. The returned partition/offset says where they went.”

For Spark, show `from_json(col("value").cast("string"), schema)` and explain:
“Kafka gives us bytes. We turn them into text, then use the schema to turn the
JSON fields into named columns. This builds a plan; the streaming write runs it.”

For SQL, show `SELECT product_id, COUNT(*) FROM trades GROUP BY product_id`:
“The input is the saved trade rows. Grouping puts BTC rows together, then COUNT
counts each group. Publishing the same trade twice produces two delivery rows.”

For later Airflow, start with “run script A before script B on a schedule,”
then show the two tasks and their dependency. For later S3, start with
`client.put_object(Bucket=bucket, Key="raw/example.json", Body=payload)`:
“Bucket is the storage container, Key is the object's name, Body is its bytes.
Ordinary PUT can replace that name; create-only protection is a separate lesson.”
