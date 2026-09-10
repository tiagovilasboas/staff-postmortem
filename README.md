# Staff Postmortem

Blameless incident-review form. Evidence-first. Copy-paste ready.

Staff pointer: write to the same density bar as [staff-impact-cases](https://github.com/tiagovilasboas/staff-impact-cases) (problem, constraint, decision, evidence, before/after). This repo is the review form. That repo is the career case corpus.

Maintainer: [Tiago Montanha](https://github.com/tiagovilasboas) · Staff · Agentic AI · AppSec · Observability

## Start

| # | Read | Why |
|---|---|---|
| 1 | [`docs/template.md`](docs/template.md) | Blank form. Fill after the incident, not during the firefight. |
| 2 | [`docs/when-to-write.md`](docs/when-to-write.md) | Sev threshold, when not to write a novel, 48-hour draft. |
| 3 | [`docs/severity.md`](docs/severity.md) | Sev = impact now. P = urgency of the follow-up. Do not mix them. |
| 4 | [`docs/example-checkout-latency.md`](docs/example-checkout-latency.md) | Dense fictional checkout fill. Quantified impact, constraints, before/after. |
| 5 | [`docs/example-short-spike.md`](docs/example-short-spike.md) | Fictional ~2 min identity 502 spike. When a short burst still gets a write-up. |

Copy `docs/template.md` into your incident doc. Keep names generic (`payments-api`, `checkout-api`). Never paste firm IP.

## Layout

| Path | Role |
|---|---|
| [`docs/template.md`](docs/template.md) | Summary · impact · timeline · detection · contributing factors · what went well · SMART actions |
| [`docs/example-checkout-latency.md`](docs/example-checkout-latency.md) | Worked Harborlot checkout latency (invented marketplace; not a real incident) |
| [`docs/example-short-spike.md`](docs/example-short-spike.md) | Worked Harborlot identity spike (invented; teaches spike vs novel) |
| [`docs/when-to-write.md`](docs/when-to-write.md) | Threshold, skip rules, 48-hour draft |
| [`docs/severity.md`](docs/severity.md) | Sev1-Sev4 and P0-P3 |
| [`docs/references.md`](docs/references.md) | Public structure links only |
| [`llms.txt`](llms.txt) | Machine index: template, examples, references |

## Contents

- [Start](#start)
- [Layout](#layout)
- [Related](#related)
- [Contributing](#contributing)
- [License](#license)

## Related

This repo is the review form. Siblings are scoped kits, not a vendor runbook.

- [staff-impact-cases](https://github.com/tiagovilasboas/staff-impact-cases): anonymized Staff cases; same density bar (before/after, constraints).
- [sentry-golden-path](https://github.com/tiagovilasboas/sentry-golden-path): error/tracing golden path (fill telemetry gaps here, not product IDs).
- [awesome-agentic-ai](https://github.com/tiagovilasboas/awesome-agentic-ai): curated HITL / ops / AppSec links. Decision filter, not an incident log.
- [agent-measurement](https://github.com/tiagovilasboas/agent-measurement): evals with named metrics, instance rows. Measure; do not train.
- [agentic-code-review](https://github.com/tiagovilasboas/agentic-code-review): AppSec PR review: `path:line` or silence.
- [grok-bot-architecture](https://github.com/tiagovilasboas/grok-bot-architecture): desktop assistant OS; traces/evals, not this form.

Public refs: [`docs/references.md`](docs/references.md) (links only).

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

[MIT](LICENSE)

Agent notes: [`AGENTS.md`](AGENTS.md).
