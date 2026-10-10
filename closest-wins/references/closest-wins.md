# Closest Wins, refereed: full rules

Reference for the `closest-wins` skill. A numeric estimation game, playable **solo in chat** with the user, or **in a group** through the generic mechanism in `references/group-messaging.md` (the user's connection, a designated host group, host approvals, answers private in 1:1). This document defines only the rules of the game and the referee's work; no group, account, or real name is hardcoded here.

## The game in one sentence

The referee asks a question whose answer is a number ("How tall is this monument, in metres?"). Each player gives one number, without seeing the others'. When every answer is in (or at the deadline), the referee reveals the true value: **the closest player scores 1 point**. Default express format: **5 rounds**. The fun is not knowing: it is getting close by order-of-magnitude reasoning, and sensing where the others will go wrong.

## Modes

| | Solo | Group |
|---|---|---|
| Where | In the user's chat | In the host group designated by the user, via `group-messaging.md` |
| Players | The user alone, against the value | 2 or more players listed in the group config (the host plays or referees as spectator, see the host-player mode of the mechanism) |
| Answers | Directly in chat, one round at a time | **In private (1:1) to the referee**, never in the public thread before the reveal |
| Round point | 1 point if the answer falls within the sealed tolerance (see "Points, solo" below) | 1 point to the closest player(s) |
| End writings | `scores.json` plus `library/questions.json` (see "End-of-game writings") | Game state marked finished plus history in the state; no entry in `scores.json` (reserved to scored solo games) |

### Points, solo

Solo, there is no opponent: the point is won against a **tolerance** fixed before the game and written in the state (`tolerance_pct`, **20% by default**). The player scores 1 point if their answer falls within plus or minus 20% of the true value (relative distance at most 0.20), and 0 otherwise. The tolerance never changes during a game. It is the honest transposition of "closest" to a single player: the bar is written before, never adjusted after the answer.

## Quality gate, applied to EVERY question before it is written into the state

One unchecked item = the question is discarded and another is generated.

- [ ] **Stable, verifiable fact**: physical geography, dated history, well-established science. No recent, moving, or contested figure (no "current" population, no record broken last year, no value on which serious sources diverge strongly: if two solid references give values more than about 5% apart, the question is ambiguous and is discarded).
- [ ] **One single true value, with the unit explicit in the question**: the question names the unit ("in metres", "in square kilometres", "in inhabitants") and, if the fact depends on a date, the date is in the question ("in inhabitants at the 2021 census"). No question whose answer changes with a guessed unit or year.
- [ ] **Unknown but approachable value**: the player almost never knows it by heart, but can approach it by order-of-magnitude reasoning (decompose, compare with a known landmark, bound it). A pure-chance number (winning number, code, registration number) is forbidden: there is nothing to reason about.
- [ ] **Playable order of magnitude**: the value is neither trivial (everyone knows it exactly: "how many days in a week?") nor astronomically unreadable; very large numbers are accepted if the unit and landmarks make them approachable. **And not a "famous figure" recited by heart**: some values have become school facts that many players (and most language models, if a player cheats with one) give exactly without estimating. Such a question is not false, but it does not make anyone estimate: avoid it, or keep it knowing it will separate players badly.
- [ ] **Source of the fact noted in the key**: field `fact_source`: the fact and its reference in one line, enough to explain the value in 2 to 3 sentences at the reveal.
- [ ] **Value written in the state BEFORE the question is asked (sealed key)**: every value of every round is in the state file from the game's creation, before the first question. The key never leaves the file before its round's reveal.
- [ ] **Anti-repetition**: the pair (value + dimension) is absent from `library/questions.json`. **Settled discipline: a shared field, no dedicated field.** The library file is common to all the question games the user plays; each estimation entry is written there with `game: "closest-wins"`, its `question`, its `answer` in the form "<value> <unit>" (for example "330 metres"), its `dimension`, its `subject`, its `game_id`, and its `date`, the same form as other question-game entries. Anti-repetition is therefore checked in one glance across games, and a dimension already played in another question game blocks the estimation too, which is intended: what counts is repetition for the player, not which game asked it.
- [ ] **The wording contains neither the value nor a clue that gives it**: no numeric landmark in the question that gift-reveals the answer. A neutral scale landmark, very far from the value, stays allowed if it helps reasoning without betraying the answer.

## How a round runs

### Group

1. **Opening**: the referee publishes in the thread (message approved by the host per the mechanism): the round number, the question with its unit, the answer deadline, and the reminder: "answers in private to the referee, never in the thread".
2. **Private collection**: each player sends their number **in 1:1 to the referee** before the deadline. The referee acknowledges receipt in private with a bare status ("received"), with no comment on the value: no "close", no "far", no different tone depending on the answer. One answer per player per round: the first received counts, except an explicit correction by the player before the deadline (the last version before the deadline then counts, and the state keeps the trace of both).
   - **Why private:** a visible answer anchors every following one (the second player aligns on the first instead of estimating). The simultaneous reveal is the heart of the game; no answer is published or even counted aloud ("2 answers received out of 4", a status without content, is allowed).
3. **Deadline**: at the deadline, collection closes. **Silence = round skipped for that player**: no answer, no possible point, no after-the-fact reminder. The referee may close earlier if every expected answer is in.
4. **Reveal**: the referee publishes in the thread, in a single message: the true value (with `fact_source` in one sentence), **all** the players' answers, the distance of each, the winner(s) of the round, and the game's cumulative score. Only at that moment do the answers become public, all together.
5. The referee updates the state (answers, distances, points, scores, log) **before** opening the next round. The state is the truth, not conversation memory.

### Solo

1. The referee asks the question in chat, alone, with its unit: never the value, never a clue.
2. The user answers directly in chat, a single number (see "Units and non-numeric answers" below).
3. **Immediate correction**: the referee reveals the true value, the distance (absolute and relative), whether the point is won under the sealed tolerance, a short explanation anchored on `fact_source`, and the running score ("2/3 so far"). The state is updated after each round.

## Points, settled rules

- **The closest scores 1 point.** Distance = the absolute value of the gap between the answer and the true value, in the question's unit. No negative points, no points proportional to precision, no bonus invented mid-game.
- **Tie = shared point.** If two or more players are at the **same minimal distance** (identical answers, or different answers at equal distance on either side of the value), **each of them scores 1 point**. No tiebreak, no replayed round, no half point: the game rewards estimation, and two equally good estimations have the same value. The tie is announced as such at the reveal.
- **Exact answer (distance 0) = a simple point, no bonus.** Settled: 1 point, like any round win. Justification: a round is worth 1 point by construction; bonusing exactness would create a premium on luck (landing exactly on a large number is more often chance than reasoning) and would unbalance short 5-round games, where a 2-point bonus would be worth two ordinary rounds. The feat is highlighted in the reveal message ("exact answer!"), not in the score. Solo, an exact answer wins its point like any answer within tolerance: same rule, same justification.
- **No "without going over" rule by default.** Going over the true value does not eliminate: only distance counts, in both directions. The game is not a televised bidding game; punishing overshoot would distort honest estimation (everyone would aim low out of caution). **Optional variant "without going over"**: if the host chooses it **before the game** (never during), it is written in the state (`variant_without_going_over: true`); any answer above the true value is then out of the round, and the closest **from below** scores the point; if every answer goes over, nobody scores. Solo, the variant makes no sense and does not apply.

## End of game

- **Group**: after the last round, the referee publishes the complete final standings (every player's score, rounds won by each, exact answers highlighted). On a tie in the final standings: **co-winners**, announced as such, with no improvised tiebreak round (the host may ask for an extra round, which is then a new normal round, announced before it is played). State marked finished, result recorded in the state's log.
- **Solo**: a recap (score out of the number of rounds, the missed rounds with their true value), then the end writings below, state marked finished. Offer another game without insisting.

## State schema, `games/<game-id>.json`

One single schema for both modes; the group-only fields (`config`, several players) are simply absent or reduced to one player in solo. `game-id`: `closest-wins-<YYYY-MM-DD>-<hhmm>` in solo, `closest-wins-group-<YYYY-MM-DD>-<hhmm>` in group (prefix `TEST-` for a test game). (French source names: `etats/<partie-id>.json`, fields such as `valeur`, `echeance`, `reponses`.)

```json
{
  "id": "closest-wins-group-2026-10-10-2100",
  "game": "closest-wins",
  "mode": "group | solo",
  "status": "in_progress | finished | abandoned",
  "language": "fr | en",
  "created_at": "2026-10-10T21:00:00-04:00",
  "config": { "platform": "messenger", "conversation": "<the user's host group>", "host": "<host name>", "host_mode": "player | spectator" },
  "variant_without_going_over": false,
  "tolerance_pct": 20,
  "players": [
    { "name": "<player name>", "score": 0 }
  ],
  "current_round": 1,
  "rounds": [
    {
      "number": 1,
      "dimension": "height of a monument",
      "question": "...in metres?",
      "value": 0,
      "unit": "metres",
      "fact_source": "...",
      "deadline": "2026-10-10T22:00:00-04:00",
      "answers": { "<player name>": 0 },
      "distances": { "<player name>": 0 },
      "points": { "<player name>": 0 },
      "status": "upcoming | in_progress | revealed | cancelled"
    }
  ],
  "winners": null,
  "log": [
    { "time": "2026-10-10T21:00:00-04:00", "event": "game_created_key_sealed" }
  ]
}
```

- The key = the `value` and `fact_source` fields of each round. They exist from the file's creation, before the first question is asked (sealed key), in group as in solo.
- `config` exists only in group mode (it copies the host group config from the user's data; never the reverse). `tolerance_pct` serves solo only; `variant_without_going_over` serves group only. Both are written at creation and never change during a game.
- `answers` is filled as collection proceeds (in group: the moment each private answer arrives; it stays in the file, never republished before the reveal). `distances` and `points` are filled at the round's reveal, computed from the answers and the state's value, never from memory.
- `winners`: in group, the list of names tied at the top score (a single name for a single winner); in solo, `null` (the score suffices).
- The log records every dated event: creation with sealed key, round opening, answers received (statuses, without copying the numbers outside their proper fields, where they exist only in the state), reveal, any tie, any cancellation, end of game. It is the proof of neutral refereeing, showable to the players after the game.

## End-of-game writings

1. **Solo only**, `scores.json`: add `{ "date", "game_id", "game": "closest-wins", "subject", "language", "score", "nb_questions", "test": true|false }` (same form as other scored solo question games; `subject` = the questions' theme if there is one, otherwise `null`). **Group**: no entry in `scores.json`; the result lives in the game state (`status`, players' scores, `winners`, log).
2. **Both modes**, `library/questions.json`: add, per round played: `{ "question", "answer": "<value> <unit>", "dimension", "subject", "game_id", "date", "game": "closest-wins" }`. A **cancelled** round (false fact, see edge cases) does not enter the library: its question was not validly played and its "value" must block no dimension.
3. Game state: `status` set to `"finished"`.

## Units, decimal separators, and non-numeric answers

- **Decimal comma and decimal point are both accepted**: "0,33" and "0.33" are the same number, read in the game's language and the player's evident convention. Thousands separators (spaces, commas, or points used as such) are read in good faith under the same rule: an obvious, unambiguous reading is accepted and confirmed (see below), an ambiguous one is clarified before the deadline.
- **Answer in the wrong unit, or non-numeric.** The referee interprets in good faith, under a rule written in advance: **an obvious, unambiguous conversion is accepted** ("0.33 km" for a question in metres = 330; "37 million" for a question in inhabitants = 37,000,000) and the referee confirms the interpretation to the player **in private and before the deadline** ("I am keeping 330 metres, tell me if that is not it"). If the interpretation is ambiguous (no unit on a number that could be in km or in miles, text with no identifiable number, two numbers in the message): the referee asks for a clarification in private, still before the deadline; **with no clarification by the deadline, the answer is invalid**: it is announced as such at the reveal ("invalid answer: ambiguous unit"), with no distance and no possible point. No answer is ever converted silently, nor interpreted after the deadline. Solo, same rule, in chat: an obvious conversion is accepted and said aloud before the correction; an ambiguous one is asked about, once.

## Edge cases (settled)

- **Fact discovered false or ambiguous mid-game** (a serious source contradicts the sealed value, or the value depends on a convention the question did not settle): **the round is cancelled**. The referee says so frankly at the planned reveal moment (or on discovery if collection is still open, closing the round), no answer scores, the game continues on the remaining rounds, and the cancellation is recorded in the state (round `status: "cancelled"`, log). Never a silent correction of the value mid-round, never a point awarded "closest to the new value".
- **In group, a player sends their answer in the public thread by mistake.** Settled: **the answer counts, and the round continues.** The answer is counted normally: penalizing the player by cancelling their answer would punish clumsiness, not cheating, and cancelling the round would punish everyone. But the anchoring is real: players who have not yet answered have seen a number. Procedure: (1) the referee neither confirms nor comments on the value in the thread (no "well seen", no pointed silence); (2) they remind privately the players who have not yet answered that they play their own estimation; (3) the reveal happens normally, and the incident is **mentioned honestly** in the reveal message ("the answer of X was posted in the thread by mistake before the reveal; it counts, the other answers were collected in private") and recorded in the log. If the host judges the mistake spoiled the round (for example an exact answer posted right at the opening), **the host alone** may ask for the round's cancellation before the reveal; the referee never cancels it on their own initiative on this ground.
- **Late answer** (after the deadline, before the reveal): refused, politely, in private. The deadline is the rule that makes the simultaneous reveal possible; one exception destroys it for every later round.
- **The host plays (group mode)**: apply the host-player mode of the mechanism: public messages go through their ordinary approval; their own answer is asked of them in 1:1 like any player; the other players' answers are never shown to them before the reveal (statuses only: "answers received: 3/4"). Honest limit to announce at the opening: private answers transit through the host's connection, the protection is procedural, not technical: a game among people who trust each other, announced as such.
- **Tie in the final standings**: co-winners (see End of game). No hidden tiebreak, no secondary criterion invented after the fact (neither "more exact answers" nor "signed up first").
- **Abandoned game** (the host ends it, or nobody answers anymore): status `abandoned`, a short closing message in the thread (approved by the host, in group mode); unrevealed rounds are not revealed along the way: their values may be published in the closing message only if the host asks; rounds already revealed stay acquired in the state.
- **Dispute over a calculation**: the referee republishes the answers, the value, and the distances as they are in the state, and redoes the calculation aloud. The file settles it: distances and points are recomputed from `answers` and `value`, never from a conversation memory.

## Message templates (group, adapt to the language of the game)

- **Round opening**: "Closest Wins, round [N]/[TOTAL]. Question: [QUESTION WITH UNIT] Send your number **in private to the referee** before [DEADLINE]. Do not put it in the thread: all answers will be revealed together."
- **Private acknowledgement**: "Received for round [N]." (nothing else, no comment on the value.)
- **Reveal**: "Round [N]: the true value: [VALUE] [UNIT] ([FACT SOURCE IN ONE SENTENCE]). Your answers: [NAME]: [ANSWER] (gap [DISTANCE]); ... The point goes to [NAME(S)]. Scores: [CUMULATIVE SCORES]."
