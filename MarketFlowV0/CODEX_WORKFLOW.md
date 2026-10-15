# Working procedure

1. Read AGENTS.md, CURRENT_STATE.md and VERSION_PLAN.md. Consult the copied
   specification/teaching guide for the relevant version, not every future feature.
2. Inspect the scripts and Git status. Show the data flow and the smallest intended
   behavioural change before editing.
3. Use short functions and direct library calls. Explain input → work → output.
4. Add a few meaningful tests. Run the relevant test and a real connection check
   when that is the concept being introduced. Preserve actual output in data/.
5. Record actual behaviour and limits in CURRENT_STATE.md, mark the plan, append
   a short learning note. Record measurements only if actually made.
6. Stop for learner review. Do not proceed because tests pass if the learner does
   not understand how the pieces fit.

The user expressly approved building the entire simpler V0 in this restart.
No V1 or cloud work is authorised by that exception. Do not delete the old project
or its evidence as part of preparing this new baseline.
