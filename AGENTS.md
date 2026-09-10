# Agents

Harness-agnostic source of truth for this **blameless post-mortem template**. Humans: [CONTRIBUTING.md](CONTRIBUTING.md).

## Layout

```text
docs/template.md                   blank form (copy this)
docs/severity.md                   Sev vs P
docs/when-to-write.md              threshold; when not to write a novel; 48h draft
docs/facilitation.md               HOW / timeline-first; early calendar; not an action pile
docs/example-short-spike.md        fictional Harborlot identity spike
docs/example-checkout-latency.md   fictional Harborlot checkout latency (dense)
docs/examples/README.md            fiction vs anonymized composite
docs/examples/silent-push-webhook.md  anonymized composite (not a company incident)
docs/references.md                 public structure links only
llms.txt                           machine index: template, examples, references
scripts/check-md-links.py          relative Markdown links (CI)
scripts/check-required-headings.py template + example H2 contract (CI)
scripts/check-related-link.py      README Related → staff-impact-cases
```

README is a map only. Do not grow a manifesto there. No `## Purpose` / `## Propósito`. Do not use an em dash.

## Do

- Keep the template **blameless**: systems, incentives, missing signals; not names of people to punish.
- Fill every summary-table cell. Prefer `unknown` + an evidence gap over invented certainty.
- Split **primary** from **secondary**. A spike is a brief burst, not a synonym for "outage".
- Give every action an owner, a due date, a P-level, a type (mitigative vs preventative), and a status. Reject "improve monitoring".
- Harborlot examples stay fictional. Composites under `docs/examples/` must say they are not a public company incident.

## Don't

- Paste firm IP: employer names, Azure DevOps, monitor IDs, real user IDs, emails, product URLs, prod SQL, or Confluence copy.
- Add a template section unless a Staff reader cannot decide without it (YAGNI).
- Treat a 90-second canary blip with no user impact as a mandatory novel. Gate: `docs/when-to-write.md`.
- Fork policy into `.cursor/rules` or `.github/copilot-instructions.md`. Point here.
- Commit to `main`. Open a PR. Keep `AGENTS.md` at ≤80 lines.

Verify:

```bash
test "$(wc -l < AGENTS.md)" -le 80
```
