# Anonymized composite: silent push and webhook ACK-before-persist

**Anonymized composite. Not a public company incident. Not a named employer. Not Harborlot fiction.**

Real-shaped failure class for a creator marketplace: sellers did not learn that a sale had landed. Numbers are teaching ranges, not a ledger. Density bar matches [staff-impact-cases](https://github.com/tiagovilasboas/staff-impact-cases) (problem, constraint, decision, evidence, before/after). Sibling rite: [ops-postmortems](https://github.com/tiagovilasboas/staff-impact-cases/blob/main/cases/ops-postmortems.md). Telemetry gaps: [sentry-golden-path](https://github.com/tiagovilasboas/sentry-golden-path) (named route, status, duration; no product IDs here).

Lesson, not lore:

- **Primary** = `notifications-service` treated a local HTTP 200 on enqueue as "push delivered" after the provider started rejecting unsigned requests.
- **Secondary / latent** = `webhook-worker` ACK'd the payments webhook before persist. Found while proving the ledger. Did not start the silent push.
- Formal post-mortem: Sev3 by blast radius, **write it** because the class is silent (no 5xx, no page) on a seller-trust path. See [`../when-to-write.md`](../when-to-write.md).

---

# Incident: sellers missed "sale landed" for eleven days

## Summary

| Field | Value |
|---|---|
| Date (UTC) | 2026-02-03 (detected); silent window from 2026-01-23 |
| Detected | 2026-02-03 11:20 UTC; N3 dashboard (push delivery rate), not the ticket pile |
| Mitigated / resolved | 2026-02-03 15:40 UTC auth header + failure-body read shipped; webhook persist-then-ACK the next day |
| Duration | **~11 days** silent push; **~6 hours** webhook drops on 2026-01-31 (found in the hunt) |
| Severity | **Sev3** (seller notification path; checkout and capture stayed up; workaround = the app inbox, which many sellers do not open) |
| Customer-facing? | Yes; sellers expecting a push that a sale or payout moved |
| Services | `notifications-service`, `push-provider` (vendor), `webhook-worker`, `payments-api` |
| Primary root cause | Provider rejected unsigned push; client counted sidecar 200 as delivered; no delivery SLI |
| Data loss? | **No money lost.** Ledger matched PSP after a 180-event replay. Push payloads themselves were not recoverable. |
| Incident commander | N3 rotation; no separate IC (checkout SLI was green) |
| Doc status | Reviewed; actions tracked; close-out filled two weeks later |

Sellers on a creator marketplace get a push when a sale lands or a payout leaves. For about eleven days the push client talked to a sidecar, saw HTTP 200, and stored `delivered=true`. The provider was rejecting the unsigned request. Checkout still captured. Support tickets said "the app is dead" while every red dashboard was green. While proving the ledger we found `webhook-worker` ACK-before-persist on a Friday window (~180 paid events). We are writing this up for the silent class, not because checkout was down.

## Impact

| Dimension | Value | How we know |
|---|---|---|
| User-visible symptom | No "sale landed" / "payout sent" push. App inbox still had the row for sellers who opened it. | Seller contacts; inbox vs push counters |
| Attempts / users | ~1.2k-1.8k sellers with zero successful provider accepts in 11 days (range) | Provider accept counter vs our `delivered=true` count; **no seller IDs** |
| Error rate | Our enqueue SLI ~0.1% 5xx (green). Provider accept rate ~92% → ~4%. | Two different counters. That split is the finding. |
| Latency | Not the story. Enqueue p95 unchanged. | `notifications-service` p95 |
| Blast radius | Sellers who rely on push. Buyers and checkout unaffected. Email channel (separate client) stayed up. | Split: push vs email vs `payments-api` capture |
| SLO / error budget | No delivery SLO existed. Checkout budget untouched. | Missing SLO is the gap |
| Data | No duplicate capture. ~180 paid webhooks ACK'd without a local row; recovered from PSP export. | Replay count; PSP vs ledger |
| Security / privacy | None confirmed. Device tokens not copied into this doc. | Redacted logs |
| Revenue / conversion | Capture continued. Unmeasured: sellers who did not ship because they never saw the sale. **unknown**, do not invent GMV. | Ledger vs missing "saw the push" event |
| Internal | ~4 h N3 the detect day; ~3 h next day on webhook replay | Rotation notes |

## Timeline

| Time (UTC) | Event | Evidence |
|---|---|---|
| 2026-01-23 09:10 | Provider auth enforcement on the push API (unsigned rejected). No ticket to us. | Provider changelog (public); our client still unsigned |
| 2026-01-23 09:40 | Sidecar still returns 200 on enqueue. Client sets `delivered=true`. | Client code path `OptimisticMarkDelivered`; sidecar status |
| 2026-01-23 → 02-03 | Provider accept rate sits ~4%. Our enqueue error rate stays flat. | Two counters, daily |
| 2026-01-31 16:05-22:10 | `webhook-worker` deploy: ACK to PSP then persist. Persist timeouts leave ~180 paid events without a local row | Worker SHA; PSP delivery log vs local `payments_events` count |
| 2026-02-03 11:20 | N3 dashboard: push delivery (provider accept / expected) off the 7-day band (**detect**) | Dashboard; not a page (there was none) |
| 2026-02-03 12:05 | Split proven: enqueue 200 ≠ provider accept | Redacted trace; provider reject body `missing_signature` |
| 2026-02-03 15:40 | Auth header + read `failed` body shipped (**mitigate** push) | SHA; accept rate returns ~90% within an hour |
| 2026-02-04 10:15 | Persist-then-ACK on `webhook-worker`; 180 events replayed from PSP export | Worker SHA; ledger match |
| 2026-02-04 16:00 | Decision: write the form (silent class + latent ACK-before-persist) | This doc |

## Detection

| Field | Value |
|---|---|
| First signal | Human on the N3 dashboard (delivery ratio), day 11 |
| First signal clock (UTC) | 2026-02-03 11:20 |
| User-visible start (UTC) | 2026-01-23 ~09:40 (first unsigned rejects) |
| Time to detect | **~11 days** |
| Page that fired | **none**. Enqueue 5xx page stayed green. |
| Gap | No page on provider **accept** rate vs a 7-day baseline. HTTP 200 on our sidecar is the wrong SLI. |

## What happened

1. **User path:** Seller makes a sale (or a payout leaves). They expect a push. For eleven days many got nothing. Sellers who opened the app saw the order. Buyers paid normally.
2. **System path:** `payments-api` capture → `notifications-service` enqueue → sidecar → `push-provider`. Sidecar 200 meant "we handed the payload to the vendor process," not "the vendor accepted it." After 23 Jan the vendor required a signature header. The client did not send one and did not read the reject body. Separately, `webhook-worker` on 31 Jan ACK'd PSP webhooks and then wrote the row; persist timeouts dropped ~180 paid events until replay.
3. **What we did:** Ship the signature header and treat provider `failed` as not delivered. Next day, persist-then-ACK and replay the 180 from a PSP export. No 11-day push backfill (consent + noise). Checkout left fail-open on push (a sale must not die because a notification dies).

**Constraint.** Cannot fail checkout or capture if push fails. Cannot paste device tokens or seller IDs into this doc. Cannot replay eleven days of push (spam + consent). Cannot pause payouts to "be safe."

**Decision.** Fix the client (signature + read failure). Persist-then-ACK. Page the delivery ratio. Replay only the 180 paid webhooks. Do not backfill push. Do not turn push into a checkout dependency.

**Rejected.** Fail checkout when push fails (money path held hostage by a vendor). Email blast to every seller in the window (PII + panic). Leave ACK-before-persist because "it is faster."

This was a **silent miss**, not a checkout outage. Green 5xx charts are how the class hides.

## Root cause

### Primary

`notifications-service` marked push `delivered` on sidecar HTTP 200. After the provider required a signature, accepts fell to ~4% and our enqueue SLI stayed green. That started the seller-visible silence.

### Secondary (latent)

`webhook-worker` ACK'd the PSP webhook before the local persist. Persist timeouts on 31 Jan dropped ~180 paid events. That did not turn off push. It would have been a second silent class if the ledger check had not happened.

### What it was not

| Hypothesis | Why not |
|---|---|
| Checkout / capture down | `payments-api` capture SLI flat; buyer receipts existed |
| App store / OS push outage | Email client (same OS) fine; provider reject body is `missing_signature` |
| Token store wipe | Token counts unchanged; rejects are auth, not "unknown device" |
| Duplicate payouts | Replay was insert-if-missing; no extras in the ledger |

## Contributing factors

1. Success metric was **our** HTTP 200, not the provider accept. Integrations that only watch the sidecar lie.
2. No delivery SLO and no page on accept-rate vs baseline, so eleven days fit in "the dashboards are green."
3. Provider breaking change arrived as a changelog, not a contract test in CI.
4. Webhook handler optimized for ACK latency (PSP retry pressure) without a persist-first invariant.
5. Support tickets said "app is dead"; that phrase did not map to a notification SLI, so they sat in a product bucket.

## What went well

- Capture and checkout stayed up. Push was not on the money path.
- N3 dashboard showed the split (enqueue vs accept) once someone looked. The catch was late, not blind forever.
- Ledger check found the webhook hole the same week; 180 events replayed; no extra payouts.
- Fail-open on push held. We did not take checkout down to "fix notifications."

## Evidence checklist

- [x] Error rate / latency for the user-facing SLI (enqueue was the wrong SLI; accept rate is the one that moved)
- [x] Dependency status (provider accept + reject body; PSP webhook log)
- [x] Deploy / config / flag diff (unsigned client unchanged; webhook SHA on 31 Jan)
- [x] Saturation (not the story; persist timeouts on the worker, not CPU)
- [x] Logs sampled, redacted (status + `request_id`; no tokens, no seller IDs)
- [x] Traces: enqueue 200 vs provider reject on the same `request_id`
- [x] Alert fire / miss (no page; enqueue 5xx green)
- [x] Data-integrity check (PSP vs ledger; 180 replayed; no duplicate capture)

## Actions

| ID | Action | Type | Owner | Due (UTC) | Urgency | Status |
|---|---|---|---|---|---|---|
| A1 | Send provider signature header; treat reject/`failed` body as not delivered; stop `OptimisticMarkDelivered` | mitigative | notifications-service squad | 2026-02-03 | **P0** | done |
| A2 | Persist-then-ACK in `webhook-worker`; nack on persist fail so PSP retries | mitigative | payments-api squad | 2026-02-04 | **P0** | done |
| A3 | Page when provider accept / expected < 80% of 7-day baseline for 60 minutes | preventative | observability + notifications | 2026-02-10 | **P1** | done |
| A4 | Contract test in CI: unsigned request must not return "delivered" against a fake provider | preventative | notifications-service squad | 2026-02-14 | **P1** | in progress |
| A5 | Webhook invariant test: ACK is illegal before the local row exists | preventative | payments-api squad | 2026-02-14 | **P1** | proposed |

Not an action: "improve monitoring." A3 names the ratio, the baseline, and the window.

## Follow-ups

| Item | Owner | Notes |
|---|---|---|
| Delivery SLO (accept rate, not enqueue 5xx) on the N3 dashboard | notifications + N3 | After A3. Sibling shape: staff-impact-cases ops-postmortems. |
| 11-day push backfill | notifications + product | Won't-do. Consent and noise. Inbox row was already there. |
| Make push a checkout dependency | checkout + product | Won't-do. Constraint stands. |

## Close-out (two weeks later)

Not in the blank template. Baseline vs after, labeled.

| Signal | Before | After | Label |
|---|---|---|---|
| Time to detect this class | ~11 days (green enqueue SLI) | Staging replay of unsigned reject pages in ~40 min (A3) | Result |
| Mark-delivered on sidecar 200 | Yes (`OptimisticMarkDelivered`) | No; provider accept only | Result |
| Webhook ACK vs persist | ACK then persist | Persist then ACK | Result |
| 180 missing paid rows | Missing until 4 Feb | Replayed; ledger match | Result |
| Sellers without push in the 11-day window | ~1.2k-1.8k | Channel restored; no push backfill | Result |
| Delivery SLO on the N3 board | None | Still a target until the SLO doc lands | Target |

## Conclusion Q&A

1. **What failed for the user?** Sellers did not get "sale landed" / "payout sent" push for ~11 days. Checkout still captured. Some paid events were missing locally for ~6 hours until replay.
2. **What was the primary mechanism?** Unsigned push rejected by the provider while our client treated sidecar 200 as delivered.
3. **What latent issue did we find that did *not* start this incident?** Webhook ACK-before-persist, which dropped ~180 paid events on 31 Jan.
4. **How will we detect this faster next time?** Page the provider accept ratio vs a 7-day baseline (A3), not enqueue 5xx.
5. **How will we make the same failure smaller or impossible?** We cannot stop a vendor from requiring a header. We can refuse to lie about delivery (A1, A4), persist-then-ACK (A2, A5), and keep push off the money path.
6. **Did we lose or corrupt data?** No money lost. 180 webhook rows were missing and replayed. Push payloads for the 11 days were not replayed (won't-do).
7. **Is a formal post-mortem the right artifact?** **Yes.** Silent class on a seller-trust path, plus a latent webhook invariant. A 90-second canary blip with a page and no latent gap would not get this document ([`../when-to-write.md`](../when-to-write.md)).

---

**Not this:** a public company postmortem, a named employer, real seller IDs, device tokens, vendor ticket IDs, or a wiki paste. If you fork the sample, keep the **anonymized composite** label and generic service names.
