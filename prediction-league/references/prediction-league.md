# Prediction League — group game template

Runs on the generic mechanism in `references/group-messaging.md` (the user's connection, designated host group, approvals, deadlines, private 1:1 messages) — this document defines only the game's rules and the referee's work. It does not repeat the mechanism.

## The game in one sentence

Over a season, the players of a group privately predict the outcomes of real upcoming events (matches, weather, the winner of a show…); in each round, the referee verifies the results from a source named in advance, awards points according to a fixed grid, and publishes the standings — the season crowns the most consistent forecaster, not the luckiest player of a single evening.

## Guiding principle: the truth is named before the game

A prediction is only worth anything if everyone knew, **before** playing, where the truth would come from. For each event, the round state names a **single verification source** (a specific site, page, or publication) **before that event's prediction deadline**. After the event, the referee verifies the result **from that source, and that source only**: never from memory, never from another source, never from the referee's or a player's recollection. If the named source says something other than what everyone believed, the source is right — that is why it was named in advance.

## Players and season

- **Players**: 3 to 12 registered in the group config (see `group-messaging.md`). Below 3, the standings have no flavour: the referee proposes postponing the launch.
- **Season**: a sequence of **rounds** (one round = a bundle of 3 to 6 events grouped around the same period, typically a weekend). The season length (number of rounds) is announced by the host at launch and recorded in the season file; it is not extended mid-season without the host's agreement.
- **Signups**: open at the announcement of the first round. A player may join mid-season (see edge cases); nobody leaves the standings, even if silent — their missed rounds simply score 0.
- **No secret roles**: this game has no hidden roles. Its only temporary "secret" is the other players' predictions, kept private until the deadline (see Filing).

## Event types and prediction formats

Each event in the state declares a `type`, which fixes the expected format, the applicable grid, and how verification works. Four types are supported; a round mixes at least two of them.

| Type | What the player sends | Example | Verification from the source |
|---|---|---|---|
| `exact_score` | The final score, home then away, two integers | "2-1" | The final score shown by the source |
| `outcome` | One outcome from a closed list named in the state (e.g. `home / draw / away`) | "draw" | The outcome deduced from the result shown by the source |
| `numeric_value` | An integer (total goals, temperature of the day, number of votes…) | "5" | The value shown by the source, or computed according to the `verification_formula` written in the state (e.g. the sum of both teams' goals according to the source's score) |
| `winner` | The name of the winner among the participants named in the state | "Team C" | The winner shown by the source |

Format rules:

- **An unreadable or off-format prediction** (two scores for an `exact_score`, a name outside the list for a `winner`, a decimal number for an integer `numeric_value`) is not interpreted: the referee flags it privately to the player, who may rephrase it **before that event's deadline**. After the deadline, an off-format prediction scores 0 — the referee never guesses.
- The `verification_formula` is mandatory as soon as the value cannot be read as-is in the source: it is written in the state **before** the deadline, in one sentence, so that no calculation is invented after the fact.
- For a weather event, the source names the station or the page and the exact quantity (e.g. the maximum temperature recorded that day at the named station); "it was hot" is not a verification.

## The source of truth — rules and procedure

1. **Named in advance, single, precise.** The state of each event contains `source`: the name of the source and how to consult it (page, section, publication). "Sports sites" is not a source; "the official site of the competition, match page" is one.
2. **Verification by the referee only**, after the real end of the event, by reading the named source. The referee writes the verified result into the state (`result`) with the time of verification (`verified_at`) — never from memory.
3. **Silent source** (nothing published, empty page, result not yet displayed): the referee **postpones the verification** and says so in the thread ("verification of event E3 postponed, source not yet updated"). Recheck after an announced delay (default 24 h). The points of the round's other events may be published without waiting, but the round standings are only **final** once every verification is done or the events are cancelled.
4. **Contradictory source** (the source corrects itself, two pages of the same source disagree) or **still silent after the delay**: the referee lays the problem before the host, with exactly what the source shows. If the disagreement cannot be settled **from the named source itself** (e.g. its official results page against its news feed: the results page prevails — this priority is written here, not invented on the spot), the event is **cancelled**: zero points for everyone, the event is marked `cancelled` in the state, and the standings are computed without it. The named source is never replaced by another source after predictions are in: that would be changing the truth after the game.
5. **Referee verification error** (they misread the source): if a player flags it with what the source displays, the referee re-checks **in the source**, corrects the state, recomputes, and republishes the corrected standings, saying so. Before the final standings are published, correction is free; afterwards, it remains possible until the next round is closed — past that delay, the round standings are frozen, except for manifest fraud settled by the host.

## Flow of a round

1. **Announcement** (public message, host-approved, via `group-messaging.md`): round number, list of events with, for each one, its type, its expected format, **its verification source**, **its own deadline**, and the points grid. The complete round state is written to the file **before** this announcement — events, sources, grid, and deadlines are already in it; none of it changes after the first prediction is received.
2. **Filing predictions — in private, always.** Each player sends their predictions to the referee **in 1:1**, never in the thread: until an event's deadline has passed, the predictions already filed for that event stay invisible to the other players (anti-copying: you do not predict by watching your neighbour). The referee acknowledges receipt privately, with the recording time — that timestamp is what decides lateness.
3. **Deadline per event, not per round.** Each event has its own deadline (default: 30 minutes before its real start, announced in the list). A filing message is judged **event by event**: what arrives in time is accepted, what arrives after its event's deadline is refused — even if the same message contains other predictions that are still in time. There is no all-or-nothing acceptance or refusal.
4. **Changes**: a player may change a prediction — or move their joker — as long as **that event's** deadline has not passed; only the last version received in time counts. After the deadline, any change is refused and the original version stands, even if the event has not yet taken place.
5. **Confidence joker**: each player has **one joker per round**. They designate it when filing the prediction concerned ("joker" next to it), before that event's deadline. The points of that prediction — whatever they are, including 0 — are **doubled**. A joker placed on a refused prediction (late, uncorrected off-format) or on a cancelled event is **not consumed** as long as another event of the round is still open: the player may place it on that one; past the last open event, an unplaced joker is simply lost, with no compensation.
6. **Lock and publication of predictions**: at each event's deadline, the referee publishes in the thread the table of predictions received for that event (all at once, jokers flagged). From then on, they are public and frozen.
7. **Verifications**: after each event, the referee verifies from the named source (see the procedure above) and writes the result into the state.
8. **End of round**: when every event is verified or cancelled, the referee computes the points **from the state** (never from memory), publishes in the thread the per-event detail (verified result, everyone's points, jokers), the round standings, and the updated **season standings**, then writes both persistence files (round state `finished`, season file updated).

## Points grid (fixed for the whole season)

The grid is written into the state of each round, identical to this reference; changing it mid-season is forbidden (a correction only takes effect from the following season).

| Type | Full rate | Intermediate | Otherwise |
|---|---|---|---|
| `exact_score` | Exact score: **5 pts** | Correct outcome (winner or draw right) but score wrong: **2 pts** | **0 pt** |
| `outcome` | Correct outcome: **3 pts** | — | **0 pt** |
| `numeric_value` | Exact value: **5 pts** | Off by 1: **2 pts**; off by 2: **1 pt** | **0 pt** |
| `winner` | Correct winner: **3 pts** | — | **0 pt** |

- **Joker**: the event total (0, 1, 2, 3, or 5) is multiplied by 2. The joker never turns a refused prediction into an accepted one.
- **Cancelled event**: 0 pt for everyone, and the event counts in no tiebreak tally.
- **No negative points**, no invented bonuses (no "prettiest prediction"): the grid above is the whole game.

## Standings and tiebreaks

At the end of each round, two standings are published: the round standings and the season standings (cumulative over all finished rounds).

**Tiebreak order** (applied in this order, to the round standings and to the season standings alike):

1. **Points** (highest first).
2. **Number of exact results**: predictions that earned the full rate of their *precise* type — exact score for `exact_score`, exact value for `numeric_value`. The `outcome` and `winner` types do **not** produce an "exact result" in the sense of this tally: their full rate is binary and would count almost every correct prediction, which would empty the criterion of its meaning. The joker does not change the count (an exact score under a joker counts as one exact, not two).
3. **Number of predictions that earned at least 1 point** (consistency over brilliance).
4. **Shared tie accepted**: if the tie persists, the players are ranked at the **same rank**, and it is published as such ("3rd equal"). No hidden criterion separates them; the display order among tied players follows signup order, purely typographical. The next rank is offset by the number of tied players ("competition" ranking: 1, 2, 3, 3, 5).

**End of season**: the season standings after the last round designate the champion or champions — a perfect tie at the top after criterion 3 gives **joint champions**, accepted as such in the final recap. The referee publishes the season recap (final standings, total exacts, each player's best round) and marks the season file `finished`.

## The referee's work (reminder of the rules that protect the game)

1. **The source above all.** No verification from memory, no substitute source, no "everyone knows that…". If the named source cannot be consulted at verification time, the "silent source" procedure applies — not a search for a replacement.
2. **The other players' predictions are a temporary secret.** Nothing in the thread, nothing privately to another player, no hint ("someone bet big on this match") until the event's deadline has passed. If the host plays, apply the host-player mode of `group-messaging.md`: the referee shows the host only statuses ("predictions received for E2: 4/5"), never contents before the scheduled publication.
3. **The timestamp decides.** Each filing is recorded in the state with its received time. A refusal for lateness cites the deadline and the received time; it is announced privately to the player concerned, and the refusal (without the content) is noted in the state's log.
4. **The state decides.** Re-read the file at every event (filing, refusal, verification), rewrite it after each one. Points are computed from the state, and the published standings can be recomputed by anyone from the public table of predictions and the verified results.
5. **Neutral tone.** The same wording for everyone, no comment on the quality of a prediction before verification, no advice ("are you sure about your draw?"): the referee records, it does not play.

## Persistence

Two files, two roles:

- **One state per round**: `rounds/prediction-league-<season>-r<NN>.json` in the user's data folder (prefix `TEST-` for a test; the French source template names this folder `etats/`). It contains the events, the sources, the accepted and refused predictions, the verifications, and the round's points. Written **before the announcement**, updated at every game event.
- **One persistent season standings file**: `league-season.json` in the data folder. One file per season, updated **at the end of each finished round** (and only there: no "provisional" points are ever written into the season for a round in progress). It survives between rounds and between conversations.

### Round state schema — `rounds/<round-id>.json`

`round-id`: `prediction-league-<season-id>-r<NN>` (prefix `TEST-` for a test).

```json
{
  "id": "prediction-league-season1-r01",
  "game": "prediction-league",
  "test": false,
  "status": "in_progress | finished | abandoned",
  "language": "fr | en",
  "season_id": "season1",
  "round": 1,
  "created_at": "2026-01-01T18:00:00-05:00",
  "config": { "platform": "messenger", "conversation": "<the user's host group>", "host": "<host name>", "host_mode": "player | spectator" },
  "players": [
    { "name": "<name in the group>", "signed_up_at": "2026-01-01T18:05:00-05:00", "joined_round": 1 }
  ],
  "grid": {
    "exact_score": { "exact": 5, "outcome": 2, "otherwise": 0 },
    "outcome": { "correct": 3, "otherwise": 0 },
    "numeric_value": { "exact": 5, "off_by_1": 2, "off_by_2": 1, "otherwise": 0 },
    "winner": { "correct": 3, "otherwise": 0 },
    "joker": "x2 on one prediction per round"
  },
  "events": [
    {
      "id": "E1",
      "title": "<real upcoming event>",
      "type": "exact_score | outcome | numeric_value | winner",
      "start": "2026-01-03T15:00:00-05:00",
      "deadline": "2026-01-03T14:30:00-05:00",
      "source": "<named, precise verification source>",
      "verification_formula": "<mandatory if the value cannot be read as-is in the source, otherwise null>",
      "options": ["<outcomes or participants, for closed-list types, otherwise null>"],
      "status": "open | closed | verified | cancelled",
      "result": null,
      "verified_at": null
    }
  ],
  "predictions": {
    "<player name>": {
      "E1": { "value": "<prediction in the type's format>", "received_at": "2026-01-02T20:12:00-05:00", "joker": false, "status": "accepted | refused_late | refused_format", "base_points": null, "points": null }
    }
  },
  "round_standings": [
    { "rank": 1, "player": "<name>", "points": 0, "exacts": 0, "predictions_with_points": 0 }
  ],
  "log": [
    { "time": "2026-01-01T18:00:00-05:00", "event": "round_created" }
  ]
}
```

- `result` and `points` stay `null` until verification and computation; `points` = `base_points` × 2 if `joker` is true.
- Refused predictions are kept in the state with their status and their time: they are the proof of the refusal, not omissions.
- `exacts` follows the tiebreak definition (full rate of the `exact_score` and `numeric_value` types only).

### Season file schema — `league-season.json`

```json
{
  "id": "season1",
  "game": "prediction-league",
  "test": false,
  "status": "in_progress | finished",
  "created_at": "2026-01-01T18:00:00-05:00",
  "planned_rounds": 10,
  "players": [
    { "name": "<name in the group>", "signed_up_at": "2026-01-01T18:05:00-05:00", "joined_round": 1 }
  ],
  "finished_rounds": [
    {
      "round": 1,
      "state": "rounds/prediction-league-season1-r01.json",
      "standings": [
        { "rank": 1, "player": "<name>", "points": 0, "exacts": 0, "predictions_with_points": 0 }
      ]
    }
  ],
  "season_standings": [
    { "rank": 1, "player": "<name>", "points": 0, "exacts": 0, "predictions_with_points": 0, "rounds_played": 1 }
  ],
  "champion": null
}
```

- After each round, the referee **adds** the round to `finished_rounds` and **recomputes** `season_standings` from the round standings written in the states — never by adding from memory.
- A player who arrived mid-season appears from the round of their arrival, with `joined_round` filled in and 0 points for the previous rounds (they do not appear in their `rounds_played`).

## Message templates — compliant examples (adapt to the game's language)

- **Round announcement**: "Prediction League — round [N]. Events: [LIST WITH TYPE, FORMAT, AND DEADLINE OF EACH]. Verification sources: [SOURCE PER EVENT]. Grid: exact score 5 (correct outcome 2), outcome 3, exact value 5 (off by 1: 2, off by 2: 1), winner 3; one joker per round doubles one prediction. Send your predictions to the referee IN PRIVATE before each deadline — they will be published after each event locks."
- **Acknowledgement (private)**: "Received [TIME]: [EVENT] = [VALUE] [JOKER IF PLACED]. You still have [EVENTS STILL OPEN]."
- **Refusal for lateness (private)**: "Too late for [EVENT]: deadline [DEADLINE TIME], received [RECEIVED TIME]. This prediction scores 0. [IF A JOKER WAS AIMED AT IT: Your joker is not consumed, you may place it on an event that is still open.]"
- **Publication of an event's predictions (thread)**: "[EVENT] — predictions locked: [PLAYER: VALUE, …]. Verification after the event, from [SOURCE]."
- **End of round (thread)**: "Round [N] finished. [PER-EVENT DETAIL: VERIFIED RESULT + EVERYONE'S POINTS]. Round standings: [LIST]. Season standings: [LIST]."

## Edge cases (decided)

- **Late prediction**: refused, with no exception and no negotiation — even by a minute, even if the event has not started (the deadline is 30 minutes before precisely to close that discussion). The refusal is announced privately, recorded in the state and the log. Accepting it "on the sly" even once destroys the rule for the whole season.
- **Mixed message straddling a deadline**: judged event by event (see Flow, point 3) — the on-time part is accepted, the late part is refused, the acknowledgement says both explicitly.
- **Change after the deadline**: refused; the last version received in time stands, even if it looks worse after the fact. Change before the deadline: free, the last in-time version wins, the joker movable within the same limits.
- **Cancelled event** (the real event does not take place): zero points for everyone, the event is marked `cancelled`, a joker placed on it is not consumed (see Flow, point 5). The event is **not** replaced by another one after predictions are in.
- **Postponed event**: if the postponement is known **before** the original deadline and the new date falls within the same league round, the deadline is moved to the new date (announced in the thread), and predictions already filed remain valid and changeable until the new deadline. If the postponement is known **after** the deadline, or pushes the event outside the round: the event is **withdrawn** from the round (zero points, like a cancellation, joker not consumed if another event of the round is still open) — a whole standings table is not made to wait for an event with no date.
- **Silent or contradictory source**: see the procedure in the Source of truth section — postponement of the verification announced, then cancellation if the source itself cannot settle it. Never a backup source.
- **Player joining mid-season**: they start at **0 points** in the season standings, with `joined_round` = the first full round they take part in (signup before the deadline of that round's first event; otherwise, the following one). No catch-up, no already-locked event reopened for them. It is announced in the thread on their arrival, so the standings stay readable.
- **Incomplete round / absent player**: an event with no accepted prediction scores 0 for that player; a whole round with no filing scores 0 for the round. No mandatory reminder, no penalty beyond the 0: the season standings absorb absences on their own.
- **Player who stops playing**: they stay in the standings with their points; the referee removes them only if the host explicitly asks, and the removal is announced in the thread (their past points are not redistributed).
- **Tie in the standings**: tiebreak by exacts, then by predictions with points, then **shared tie accepted** (see Standings and tiebreaks). No playoff event is invented mid-season; if the host wants one, they announce it **before** the last round and it counts as an ordinary event of that round.
- **Scoring dispute**: the referee republishes the computation detail from the state (accepted predictions, verified results, grid). The file settles it; if the file reveals a verification error, the verification-error procedure applies.
- **Abandoned round** (the host ends it): status `abandoned`, no point enters the season standings, a short closing message in the thread (host-approved). Rounds already finished and written into the season do not move.
