# Staff Postmortem

Blameless incident-review form. Evidence-first. Copy-paste ready.

Staff pointer: write to the same density bar as [staff-impact-cases](https://github.com/tiagovilasboas/staff-impact-cases) (problem, constraint, decision, evidence, before/after). This repo is the review form. That repo is the career case corpus. Ops rite: [ops-postmortems](https://github.com/tiagovilasboas/staff-impact-cases/blob/main/cases/ops-postmortems.md).

Maintainer: [Tiago Montanha](https://github.com/tiagovilasboas) · Staff · Agentic AI · AppSec · Observability

## Start

| # | Read | Why |
|---|---|---|
| 1 | [`docs/template.md`](docs/template.md) | Blank form. Fill after the incident, not during the firefight. |
| 2 | [`docs/when-to-write.md`](docs/when-to-write.md) | Sev threshold, when not to write a novel, 48-hour draft. |
| 3 | [`docs/facilitation.md`](docs/facilitation.md) | HOW / timeline-first. Schedule the review early. Learning is not an action pile. |
| 4 | [`docs/severity.md`](docs/severity.md) | Sev = impact now. P = urgency of the follow-up. Do not mix them. |
| 5 | [`docs/examples/README.md`](docs/examples/README.md) | Fiction (Harborlot) vs anonymized composite. |
| 6 | [`docs/example-checkout-latency.md`](docs/example-checkout-latency.md) | Dense fictional checkout fill. Quantified impact, constraints, before/after. |

Copy `docs/template.md` into your incident doc. Keep names generic (`payments-api`, `checkout-api`). Never paste firm IP.

## Layout

| Path | Role |
|---|---|
| [`docs/template.md`](docs/template.md) | Summary · impact · timeline · detection · contributing factors · what went well · SMART actions |
| [`docs/facilitation.md`](docs/facilitation.md) | HOW questions, timeline first, early calendar, learning vs ticket pile |
| [`docs/examples/README.md`](docs/examples/README.md) | Fiction vs anonymized composite |
| [`docs/example-checkout-latency.md`](docs/example-checkout-latency.md) | Harborlot checkout latency (invented marketplace) |
| [`docs/example-short-spike.md`](docs/example-short-spike.md) | Harborlot identity spike (invented; spike vs novel) |
| [`docs/examples/silent-push-webhook.md`](docs/examples/silent-push-webhook.md) | Anonymized composite: silent push + webhook ACK-before-persist |
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

- [staff-impact-cases](https://github.com/tiagovilasboas/staff-impact-cases): anonymized Staff cases; same density bar (before/after, constraints). Ops rite: [ops-postmortems](https://github.com/tiagovilasboas/staff-impact-cases/blob/main/cases/ops-postmortems.md).
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
