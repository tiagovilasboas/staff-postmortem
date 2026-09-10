# Contributing

This repository is a **Staff-grade, blameless post-mortem / incident-review template**. Copy the form into your own incident doc. Do not treat this repo as a log of real outages.

Contributing language for this file, issue forms, and pull requests is **English**. Commands and paths stay in English fences.

```text
docs/template.md
docs/severity.md
docs/when-to-write.md
docs/example-checkout-latency.md
docs/example-short-spike.md
docs/references.md
llms.txt
```

Propose changes through issues and pull requests. Do not commit to `main`.

## What belongs here

- Clearer prompts in the blank template (one extra row, one missing question, not a new framework).
- Sharper Sev / P guidance, including when a formal write-up is skippable.
- Fictional worked examples that teach a distinction (spike vs outage, primary vs latent, constraint vs decision).

This repo is **not** a company playbook, an observability vendor SDK, or a dump of real tickets. Do not add Datadog JSON, PagerDuty service IDs, or internal wiki paste.

## Quality bar

Keep the kit **short, copy-pasteable, and evidence-first**. Public structure we treat as pattern refs, not dependencies: [`docs/references.md`](docs/references.md). Density bar for a filled example matches [staff-impact-cases](https://github.com/tiagovilasboas/staff-impact-cases) (problem, constraint, decision, evidence, before/after).

A useful change is **concrete**: one checklist item, one severity rule, one sentence in the example that a Staff reader would otherwise miss.

## How to change the template

`docs/template.md` is the contract. Keep these sections, in this order:

1. Summary table (date, severity, duration, services, root cause, data loss?)
2. Impact (quantified placeholders)
3. Timeline (UTC)
4. Detection
5. What happened (constraint + decision in the prose)
6. Root cause (primary / secondary / what it was not)
7. Contributing factors (systemic)
8. What went well
9. Evidence checklist
10. Actions (SMART: owner, due, mitigative vs preventative, P, status)
11. Follow-ups
12. Conclusion Q&A

Do not rename sections for house style. Callers and CI grep these headings (`scripts/check-required-headings.py`). Prompts under a heading may get denser; do not add a parallel template file.

## How to change severity or the write gate

`docs/severity.md` owns Sev (incident impact) and P (action urgency). `docs/when-to-write.md` owns the artifact gate (threshold, skip, 48-hour draft). If you change a gate, update both examples so the docs still agree.

## How to add or edit an example

Examples must be **fully fictional**. Allowed: invented marketplace names, generic services (`payments-api`, `checkout-api`, `pricing-service`). Forbidden: real employers, real users, real monitor IDs, production SQL, copy from any company wiki.

Label the file as fictional in the first paragraph. Teach at least one distinction (spike vs outage, primary vs latent, or constraint vs decision). Dense examples need a before/after table with labeled columns (Result / Target / Qualitative).

## Pull requests

- Branch from `main`; never push commits to `main`.
- Keep PRs focused. Hygiene and a template-section change do not belong in the same PR after this bootstrap.
- Commands and paths in descriptions stay in English fences.

```bash
test "$(wc -l < AGENTS.md)" -le 80
python3 scripts/check-required-headings.py
python3 scripts/check-md-links.py
ls LICENSE CONTRIBUTING.md docs/template.md docs/severity.md \
  docs/when-to-write.md docs/example-checkout-latency.md \
  docs/example-short-spike.md docs/references.md llms.txt
```

## Principles (do / don't)

**Do**

- Stay blameless. Name systems, missing alerts, and incentives.
- Prefer `unknown` over a guessed root cause.
- Give actions an owner, a due date, a type (mitigative vs preventative), a P-level, and a status.
- Keep README a map. Keep `AGENTS.md` ≤80 lines as the agent source of truth.
- Do not use an em dash.

**Don't**

- Mix Sev and P.
- Add a Purpose / Propósito section to the README.
- Paste firm IP or a real incident, even "anonymized" if the IDs are still real.
- Grow a manifesto. KISS / YAGNI: one extra sentence that a reviewer can use, or delete it.

## License

Contributions are licensed under [MIT](LICENSE).
