# AcceleratorHub / MarketFlow / RepoPilot Codex Instructions

## Authority

The following files have distinct responsibilities:

1. `PROJECT_SPEC.md`

   - Defines **what the finished project should become**.
   - Do not rewrite or silently change it.

2. `TEACHING_STYLE.md`

   - Defines **how the project should be developed and taught**.
   - Do not rewrite or silently change it.

3. `CHAT_HANDOVER.md`

   - Historical context reconstructed from earlier ChatGPT conversations.
   - Useful context, but not proof of repository state.

4. `CURRENT_STATE.md`

   - The authoritative description of what is actually present and verified in the current repository.

5. `VERSION_PLAN.md`

   - Ordered remaining implementation slices up to the currently approved target.

6. `METRICS.md`

   - Measurement and CV-claim evidence ledger.

7. `LEARNING_LOG.md`

   - Concise technical explain-back notes for the learner.

8. `CODEX_WORKFLOW.md`

   - Mandatory detailed working procedure.

## Current scope

The immediate target is **V2 only**.

Do not implement V3, V4, V5, optional stretch features, or unrelated infrastructure unless the user explicitly changes the scope.

## Undergraduate learning priority

This is an undergraduate learning project, not a service intended for deployment.
The user wants to learn the tech stack and its fundamentals one slice at a time.
The existing task prompts and version sequence still apply, but implementations
must make the main concept easy to see.

- Prefer short, readable functions, explicit loops and the existing script conventions.
- Introduce only the concepts needed for the current slice. Explain unfamiliar syntax briefly.
- Avoid defensive checks for every possible input, generic abstractions, elaborate configuration and production hardening unless they are the subject of the slice.
- Use ordinary Python exceptions for unexpected inputs when that keeps the lesson clear. Do not swallow errors or silently discard data to simplify code.
- Keep basic resource cleanup and safe handling of credentials. Add further security/reliability mechanisms when the slice teaches them or an actual use requires them.
- Keep tests small and focused on the main behaviour and, where useful, one important failure. Do not add large malformed-input matrices or complex test scaffolding for hypothetical cases.
- Explain assumptions and deferred limitations concisely instead of implementing every safeguard immediately.
- Preserve honest provenance, event-time semantics and measurement claims. Simpler code must not imply guarantees it does not provide.
- Prefer a short learning explanation over an exhaustive operational checklist. Stop after the slice for learner review.
- Add short comments beside the main processing steps, explaining the slice concept and why the step exists. Avoid narrating obvious syntax.
- Use README.md and docs/use.md for the current Docker/Make workflow; keep historical slice notes and measurement evidence intact.

This priority records the user's explicit learning preference and governs how to
apply the broader working and teaching guidance. It does not change the project
specification or authorize skipping ahead in the version plan. When asked to
implement, implement the small slice; otherwise teach and review.

## Fundamentals-first restart — explicit user direction (2026-10-15)

This section governs how to apply the broader rules above. The learner reports
that much of V1 was too complex to understand. Prior completed tests do not mean
the learner understands the code. Optimise for a small program they can explain.

- The active starting point is now `MarketFlowV0/`, a standalone learning project
  inside this repository. The user authorises building its whole V0 at once.
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

## Before editing code

For every new coding session or substantial task:

1. Read:

   - `PROJECT_SPEC.md`
   - `TEACHING_STYLE.md`
   - `CHAT_HANDOVER.md`
   - `CURRENT_STATE.md`
   - `VERSION_PLAN.md`
   - `METRICS.md`
   - `CODEX_WORKFLOW.md`

2. Inspect the actual repository.

3. Run `git status`.

4. Identify the exact next incomplete slice.

5. Verify that the proposed work does not jump ahead in the teaching/version sequence.

6. State the intended behavioural change and verification before editing.

## Working rules

- Work on **one coherent implementation slice at a time**.
- Prefer small reviewable diffs.
- Preserve existing behaviour unless the task explicitly changes it.
- Do not perform broad unrelated refactors.
- Do not replace deliberately naive baselines before their limitation has been demonstrated.
- Do not introduce a new production dependency merely because it appears in the final specification.
- Reuse the project's existing build/package conventions.
- Do not change language, framework, build system, or major architecture without an explicit justified decision.
- Write or update tests for consequential behaviour.
- Run relevant tests before declaring a slice complete.
- When correctness, concurrency, quality, or performance is involved, define the failure/metric before optimisation.
- Never fabricate benchmark results, scale figures, latency, throughput, accuracy, or CV claims.
- Preserve raw benchmark/evaluation output where metrics are produced.
- Distinguish synthetic/replayed workloads from authentic/unique data where relevant.
- Treat security and failure behaviour as part of implementation, not final polish.

## User-review boundary

After one meaningful slice is implemented and verified:

STOP.

Do not automatically continue into the next major slice.

Report:

- what changed;
- why;
- files changed;
- tests/commands run;
- result;
- architectural/correctness guarantee added;
- what it does **not** guarantee;
- one important failure mode;
- metrics produced, if any;
- next recommended slice.

Then update the repository state files defined in `CODEX_WORKFLOW.md`.

## Git

- Do not rewrite unrelated history.
- Do not force-push.
- Do not push unless explicitly asked.
- Do not create large multi-feature commits.
- Suggest one concise commit message for each completed slice.
- Preserve benchmark baselines and failed experiments when they are educational/evidentiary.

## Completion definition

A slice is not complete merely because code exists.

It must have:

- correct observable behaviour;
- relevant tests;
- verification output;
- documentation/state update;
- learner-facing explanation;
- no known silent invariant break.

---

# PROJECT-SPECIFIC ADDENDUM

## MarketFlow Addendum

Immediate target: V2 only.

Primary technical story:

Python / Kafka / Spark / Delta / Airflow / Databricks / Snowflake / dbt.

Responsibilities must remain explicit:

- Kafka = durable event transport/log.
- Spark = distributed batch/stream processing.
- Delta/Databricks = lakehouse processing/storage layer.
- Airflow = orchestration/backfills, not stream processing.
- Snowflake = analytical warehouse.
- dbt = warehouse modelling/testing.

Never violate:

- authentic raw source events remain reproducible;
- replay must not be confused with unique event volume;
- Kafka ordering assumptions are partition-scoped;
- duplicate delivery must be handled safely;
- event time and processing time remain distinct;
- late-data policy must be explicit;
- backfills must not silently corrupt live logical data;
- critical layers must be reconcilable.

Do not benchmark the public upstream data provider.

Use local/archive replay for scale experiments.
