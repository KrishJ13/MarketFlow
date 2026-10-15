# New baseline handover — 2026-10-15

The learner found the original V1 too complex and requested a minimal V0 restart
inside MarketFlowV0. They authorised the whole V0 at once, with simple scripts,
a few tests, an intuitive flow explanation and important guidance carried over.
Understanding the stack takes priority over added infrastructure/hardening.

Original PROJECT_SPEC.md and TEACHING_STYLE.md are copied unchanged. The explicit
new teaching preference is in AGENTS.md. Previous state/plan/metrics/learning/
handover/workflow instructions are copied in docs/history/ as historical context,
not proof of this new project's behaviour. Consult CURRENT_STATE.md for that.

The user subsequently authorised removal of the old files after proving technical
independence. An external copy built and passed the focused and real pipeline
checks. Old source (including uncommitted V2.1 work), authentic data and ignored
evidence are preserved in data/legacy-backup-20261015/old-project.tar.gz; SHA-256
comparisons verified 3,012 files before originals were removed. Old venvs/caches
were removed with package lists saved. Old Docker volumes remain;
old services are stopped. Work exclusively in this folder. The backup is ignored
by Git, so preserve it separately before any future workspace deletion.

The user then explicitly authorised resetting local Git history to a single
starting commit of the retained V0. The new repository stays at the parent root;
origin is retained, with no push or remote history change. Theory review precedes
any next slice. Existing V0 processing behaviour and tests are unchanged.
