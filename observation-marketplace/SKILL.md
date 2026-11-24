---
name: "observation-marketplace"
description: "Observation Marketplace turns a classified market into an observatory, in read only mode. You define a watchlist once, with a regional centre, a radius, and queries by category and priority, then you capture regular snapshots and keep them as they are. From those snapshots, you get three honest views: price by precise category and model, lifecycle by first view, last view and number of passes seen, and seller by number of listings and store signals.\n\nTwo guards keep the views honest. Trap prices, such as 0 and 9999, are filtered before any median, and medians are used instead of averages on mixed groups. A disappearance is never counted, on its own, as a sale: a sale and a withdrawal without a sale are two distinct outcomes, classified separately. A store seller, recognised by signals such as stock numbers, taxes or inventory, is labelled as such and excluded from private seller price references. Furniture, large appliances and bulky items are filtered out.\n\nNothing here buys, contacts or spends. Every judgement stays on paper, every real purchase, real contact or change of scope needs a separate explicit decision, and no existing snapshot job is modified by this skill.\n\nImportant, stated in the skill itself: this draft is pending the review on 30 October 2026. Do not assume that the system continues after that review. Phase 3 has no fixed content in this draft, and phase 2 needs a separate go."
---

Install Observation Marketplace as a read only observatory for public classified listings, on paper only.

First, create a watchlist file, with placeholders only, never real values in this prompt:
- regional centre: <REGION_CENTRE>
- radius: <RADIUS>
- one query per line, each with its category and priority
- a maximum number of results per query and per pass

Then create a SQLite database with two tables:
- listings: one row per observed listing, with an identifier, a normalised title, a category, a seller, and a date of first view
- snapshots: one row per listing and per capture pass, with the displayed price, the pass date, the category, the seller, and extracted signals

Then, for each capture pass:
- capture the public listings from the watchlist, and never modify the observed source
- keep snapshots as they are, and build analyses only as queries or views on snapshots
- filter trap prices, such as 0 and 9999, before any median
- use medians by precise model, never an average on a mixed group
- never count a disappearance, on its own, as a sale
- label store sellers from their signals, and exclude them from private seller price references
- filter furniture, large appliances and bulky items
- report the pass with counts before and after, new listings, new snapshots, updated views, and any anomaly

Paper only, always: propose, never buy, never contact a seller, never spend money. Do not modify any existing snapshot job. Do not build phase 2 or phase 3 without a separate go. This draft is pending the review on 30 October 2026, and it does not assume that the system continues after that review.
