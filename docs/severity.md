# Severity and when to write

Two scales. Do not mix them. The artifact gate (threshold, when not to write a novel, 48-hour draft) is [`when-to-write.md`](when-to-write.md).

| Scale | Answers | Used on |
|---|---|---|
| **Sev** (Sev1-Sev4) | How bad was the **incident** for users and data **now**? | Summary table |
| **P** (P0-P3) | How soon must this **follow-up** land? | Actions table |

A Sev3 incident can still have a P0 action (unsafe default on a hot path). A Sev1 can have a P3 doc-only leftover.

## Sev (incident impact)

Calibrate to **user path + data**, not to how loud Slack was. If two rows fit, pick the worse.

| Sev | User / product | Data / security | Typical response |
|---|---|---|---|
| **Sev1** | Core path down (checkout, login, pay, or the only onboarding gate) with no usable workaround | Confirmed loss, corruption, or a security/privacy incident | Incident commander. Formal post-mortem **required**. |
| **Sev2** | Major flow broken or SLO burn that pages; workaround painful or partial | Possible integrity issue still being proven | Commander or lead on-call. Formal post-mortem **required**. |
| **Sev3** | Degraded: errors/latency on a slice of traffic; workaround exists; blast radius limited | No evidence of loss | Mitigate, then decide ([`when-to-write.md`](when-to-write.md)). |
| **Sev4** | Minor / internal / no customer-visible error | None | Ticket. Formal post-mortem **optional**. |

If you cannot yet tell Sev1 from Sev2, run the incident as Sev2 until data says otherwise. Downgrade in the doc when evidence lands.

## P (action urgency)

| P | Land it | Examples |
|---|---|---|
| **P0** | Before the next risky deploy of this path, or within a few days | Turn off unbounded retries; fix a drop-write; page on the real SLI |
| **P1** | This sprint | Circuit breaker, idempotency test, runbook gap that delayed mitigate |
| **P2** | Dated backlog (next sprint or a named milestone) | Better dashboard, vendor status integration |
| **P3** | Opportunistic / won't-do needs a sentence | Rename a metric, nice-to-have game-day |

"Owner = TBD" is not a P0. Name a team or rotation. A P0 row also needs a UTC due date on the Actions table.

## Spike vs outage

A **spike** is a brief burst of errors or latency that returns to baseline. Duration is measured on the **user-visible SLI**, not on how long the Zoom stayed open.

An **outage** means the product path was actually unusable (failed open/closed the wrong way, or error rate high enough that users could not complete the job).

Do not upgrade a two-minute 502 burst to "we were down all morning" because the write-up meeting was at noon. Do not hide a Sev1 behind "just a spike" if checkout was hard-down.

## Primary vs secondary

| | Meaning | In the template |
|---|---|---|
| **Primary** | Mechanism that **started** customer-visible pain | Root cause → Primary |
| **Secondary / latent** | Bug or gap **found during the hunt** that amplified, hid, or would cause the next one | Root cause → Secondary |

Retries without jitter that stampeded a recovering dependency are usually **secondary** if the dependency 502 started the pain. Alert-on-the-wrong-SLI is secondary unless the missed page *was* the customer impact (it rarely is).
