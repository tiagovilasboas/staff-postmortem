# Post-mortem template

Copy this file. Fill it **after** mitigation, not during the firefight. Blameless: describe systems, signals, and incentives, not who to punish.

When a formal write-up is required vs skippable: [`when-to-write.md`](when-to-write.md). Sev vs P: [`severity.md`](severity.md). How to run the review: [`facilitation.md`](facilitation.md). Worked fills: [`examples/README.md`](examples/README.md).

Replace every `<!-- prompt -->` block. Prefer `unknown` + an evidence gap over a guessed story.

---

# Incident: <!-- short name, e.g. checkout place-order latency during Saturday peak -->

## Summary

| Field | Value |
|---|---|
| Date (UTC) | <!-- 2026-04-18 --> |
| Detected | <!-- clock + how (alert, customer, synthetic) --> |
| Mitigated / resolved | <!-- clock; say if still degraded --> |
| Duration | <!-- customer-visible window, not "until the ticket closed" --> |
| Severity | <!-- Sev1-Sev4; see severity.md --> |
| Customer-facing? | <!-- yes / no / internal only --> |
| Services | <!-- generic names: checkout-api, payments-api, pricing-service --> |
| Primary root cause | <!-- one sentence; what started the pain --> |
| Data loss? | <!-- no / yes (what) / unknown (what we still cannot prove) --> |
| Incident commander | <!-- role or rotation, not a blame target --> |
| Doc status | <!-- draft / reviewed / actions tracked --> |

One paragraph a VP can read: what broke, who felt it, how it stopped, whether data moved. No timeline dump. No vendor ticket IDs. No real user or seller IDs.

## Impact

Numbers or ranges. `unknown` plus the gap beats a confident guess. Do not paste account IDs.

| Dimension | Value | How we know |
|---|---|---|
| User-visible symptom | <!-- spinner, 504, wrong price, cannot pay --> | <!-- named SLI or UI copy; not a vibe --> |
| Attempts / users | <!-- count or % of the path; range OK (e.g. 2k-3k POSTs) --> | <!-- 1m counter --> |
| Error rate | <!-- baseline → peak, same SLI --> | <!-- same window as Timeline --> |
| Latency | <!-- p95 and p99, baseline → peak --> | <!-- same SLI as the user path --> |
| Blast radius | <!-- region, new vs existing, % of checkout --> | |
| SLO / error budget | <!-- % of monthly budget burned, or not measured --> | |
| Data | <!-- none lost / none duplicated / unknown pending check --> | |
| Security / privacy | <!-- none / possible (what) / confirmed (what) --> | |
| Revenue / conversion | <!-- blocked GMV range, abandoned checkout, or unknown --> | <!-- do not invent GMV --> |
| Internal | <!-- on-call hours, deploy freeze --> | |

## Timeline

Clocks in **UTC**. One row = one observed fact (alert, deploy, error-rate step, mitigate, all-clear). Not a chat log. Mark **detect**, **mitigate**, **resolve**. If clocks disagree, say so.

| Time (UTC) | Event | Evidence |
|---|---|---|
| <!-- HH:MM --> | <!-- what changed in the system or the user path --> | <!-- dashboard / log query / deploy SHA; no prod secrets --> |
| | | |
| | | |

<!-- prompt: start at first user-visible pain or a clear precursor. Do not backfill a story that logs do not support. -->

## Detection

How the room learned. If a human beat the page, that is a finding, not color.

| Field | Value |
|---|---|
| First signal | <!-- customer / support / synthetic / alert / engineer watching --> |
| First signal clock (UTC) | |
| User-visible start (UTC) | <!-- from the SLI, not from the Zoom --> |
| Time to detect | <!-- user-visible start → first signal --> |
| Page that fired | <!-- named SLI + threshold, or none --> |
| Gap | <!-- what should have paged, or "page was correct" --> |

## What happened

Facts, in order. User terms, then system terms. Do not retell the Detection table.

1. **User path:** which flow failed (checkout, onboarding, search) and what the user saw.
2. **System path:** which service called which dependency; which status codes or latency bands moved.
3. **What we did:** mitigate (rollback, feature flag, fail open/closed, scale, vendor). Separate mitigate from "root cause found".

**Constraint.** What you were not allowed to break while mitigating (checkout up, correct price, fail-closed identity, no dual-write mid-incident).

**Decision.** What you chose, plus one rejected alternative. A trigger ("we deployed") is not a decision.

<!-- prompt: a spike is a brief burst of errors or latency. Do not call a two-minute blip an "outage" unless the product was actually down. -->

## Root cause

### Primary

The condition that **started customer-visible pain**. One mechanism. Example shape: "dependency X returned HTTP 502 for ~N minutes; callers had no fallback on this path."

<!-- prompt: "someone deployed" is a trigger, not a cause. Ask what made that change unsafe (missing test, missing canary signal, unsafe default). -->

### Secondary (latent)

Defects **found while investigating** that did not start the incident but made it worse, longer, or more likely to recur. Label them latent. Do not promote them to primary.

<!-- prompt: retries without jitter, missing deadline, alert on the wrong SLI, runbook that assumes the happy path. If none, write "none found". Do not invent. -->

### What it was not

Hypotheses you **ruled out**, with the evidence. Stops the next review from re-litigating.

| Hypothesis | Why not |
|---|---|
| <!-- bad deploy of service Y --> | <!-- no SHA in window / SLI flat --> |

## Contributing factors

Two to five **systemic** conditions (process, tool limit, missing signal, incentive). Not a roster. "Someone deployed" is a trigger; "flag schema accepted 0 as disable with no checkout canary" is a factor.

1. <!-- process or schema gap -->
2. <!-- missing signal or unsafe default -->
3. <!-- incentive or traffic shape, if it changed the blast radius -->

## What went well

Name the system or ritual that shrunk the blast radius. If nothing notable, write `none` and move on. Do not invent praise.

- <!-- e.g. idempotency key held; no double charge -->
- <!-- e.g. flag rollback was one control; no hotfix compile -->

## Evidence checklist

Tick what you actually pulled. Unticked items that matter become follow-ups. Telemetry gaps: use the pattern in [sentry-golden-path](https://github.com/tiagovilasboas/sentry-golden-path) (named route, status, duration; no product IDs in this doc).

- [ ] Error rate / latency for the user-facing SLI (before, during, after)
- [ ] Dependency status (our gateway **and** the upstream, if any)
- [ ] Deploy / config / flag diff in the window
- [ ] Saturation (CPU, threads, connection pools, queue depth)
- [ ] Logs sampled with a **redacted** query (no PII, no real account IDs in this doc)
- [ ] Traces for a failing request vs a success (same route)
- [ ] Alert fire / miss (did the page happen? delay?)
- [ ] Data-integrity check (counts, idempotency, "did we double-charge or drop a write?")

If an item is N/A, say why. Do not paste vendor monitor IDs or production SQL.

## Actions

SMART: one verb, one artifact (PR, flag, alert, test), one owner, one UTC due date. Mark **mitigative** (closes this gap) vs **preventative** (closes the class). Urgency is P0-P3 ([`severity.md`](severity.md)), not a second Sev.

Reject rows like "improve monitoring", "be more careful", "add alerts", or "investigate later" unless the output is named (SLI, threshold, destination, query).

| ID | Action | Type | Owner | Due (UTC) | Urgency | Status |
|---|---|---|---|---|---|---|
| A1 | <!-- e.g. reject pricing.cache_ttl_seconds=0 at config parse --> | mitigative / preventative | <!-- team or rotation --> | <!-- YYYY-MM-DD --> | P0 / P1 / P2 / P3 | proposed / in progress / done |
| A2 | | | | | | |
| A3 | | | | | | |

Done means merged or a dated ticket. "Investigate" is not an action unless the output is named.

## Follow-ups

Work that is **not** required to close the incident but would reduce the next one: game-day, SLO rewrite, vendor contract, runbook drill. Still need an owner or an explicit "won't do".

| Item | Owner | Notes |
|---|---|---|
| | | |

## Conclusion Q&A

Answer in one to four sentences each. If you cannot, the doc is not finished.

1. **What failed for the user?**
2. **What was the primary mechanism?** (not the first alert, not the person who deployed)
3. **What latent issue did we find that did *not* start this incident?** (or "none")
4. **How will we detect this faster next time?**
5. **How will we make the same failure smaller or impossible?**
6. **Did we lose or corrupt data?** What did we check?
7. **Is a formal post-mortem the right artifact?** If this was a short spike with no lasting impact and no latent finding, a ticket + graph link may be enough. Say so and point at [`when-to-write.md`](when-to-write.md).

---

Facilitator checklist (not part of the published story): draft within 48 hours of mitigate; invite people who were in the path, not a tribunal; keep the review under an hour; file actions before the meeting ends; do not paste this repo's example into a real incident doc and search-replace the clocks.
