# Example: short identity-verification spike (fictional)

**This is not a real incident.** Harborlot Market is an invented C2C marketplace. Service names are generic. No employer, no real users, no monitor IDs.

Use it to see how [`template.md`](template.md) reads when filled. Lesson, not lore:

- A **spike** is a brief burst of errors or latency. Here the user-visible burst was ~2 minutes.
- **Primary** = the dependency 502 that started the pain.
- **Secondary / latent** = unbounded retries in `accounts-service` found **while looking**. They did not start the 502.
- Formal post-mortem: duration alone would argue “skip”; the latent retry bug and a core onboarding path argue **write it**. See [`severity.md`](severity.md).

---

# Incident: identity-gateway 502 during new-seller onboarding

## Summary

| Field | Value |
|---|---|
| Date (UTC) | 2026-03-12 |
| Detected | 14:03 UTC — on-call noticed a Slack ping from support (“verify ID” failing), ~90s before the latency alert |
| Mitigated / resolved | 14:05 UTC — `idv-provider` 502s stopped; user-visible error rate back to baseline by 14:06 |
| Duration | **~2 minutes** customer-visible (14:03–14:05); retry tail until 14:06 |
| Severity | **Sev3** — onboarding identity check degraded; payments and browse unaffected; workaround = retry |
| Customer-facing? | Yes — new sellers on the identity step |
| Services | `accounts-service`, `identity-gateway`; upstream `idv-provider` (vendor) |
| Primary root cause | `idv-provider` returned HTTP 502 for ~2 minutes; `identity-gateway` had no alternate vendor on this path |
| Data loss? | **No** — identity checks are read/validate; no seller record written until a 200 from the vendor |
| Incident commander | On-call (payments/accounts rotation); no separate IC — blast radius did not justify one |
| Doc status | Reviewed — actions tracked |

Harborlot new-seller onboarding calls `accounts-service` → `identity-gateway` → `idv-provider` to check an ID document. For about two minutes the vendor returned 502. Sellers saw “could not verify identity, try again.” Checkout and existing accounts were fine. While pulling traces we found `accounts-service` retrying those 502s **eight times with no jitter**, which held pools and added a one-minute error tail after the vendor recovered. We are writing this up for the latent retry bug, not because two minutes of vendor 502 is automatically a novel.

## Timeline

| Time (UTC) | Event | Evidence |
|---|---|---|
| 14:02:40 | `idv-provider` 5xx rate leaves baseline (vendor status later confirmed a regional fault) | `identity-gateway` outbound 5xx; vendor status page (public, no ticket ID copied here) |
| 14:03:10 | User-visible errors on `POST /onboarding/identity` step from ~0.2% to ~18% of attempts | `accounts-service` SLI: error rate, 1m |
| 14:03:20 | Support reports two sellers stuck on “verify ID” | Support queue (counts only; no seller IDs in this doc) |
| 14:03:40 | On-call opens the onboarding dashboard; confirms payments-api p99 unchanged | Split: onboarding identity vs `payments-api` checkout |
| 14:04:10 | Latency alert on `identity-gateway` p95 (threshold 2s) — **after** humans | Alert: gateway p95; note: no alert on the **user** identity-step SLI |
| 14:05:05 | Vendor 502s stop | Outbound 5xx returns to baseline |
| 14:05–14:06 | Small 504 tail on `accounts-service` while in-flight retries drain | In-flight retry traces; pool wait time |
| 14:06:20 | User-visible error rate back to baseline | Same SLI as 14:03 |
| 15:10 | On-call traces a failing span: 8 retries, no jitter, no circuit breaker | Trace sample (redacted); code path `RetryingIdvClient` |
| 16:00 | Decision: Sev3, write a short post-mortem because of the latent client | This doc |

## What happened

1. **User path** — A new seller on Harborlot reaches identity verification (KYC-like: upload document, wait for pass/fail). During the spike the UI showed a generic “could not verify identity, try again.” Retry after 14:05 succeeded for the sampled cases. No seller was marked rejected; the step simply did not complete.
2. **System path** — Browser → `accounts-service` (`POST /onboarding/identity`) → `identity-gateway` → `idv-provider`. Vendor HTTP 502 for ~2 minutes. `identity-gateway` mapped 502 → 503 to the caller. `accounts-service` treated 503 as retryable and fired up to 8 attempts, no backoff/jitter, per user click. `payments-api` was not on this path.
3. **How we knew** — Support, then dashboards. The first automated signal was **gateway latency**, not the onboarding identity **error** SLI. Gap: we do not page on the user-step error rate.
4. **What we did** — Waited; vendor recovered. No rollback (we had not shipped). No fail-open (failing open on identity would create unverified sellers — out of policy). Mitigate for *next* time is the retry cap, not something we flipped during the two minutes.

This was a **spike**, not an outage of Harborlot. Browse, cart, and pay stayed up. The identity **step** was unusable for ~2 minutes for sellers who attempted it then.

## Root cause

### Primary

`idv-provider` returned HTTP 502 for approximately two minutes. `identity-gateway` has a single vendor for this check and no cached “last known good” (correct — identity must be live). Callers therefore failed until the vendor recovered.

### Secondary (latent)

`accounts-service` retries retryable identity errors **eight times with no delay or jitter** (`RetryingIdvClient`). That did not start the 502s. It (a) amplified load on a sick vendor, (b) held connection pool slots, (c) extended user-visible 504s about a minute after 502s stopped. There is no circuit breaker on this client. Alerting pages on gateway **latency**, not on the identity-step **error** SLI, which is why support beat the page.

### Contributing factors

- Onboarding traffic is bursty around local evenings; the window hit a busy half-hour, so more sellers saw the generic error than a quiet Tuesday morning would have.
- Runbook for `identity-gateway` assumes we can “check vendor status” but does not say **fail closed and wait** vs search for a deploy.

### What it was not

| Hypothesis | Why not |
|---|---|
| Bad deploy of `accounts-service` or `identity-gateway` | No deploys in a 6h window; configs unchanged |
| `payments-api` regression | Checkout error rate and p99 flat; different SLO |
| Document-type parser bug | Failures were 502/503 from gateway, not 422 validation |
| Data wipe / duplicate seller rows | Identity step does not insert the seller profile until vendor 200; counts matched |

## Evidence checklist

- [x] Error rate / latency for the user-facing SLI (before, during, after)
- [x] Dependency status (gateway outbound 5xx **and** vendor public status)
- [x] Deploy / config / flag diff in the window (none)
- [x] Saturation (gateway pool wait up during retry tail; CPU uninteresting)
- [x] Logs sampled, redacted (status codes + `request_id` only)
- [x] Traces: failing identity span vs success after 14:06
- [x] Alert fire / miss (latency alert late; no error-SLI page)
- [x] Data-integrity check (no seller profile writes without vendor 200; no payment objects in this flow)

## Impact

| Dimension | What we know |
|---|---|
| User-visible | Generic failure on identity step; retry worked after 14:05 |
| Who / blast radius | On the order of tens of seller attempts in 2 minutes (not hundreds). Existing sellers and buyers unaffected. Exact count: team range from 1m request counter; **no account IDs listed here**. |
| SLO / error budget | Identity-step availability SLO burned a small slice of the monthly budget; checkout SLO untouched |
| Data | None lost, none duplicated |
| Security / privacy | None — no bypass of the identity gate |
| Revenue / ops | No payments blocked. Support: a handful of contacts. Unmeasured: sellers who abandoned and did not come back. |
| Internal | ~45 minutes on-call after the spike to prove retries + data safety |

## Actions

| ID | Action | Owner | Urgency | Status |
|---|---|---|---|---|
| A1 | Cap identity-step retries (e.g. 2) with exponential backoff + jitter; fail the click fast with “try again in a minute” | accounts-service squad | **P0** | proposed |
| A2 | Circuit breaker on `RetryingIdvClient` when vendor 5xx crosses a short window | accounts-service squad | **P1** | proposed |
| A3 | Page on **user-step** identity error rate, not only `identity-gateway` p95 | observability + accounts | **P1** | proposed |
| A4 | Runbook: vendor 5xx → fail closed, do not hunt a deploy unless SHA changed | identity-gateway squad | **P2** | proposed |

## Follow-ups

| Item | Owner | Notes |
|---|---|---|
| Second vendor or queue-and-retry-later for identity (product + risk) | identity-gateway + product | Out of scope for P0; would change policy. Won’t-do until risk signs off. |
| Game-day: inject 502 from a fake `idv-provider` in staging | accounts-service | After A1 lands |

## Conclusion Q&A

1. **What failed for the user?** New sellers could not complete identity verification for ~2 minutes and saw a generic retry error. Pay and browse were fine.
2. **What was the primary mechanism?** Upstream `idv-provider` HTTP 502; single-vendor path in `identity-gateway` with no valid fallback.
3. **What latent issue did we find that did *not* start this incident?** Unbounded, un-jittered retries in `accounts-service` plus paging on the wrong SLI.
4. **How will we detect this faster next time?** Alert on the identity-step **error rate** (A3), not only gateway latency.
5. **How will we make the same failure smaller or impossible?** We cannot stop a vendor 502. We can stop turning it into a retry storm (A1, A2) and we keep fail-closed on identity (no unverified sellers).
6. **Did we lose or corrupt data?** No. The seller profile is not written until a vendor 200. Payments are not on this path.
7. **Is a formal post-mortem the right artifact?** **Yes, short form.** A two-minute self-healing vendor blip with no data loss would normally be a ticket ([`severity.md`](severity.md) — skip when there is no latent finding). We found a client that will make the **next** blip worse, on a core onboarding gate. That is the bar. A 90-second CPU wobble on a canary with **zero** user errors and **no** latent bug would **not** get this document.

---

**Not this:** real seller IDs, Datadog graph URLs with org IDs, SQL against production, or a company wiki paste. If you fork the sample, keep Harborlot (or invent another market) and keep generic service names.
