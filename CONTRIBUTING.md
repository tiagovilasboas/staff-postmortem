# Contributing

This repository is a **Staff-grade, blameless post-mortem / incident-review template**. Copy the form into your own incident doc. Do not treat this repo as a log of real outages.

Contributing language for this file, issue forms, and pull requests is **English**. Commands and paths stay in English fences.

```text
docs/template.md
docs/severity.md
docs/example-short-spike.md
```

Propose changes through issues and pull requests. Do not commit to `main`.

## What belongs here

- Clearer prompts in the blank template (one extra row, one missing question — not a new framework).
- Sharper Sev / P guidance, including when a formal write-up is skippable.
- Fictional worked examples that teach a distinction (spike vs outage, primary vs latent).

This repo is **not** a company playbook, an observability vendor SDK, or a dump of real tickets. Do not add Datadog JSON, PagerDuty service IDs, or internal wiki paste.

## Quality bar

Keep the kit **short, copy-pasteable, and evidence-first**. Public SRE materials we treat as pattern refs, not dependencies:

| Pattern | What to keep in our docs |
|---|---|
| [Google SRE — postmortem culture](https://sre.google/sre-book/postmortem-culture/) | Blameless. Fix the system. Write so the next on-call can act. |
| [SRE workbook — example](https://sre.google/workbook/postmortem-culture/) | Timeline with clocks. Impact in user terms. Actions with owners. |
| [PagerDuty after-incident](https://response.pagerduty.com/after/post_mortem_process/) | Facilitate learning. Separate the review from the firefight. |
| [Learning from Incidents](https://www.learningfromincidents.io/) | Ask what made the failure possible, not who to blame. |

A useful change is **concrete**: one checklist item, one severity rule, one sentence in the example that a Staff reader would otherwise miss.

## How to change the template

`docs/template.md` is the contract. Keep these sections, in this order:

1. Summary table (date, severity, duration, services, root cause, data loss?)
2. Timeline
3. What happened
4. Root cause (primary / secondary)
5. Evidence checklist
6. Impact
7. Actions (owner / urgency / status)
8. Follow-ups
9. Conclusion Q&A

Do not rename sections for house style. Callers grep these headings. Prompts under a heading may get denser; do not add a parallel template file.

## How to change severity

`docs/severity.md` owns Sev (incident impact) and P (action urgency). If you change a gate (“formal PM required when…”), update the example so the two docs still agree.

## How to add or edit an example

Examples must be **fully fictional**. Allowed: invented marketplace names, generic services (`payments-api`, `accounts-service`, `identity-gateway`). Forbidden: real employers, real users, real monitor IDs, production SQL, copy from any company wiki.

Label the file as fictional in the first paragraph. Teach at least one distinction (for example spike vs outage, or primary failure vs latent bug).

## Pull requests

- Branch from `main`; never push commits to `main`.
- Keep PRs focused. Hygiene and a template-section change do not belong in the same PR after this bootstrap.
- Commands and paths in descriptions stay in English fences.

```bash
test "$(wc -l < AGENTS.md)" -le 80
ls LICENSE CONTRIBUTING.md docs/template.md docs/severity.md docs/example-short-spike.md
```

## Principles (do / don't)

**Do**

- Stay blameless. Name systems, missing alerts, and incentives.
- Prefer `unknown` over a guessed root cause.
- Give actions an owner, a P-level, and a status.
- Keep README a map. Keep `AGENTS.md` ≤80 lines as the agent source of truth.

**Don't**

- Mix Sev and P.
- Add a Purpose / Propósito section to the README.
- Paste firm IP or a real incident, even “anonymized” if the IDs are still real.
- Grow a manifesto. KISS / YAGNI: one extra sentence that a reviewer can use, or delete it.

## License

Contributions are licensed under [MIT](LICENSE).
