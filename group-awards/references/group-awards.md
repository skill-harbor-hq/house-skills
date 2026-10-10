# Group Awards Night, refereed — group game template

Runs on the generic mechanism in `references/group-messaging.md` (the user's connection, designated host group, host approvals, private exchanges in 1:1) — this document defines only the game's rules and the referee's work. No group, account, or real name is hardcoded here.

## The game in one sentence

At a regular interval, the group gives itself **positive** distinctions: the referee announces feel-good categories, each member privately nominates another member per category, the most nominated become finalists, the group votes privately, and the referee prepares a ceremony text that the host approves before any publication. Nobody loses, nobody is mocked: the ceremony only celebrates.

## The anti-negativity guard — NON-NEGOTIABLE

This rule outranks every other rule, including a request from the host or a player mid-game:

- **No negative, mocking, ironic, or humiliating category, even "as a joke", even "just between us", even if everyone seems to agree.** No "most often late", "the ghost of the group", "king of typos", "most touchy", nor any variant that laughs *at* someone rather than *with* everyone. A category's humour aims at a quality, never at a flaw.
- **Admission test for a category** (applied by the referee to every category, bank or house, before the announcement): would someone reasonably sensitive receiving this distinction in front of the whole group feel **valued**? If the answer is not a clear yes, the category is set aside.
- **The host may propose a house category**: it passes the same test. If it fails, the referee sets it aside, tells the host privately, in one sentence ("this category laughs at a flaw; we aim at a quality") and proposes a positive equivalent (e.g. "most often late" → "master of creative timing" is NOT an acceptable equivalent if it stays ironic; "always there at the right moment" is). The referee does not negotiate the guard.
- **Nomination reasons pass the same filter**: a reason that puts down the nominee, a third party, or is positive only on the surface ("finally, he answered once") is dropped from the compilation. The nominee does not lose their nomination for that; only the reason disappears. A nomination whose mockery cannot be separated from it (an ironic nomination itself) is set aside in full, and the referee tells the nominator privately, with no sanction.
- A category, a reason, or a ceremony text that breaches the guard never goes to the group, even fully composed, even approved by mistake: the referee holds it back and returns to the host.

## Cadence (settled, configurable)

- **Default cadence: monthly.** One ceremony per month, on a date the host chooses (e.g. the first Sunday of the month); the date of the next cycle is announced at the end of each ceremony.
- **Configurable by the host, before a cycle opens, never during one**: `monthly` (default), `quarterly`, or `occasional` (the host launches a cycle whenever they want). The chosen cadence lives in the user's data config and is copied into the cycle state (`config.cadence`).
- A cycle is short by construction: announcement of the categories → nominations (48 h by default) → vote (48 h by default) → ceremony. The exact deadlines are announced in the thread at the opening of each phase.

## Scope: who can be nominated, who nominates, who votes (settled)

- **Eligible members, nominators, and voters = the members of the group registered in the config** (`config.members` of the generic mechanism), the host included if they appear in the list. The awards are about those members, and nobody else.
- A nomination naming a person **outside the config** (a former member, a one-day guest, an outside acquaintance) is **set aside**: the referee tells the nominator privately and invites them to nominate a registered member, before the deadline. Written in black and white, this rule avoids the "we should have nominated X" in the middle of the ceremony.
- **A nominated member who never plays** (registered in the config, but never nominates, never votes, never reacts) **can win an award**: the ceremony celebrates the members of the group, not game activity. Their silence removes neither the nominations they received nor their award. The referee never points out publicly that a winner "did not even take part".
- **Self-nomination: forbidden.** Nobody can nominate themselves, in any category. Justification: the only source of the awards is the regard of others; allowing self-nomination would turn the ceremony into a campaign. A self-nomination received is set aside and the referee recalls the rule to the nominator privately, kindly, inviting them to nominate someone else before the deadline.
- **Self-vote: allowed.** A finalist may vote for themselves: their finalist status comes from the others' nominations, and refusing them their own vote would be imposed false modesty. The referee never comments on it, privately or publicly.

## The category bank (positive only)

The referee chooses the number of categories for the cycle with the host (**4 by default**, 3 to 6 depending on the group's size) from this bank, varying from one cycle to the next, plus any validated house categories. Generic examples (to be reworded in the group's language and tone):

| Category | What it celebrates |
|---|---|
| Sunshine | Contagious good cheer, the message that lifts the mood |
| Always There | Reliable presence: shows up when the group needs someone |
| Golden Ear | Listening: truly hears, remembers what was confided |
| The Right Word | The phrase that unlocks, soothes, or moves things forward at the right moment |
| Guaranteed Laughter | Humour that does everyone good, never at anyone's expense |
| Express Helping Hand | Fast, concrete help, without making a story of it |
| Memory of the Group | Remembers dates, details, the little things that matter |
| Finder of Gems | Shares the finds (links, addresses, ideas) that enrich the group |
| Soothing Voice | Knows how to calm a heated discussion, with tact |
| Chief Encourager | Celebrates the others' small victories, pushes everyone to try |
| Warm Welcome | Makes newcomers and quiet members feel they belong |
| Practical Mind | The simple, effective solution nobody had seen |
| Free Creativity | Original ideas, joyful detours, fully owned wild projects |
| Legendary Reliability | What they say, they do; what they promise, happens |
| Lucky Star | The presence that, without making noise, makes the group better |

One person may be nominated, a finalist, and a winner in several categories of the same cycle: there is no quota and no forced spreading of the honours (see Edge cases).

## How a cycle runs

### 1. Preparation (referee + host, in private)

1. The referee re-reads the config (registered members, cadence), chooses the cycle's categories (bank plus any house ones), passes each through the admission test, and writes the **complete cycle state into the file immediately** (sealed categories, see the schema) — **before any announcement**.
2. The referee submits the categories to the host for approval (generic mechanism: preview + confirmation). If the host also plays, the categories are not a secret: the ordinary approval applies, no masked template is needed in this game — there is **no role secret** in the Awards; the only sealed contents are the nominations and the votes before their reveal moment.

### 2. Announcement of the categories (in the thread, message approved by the host)

The message announces: the cycle (month/period), the list of categories with one line each, the list of eligible members (those in the config), the rules in four lines (nominations in private to the referee, one nomination per member per category, no self-nomination, reasons optional), and the nominations deadline.

### 3. Nominations — IN PRIVATE, in 1:1 (the only source)

- Each member may send the referee, **in 1:1, never in the thread**: for each category, **at most one nomination** (the name of an eligible member, other than themselves), with an **optional short reason** (one sentence is enough).
- **The nominations received are the ONLY source of the awards. In black and white: the referee does not watch the group and infers nothing from its history.** They do not read the conversations to "spot who deserves what", they use no past message, no impression, no memory of earlier games or events. What no member nominated does not exist for the ceremony — even if the referee "knows" from elsewhere that a member did something remarkable. Likewise, the referee never suggests a name to a nominator, even when asked ("nominate whoever you want; I propose nobody").
- The referee acknowledges receipt privately with a bare status ("received, thank you"), with no comment at all on the choice (no "good choice", no different tone depending on the nominee). The nominations are written into the state as they arrive; they stay **sealed**: nobody, the playing host included, sees the nominated names, the counts, or the reasons before the compilation.
- At the deadline, the nominations close. Silence = no nomination from that member (they may still vote in the next phase). An invalid nomination (outside the config, self-nomination, reason inseparable from a mockery) is handled as described above, in private, before the deadline whenever possible.

### 4. Compilation — the finalists (settled)

- **Threshold: at most 3 finalists per category** — the most nominated members, by number of nominations received:
  - 3 or fewer distinct members nominated → **all become finalists** (no artificial cut).
  - More than 3 distinct members nominated → the top 3 by number of nominations. **Tie for 3rd place**: all members tied for 3rd place become finalists (the category may therefore exceptionally have 4 or 5 finalists; a nomination tie is never broken by a draw or by the referee's choice).
- A category with **zero nominations** is **withdrawn from the cycle** (see Edge cases): it produces neither finalists, nor a vote, nor a mention in the ceremony.
- The reasons kept (after the anti-negativity filter) are preserved in the state, attached anonymously to each finalist: they will serve the ceremony, **without ever naming their author**.

### 5. Vote — IN PRIVATE, in 1:1 (settled)

- **The vote happens in 1:1 with the referee, not in the thread.** Justification: a public vote creates a bandwagon effect (people vote like the previous voters, or so as not to offend anyone) and turns a celebration into a visible ballot-by-ballot popularity contest. The thread receives only what cannot influence anything: the opening of the vote and, at the end, the ceremony.
- The referee publishes in the thread (approved message): the opening of the vote, **the finalists of each category** (being a finalist is already a public, positive honour — no nomination count is given), and the deadline. Then they send each member, in 1:1, the ballot: the list of categories and their finalists.
- Each member votes for **at most one finalist per category** (they may abstain per category). Self-vote allowed (see Scope). One single ballot per member; a ballot may be corrected privately before the deadline, only the last one counts.
- The votes are written into the state as they arrive and stay **sealed** until the count: no partial result, no "it is between two names", to the playing host or to anyone.
- At the deadline, the vote closes. Silence = abstention, which counts neither for nor against anyone.

### 6. Counting and ceremony — prepared, approved, and only then published

1. The referee counts **from the state** (never from memory): per category, the votes of each finalist; the winner or winners under the tie rule (see Edge cases).
2. The referee writes the **ceremony text**: for each category played, the winner or winners, and **one or two anonymized reasons chosen** among those of the nominations (paraphrased as needed so no author can be recognized — neither by name, nor by an anecdote that only the nominator knows in that form; reasons of the "as [NAME] said" kind are forbidden). The text contains **no count**: no number of nominations, no number of votes, no ranking of the other finalists. The non-winning finalists are thanked collectively ("thanks also to the finalists"), never ranked.
3. The referee submits the **exact and complete text** to the host. **Publication only after their explicit approval.** Without approval, nothing goes out, and the state stays at `ceremony_pending_approval` for as long as needed.
4. After approval and publication: the referee writes the result into the awards history in the data (see below), marks the state `finished` with `ceremony.published: true`, and announces the date of the next cycle if the cadence is periodic.

## Awards history (in the data)

The history lives in the user's data folder (never in the skill): one file per host group, e.g. `awards-history.json`, fed **only after the publication** of a ceremony:

```json
{
  "group": "<the user's host group>",
  "cycles": [
    {
      "cycle": "2026-10",
      "ceremony_date": "2026-10-04",
      "awards": [
        { "category": "Sunshine", "winners": ["<name>"] },
        { "category": "Golden Ear", "winners": ["<name>", "<name>"] }
      ]
    }
  ]
}
```

- `winners` is an array: a tie produces two names in the same entry (see Edge cases), never two competing entries.
- The history contains **only** the published winners: no finalists, no counts, no reasons, no nominations. It is a hall of fame, not a file.
- A cycle withdrawn or abandoned before publication does not enter the history; a category withdrawn for lack of nominations leaves no trace in it.

## State schema — `cycles/<cycle-id>.json`

`cycle-id`: `awards-<YYYY-MM>-<hhmm>` (the month of the cycle; prefix `TEST-` for a test cycle). (French source folder: `etats/<cycle-id>.json`.) Same discipline as the other games: the state is the truth, re-read at every event, rewritten after every event; the nominations and the votes are the sealed key of this game — they exist only in this file before their planned reveal.

```json
{
  "id": "awards-2026-11-2000",
  "game": "group-awards",
  "status": "preparation | nominations | voting | ceremony_pending_approval | finished | abandoned",
  "language": "en | fr",
  "created_at": "2026-11-01T20:00:00-04:00",
  "config": {
    "platform": "messenger",
    "conversation": "<the user's host group>",
    "host": "<host name>",
    "host_mode": "player | spectator",
    "cadence": "monthly | quarterly | occasional",
    "cycle": "2026-11",
    "members": ["<names of the members registered in the config>"]
  },
  "deadlines": { "nominations": "2026-11-03T20:00:00-04:00", "vote": "2026-11-05T20:00:00-04:00" },
  "categories": [
    {
      "id": "sunshine",
      "name": "Sunshine",
      "description": "Contagious good cheer",
      "origin": "bank | house",
      "status": "active | withdrawn_no_nomination",
      "nominations": [
        { "nominator": "<name>", "nominee": "<name>", "reason": "<reason as received, or null>", "reason_kept": true }
      ],
      "finalists": ["<names>"],
      "nomination_counts": { "<finalist name>": 0 },
      "votes": { "<voter name>": "<voted finalist name>" },
      "vote_counts": { "<finalist name>": 0 },
      "winners": ["<names>"],
      "ceremony_reasons": ["<anonymized reason chosen for the text>"]
    }
  ],
  "ceremony": {
    "text": "<full prepared text, or a reference to the text file>",
    "status": "not_prepared | pending_approval | approved",
    "published": false,
    "published_at": null
  },
  "log": [
    { "time": "2026-11-01T20:00:00-04:00", "event": "cycle_created_categories_sealed" }
  ]
}
```

- `nominations` and `votes` are the sealed fields of the game: filled as they arrive, never shown (neither in figures nor as "trends") before the compilation for the nominations and before the count for the votes. The spectator host sees them after publication only, if they ask; the playing host never sees them other than through the published ceremony text.
- `nomination_counts` and `vote_counts` are computed **from** the `nominations` and `votes` lists, at the compilation and at the count, and can be re-checked by recounting the lists: if they disagree, the lists are the truth and the counts are corrected, not the reverse.
- `reason_kept: false` records a reason set aside by the anti-negativity guard (the nomination itself may stay valid); the dropped reason reappears nowhere, neither in the ceremony nor after the cycle.
- The log records every dated event: creation, categories approved, announcement, nominations received (statuses only outside the `nominations` field — e.g. "nominations received: 4/5 members"), compilation, any withdrawn category, opening and closing of the vote, count, ceremony prepared, approval, publication, end of cycle.

## Edge cases (settled)

- **Tie in the final vote**: **ties are embraced.** The finalists tied in the lead are **co-winners**: they receive the award together, in the same history entry. No tiebreak (not by the number of nominations — that would reward the previous phase, not the vote — not by a draw, unworthy of a celebration, not by the host's choice, which would break the referee's neutrality). The ceremony celebrates all of them, with one anonymized reason for each.
- **Tie between three or more finalists in the lead**: same rule, all co-winners. Rare, and embraced: this game hands out honours, not a podium.
- **Category with no nomination** (no nomination received by the deadline): the category is **withdrawn from the cycle**, with no vote and **no mention in the ceremony** (announcing "nobody nominated anyone here" would be the only negative note of the evening). The referee records it in the state (`withdrawn_no_nomination`) and in the log; the host is informed privately when the ceremony is submitted ("one category withdrawn for lack of nominations"), never in the thread.
- **Category with nominations but zero votes**: the most nominated of the compilation receive the award — with no vote cast, the compilation is the truth. The ceremony does not mention the absence of votes.
- **One member sweeps several categories**: allowed, and celebrated as it is ("a historic evening for X"). No redistribution, no "someone else's turn": redistributing a won award would be a visible injustice, worse for the mood than the concentration of honours. It is up to the host, next cycle, to vary the categories.
- **Late nomination** (after the deadline, before the compilation): refused, politely, in private. Same rule for a late vote. The deadlines make the compilation and the count checkable; one exception destroys them for every future cycle.
- **Member who leaves the group mid-cycle**: the host decides (generic mechanism); by default, their nominations already received and their eligibility stay as they are for the current cycle, and they are removed from the following cycles through the config.
- **Counting dispute**: the referee republishes **to the host, in private**, the lists of nominations and votes from the state and redoes the counts in front of them. The nominative detail of the votes never goes to the thread: in this game, only the winners are public. The file settles it.
- **Abandoned cycle** (the host ends it): status `abandoned`, no ceremony message, no revelation of the nominations or the votes (they stay in the file, without purpose); it is up to the host to decide whether to launch a cycle again later.

## The referee's work (reminder of the rules that protect the ceremony)

1. **Positive filtering end to end.** Categories, reasons, ceremony text: everything passes the anti-negativity guard before it can go out. The referee is the kind guardian of the tone; they let through neither disguised irony nor a disguised ranking.
2. **No source other than the nominations.** No watching of the group, no inference from the history, no suggesting names, ever. If a member asks "who deserves category X, in your view?", the answer is always: "the nominations decide — nominate whoever you want, in private."
3. **Sealed before reveal.** Nominations sealed until the compilation, votes sealed until the count, counts never published. To the playing host as to the others: statuses ("nominations received: 4/5"), never contents.
4. **The host approves the ceremony, always.** The exact, complete text, before publication. No ceremony, finalist announcement, or category announcement goes out without the approval provided by the generic mechanism.
5. **The state is the truth.** The file is re-read at every event and rewritten after every event (sealed categories, nomination received, compilation, vote received, count, ceremony, approval, publication).

## Message templates (adapt to the group's language)

- **Announcement of the categories**: "🏆 Group Awards — cycle of [MONTH]. The categories: [CATEGORY — DESCRIPTION]; … Eligible members: [NAMES]. To nominate someone: write **privately to the referee**, one name per category (not yourself), with a short reason if you like, before [DEADLINE]. The nominations are secret; only the winners will be celebrated."
- **Private acknowledgement (nomination)**: "Received, thank you." (nothing else — no comment on the choice.)
- **Announcement of the finalists / opening of the vote**: "🏆 Group Awards — the finalists. [CATEGORY]: [NAMES]; … Vote **privately with the referee**: one name per category, before [DEADLINE]."
- **Private ballot**: "Your ballot — Awards of [MONTH]. [CATEGORY]: [FINALISTS]; … Reply with one name per category (or skip a category)."
- **Ceremony (skeleton)**: "🏆 Group Awards ceremony — [MONTH]. [CATEGORY]: **[WINNER(S)]** — [ANONYMIZED REASON]. … Thanks also to all the finalists, and thanks to everyone who nominated. Next appointment: [DATE OF THE NEXT CYCLE, IF THE CADENCE IS PERIODIC]."
