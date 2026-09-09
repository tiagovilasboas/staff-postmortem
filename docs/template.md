# Post-mortem template

Copy this file. Fill it **after** mitigation, not during the firefight. Blameless: describe systems, signals, and incentives — not who to punish.

When a formal write-up is required vs skippable: [`severity.md`](severity.md). Worked (fictional) fill: [`example-short-spike.md`](example-short-spike.md).

Replace every `<!-- prompt -->` block. Prefer `unknown` + an evidence gap over a guessed story.

---

# Incident: <!-- short name, e.g. identity-gateway 502 during seller onboarding -->

## Summary

| Field | Value |
|---|---|
| Date (UTC) | <!-- 2026-03-12 --> |
| Detected | <!-- clock + how (alert, customer, synthetic) --> |
| Mitigated / resolved | <!-- clock; say if still degraded --> |
| Duration | <!-- customer-visible window, not “until the ticket closed” --> |
| Severity | <!-- Sev1–Sev4 — see severity.md --> |
| Customer-facing? | <!-- yes / no / internal only --> |
| Services | <!-- generic names: payments-api, accounts-service, … --> |
| Primary root cause | <!-- one sentence; what started the pain --> |
| Data loss? | <!-- no / yes (what) / unknown (what we still cannot prove) --> |
| Incident commander | <!-- role or rotation, not a blame target --> |
| Doc status | <!-- draft / reviewed / actions tracked --> |

One paragraph a VP can read: what broke, who felt it, how it stopped, whether data moved.

<!-- prompt: no timeline dump here. no vendor ticket IDs. no real user/seller IDs. -->

## Timeline

Clocks in **UTC**. One row = one observed fact (alert, deploy, error-rate step, mitigate, all-clear). Not a chat log.

| Time (UTC) | Event | Evidence |
|---|---|---|
| <!-- HH:MM --> | <!-- what changed in the system or the user path --> | <!-- dashboard / log query / deploy SHA — no prod secrets --> |
| | | |
| | | |

<!-- prompt: mark detect, mitigate, resolve. If clocks disagree, say so. Do not backfill a story that logs do not support. -->

## What happened

Facts, in order, in user terms then system terms.

1. **User path** — which flow failed (checkout, onboarding, search, …) and what the user saw.
2. **System path** — which service called which dependency; which status codes or latency bands moved.
3. **How we knew** — alert, synthetic, customer ticket, or someone watching a graph. Name the **gap** if we learned from a human first.
4. **What we did** — mitigate (rollback, feature flag, fail open/closed, scale, vendor). Separate mitigate from “root cause found”.

<!-- prompt: a spike is a brief burst of errors or latency. Do not call a two-minute blip an “outage” unless the product was actually down. -->

## Root cause

### Primary

The condition that **started customer-visible pain**. One mechanism. Example shape: “dependency X returned HTTP 502 for ~N minutes; callers had no fallback on this path.”

<!-- prompt: “someone deployed” is a trigger, not a cause. Ask what made that deploy unsafe (missing test, missing canary signal, unsafe default). -->

### Secondary (latent)

Defects **found while investigating** that did not start the incident but made it worse, longer, or more likely to recur. Label them latent. Do not promote them to primary.

<!-- prompt: retries without jitter, missing circuit breaker, alert on the wrong SLI, runbook that assumes the happy path. If none, write “none found” — do not invent. -->

### Contributing factors

Conditions that were true and relevant but are not the mechanism (traffic shape, recent migration, vendor maintenance window we did not track). Not a blame list.

### What it was not

Hypotheses you **ruled out**, with the evidence. Stops the next review from re-litigating.

## Evidence checklist

Tick what you actually pulled. Unticked items that matter become follow-ups.

- [ ] Error rate / latency for the user-facing SLI (before, during, after)
- [ ] Dependency status (our gateway **and** the upstream, if any)
- [ ] Deploy / config / flag diff in the window
- [ ] Saturation (CPU, threads, connection pools, queue depth)
- [ ] Logs sampled with a **redacted** query (no PII, no real account IDs in this doc)
- [ ] Traces for a failing request vs a success (same route)
- [ ] Alert fire / miss (did the page happen? delay?)
- [ ] Data-integrity check (counts, idempotency, “did we double-charge or drop a write?”)

If an item is N/A, say why. Do not paste vendor monitor IDs or production SQL.

## Impact

| Dimension | What we know |
|---|---|
| User-visible | <!-- errors, timeouts, wrong message, cannot complete flow --> |
| Who / blast radius | <!-- % or count of attempts; region; new vs existing users. Ranges OK. --> |
| SLO / error budget | <!-- burned / not burned / not measured --> |
| Data | <!-- none lost / none duplicated / unknown pending check --> |
| Security / privacy | <!-- none / possible (what) / confirmed (what) --> |
| Revenue / ops | <!-- payments blocked? support volume? leave unknown if not measured --> |
| Internal | <!-- on-call hours, blocked deploys --> |

## Actions

Every row needs an **owner**, a **P-level** ([`severity.md`](severity.md): urgency of the work, not a second Sev), and a **status**. Prefer prevent / detect over “be more careful”.

| ID | Action | Owner | Urgency | Status |
|---|---|---|---|---|
| A1 | <!-- e.g. cap retries + add jitter on identity 5xx --> | <!-- team or rotation --> | P0 / P1 / P2 / P3 | proposed / in progress / done |
| A2 | | | | |
| A3 | | | | |

Done means merged or a dated ticket. “Investigate” is not an action unless the output is named (dashboard, test, flag).

## Follow-ups

Work that is **not** required to close the incident but would reduce the next one: game-day, SLO rewrite, vendor contract, runbook drill. Still need an owner or an explicit “won’t do”.

| Item | Owner | Notes |
|---|---|---|
| | | |

## Conclusion Q&A

Answer in one to four sentences each. If you cannot, the doc is not finished.

1. **What failed for the user?**
2. **What was the primary mechanism?** (not the first alert, not the person who deployed)
3. **What latent issue did we find that did *not* start this incident?** (or “none”)
4. **How will we detect this faster next time?**
5. **How will we make the same failure smaller or impossible?**
6. **Did we lose or corrupt data?** What did we check?
7. **Is a formal post-mortem the right artifact?** If this was a short spike with no lasting impact and no latent finding, a ticket + graph link may be enough — say so and point at [`severity.md`](severity.md).

---

Facilitator checklist (not part of the published story): invite people who were in the path, not a tribunal; keep the review under an hour; file actions before the meeting ends; do not paste this repo’s example into a real incident doc and search-replace the clocks.
