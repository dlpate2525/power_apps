# Domain documentation

Use a single context for this repository. Shared terminology belongs in root `GLOSSARY.md`; architectural decisions belong in root `docs/adr/`.

An architectural decision record, or ADR, explains an important design choice and its consequences.

## Read before exploring

1. Read root `GLOSSARY.md` if it exists.
2. Read ADRs that concern the area being explored or changed.
3. Use the glossary's terms in code, tests, tickets, reviews, and documentation.
4. Identify any conflict with an existing ADR before proposing a different design.

If these files are absent, continue silently. Create them through domain modeling only when real terms or decisions are resolved.

## Record resolved knowledge

Keep one root glossary for the shared vocabulary. Record each accepted architectural decision in a numbered Markdown file under `docs/adr/`.

Create the directory and its first record together. Empty glossary files and empty ADR directories are not setup requirements.

When a needed term is missing, check existing project language first. Record a real terminology gap for the next domain-modeling task.

When proposing a change that conflicts with an ADR, link the record and explain why the decision should be revisited.
