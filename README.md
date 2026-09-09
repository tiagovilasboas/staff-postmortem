# Staff Postmortem

Blameless incident-review template — evidence-first, actionable, copy-paste ready.

Maintainer: [Tiago Montanha](https://github.com/tiagovilasboas) · Staff · Agentic AI · AppSec · Observability

## Start

| # | Read | Why |
|---|---|---|
| 1 | [`docs/template.md`](docs/template.md) | Blank form. Fill after the incident, not during the firefight. |
| 2 | [`docs/severity.md`](docs/severity.md) | Sev = impact now. P = urgency of the follow-up. Do not mix them. |
| 3 | [`docs/example-short-spike.md`](docs/example-short-spike.md) | Fictional ~2 min KYC-like 502 spike. Shows when a formal write-up is worth it. |

Copy `docs/template.md` into your incident doc. Keep names generic (`payments-api`, `accounts-service`). Never paste firm IP.

## Layout

| Path | Role |
|---|---|
| [`docs/template.md`](docs/template.md) | Summary table · timeline · what happened · root cause · evidence · impact · actions · follow-ups · Q&A |
| [`docs/example-short-spike.md`](docs/example-short-spike.md) | Worked Harborlot Market sample (invented marketplace; not a real incident) |
| [`docs/severity.md`](docs/severity.md) | Sev1–Sev4 and P0–P3; when a formal post-mortem is vs is not required |

## Contents

- [Start](#start)
- [Layout](#layout)
- [Related](#related)
- [Contributing](#contributing)
- [License](#license)

## Related

This repo is the review form. Siblings are scoped kits — not a vendor runbook.

- [awesome-agentic-ai](https://github.com/tiagovilasboas/awesome-agentic-ai) — Curated HITL / ops / AppSec links. Decision filter, not an incident log.
- [agent-measurement](https://github.com/tiagovilasboas/agent-measurement) — Evals: named metrics, instance rows. Measure; do not train.
- [agentic-code-review](https://github.com/tiagovilasboas/agentic-code-review) — AppSec PR review: `path:line` or silence.
- [grok-bot-architecture](https://github.com/tiagovilasboas/grok-bot-architecture) — Desktop assistant OS; Obs traces/evals, not this form.
- [sentry-golden-path](https://github.com/tiagovilasboas/sentry-golden-path) — Error/tracing golden path (sibling; fill telemetry gaps here, not product IDs).

Public refs (patterns, not dependencies): [Google SRE — postmortem](https://sre.google/sre-book/postmortem-culture/) · [Google SRE workbook — example](https://sre.google/workbook/postmortem-culture/) · [PagerDuty — postmortem](https://response.pagerduty.com/after/post_mortem_process/) · [Learning from Incidents](https://www.learningfromincidents.io/)

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

[MIT](LICENSE)

Agent notes: [`AGENTS.md`](AGENTS.md).
