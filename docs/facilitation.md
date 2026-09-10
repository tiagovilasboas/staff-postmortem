# Facilitation

Run the review as a learning meeting, not a tribunal. Structure inspiration: [Etsy DebriefingFacilitationGuide](https://github.com/etsy/DebriefingFacilitationGuide) (HOW questions, timeline first). Do not paste that guide into an incident doc.

The form is [`template.md`](template.md). The artifact gate is [`when-to-write.md`](when-to-write.md).

## Timeline first

Open with clocks and evidence. Analysis waits. If the room jumps to "root cause" before the timeline is shared, walk it back.

One row in the timeline is one observed fact. Chat reconstruction is a last resort. If two clocks disagree, say so; do not pick the prettier story.

## Ask HOW, not who

Questions that keep the room on the system:

- How did this path look from the user's seat?
- How did the first signal reach the room (or fail to)?
- How did the tools, defaults, and incentives make the unsafe action the easy one?
- How will we detect the same class faster?

"Who deployed" is a trigger. It is not a finding. If a name appears, rewrite the sentence around the missing test, missing canary, or missing page.

## Schedule the meeting early

When you open the 48-hour draft, put the review on the calendar. An empty calendar and a polished novel is backwards. The meeting challenges a draft; it does not write one.

Invite people who were in the path (on-call, service owners, support lead). Do not assemble a jury. Keep it under an hour. File or reject actions before you leave.

## Learning is not an action pile

A useful review can end with two owned SMART actions and an explicit won't-do. Ten tickets titled "improve monitoring" is not more learning. Measure the rite by recurrence of the class and by actions that land, not by how many rows you added.

If the only honest outcome is "vendor blipped; we waited; no latent gap", you did not need this meeting. Close with a ticket. See [`when-to-write.md`](when-to-write.md).
