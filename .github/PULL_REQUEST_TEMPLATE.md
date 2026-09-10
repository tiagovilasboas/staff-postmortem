## Why

What gap in the template, severity gate, or fictional example does this close? Link the issue when one exists.

## What

What files changed? Name the heading or rule, not a vibe.

## How to verify

Paths and commands in English fences:

```bash
test "$(wc -l < AGENTS.md)" -le 80
python3 scripts/check-required-headings.py
python3 scripts/check-related-link.py
python3 scripts/check-md-links.py
ls LICENSE CONTRIBUTING.md docs/template.md docs/severity.md \
  docs/when-to-write.md docs/facilitation.md \
  docs/example-checkout-latency.md docs/example-short-spike.md \
  docs/examples/README.md docs/examples/silent-push-webhook.md \
  docs/references.md llms.txt
```

## Guardrails

- [ ] README stays a map (no `## Purpose` / `## Propósito`)
- [ ] Template sections are not renamed or dropped
- [ ] Sev (impact) and P (action urgency) stay distinct
- [ ] Examples stay Harborlot fiction or a labeled anonymized composite: no firm IP, real IDs, or wiki paste
- [ ] `AGENTS.md` is still ≤80 lines and remains the agent source of truth
