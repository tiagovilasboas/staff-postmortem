# Examples

Two kinds. Both must stay free of firm IP (no employer names, no real user IDs, no monitor IDs, no production SQL).

| Kind | What it is | What it is not | Start here |
|---|---|---|---|
| **Fiction** | Invented marketplace (Harborlot) used to teach a distinction | A real outage with the names swapped | [`../example-checkout-latency.md`](../example-checkout-latency.md), [`../example-short-spike.md`](../example-short-spike.md) |
| **Anonymized composite** | Real-shaped failure class (silent push, webhook ACK-before-persist) assembled from public patterns | A public company incident, a named employer, or a career case | [`silent-push-webhook.md`](silent-push-webhook.md) |

Career cases (first person, PT-BR, same density bar) live in [staff-impact-cases](https://github.com/tiagovilasboas/staff-impact-cases), including [ops-postmortems](https://github.com/tiagovilasboas/staff-impact-cases/blob/main/cases/ops-postmortems.md). This repo is the review form. That repo is the case corpus. Do not paste a case into an incident doc.

## Fiction (Harborlot)

Harborlot Market is invented. Use it when you need a full fill of [`../template.md`](../template.md) without anyone asking "which company was that?"

- [`../example-checkout-latency.md`](../example-checkout-latency.md): core checkout latency. Constraint, decision, before/after.
- [`../example-short-spike.md`](../example-short-spike.md): ~2 min identity 502. When a short burst still gets a write-up.

## Anonymized composite

Labeled in the first paragraph. Composite means the clocks, counts, and service names were written for teaching. They are not a reconstruction of one employer's night.

If you add another composite, keep the heading contract (CI greps the same H2s as the template) and say **anonymized composite** on line one.
