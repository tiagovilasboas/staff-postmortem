# Agents

Harness-agnostic source of truth for this **blameless post-mortem template**. Humans: [CONTRIBUTING.md](CONTRIBUTING.md).

## Layout

```text
docs/template.md              blank form (copy this)
docs/severity.md              Sev vs P; when a formal PM is required
docs/example-short-spike.md   fictional Harborlot Market spike (not a real incident)
scripts/check-md-links.py     relative Markdown links (CI)
```

README is a map only. Do not grow a manifesto there. No `## Purpose` / `## Propósito`.

## Do

- Keep the template **blameless**: systems, incentives, missing signals — not names of people to punish.
- Fill every summary-table cell. Prefer `unknown` + an evidence gap over invented certainty.
- Split **primary** (what started customer pain) from **secondary** (latent bug found while looking). A spike is a brief burst of errors or latency, not a synonym for “outage”.
- Give every action an owner, a P-level, and a status. Sev describes the incident; P describes the follow-up.
- Keep examples fully fictional: generic service names (`payments-api`, `accounts-service`). Invent a marketplace if you need a story.

## Don't

- Paste firm IP: employer names, internal Azure DevOps, Datadog monitor IDs, real seller/user IDs, real emails, real product URLs, SQL against production, or Confluence copy.
- Add a new section to the template unless a Staff reader cannot decide without it (YAGNI).
- Treat a 90-second canary blip with no user impact as a mandatory novel. Teach the gate in `docs/severity.md`.
- Fork policy into `.cursor/rules` or `.github/copilot-instructions.md`. Point here.
- Commit to `main`. Open a PR. Keep `AGENTS.md` at ≤80 lines.

Verify:

```bash
test "$(wc -l < AGENTS.md)" -le 80
```
