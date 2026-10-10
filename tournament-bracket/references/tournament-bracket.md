# Tournament Bracket — group game template

Runs on the generic mechanism in `references/group-messaging.md` (the user's connection, designated host group, host approvals, secrets in 1:1) — this document defines only the game's rules and the referee's work. The questions of every duel obey, in full, the quality gate below (the reasoned-trivia gate), with no exception and no lightened version.

## The game in one sentence

The entrants face each other in a single-elimination bracket: each duel is an asynchronous mini-quiz played separately in private by the two opponents, on different but comparable questions whose key is sealed in the state before the duel; the better score advances, the updated bracket is published after every round, and the final crowns a champion.

## Guiding principle: the duel is fair because it is sealed before it is played

No player ever sees their opponent's questions, and the referee cannot favour anyone: for each duel, **all** of both players' questions, their answers (the key), and each player's reserve question are written into the state file **before** the first question of the duel is sent. After the duel, the finished duel's key becomes public with the result: anyone can recount. The tournament's fairness rests on three pillars, in this order: key sealed before the duel, different questions per player, tiebreak written before the first tournament is played.

## Bracket sizes, signups and byes (rounding rule, settled)

- **Entrants accepted: 4 to 16.** The full sizes are powers of 2: **4** (small group: semi-finals + final), **8** (quarter-finals, semi-finals, final), **16** (round of 16, quarter-finals, semi-finals, final). Below 4 entrants, the bracket has no bite: the referee proposes waiting for more signups or launching another game. Above 16, the list closes at 16 and the next names form a waiting list (usable only before round 1 is launched — see Edge cases).
- **A count that is not a power of 2 is completed with byes.** The bracket size is the smallest power of 2 at or above the number of entrants (5, 6 or 7 entrants → bracket of 8; 9 to 15 entrants → bracket of 16). The number of **byes** (free passes to the next round) is: `bracket size − number of entrants` (e.g. 6 entrants → bracket of 8 → 2 byes; 12 entrants → bracket of 16 → 4 byes).
- **Bye allocation, settled: to the earliest signups, in timestamped signup order.** No draw, no host choice: signup speed is the only criterion; it is public and verifiable in the state (`signed_up_at`). A bye is neither a point nor a win: the exempted player advances to the next round without a duel, and their bracket duel is marked `bye` in the state and in the published bracket.
- **Seeding: signup order makes the seeds.** The first signup is seed 1, the second seed 2, and so on. **Classic crossed pairings**: in each opening round, the highest seed still in play faces the lowest (1 against last, 2 against second-to-last, …), so that the high seeds' byes send them toward the lowest-ranked opponents of the next round. The full round 1 pairing table is published in the thread **before** the first duel; after every round, the referee republishes the updated bracket.
- **No third-place match by default**: the semi-final losers are ranked **joint third**. A ranking match may exist only if it was announced before round 1; it is then played as an ordinary duel of the final round.

## The duel — format

1. **Two separate mini-quizzes, never a shared quiz.** Each opponent receives **their own questions, in a private 1:1 message**, and answers privately to the referee. A player sees neither the other's questions nor the other's answers before the duel result is published. The questions are **different from one player to the other, always**: never the same question to both opponents of a duel (if one talked about their questions in the group, the other must not be able to profit from it — and vice versa).
2. **Number of questions per player: fixed at the tournament announcement, identical for both opponents, 3 by default** (5 if the host wants longer duels). That number holds for the whole tournament, final included; it is written into the state (`questions_per_player`). The tiebreak question and the reserve question do not count in that number.
3. **Comparable difficulty — the rule that makes the duel honest.** Both sets pass the same gate (below); the referee additionally balances at generation: same family of effort (listable sets of comparable size, conditions of the same type), no question with one obvious lone finalist on one side and a hard question on the other, varied dimensions within each set (never two questions on the same dimension for one player in one duel). "Comparable" does not mean identical: the residual chance is part of the game, but it is bounded by the gate and by this balancing, both written here — not left to the referee's mood.
4. **Question quality gate (full, per question, before writing it into the state)**:
   - [ ] Named, listable answer-set, written into the state (field `answer_set`)
   - [ ] At least one testable condition that eliminates candidates; reasoning that narrows the field to 2–4 finalists, not one obvious lone finalist
   - [ ] **Exactly one correct answer** (edge cases checked: specify "by surface area", "seat of government", etc., or discard the question)
   - [ ] **Well-established, stable fact**; no recent, disputed, or yearly-changing figure
   - [ ] Source of the fact known well enough to explain it in 2–3 sentences (field `source_fact`)
   - [ ] (Answer + dimension) pair absent from `library/questions.json` — **anti-repetition via the shared library** of all the skill's question games: checked before every duel, not only at the tournament launch, because the library may have moved between rounds
   - [ ] The wording contains neither the answer nor a clue that gives it away
   A single unchecked item = question discarded, another is generated. The gate also applies to the reserve question and to the tiebreak question.
5. **Sealed key per duel.** Before the questions of a duel are sent, the referee writes into the state, for that duel: both question sets with their complete key (`answer`, `explanation`, `source_fact`), each player's reserve question with its key, the duel deadline, and logs `keys_sealed_at` in the journal. **No question of a duel leaves before that duel's entire key is in the file.** The keys of later rounds are not written in advance: each round is generated and sealed after the previous round is published (the opponents are only known then), under the same discipline.
6. **Answers in private, before the deadline.** The player answers in 1:1, in one or several instalments, but only the situation at the deadline counts. The referee acknowledges receipt with a bare status ("received"), with no comment at all on the answers. A **complete answer** = every question of the duel has received an answer; the state records `complete_received_at`, the timestamp of the reception of the **last** answer that completes the set. A question with no answer at the deadline counts as wrong (see Forfeits: it is not a forfeit if the player answered at least in part).
7. **Duel score = number of correct answers** (1 point per correct answer, no negative, no bonus). Marking is done **from the sealed key**, after the deadline or as soon as both complete sets are received — never before, never from memory.
8. **Publication of the result.** At the duel's closing, the referee publishes in the thread (host-approved message): both scores, the detail of both sets (questions, answers given, correct answers — the duel is finished, its key is no longer a secret), the winner and how they won (score, tiebreak, forfeit or bye), then the updated bracket as soon as the round is complete. An eliminated player becomes a spectator: they may follow the bracket; they no longer play.

## Deadlines and round rhythm

- **One round per period, fixed at the announcement**: the period (a day, a week, or any duration announced by the host) is written into the state (`round_period`) and holds for the whole tournament. All the duels of one round share **the same deadline**, announced in the published bracket and repeated in every question send.
- The next round starts only after the current round is fully published (all its duels closed, tiebreaks included): two rounds are never played at once.
- **Early closing of a duel**: allowed as soon as both opponents have delivered their complete set — the referee may then mark it and, if the round's other duel is also closed, publish earlier. Never an early closing against a player who has not finished: the announced deadline is a right.
- Reminders to silent players: via the host, in the thread ("one duel of the round is still waiting for its answers before [deadline]") or privately to the player concerned, always as a status without content — never "you are missing question 2", never a hint about the opponent's set.

## Tiebreak — settled procedure (in this order, without exception)

A tied score at a duel's closing **never** sends both players through, and is **never** settled at random: a knowledge tournament does not crown a coin toss. The referee applies, in order:

1. **Sudden death: one extra question for each.** The referee generates **two new questions** (one per player, different, comparable difficulty, full gate), writes them into the state with their key (`tiebreak.keys_sealed_at`) **before** sending them in 1:1 to both players, at the same time. Tiebreak deadline: short, announced in the sending message — **120 minutes by default**, another duration possible if it was fixed at the tournament announcement and written into the state (`tiebreak_deadline_minutes`). The player who is correct in sudden death advances if the other is wrong or silent at the tiebreak deadline.
2. **If sudden death does not separate them** (both correct, or both wrong/silent): **the player whose complete answer to the initial duel was received earliest advances.** The authoritative timestamp is the state's `complete_received_at`: the reception of the complete set of answers to the duel (not the tiebreak's). Justification, announced from the tournament launch so everyone knows it before playing: at equal knowledge over the whole duel, the tournament rewards the one who played fastest. If only one of the two delivered a complete set, they win this criterion outright; if **neither** delivered a complete set (a tie on partial sets after a sudden death with no winner), the one who answered the greatest number of the duel's questions advances; a still-perfect tie at that stage (same number of answers, timestamps indistinguishable at the logged minute): the referee says so frankly to the host, who alone decides between replaying a second sudden death or declaring both players eliminated (the place then follows the double-forfeit rule below) — the referee invents no additional criterion.
- The tiebreak is part of the duel: its detail (questions, answers, timestamps, the step that decided) is recorded in the state and published with the duel result. A player who disputes it can recount everything from the file.

## Forfeits and silences

- **Player silent at the duel deadline** (no answer received): **forfeit**. The opponent advances, whatever their score — even a complete set at 0 beats a forfeit. Published as "win by forfeit", without mockery or detail.
- **Partial set** (at least one answer, but not all): this is not a forfeit. The player is marked on what they delivered, unanswered questions count as wrong, `complete_received_at` stays `null` (which penalises them in the tiebreak, see above) — a rule known from the announcement.
- **Double silence** (neither opponent answers the duel): **both are eliminated**, nobody advances on that bracket place. Procedure: the place stays vacant; the winner of the other duel of the same bracket pair will therefore face a **bye** in the next round (they advance without a duel if that place is their direct opponent, which is announced in the published bracket); if the double silence happens in the **final**, the tournament ends **without a champion** (`champion: null`), published honestly as such — an absent player is not crowned, and the final is not replayed by other players.
- **Forfeit in the tiebreak**: a player silent at the sudden-death deadline counts there as "wrong" for step 1; step 2 (timestamp) then applies normally.
- **Withdrawal between rounds** (a qualified player announces they will no longer play, or stays silent at the next duel): forfeit at the duel concerned, same procedure. A player cannot "give" their place to an eliminated player: the place follows the vacancy rules above, never an invented repechage.

## The referee's work (reminder of the rules that protect the tournament)

1. **The key does not circulate.** While a duel is not closed, its questions and answers are shown to no one other than their recipient (for their questions) and never leave the state file. In host-player mode (`group-messaging.md`, section b bis): the duel message template (fixed text + a `[YOUR QUESTIONS]` slot) is approved once before the first send of that type; the filled versions are never shown to the playing host — they receive only statuses ("sets received for the round: 3/4"). The host receives their own questions in 1:1 like any player.
2. **Neutrality of generation and tone.** The sets are generated before knowing who will answer best, balanced under the comparability rule, and no send comments on a set's difficulty or an opponent's form ("easy set for X" is a refereeing leak, not conversation).
3. **The state is authoritative.** Re-read the file at the start of every event (send, answer received, deadline, tiebreak), rewrite it after each. Scores, timestamps and the published bracket are recounted from the state, never from memory.
4. **Dispute of a result**: the referee republishes the duel detail from the state (the closed duel's key is public by the publication rule). If the key reveals a marking error by the referee, they correct it, republish the corrected result and bracket saying so, and log the correction in the journal. If the bracket has already advanced a round on the basis of the wrong result and the correction changes a qualifier, the host alone decides: resume at the round concerned or freeze — never a silent correction.

## State schema — `games/<game-id>.json`

`game-id`: `tournament-bracket-<YYYY-MM-DD>-<hhmm>` (prefix `TEST-` for a test tournament). One file per tournament, kept by the referee alone. The tournament's sealed keys = the `answer` / `explanation` / `source_fact` fields of each duel's questions (sets, reserves, tiebreak), written duel by duel, each before its duel is sent.

```json
{
  "id": "tournament-bracket-2026-01-01-2000",
  "game": "tournament-bracket",
  "test": false,
  "status": "in_progress | finished | abandoned",
  "language": "fr | en",
  "created_at": "2026-01-01T20:00:00-05:00",
  "config": { "platform": "messenger", "conversation": "<the user's host group>", "host": "<host name>", "host_mode": "player | spectator" },
  "parameters": {
    "bracket_size": 8,
    "questions_per_player": 3,
    "round_period": "one week",
    "tiebreak_deadline_minutes": 120
  },
  "players": [
    { "name": "<name in the group>", "seed": 1, "signed_up_at": "2026-01-01T20:03:00-05:00", "status": "in_play | eliminated | forfeit | champion", "eliminated_at": null }
  ],
  "bracket": {
    "byes": ["<name of the exempted player, or empty list>"],
    "rounds": [
      { "number": 1, "name": "quarter-finals", "duels": ["QF1", "QF2", "QF3", "QF4"] }
    ]
  },
  "history": [
    { "round": 1, "duel": "QF1", "winner": "<name>", "score": "3-2", "mode": "score | tiebreak_sudden_death | tiebreak_timestamp | forfeit | bye | double_forfeit" }
  ],
  "duels": [
    {
      "id": "QF1",
      "round": 1,
      "phase": "quarter-final",
      "player_a": "<name>",
      "player_b": "<name>",
      "status": "upcoming | in_progress | tiebreak | finished | bye | double_forfeit",
      "deadline": "2026-01-08T20:00:00-05:00",
      "keys_sealed_at": "2026-01-01T20:10:00-05:00",
      "questions": {
        "<player_a>": [
          { "number": 1, "answer_set": "…", "dimension": "…", "question": "…", "answer": "…", "explanation": "…", "source_fact": "…", "answer_given": null, "correct": null }
        ],
        "<player_b>": []
      },
      "reserves": {
        "<player_a>": { "answer_set": "…", "dimension": "…", "question": "…", "answer": "…", "explanation": "…", "source_fact": "…", "used": false },
        "<player_b>": {}
      },
      "receptions": { "<player_a>": null, "<player_b>": null },
      "scores": { "<player_a>": null, "<player_b>": null },
      "tiebreak": null,
      "winner": null,
      "win_mode": null,
      "published_at": null
    }
  ],
  "final_ranking": null,
  "champion": null,
  "journal": [
    { "moment": "2026-01-01T20:00:00-05:00", "event": "tournament_created" }
  ]
}
```

- `tiebreak`, when it happens, has the form: `{ "reason": "tie <a>-<b>", "keys_sealed_at": "…", "deadline": "…", "questions": { "<player>": [ { …same form as a set question… } ] }, "receptions": { "<player>": "…" }, "scores": { "<player>": 0 }, "deciding_step": "sudden_death | timestamp", "winner": "<name>" }`.
- A `bye` duel has neither `questions`, nor `reserves`, nor `scores`: only `player_a` (the exempted player), `winner` = that player, `win_mode: "bye"`. A `double_forfeit` duel has `winner: null` and `win_mode: "double_forfeit"`.
- `receptions` = each player's `complete_received_at` field for this duel (`null` if the set is incomplete or silence); it is what tiebreak step 2 reads. Partial answers and their timestamps live in the questions' `answer_given` and in the journal.
- `history` grows at each closed duel, in order; `final_ranking` and `champion` are written at the end (champion `null` accepted if the final is a double forfeit).

## End writings and persistence (end of tournament)

1. **Tournament state**: `status` → `"finished"`, complete `final_ranking` (champion, finalist, semi-finalists joint third, then eliminated players by round), `champion` filled (or `null` accepted), complete bracket `history`. The state is the tournament's persistence: ranking and bracket history live there, as group results live in their own states.
2. **`library/questions.json`**: add every question **actually asked** (sets played + tiebreak questions played), in the shared format: `{ "question", "answer", "dimension", "subject": null, "game_id", "date", "game": "tournament-bracket" }`. **Unused reserve questions do not enter it** (they were not asked; their answer + dimension pair stays available for a future tournament) — but a **used** reserve enters it like an ordinary asked question.
3. **`scores.json`**: **no entry** — that file stays reserved for scored solo rounds (trivia, closest-wins solo), the same decision as for Werewolf and the Prediction League. A tournament's result is re-read in its state (`final_ranking`, `champion`, `history`), never in `scores.json`.
4. **Final publication**: the champion (or the absence of a champion) and the final ranking are published in the thread, and the complete final bracket is attached to the recap.

## Message templates (adapt to the game's language)

- **Tournament announcement**: "Tournament Bracket — [NUMBER] places (bracket of [SIZE], [BYES] bye(s) for the earliest signups if applicable). Each duel: [N] questions in private against your opponent, one round per [PERIOD]. Tie in a duel: sudden-death question, then the fastest to have delivered their complete set advances. Silence at the deadline = forfeit. Sign up in the thread before [SIGNUP DEADLINE]."
- **Question send (private, one per player)**: "Tournament — [PHASE], your duel against [OPPONENT]. Here are YOUR [N] questions: [YOUR QUESTIONS]. Answer in private in this thread before [DEADLINE]. Your questions are not your opponent's; do not publish them in the group."
- **Receipt acknowledgement (private)**: "Received for your [PHASE] duel." (nothing else — no comment on the answers.)
- **Duel result (thread)**: "[PHASE] — [PLAYER A] [SCORE] — [SCORE] [PLAYER B]. Detail: [QUESTIONS, ANSWERS GIVEN AND CORRECT ANSWERS OF BOTH SETS]. [WINNER] advances [MODE: on score / on tiebreak / by forfeit / bye]. Bracket: [UPDATED BRACKET]."
- **Tiebreak (private, to both players)**: "Tie [SCORE]-[SCORE] in your [PHASE] duel. Sudden death: here is YOUR question: [QUESTION]. Answer in private before [TIEBREAK DEADLINE]. If sudden death does not separate you, the player whose complete duel set was received earliest advances."
- **Champion (thread)**: "Tournament finished — champion: [NAME]. Final: [DETAIL]. Final ranking: [RANKING]. Thank you all; the complete duel detail (questions and keys) is in the tournament history."

## Edge cases (settled)

- **Entrant count not a power of 2**: byes under the rounding rule (see Bracket sizes) — never an invented preliminary round, never a three-way duel.
- **A question's fact discovered false or ambiguous.** Before the player concerned has answered that question: the question is withdrawn and **replaced by their sealed reserve question** (sent in 1:1, presented honestly as a replacement, without saying more); marking is done on the set with the reserve. After their answer, but before the result is published: the faulty question is withdrawn, the reserve is asked with an **announced mini-deadline** (by default: the same duration as the tiebreak), and the player answers within that delay — if they do not answer, the reserve counts as wrong. After the result is published: no reopening on this ground; only a proven **marking** error in the published key follows the dispute procedure (see The referee's work, point 4). In every case, the faulty question does not enter the library and the incident is logged in the journal.
- **A player publishes their answers (or their questions) in the thread instead of privately.** Settled: **the duel continues.** Their answers count as they stand if they are legible and received before the deadline; since the sets are different, their publication reveals nothing of the opponent's set — the harm is limited, and cancelling would punish a clumsiness more than cheating. The referee reminds the player of the rule in private, mentions the incident honestly in the published duel result, and logs it in the journal. If the publication also reveals an element of the key of **another duel in progress** (textbook case: a copy of a referee draft), the duel concerned follows the mechanism's "compromised game" rule (stop, host decision) — never concealment.
- **Tie in the final**: the ordinary tiebreak applies, in full. **No co-champions**: a tournament crowns one champion, except a double-forfeit final (then `champion: null`, published as such).
- **Faulty tiebreak question**: same "fact discovered false" procedure as for a set, applied to the tiebreak: the duel reserve of the player concerned if it has not been used, otherwise a new question generated and sealed before sending, with a mini-deadline announced to both players (the opponent keeps their sudden-death answer already received).
- **Player unreachable in 1:1 before round 1** (no private thread resolved): the referee tells the host **before** the launch; if a waiting-list player can replace them before the bracket is published, the replacement is made at the same seed and the published bracket mentions it; otherwise, their place becomes a bye for their round 1 opponent (never a rearrangement of the bracket after publication).
- **Delay of a whole round** (the host suspends the game, group unavailable): unexpired deadlines are shifted by the same amount, announced in the thread, and logged in the journal; answers already received stay valid and keep their original timestamp (a future tiebreak reads the real timestamps, not the shifted ones).
- **Abandoned game** (the host ends it): status `abandoned`, short closing message in the thread (host-approved), no champion declared even if a finalist was leading — an interrupted tournament has no champion; the results of duels already published stay in the state and the history.
- **Dispute of a count or a timestamp**: the referee republishes the detail from the state (closed duel's key, `receptions`, journal). The file settles it.
