# When to write

Sev describes impact **now**. P describes follow-up urgency. Neither is the artifact gate. Scales: [`severity.md`](severity.md). Form: [`template.md`](template.md).

## Threshold

Write the full form when **any** of these is true:

- Sev1 or Sev2
- Data loss, duplication, or a security/privacy question that needed a check
- Customer-visible impact on a core path, even if short, **and** a latent defect that would fire again
- Repeat of an incident that already had a "we'll fix it later"
- Leadership or a customer asked for a written review

## When not to write a novel

Skip the ceremony (ticket, graph link, short note) when **all** of these are true:

- Sev4, or a Sev3 with **no** customer-visible lasting impact
- Duration is a short spike (minutes) that self-healed or flipped back with a known mitigate
- **No** data question
- **No** latent bug worth an owned action
- Not a repeat

A 90-second canary blip with zero user errors and no latent finding is a ticket. It is not eight pages.

Borderline Sev3: if the only learning is "vendor blipped and we waited", a ticket is enough. If the learning is "our client turned a 2-minute vendor 502 into a 15-minute retry storm", write the post-mortem. The minutes are not the point.

Worked cases: [`example-checkout-latency.md`](example-checkout-latency.md) (fiction; write), [`example-short-spike.md`](example-short-spike.md) (fiction; write short), [`examples/silent-push-webhook.md`](examples/silent-push-webhook.md) (anonymized composite; write for the silent class). Index: [`examples/README.md`](examples/README.md).

## 48-hour draft

Open a **draft** within 48 hours of mitigate. Clocks are still in chat; graphs are still in cache. The review meeting does not start from a blank page.

Published polish can wait for the review. The draft cannot. If you miss the window, say so in Doc status and list what you can no longer prove.

Owner of the draft is a role or rotation (often the incident commander), not a blame target.
