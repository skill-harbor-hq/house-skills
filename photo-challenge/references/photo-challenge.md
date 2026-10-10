# Photo Challenge, refereed — group game template

Runs on the generic mechanism in `references/group-messaging.md` (the user's connection, designated host group, host approvals, private 1:1 messages) — this document defines only the game's rules and the referee's work. It does not repeat the mechanism. No group, account, or proper name is hardcoded here.

## The game in one sentence

On a rolling cycle, the referee announces a theme ("something red", "my favourite corner"); each member photographs the theme in their own way and submits one photo; then the group votes by reactions on the photos, with the referee never judging anyone's taste. The referee announces, collects, republishes, counts and prepares the recap — the host approves and publishes. The season ranking rewards regularity, not one evening of glory.

## Guiding principles

1. **The voters judge the theme, not the referee.** Whether a photo embodies the theme well, is beautiful, funny or touching is what the vote says, never the referee. The referee comments on no photo before the end of the vote — not "superb", not a pointed silence.
2. **The referee counts, the host publishes.** Everything the group sees (announcement, vote opening, recap) is a message prepared by the referee and **approved by the host before sending**, per `group-messaging.md`. The recap in particular exists only as a **prepared** text until the host has approved it: the referee never declares a winner in the thread on their own initiative.
3. **Equal exposure.** All photos of a cycle become visible **at the same time**, when the vote opens. Nobody collects reactions while the others are still photographing.
4. **Honour system, announced as such.** The photo must be taken by the member who submits it (see Photo rules); the game promises **no technical verification** (no EXIF analysis, no detection of generated or found images). It is a game among people who trust each other, and the announcement says so.

## Cadence and configuration

### Default cadence: weekly

A cycle lasts **7 days**, in three fixed windows, announced from the theme announcement on:

| Window | Default duration | What happens there |
|---|---|---|
| Submissions | Day 1 (announcement) → day 4, 8 p.m. | Members photograph and submit in 1:1 (see Collection) |
| Vote | Day 5, 9 a.m. → day 7, 8 p.m. | Grouped republication of the photos, reactions open |
| Recap | Day 7, after 8 p.m. | Count, recap prepared, host approval, publication |

Justification: four days to photograph leave room for a weekend or an outing; two and a half days of vote leave time for less-connected members to pass by; the cycle closes before the next theme arrives, otherwise themes overlap and nobody knows what they are voting on anymore. The next cycle's theme is announced the day after the recap is published (day 8 = day 1 of the next cycle) — never before the current vote closes.

### What is configurable (written into the state at the cycle's creation, never changed mid-cycle)

| Setting | State field | Default | Allowed variants |
|---|---|---|---|
| Cycle length | `config.cycle_days` | 7 | 3 (express) or 14 (slow) — the windows rescale keeping their proportions: ~55% submissions, ~35% vote, the rest to the recap |
| Collection mode | `config.collection` | `deferred_1to1` | `direct_thread` (see Collection — when to use it) |
| Vote reactions | `config.reaction_budget` | 2 per voter | 1 (dry duel, frequent ties) or 3 (large groups, 8 photos and more) |
| Anonymity during the vote | `config.vote_anonymity` | `true` | `false` if the group prefers open play (photos signed from the vote on) |
| Season points | `config.rank_points` | `[5, 3, 2, 1]` | Fixed for the whole season once the season is open |

- The season counts **8 cycles by default** (field `planned_cycles` of the season file); the host may set another number when the season opens, never mid-season without saying so in the thread.
- Deadline times are those of the host group, written in full words in every message ("Thursday 8 p.m."), not only as machine timestamps.

## Players

- **3 to 12 members** registered in the group config (`group-messaging.md`). Below 3 accepted submissions, the cycle is **postponed**: with 2 photos, the vote is not a game, it is an imposed duel — the referee tells the host before the vote opens and proposes extending the submission window once (24 h) or merging with the next cycle.
- A member may **vote without having submitted** (they had no photo that week): the vote is open to all registered members. A member whose submission was refused (late, duplicate) may vote normally — the refusal bears only on their photo.
- The host may play like the others (submit and vote): their public messages go through the mechanism's ordinary approval; their photo is requested from them in 1:1 like any member's, and before publication the referee shows them only statuses ("submissions received: 3/5"), never the others' photos while anonymity is active.

## Themes

- The referee **proposes** the theme, the host **approves** it with the announcement (a public message like the others). Rotation of theme sources, so as not to exhaust a single vein: the bank below, a member's suggestion (collected in 1:1, credited in the recap if retained), the theme of the previous cycle's winner (if they propose one before the announcement; otherwise the bank serves).
- A good theme is: **photographable by everyone** without special equipment or travel, **open enough** for 4 members to return 4 different photos, **precise enough** for "manifestly off-topic" to mean something. "Beauty" is too vague; "the contents of your fridge at 8 a.m." is perfect.
- **Season anti-repetition**: a played theme does not come back in the same season; used themes are recorded in the season file (`used_themes`).

### Theme bank (generic examples, to draw from and adapt)

Colours and light: something red; a shadow more interesting than its object; a reflection; the light at 7 a.m.; something yellow in a grey place.
Everyday life seen differently: my favourite corner; the contents of a pocket or a bag; a tool that has lived; the view from a window at home; something small photographed as if it were immense.
Outside: a lone tree; a remarkable door; something growing where it is not expected; today's sky, unfiltered; a trace of passage (footprint, wear, graffiti).
Objects and materials: something round; metal and wood together; a book open at a page that matters; something broken but still used; three objects that tell a trade or a pastime.
People and life (with no face obligation): hands at work; a shoe with a story; a meal being prepared; an animal met this week; the organized mess of a desk or a workbench.

## Photo rules (written, announced at the first cycle)

1. **Photo taken by the member who submits it**, during the cycle's submission window or before — the game asks for no proof of date, but an "archive" photo must still be their own. **Honour system, stated as such in the first cycle's announcement**: "nothing is checked technically; we trust each other; a photo that is not yours is simply not playing". An image found on the internet, another member's photo, or a generated image presented as a photograph: out of the game *if the group notices it* — the referee runs no investigation and accuses nobody; if a member raises a doubt, the host settles it off-thread (see Edge cases).
2. **One photo per member per cycle.** A member who sends two: the referee keeps **the first received**, refuses the second while saying so privately ("I am keeping the first; tell me before the deadline if you want to exchange it"); an explicit **exchange** before the deadline is allowed, the last requested version stands and the state keeps the trace of both.
3. **Light retouching allowed** (cropping, brightness); a montage that fabricates the scene is no longer the theme's photo — the voters will judge it anyway.
4. **Recognizable people**: the member who submits guarantees that the people photographed agree to appear in the group. The referee publishes at the vote no photo that a member reports, before the vote opens, as showing a non-consenting person: it is withdrawn without debate in the thread, and the member may submit another if the deadline has not passed.

## Collection of submissions — settled mechanics

### Default mode: deferred 1:1 collection, grouped republication at the vote

1. Each member sends their photo **in a private 1:1 message to the referee**, before the submission deadline. Never in the thread during this window.
2. The referee acknowledges receipt privately with a bare status ("received for cycle [N]") — no comment on the photo, no "it will please people", ever.
3. At the close of submissions, the referee prepares the **vote-opening message**: the accepted photos, **all together**, in a randomly drawn order recorded in the log, each under a **letter** (A, B, C…) **without its author's name** if `vote_anonymity` is active. The host approves this message (exact preview, like every public send); it goes to the thread; the vote opens at that instant, not before.
4. The letter → author link lives **only in the state** (cycle key, see Schema). It is revealed only at the recap.

Why this default mode: it makes equal exposure real (a photo posted on day 1 does not harvest three days of reactions in advance), it prevents sympathy voting before all the photos even exist, and anonymity forces the vote onto the photo rather than the person. Its assumed cost: two refereeing passes (acknowledgements, then republication) and the host's approval on the vote message.

### Alternative mode: direct submission in the thread (`direct_thread`)

If the group's platform does not let the referee republish images cleanly (or if the group prefers simplicity), members post their photo **directly in the thread** during the submission window. Written derogations, announced at the theme announcement:

- The vote opens only at the submission deadline, even if the photos are visible before: **any reaction placed before the vote opens does not count** (the referee recalls this at the announcement and enforces it at counting, from the platform's timestamps when they exist).
- Anonymity is impossible in this mode (`vote_anonymity` forced to `false`): authorship is visible from the post. The self-vote stays excluded at counting.
- The exposure order is the arrival order; the recap does not correct it, it mentions it if a member raises it.

The mode is chosen **per season** (or, at the limit, before a cycle's announcement) — never mid-cycle.

### Manifestly off-topic — the referee's bounded power

The referee does not judge the **quality of an interpretation** of the theme: a clever, distant or funny reading of the theme is exactly what the voters reward or not. The referee may set a submission aside only if it is **manifestly without any discernible relation to the theme** (e.g. theme "something red", photo of a blue sky with no red element and no readable wordplay). Bounded, cumulative procedure:

1. The referee writes the reason in one sentence in the state (`status: "set_aside_off_topic"`, field `reason`) **before** the vote opens;
2. They submit the set-aside to the **host's approval** in private, with the photo and the reason — without the host's approval, the photo goes to the vote;
3. The set-aside member is warned privately before the vote opens and may submit another photo if the window is still open;
4. **Doubt keeps the photo.** Any interpretation its author can defend in one sentence stays at the vote: the voters will say, by not voting for it, what they think of it.

A set-aside photo appears neither at the vote nor in the recap (the recap counts only "[N] photos at the vote").

## The vote — by reactions, with a written fallback

### Vote by reactions (main mode)

From the moment the vote-opening message is published, until the vote deadline:

- Each voter places their reactions **on the photos themselves** in the thread (the platform reaction attached to the message/photo, or, if the republication groups all the photos into a single message, on each photo by whatever means the platform offers — otherwise, written fallback, below).
- **Budget: each voter has `reaction_budget` reactions for the cycle (2 by default), at most 1 per photo.** A second reaction from the same voter on the same photo does not count double — the platform generally does not allow it, and if it does, counting deduplicates.
- **Any reaction counts for 1** (👍, ❤️, 😮…: no emoji hierarchy is invented — weighting hearts against thumbs would be an unreadable, contestable rule).
- **Self-vote excluded, written rule: a photographer's reaction on their own photo is not counted.** In anonymized mode, the photographer recognizes their photo: their reaction on it is spotted at counting from the state and discarded, and the recap gives the totals **after** exclusion. The self-vote is not a fault and is never denounced by name in the thread; it is simply void, like an abstention.
- Only **registered members'** reactions count; a reaction from a non-registered reader of the thread is ignored at counting (and the state notes the number ignored, without names).
- A reaction may be withdrawn or moved **until the vote deadline**: only the state of the reactions at closing counts.

### Fallback: written votes

If the platform does not allow reactions on the photos (or if the republication makes them impractical), the referee announces the fallback **in the vote-opening message itself** — never mid-vote: each voter writes in the thread, before the deadline, "I vote for [LETTER(S)]" (as many letters as their budget). Same budget, same self-vote exclusion, same counting. An ambiguous written vote (nonexistent letter, more letters than the budget) is flagged privately to the voter, correctable until the deadline; uncorrected, only the first letters within the budget count, in written order.

### Closing and counting

At the deadline, the referee counts **from the thread re-read at closing and from the state** (letter → author), never from memory:

1. Raw reaction totals per photo;
2. Exclusion of self-votes (deducted by name in the state, not in the thread);
3. Exclusion of out-of-window reactions (`direct_thread` mode) and of non-members;
4. **Valid** total per photo = the cycle score.

The count detail (raw, exclusions by category, valid) lives in the state; the recap publishes the valid totals and, in one line, the number of exclusions ("counting: 16 reactions, 1 self-vote discarded") — the transparency of the count without the humiliation of a name.

## Points and ranking

### Cycle points

The cycle ranking orders the photos by **descending valid total**. Season points awarded by rank (`rank_points`, default `[5, 3, 2, 1]`):

| Rank | Points |
|---|---|
| 1st | 5 |
| 2nd | 3 |
| 3rd | 2 |
| 4th and below (with an accepted submission) | 1 |
| No accepted submission | 0 |

- **Tie at the vote = tied winners, settled.** Two photos tied on valid total carry the **same rank** and receive that rank's points; the next rank is shifted by the number of tied photos ("competition" ranking: 1, 2, 2, 4). **No tiebreak, no lightning round, no casting vote**: the weekly rolling is worth more than an artificial suspense, and a tie in the lead simply gives two winners in the recap. (In the lead as elsewhere: the rule is one, it does not change with the rank touched.)
- A member whose photo was set aside off-topic or refused (late, unexchanged duplicate) scores 0 for the cycle; their vote, however, counts normally.

### Cumulative season ranking

Persistent file `photo-challenge-season.json` in the user's data (schema below), updated **only at the publication of a finished cycle's recap** — never any provisional points written to the season for a cycle in progress. The general ranking orders by:

1. **Season points** (cumulative);
2. **Number of cycle wins** (ranks 1, ties included);
3. **Cumulative total of valid reactions** received over the season;
4. **An assumed tie** beyond that: same rank published as is.

End of season (after the last planned cycle): the first placed are **champion(s)** — a tie in the lead after criterion 3 means tied champions, announced as such. The season recap gives, per member: points, wins, total reactions, cycles played.

## Running of a cycle (step by step)

1. **Creation of the state** — The referee writes the cycle's complete state (config, theme approved by the host, windows and deadlines) **before** the announcement. Nothing in the config changes afterwards.
2. **Announcement** (public message, approved): cycle number, theme, submission deadline, collection mode recalled ("photo privately to the referee" or "photo in the thread"), the coming vote deadline, rules in one line (one photo per member, taken by you, vote by reactions, no self-vote).
3. **Collection** — Private acknowledgements as they come; immediate, private refusals for: late (after the deadline), duplicate (first kept, exchange possible before the deadline), photo from a non-member. Every event is recorded in the state at the time received.
4. **Close of submissions** — The referee freezes the list of accepted photos, draws the publication order at random (recorded), assigns the letters, prepares the vote-opening message and submits it to the host. Eventual off-topic set-asides: bounded procedure above, before this preparation.
5. **Opening of the vote** (public message, approved): the photos under their letters, the vote deadline, the budget recalled ("2 reactions, not on your own photo: it will not count"), the written fallback if the platform requires it.
6. **Vote** — The referee says nothing in the thread during the vote, except a deadline reminder (approved) if the host asks. They react themselves to **no** photo.
7. **Closing and counting** — Count in three passes (raw, exclusions, valid) from the re-read thread and the state; cycle ranking and points computed from the state; the cycle moves to `to_publish` in the state.
8. **Recap PREPARED** — The referee drafts the complete recap (template below) and submits it to the host **privately**, marked waiting for approval. **Nothing is published at this stage**, the season ranking is not yet updated.
9. **Publication** — Only after the host's explicit approval does the recap go to the thread; only then does the referee update the season file, mark the cycle `finished` and log the publication.

## The referee's work (reminder of the rules that protect the game)

1. **Neutrality of taste, total.** No comment on a photo — in public, in private, to the host — before the recap is published. The same acknowledgement for everyone, the same wordings. A referee who "adores" a photo before the vote has voted.
2. **The state is authoritative.** Re-reading of the file at every event (submission, refusal, opening, counted reaction), rewriting after each. The published ranking can be recounted by anyone from the state's count detail.
3. **The cycle key stays in the file.** The letter → author link and the set-aside reasons leave the state only at the recap (for the authors). No draft shown to the host for approval reveals an author while anonymity is active — the host approves the vote message as the group will see it, letters included, without the key. (If the host plays, this is also what protects their own game: see the host-player mode in `group-messaging.md`.)
4. **The host publishes, the referee prepares.** Announcement, vote opening, recap: three public messages, three approvals. A recap "waiting for approval" for more than a cycle: the referee flags it to the host and does not announce the next theme until the ranking is published — the rolling must not run ahead of its own results.
5. **Deadlines kept.** The windows close at the announced times. A delay of one minute is a delay (see Edge cases); reopening a window "just this once" destroys the rule for every following cycle.

## State schema — one cycle (`games/<cycle-id>.json`)

`cycle-id`: `photo-challenge-<season-id>-c<NN>` (prefix `TEST-` for a test). One file per cycle; the cumulative ranking lives in the season file, not in the cycle. (French source folder and names: `etats/<cycle-id>.json`.)

```json
{
  "id": "photo-challenge-season1-c01",
  "game": "photo-challenge",
  "test": false,
  "status": "in_progress | to_publish | finished | abandoned",
  "language": "en | fr",
  "season_id": "season1",
  "cycle": 1,
  "created_at": "2026-01-05T09:00:00-05:00",
  "config": {
    "platform": "messenger",
    "conversation": "<the user's host group>",
    "host": "<host name>",
    "host_mode": "player | spectator",
    "cycle_days": 7,
    "collection": "deferred_1to1 | direct_thread",
    "reaction_budget": 2,
    "vote_anonymity": true,
    "rank_points": [5, 3, 2, 1]
  },
  "theme": { "text": "<cycle theme>", "source": "bank | member | previous_winner", "proposed_by": null },
  "windows": {
    "announced_at": "2026-01-05T09:00:00-05:00",
    "submissions_end": "2026-01-08T20:00:00-05:00",
    "vote_start": "2026-01-09T09:00:00-05:00",
    "vote_end": "2026-01-11T20:00:00-05:00"
  },
  "players": [{ "name": "<name in the group>", "registered_at": "2026-01-05T09:05:00-05:00" }],
  "submissions": [
    {
      "player": "<name>",
      "received_at": "2026-01-06T18:12:00-05:00",
      "status": "accepted | refused_late | refused_duplicate | exchanged | set_aside_off_topic | withdrawn_consent",
      "letter": "A | null",
      "referee_description": "<internal marker for the photo, to identify it unambiguously at counting>",
      "reason": null
    }
  ],
  "vote": {
    "mode": "reactions | written",
    "raw_reactions": { "A": 0 },
    "exclusions": { "self_votes": 0, "out_of_window": 0, "non_members": 0 },
    "valid_totals": { "A": 0 },
    "detail": { "<voter name>": ["A", "D"] }
  },
  "cycle_ranking": [
    { "rank": 1, "player": "<name>", "letter": "A", "valid_reactions": 0, "points": 0 }
  ],
  "recap": { "status": "not_prepared | waiting_approval | published", "published_at": null },
  "log": [{ "time": "2026-01-05T09:00:00-05:00", "event": "cycle_created" }]
}
```

- `referee_description` is a technical marker (a few words that distinguish the photo), not a judgement: "red door, evening light", never "very beautiful red door".
- `submissions` also keeps the **refused** ones, with their status and their time: they are the proof of the refusal, not oversights. An `exchanged` photo is replaced by its final version, both stay in the log.
- `vote.detail` (who reacted to what, at closing) is authoritative for the count; the published totals can be recounted from it and from `submissions` (letter → author, for the self-votes).
- `recap.status` moves to `published` only after the real, approved send; while it reads `waiting_approval`, the cycle is not `finished` and the season is untouched.

### Season file schema — `photo-challenge-season.json`

```json
{
  "id": "season1",
  "game": "photo-challenge",
  "test": false,
  "status": "in_progress | finished",
  "created_at": "2026-01-05T09:00:00-05:00",
  "planned_cycles": 8,
  "used_themes": ["<cycle 1 theme>"],
  "players": [{ "name": "<name in the group>", "registered_at": "2026-01-05T09:05:00-05:00", "arrival_cycle": 1 }],
  "finished_cycles": [
    { "cycle": 1, "state": "games/photo-challenge-season1-c01.json", "ranking": [{ "rank": 1, "player": "<name>", "points": 0, "valid_reactions": 0 }] }
  ],
  "general_ranking": [
    { "rank": 1, "player": "<name>", "points": 0, "wins": 0, "total_reactions": 0, "cycles_played": 0 }
  ],
  "champion": null
}
```

- After each published cycle, the referee **adds** the cycle to `finished_cycles`, adds its theme to `used_themes`, and **recomputes** `general_ranking` from the cycle rankings written in the states — never by adding from memory.
- A player arriving mid-season appears from the cycle of their arrival (`arrival_cycle`), with 0 points for the previous cycles; their `cycles_played` count only the cycles they were registered for.

## Message templates — conforming examples (adapt to the group's language)

- **Cycle announcement**: "Photo Challenge — cycle [N]. Theme: **[THEME]**. Your photo (taken by you, only one) **privately to the referee** before **[SUBMISSION DEADLINE]**. All photos will be published together, without names, on [VOTE DATE]; vote by reactions (2 per person, not on your own photo: it will not count) until **[VOTE DEADLINE]**. Honour system: no verification, just your own photo."
- **Acknowledgement of receipt (private)**: "Received for cycle [N]." (nothing else — no comment on the photo.)
- **Late refusal (private)**: "Too late for cycle [N]: deadline [TIME], received [TIME]. Your photo does not go to this cycle's vote; you may vote normally, and the next theme arrives on [DATE]."
- **Opening of the vote (thread)**: "Photo Challenge — cycle [N], theme '[THEME]': the vote is open. [PHOTOS UNDER LETTERS A, B, C…] Place your reactions on the photos (at most [BUDGET]) before **[VOTE DEADLINE]**. Your own photo: your reaction on it will not count. The authors will be revealed in the recap."
- **Recap (PREPARED, submitted to the host — never sent without their approval)**: "Photo Challenge — cycle [N], theme '[THEME]'. Winner: **[NAME]** (photo [LETTER] — [NEUTRAL RESTATEMENT OF THE PHOTO'S SUBJECT]) with [X] reactions. Ranking: [RANK. NAME (LETTER) — X reactions — P points; …]. Counting: [TOTAL] reactions, [EXCLUSIONS] discarded per the rules. Season ranking: [LIST]. Next theme on [DATE]."
- **Answer to a counting dispute (thread, after publication)**: "Counting of cycle [N], redone from the thread and the state: [DETAIL PER PHOTO: RAW, EXCLUSIONS BY CATEGORY, VALID]. The cycle's state file is authoritative; if the detail shows a referee error, the corrected ranking will be republished saying so."

## Writings

1. **Cycle state** (`games/photo-challenge-<season>-c<NN>.json`): created before the announcement, updated at every event (submission, refusal, set-aside, opening, closing, counting, recap status), `status` → `finished` **only after the recap is published**.
2. **Season file** (`photo-challenge-season.json`): updated at the publication of each recap (cycle added, theme recorded, general ranking recomputed) — and at no other moment.
3. **No entry in any scores file**: that kind of file stays dedicated to scored solo rounds; a cycle's result lives in its state and in the season, the same decision as for the other group games.

## Edge cases (settled)

- **Late submission**: refused, without exception and without negotiation — even by one minute, even if the vote has not started. The submission window *is* the rule that makes the grouped republication possible; quietly accepting a late photo would break equal exposure for every following cycle. Refusal announced privately to the member (template above), recorded in the state (`refused_late`, received time against deadline). The member votes normally in the cycle.
- **Duplicate / exchange**: first photo kept; second refused as a duplicate, unless an explicit exchange is requested before the deadline — then the new one replaces the old (`exchanged`), and only the final one goes to the vote. After the deadline, no exchange.
- **Fewer than 3 accepted submissions** at closing: the cycle does not go to the vote as it stands. The referee proposes to the host: a single 24-hour extension of the window (announced in the thread), or postponing the theme to the next cycle (the theme is not "used" and joins `used_themes` only after a real vote). Never a 2-photo vote presented as a normal cycle.
- **Tie at the vote**: tied at the rank concerned, that rank's points shared (see Points and ranking). No tiebreak, even in the lead, even in the season's last cycle (tied champions exist).
- **Self-vote**: discarded at counting, never counted, never denounced by name. If a member places reactions beyond their budget (permissive platform), only the first ones, in chronological timestamp order, count up to the budget; the excess is discarded in the same way and enters the recap's exclusion total.
- **Photo set aside off-topic**: only by the bounded procedure (written reason + host approval + doubt in the photo's favour). A photo that has gone to the vote can no longer be set aside afterwards, even if the group finds it off-topic: the voters settle it by their reactions, and the recap will not re-judge it.
- **Authorship dispute** (a member claims a photo is not its author's): the referee does not investigate and withdraws nothing on their own initiative. They pass the report to the host, off-thread; the host decides (let the honour system run, speak to the member, or withdraw the photo before the vote opens if it has not yet). After the vote opens, the disputed photo stays to the end unless the host explicitly decides to close the cycle; the recap never mentions the dispute.
- **Photo withdrawn for consent** (recognizable non-consenting person reported before the vote opens): withdrawn without debate, status `withdrawn_consent`, the member may resubmit before the deadline. After the vote opens, withdrawal stays possible at any time at the request of the person concerned relayed by the host — protecting people comes before the ranking; the cycle continues with the remaining photos and the recap notes it in one neutral line.
- **Reaction from a non-member, or out-of-window (`direct_thread` mode)**: ignored at counting, counted in the exclusions by category. No follow-up, no remark in the thread.
- **Platform without usable reactions**: written fallback, announced from the vote opening (see The vote). Changing mode mid-vote is forbidden: it would be changing the rules while people are voting.
- **Abandoned cycle** (the host ends it, or no submission): status `abandoned`, short closing message in the thread (approved by the host), no season points, the season file is not touched; the theme may be proposed again later (it does not enter `used_themes`).
- **Recap disputed after publication**: the referee republishes the count detail from the state (raw, exclusions, valid, per photo). If the detail reveals a referee error, the corrected ranking is republished saying so, and the season is recomputed; otherwise, the file settles it and the discussion is closed.
