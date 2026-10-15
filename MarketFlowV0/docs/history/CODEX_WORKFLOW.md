# Codex Working Procedure

## Phase 1 — Reconcile context with reality

Before the first implementation task after handover:

1. Read all repository guidance.
2. Inspect repository layout.
3. Inspect Git history where useful.
4. Identify build/test commands.
5. Run existing test suite if practical.
6. Compare actual code against `CHAT_HANDOVER.md`.
7. Create/update `CURRENT_STATE.md`.
8. Create/update `VERSION_PLAN.md`.

Conversation history is context.

Repository evidence is authoritative for implementation state.

---

## Phase 2 — Select one slice

Choose the smallest incomplete slice from `VERSION_PLAN.md`.

A valid slice should have:

- one main behavioural goal;
- one motivating limitation/problem;
- a bounded set of files;
- a clear verification method.

Avoid tasks such as:

`Complete V2.`

Prefer:

`Make reservation creation idempotent under duplicate client retries.`

---

## Phase 3 — Pre-implementation explanation

Before editing, state briefly:

### Problem

What currently goes wrong or is missing?

### Mental model

What concept solves it?

### Planned behaviour

What observable behaviour will change?

### Invariant / requirement

Which project rule does this serve?

### Verification

Which test/experiment will prove it?

### Non-goals

What are we explicitly not implementing yet?

Then implement.

---

## Phase 4 — Implementation

While working:

- keep change scoped;
- follow existing conventions;
- preserve the baseline;
- add tests alongside behaviour;
- avoid unrelated cleanup;
- document important assumptions.

If unexpected architecture is discovered:

pause and explain before performing a large redesign.

---

## Phase 5 — Verification

Run the smallest sufficient verification first.

Then broader tests where appropriate.

Possible evidence:

- unit test;
- integration test;
- deterministic race;
- data reconciliation;
- API smoke test;
- benchmark;
- manual end-to-end flow.

Do not declare success if tests were not run unless execution is genuinely unavailable.

If unavailable, state exactly why.

---

## Phase 6 — Measurement

If the slice is performance/quality related:

1. define workload;
2. preserve baseline;
3. record environment/configuration;
4. run before measurement;
5. make one main change;
6. run after measurement;
7. preserve raw outputs;
8. update `METRICS.md`.

No invented numbers.

No extrapolation from tiny local measurements into production-scale claims.

---

## Phase 7 — Learning summary

Append a concise entry to `LEARNING_LOG.md`:

- concept;
- problem;
- implementation;
- guarantee;
- what it does not guarantee;
- failure mode;
- tests/evidence;
- important files;
- one interview-style question.

---

## Phase 8 — State update

Update `CURRENT_STATE.md` with actual verified code state.

Update `VERSION_PLAN.md`:

- mark current slice complete;
- identify next smallest slice.

Update `METRICS.md` if any metric changed.

Do not modify `PROJECT_SPEC.md` or `TEACHING_STYLE.md`.

---

## Phase 9 — Stop for user review

Report the completed slice and STOP.

Wait for the user to inspect/understand the change before starting the next consequential slice.
