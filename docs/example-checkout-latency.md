# Example: checkout place-order latency (fictional)

**This is not a real incident.** Harborlot Market is an invented C2C marketplace. Service names are generic. No employer, no real users, no monitor IDs.

Use it to see how [`template.md`](template.md) reads when filled at Staff density. Same bar as [staff-impact-cases](https://github.com/tiagovilasboas/staff-impact-cases): problem, constraint, decision, evidence, before/after. Telemetry gaps follow [sentry-golden-path](https://github.com/tiagovilasboas/sentry-golden-path) (named route, status, duration; no product IDs here).

Lesson, not lore:

- **Primary** = a config flag that disabled the pricing cache on the place-order path.
- **Secondary / latent** = no deadline on the pricing client; page on a 5-minute average, not 1-minute checkout p95.
- Formal post-mortem: Sev2 core checkout + latent client. Write it. See [`when-to-write.md`](when-to-write.md).

---

# Incident: checkout place-order latency during Saturday peak

## Summary

| Field | Value |
|---|---|
| Date (UTC) | 2026-04-18 |
| Detected | 18:44 UTC; support queue ("Pay keeps spinning"), ~3 min before the first automated page |
| Mitigated / resolved | 18:56 UTC flag revert; user-visible p95 back to baseline by 18:58 |
| Duration | **~14 minutes** customer-visible (18:44-18:58 on the place-order SLI) |
| Severity | **Sev2** (core checkout degraded; retry worked; some users double-clicked) |
| Customer-facing? | Yes; buyers on `POST /checkout/place-order` |
| Services | `checkout-api`, `pricing-service`; `payments-api` on the capture path only |
| Primary root cause | Flag `pricing.cache_ttl_seconds=0` disabled the hot-SKU cache; `pricing-service` computed every place-order live |
| Data loss? | **No**. Captures are idempotent; no double charge in the sampled window |
| Incident commander | On-call (checkout/payments rotation); named IC at 18:48 |
| Doc status | Reviewed; actions tracked; close-out filled two weeks later |

Harborlot checkout calls `checkout-api` → `pricing-service` for a live price, then `payments-api` to capture. For about fourteen minutes on a Saturday peak the pricing cache was off. Buyers saw a spinner, then a generic "try again." Place-order p95 moved from ~380 ms to ~4.8 s; about 11% of attempts returned 504. We reverted the flag. We are writing this up because checkout is a core path and the client had no deadline.

## Impact

| Dimension | Value | How we know |
|---|---|---|
| User-visible symptom | Spinner, then generic retry on Place order | Checkout UI copy; `checkout.place_order` 504s |
| Attempts / users | ~2.4k place-order POSTs in the 14 min window (range 2.2k-2.6k) | 1m counter on `checkout-api`; **no account IDs** |
| Error rate | ~0.4% → ~11% 504 on `POST /checkout/place-order` | Same SLI, 1m |
| Latency | p95 ~380 ms → ~4.8 s; p99 ~900 ms → ~8 s | Same SLI |
| Blast radius | Buyers in the peak hour, all regions on this stack. Browse and cart were fine. Existing orders unchanged. | Split: place-order vs `GET /cart` |
| SLO / error budget | Checkout availability burned ~8% of the monthly budget. Latency SLO also burned (not separately budgeted). | Monthly error-budget sheet; range |
| Data | None lost. None duplicated. Idempotency key held on capture. | `payments-api` replay count = 0 extras |
| Security / privacy | None | No auth bypass; no price override from the client |
| Revenue / conversion | Completed-after-retry orders are in the ledger. Abandoned checkouts in the window: **unknown** (no funnel event on "gave up"). Do not invent GMV. | Ledger vs missing abandon signal |
| Internal | ~2 h on-call the night of; ~1 h next day to prove idempotency + flag parse | Rotation notes |

## Timeline

| Time (UTC) | Event | Evidence |
|---|---|---|
| 18:41:10 | Config flag `pricing.cache_ttl_seconds` set to `0` (meant as "use default"; parser treats 0 as disable) | Flag diff; no checkout SHA |
| 18:42:05 | `pricing-service` cache hit ratio falls ~92% → ~1% on the hot-SKU path | Cache hit counter |
| 18:43:40 | `checkout-api` pool wait climbs; 50 outbound slots to pricing hold on live compute | Pool wait; in-flight count |
| 18:44:10 | User-visible p95 on place-order leaves the 800 ms band (**user-visible start**) | `checkout.place_order` p95, 1m |
| 18:44:40 | Support: three buyers "Pay keeps spinning" (**detect**, human) | Support queue; counts only |
| 18:47:20 | Automated page: checkout latency 5m average > 2 s (**detect**, late) | Alert on 5m avg; not 1m p95 |
| 18:48:00 | IC named; payments-api capture error rate confirmed flat | Split SLI |
| 18:51:30 | Flag identified as the only change in the window | Flag audit; deploy list empty |
| 18:56:05 | Flag reverted to `300` (**mitigate**) | Flag diff |
| 18:58:20 | Place-order p95 and 504 rate back to baseline (**resolve**) | Same SLI as 18:44 |
| 19:40 | Trace: pricing span 3-7 s, no client deadline; checkout waited the full call | Redacted trace vs success after 18:58 |
| 20:10 | Decision: Sev2, write the form (core path + latent deadline) | This doc |

## Detection

| Field | Value |
|---|---|
| First signal | Support (buyer contacts), then dashboards |
| First signal clock (UTC) | 18:44:40 |
| User-visible start (UTC) | 18:44:10 (place-order p95 leaves band) |
| Time to detect | ~30 s to a human; ~3 min to the first page |
| Page that fired | Checkout latency 5-minute **average** > 2 s at 18:47:20 |
| Gap | No page on 1-minute place-order **p95**. No page on pricing cache hit ratio. Support beat the automated signal. |

## What happened

1. **User path:** Buyer on Harborlot taps Place order. During the window the button spun, then showed "could not complete, try again." A second tap after 18:58 succeeded in the sampled cases. Browse, cart, and already-paid orders were fine.
2. **System path:** Browser → `checkout-api` (`POST /checkout/place-order`) → `pricing-service` (live price) → `payments-api` (capture). With cache off, pricing computed every SKU live. `checkout-api` has **no deadline** on that call, so 50 outbound slots sat full. `payments-api` was not entered until pricing returned; its error rate stayed flat.
3. **What we did:** Reverted the flag. No checkout-api hotfix (compile mid-peak was slower than the known flag control). No fail-open on price (wrong price on a featured SKU is out of policy).

**Constraint.** Cannot serve a guessed or stale-silent price (trust + advertised price). Cannot freeze checkout deploys for a week to rewrite `pricing-service`. Payment capture must stay idempotent. Peak traffic stays on.

**Decision.** Revert the flag. Add a 200 ms deadline on the pricing client and fail the click with retry. Reject `cache_ttl_seconds=0` at parse. Do not dual-write a new pricing path during the incident.

**Rejected.** Silent last-week price (wrong featured SKU). Hotfix compile of `checkout-api` during peak (flag rollback was faster and already a known control).

This was a **degradation** of place-order, not an outage of Harborlot. Cart and browse stayed up. Capture did not double-charge.

## Root cause

### Primary

`pricing.cache_ttl_seconds=0` disabled the hot-SKU cache. The flag schema treated `0` as "off" and had no "use default" value. Every place-order hit live compute on `pricing-service`. That started the latency.

### Secondary (latent)

`checkout-api` waits on pricing with **no deadline** and no shed. That did not set the flag. It turned a cache miss into pool exhaustion and 504s. Alerting pages on a **5-minute average**, so the room learned from support first.

### What it was not

| Hypothesis | Why not |
|---|---|
| Bad deploy of `checkout-api` or `payments-api` | No SHA in a 6 h window; capture SLI flat |
| Payment vendor slowness | `payments-api` p99 unchanged; we never reached capture on the 504 path |
| Browser / app release | Failures are 504 from `checkout-api`, same on web and iOS samples |
| Duplicate captures | Idempotency key on `payments-api`; replay count showed no extras |

## Contributing factors

1. Flag schema accepted `0` as disable with no parse-time reject and no checkout SLI hold on flag change.
2. Pricing client in `checkout-api` has no deadline, so a slow dependency owns the user-visible budget.
3. Page is on a 5-minute average, not the 1-minute place-order p95 the user feels.
4. Saturday evening peak made the same miss cost more attempts than a Tuesday morning would have. Traffic shape, not a person.

## What went well

- Idempotency key on `payments-api` held. Double-clicks did not double-charge.
- Flag rollback was one control. No hotfix compile during peak.
- IC named in ~4 minutes; `payments-api` split SLI ruled out capture early.
- Fail-closed on price. We did not ship a guessed number to clear the queue.

## Evidence checklist

- [x] Error rate / latency for the user-facing SLI (before, during, after)
- [x] Dependency status (`pricing-service` cache hit + compute time; `payments-api` flat)
- [x] Deploy / config / flag diff in the window (flag only)
- [x] Saturation (`checkout-api` outbound pool wait)
- [x] Logs sampled, redacted (status + `request_id` only)
- [x] Traces: failing place-order vs success after 18:58
- [x] Alert fire / miss (5m avg late; no 1m p95 page)
- [x] Data-integrity check (idempotency replay count; no extra captures)

## Actions

| ID | Action | Type | Owner | Due (UTC) | Urgency | Status |
|---|---|---|---|---|---|---|
| A1 | Reject `pricing.cache_ttl_seconds=0` (and negatives) at config parse; fail the flag write | mitigative | pricing-service squad | 2026-04-19 | **P0** | done |
| A2 | Set a 200 ms deadline on the pricing client in `checkout-api`; on timeout return 503 + "try again" (no silent price) | mitigative | checkout-api squad | 2026-04-20 | **P0** | done |
| A3 | Page on `checkout.place_order` p95 (1m) > 1.5 s, not only the 5m average | preventative | observability + checkout | 2026-04-25 | **P1** | done |
| A4 | Flag changes that touch checkout or pricing require the place-order SLI to hold on a canary slice before 100% | preventative | checkout-api + platform | 2026-05-02 | **P1** | in progress |
| A5 | Funnel event for "place-order abandoned after error" so GMV-at-risk is measurable next time | preventative | checkout-api + product | 2026-05-09 | **P2** | proposed |

Not an action: "improve monitoring." A3 names the SLI, the window, and the threshold.

## Follow-ups

| Item | Owner | Notes |
|---|---|---|
| Game-day: inject cache-off on a fake `pricing-service` in staging | checkout-api | After A2 + A3 land |
| Last-known-good price with an explicit "price may update" banner | pricing + product | Policy change. Won't-do until risk signs off. |
| Rewrite `pricing-service` hot path | pricing-service | Out of scope for this incident. Not a P0. |

## Close-out (two weeks later)

Not in the blank template. Shows the Staff bar: baseline vs after, labeled. Same shape as [staff-impact-cases](https://github.com/tiagovilasboas/staff-impact-cases).

| Signal | Before | After | Label |
|---|---|---|---|
| Time to detect (user-visible → first page) | ~3 min (5m average) | ~40 s in a staging replay with A3 | Result |
| Place-order p95 under a cache-off replay | ~4.8 s (incident) | ~410 ms (deadline sheds; click fails fast) | Result |
| Flag `cache_ttl_seconds=0` | Accepted; means "off" | Rejected at parse | Result |
| Abandoned-checkout GMV | Not measured | Still not measured until A5 | Target |
| Double charge | 0 extras (idempotency held) | 0 extras (unchanged) | Result |

## Conclusion Q&A

1. **What failed for the user?** Buyers could not finish Place order for ~14 minutes. They saw a spinner, then retry. Cart and browse were fine.
2. **What was the primary mechanism?** `pricing.cache_ttl_seconds=0` turned off the hot-SKU cache. Live compute on every place-order started the latency.
3. **What latent issue did we find that did *not* start this incident?** No deadline on the pricing client; page on a 5-minute average instead of 1-minute place-order p95.
4. **How will we detect this faster next time?** Page on 1-minute place-order p95 (A3). Cache hit ratio is a useful dashboard, not the page.
5. **How will we make the same failure smaller or impossible?** We cannot stop a bad flag forever. We can reject `0` at parse (A1), shed at 200 ms (A2), and hold the SLI on a canary (A4).
6. **Did we lose or corrupt data?** No. Capture uses an idempotency key. Replay count showed no extra charges. Price was not fail-opened.
7. **Is a formal post-mortem the right artifact?** **Yes.** Sev2 core checkout plus a latent deadline and a flag schema that will fire again. A 90-second canary CPU wobble with zero user errors would not get this document ([`when-to-write.md`](when-to-write.md)).

---

**Not this:** real buyer IDs, Datadog graph URLs with org IDs, SQL against production, or a company wiki paste. If you fork the sample, keep Harborlot (or invent another market) and keep generic service names.
