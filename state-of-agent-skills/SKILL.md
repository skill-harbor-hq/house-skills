---
name: "state-of-agent-skills"
description: "State of Agent Skills is a method for writing an honest biweekly report about what really moved in an agent-skill catalogue. It starts from verified snapshots, never from a summary or a previous edition. For each edition, it fixes the covered period and the cutoff night, then recounts from the source: file-change events, affected listings, distinct sellers and hosts, changes per night, how often listings changed, the median gap between two changes of the same file, final outcomes in the current categories, and series coverage.\n\nThe report states what the series covers and what it does not cover. A file change is not proof of an improvement, and a disappearance is not proof of a sale. The draft is written in full in English and in French, each language on its own page, and short announcement posts only link to the page. Nothing is published until a separate go is given for that exact edition, and a go for one edition never covers the next one.\n\nThe reference method comes from edition 2, published on 2026-10-24, covering data from 3 to 23 October 2026, with a clean comparable series of 12 nights from 12 to 23 October: 486 file-change events and 296 affected listings, recounted in the source. Edition 1, on 2026-10-10, stayed a draft and was never published. The cadence is biweekly, not weekly and not monthly, with a reminder two weeks after each published edition."
---

Use State of Agent Skills to draft a biweekly report about an agent-skill
catalogue, from verified snapshots only.

1. Fix the covered period and the cutoff night. Write both in the draft.
   Nothing after the cutoff enters this edition, even if a newer night
   already exists. That night waits for the next edition.
2. Recount from <snapshot-source>, for the fixed period only:
   file-change events, affected listings, distinct sellers, distinct
   hosts, changes per night, listings changed once, at least twice,
   and at least four times, median and mean gap between two changes
   of the same file, final outcomes in the current categories, and
   series coverage. Never copy a number from a summary or a previous
   edition without recounting it. A number with no recount source
   stays out of the draft.
3. Draft the full report in English and in French, each language on
   its own page: exact numbers first, what the series covers and
   what it does not cover, movements, active hosts, categories,
   remarkable listings, verified delisted listings, and an honesty
   section stating what a change does not prove and what a
   disappearance does not prove.
4. Read the draft number by number against the recount. Check that
   the header, the body and any announcement text carry the same
   numbers.
5. Stop there. Publish nothing, deploy nothing, and touch no
   production database. Publication waits for a separate go for
   this exact edition, and announcement posts wait for approval
   of their exact text.
