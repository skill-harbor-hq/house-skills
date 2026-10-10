# True or False, fabricated edition, refereed — group game template

Runs on the generic mechanism in `references/group-messaging.md` (the user's connection, designated host group, host approvals, private 1:1 messages, host-player mode) — this document defines only the game's rules, how the statements are made, how the key is protected, and the referee's work. True or False is a classic quiz format; the "fabricated edition" variant, where the referee invents the false statements itself, plausibly and in a documented way, is written for this skill and adapted to asynchronous play. No group, account, or proper name is hardcoded here.

## The game in one sentence

The referee composes a round of statements of which about half are true and the other half are false statements it has fabricated to be plausible; it publishes them in the thread, each player answers **True** or **False** before the deadline, and the referee reveals the truth, statement by statement, only once collection is closed. Nobody knows the key in advance, not even the host when the host plays: it is sealed in the state before the first publication.

## Players and round

| Parameter | Rule |
|---|---|
| Players | **2 to 10 players**. Below 2, there is neither guessing nor standings; above 10, 1:1 collection becomes heavy for the referee. Outside those bounds: the referee tells the host before the announcement and proposes waiting for signups or launching another game. |
| Round | **8 statements by default**; 5 = express, 12 = long, if the host asks. Target balance: half true, half false (see the gate: the balance is **counted**, not approximated). |
| Publication | **In one block by default**: the 8 numbered statements go out in a single message, with a single collection deadline. "One by one" variant: each statement goes out separately with its own mini-deadline and its own reveal — more tension, many more approvals; the host chooses at the announcement, never mid-round. |
| Host | The host picks their mode (**player** or **spectator**, see `group-messaging.md`, section b bis); the choice is recorded in the state (`config.host_mode`) and it determines the collection mode (see How a round runs, point 3). |

## Generating the statements — the quality gate

The referee composes the **whole** round before any publication. Each statement passes the gate below; a single unchecked item means the statement is discarded and another one is generated.

### For the TRUE statements

- [ ] A **stable, well-established fact**: geography, nature, dated history, basic science — no recent, contested figure, and none that changes every year.
- [ ] A **verifiable fact**: the referee knows the source of the fact well enough to explain it in 2-3 sentences; the key's `source_fact` field notes it in one line (e.g. "largest hot desert, ~9.2M km²; the polar deserts, larger, are cold").
- [ ] Wording **with no ambiguity of scope**: state what makes the fact true ("the largest **hot** desert", "the smallest **independent state**"); if the scope does not fit in one clear sentence, discard the statement rather than play on a misunderstanding.
- [ ] The wording contains no clue to its own truth (no "it is well known that…", no tone different from the false statements).

### For the FALSE statements — fabricated, plausible, never absurd

A false statement in this game is not a random lie: it is a statement **fabricated by the referee** to look true, by one of these four techniques (noted in the key, field `fabrication_type`):

| Technique | Principle | Example of form |
|---|---|---|
| **Inversion** | A real fact reversed (organ ↔ location, sense ↔ absence of sense, cause ↔ effect) | "The heart of X is in its tail" when it is in its head |
| **Exaggeration** | A real fact pushed beyond the truth (scale, scope, "the only one", "visible from…") | A structure "visible to the naked eye from the Moon" |
| **Shift** | A real element moved by one step: a date, place, name or number neighbouring the true one | "First modern Games in Paris in 1900" for Athens in 1896 |
| **Popular belief** | A widely repeated myth, presented as is | "Bats are blind" |

- [ ] The false statement is **plausible**: a reasonable player can hesitate. Never absurd ("the Moon is made of cheese"), never detectable from the wording alone.
- [ ] The false statement is **fabricated by the referee**, not copied from a false item circulating as real news: it starts from a real fact known to the referee, and the key notes the real fact (`source_fact`) as much as the deformation.
- [ ] **Never** on a sensitive topic (health, money, conflicts, private life, minors, confidential work), **never** insulting or mocking, **never** about a real private person. Historical public figures are admitted only for notorious, non-defamatory public facts — and the simplest course remains to do without them.
- [ ] The same length, the same tone, the same apparent level of precision as the true statements: if the false ones are systematically shorter, vaguer or more spectacular, the round is readable and the game is dead.

### For the whole round

- [ ] **Balance counted before sealing**: the referee counts the true and the false statements in the final list (8 statements → 4 true, 4 false; 5 → 3/2; 12 → 6/6) and records the count in the state (`parameters.balance`). A round with 6 true and 2 false is remade, not "roughly balanced".
- [ ] **Shuffled order**: neither a regular alternation (T, F, T, F…), nor grouping; the sequence of truths must form no guessable pattern.
- [ ] **Varied difficulty**: at least one easy statement, at least one tricky one, the rest in between; the estimated difficulty of each statement is noted in the key (`difficulty`) so the mix is verifiable.
- [ ] **Varied themes**: no two statements on the same subject in one round.
- [ ] No statement repeats, even reworded, a statement from a previous round with the same players (the referee checks the history of the states in the data folder).

## The secret of the key — including against a playing host

The **key** = for each statement, its truth (`true` / `false`), its `source_fact`, its explanation and, for a false statement, its `fabrication_type`. It follows the sealed-key discipline, reinforced here because **the only secret of the game is the key itself** — this game has neither roles nor outgoing secret messages; all the protection bears on what the host sees while approving.

1. **Sealed before publication.** The referee writes the complete state — statements **and** key — into the game's file **before** the first message, announcement included (see the schema). The key never leaves the file before the reveals.
2. **Public messages contain ONLY the statements.** Announcement, publication (block or one by one), deadline reminders, statuses: none of them contains the key, a marking ("✔", asterisk, differentiated bold), a partial count of correct answers per statement, or any hint of tone ("that one is easy"). Statements are published **bare and numbered**, all formatted identically.
3. **In host-player mode, approval drafts are blind by construction.** The host approves each public send on an exact preview (`group-messaging.md`, rule d (3)): that preview is the public message itself, which by point 2 contains nothing of the key. The **intermediate drafts and recaps** shown to the host between phases (e.g. "answers received: 3/4", current scores) contain **neither the key of statements still to come or in collection, nor the correct answers**: a global current score is allowed (it is a total, not an answer), a per-statement detail before its reveal is not. What a playing host learns of the round, they learn in the thread, at the same time as everyone else.
4. **A playing host answers like a player.** Their answers go in 1:1 to the referee, before the deadline, with no prior access to the state or to the other players' answers (see the settled collection mode below). Their possibly poor score is the ordinary proof that the protection held — the referee does not comment on it otherwise.
5. **Reveals statement by statement, at the deadline only.** The truth of a statement is revealed only at the closure of ITS collection (one-by-one mode) or at the closure of the round (block mode: the reveal then goes out in one message **sequenced statement by statement**, in number order). The reveal draft submitted to the host's approval contains the verdicts — it is the only draft that contains them, and it is prepared **only after** closure. Before that moment, no confirmation or denial, in public or in private, even to a player who is "sure", even to the host.
6. **A leak means a compromised game.** If the key (or the verdict of a single unrevealed statement) reaches a player or the playing host by accident — wrong preview, wrong recipient, one detail too many in a status — the referee stops everything, declares it frankly to the host in private without naming more content than necessary, and follows the "compromised game" conduct of `group-messaging.md` (section b bis, point 5): the host decides, restart the round with fresh statements or continue knowingly. Never concealment.

### Templates — compliant examples (adapt to the language of the game)

- **Announcement**: "True or False — fabricated edition! A round of [N] statements: about half are true, the other half are false statements fabricated by the referee to look true. Answer True or False for each statement before [DEADLINE]. 1 point per correct answer. The truth of each statement is revealed only at the end of collection — nobody knows it in advance, not even the host if they play."
- **Block publication**: "Round — answer for each number: **True** or **False**. Deadline: [DEADLINE]. 1. [STATEMENT] 2. [STATEMENT] …" (bare statements, no marking).
- **Intermediate status** (to the host, and in the thread if needed): "Answers received: [X]/[N] players. Deadline: [DEADLINE]." — nothing else.
- **Reveal** (after closure only): "Reveals! 1. [STATEMENT] → **TRUE**. [Short explanation anchored on the source fact.] Correct answers: [NAMES]. …" then current or final scores.

## How a round runs

1. **Announcement** — The host asks for a game and picks their mode (player or spectator). The referee prepares the announcement (see template); the host approves it; it goes to the thread: format, round size, publication mode (block by default), collection mode (per point 3), typical deadline, scoring, and — if the host plays — the honest limit of host-player mode (procedural protection, `group-messaging.md` b bis point 4).
2. **Generation + sealed state** — The referee composes the round, applies the gate, **counts the balance**, writes the complete state (key included) and the log records it (`state_sealed_before_publication`) — **before** publication.
3. **Publication and collection — response mode SETTLED by the host's mode**:
   - **Host plays → answers privately, in 1:1 to the referee. Mandatory, not an option.** Justification: in public, the other players' answers would appear in the thread the host frequents and approves — early answers would influence their own answer (and their public answer, visible, would influence the following ones, with the weight of the host). In 1:1 and at the same time, nobody sees anyone's answer before the reveal, the playing host included; collection stays sealed and the round is played on equal terms.
   - **Host spectates → answers in the thread, by default.** The host does not play: there is nothing to protect on their side, and answering in the thread is simpler and livelier for the group. The copying effect between players (late answers see the early ones) is then **assumed and announced at the announcement**; if a spectating host prefers rigour, they choose 1:1 collection at the announcement — the choice is recorded in the state (`config.response_mode`) and never changes mid-round.
   - In both modes: a player may **change an answer until the deadline**; only the last one counts. Silence at the deadline = **abstention** on the statement or round concerned (0 points, counts neither for nor against).
4. **Closure** — At the deadline (or as soon as every answer is in), the referee closes collection, re-reads the state, recounts the points from the file (never from memory) and prepares the reveal.
5. **Reveal** — A message from the referee in the thread, approved by the host (draft prepared after closure, see Secret of the key, point 5): for each statement, in order, the verdict, the short explanation, the detail of the answers and the points; then the current scores or, at the last statement, the final ones.
6. **End of round** — Final recap in the thread (complete standings, best guesser = first in the standings, statements nobody got right), result written into the state, state marked `finished`. A tie at the top: **co-winners**, no invented tiebreaker; a complete tiebreaker round may be proposed by the host, as a new game.

## Points — fixed scoring, announced in advance

| Event | Points |
|---|---|
| Correct answer (True on a true statement, False on a false one) | **+1** |
| Wrong answer, abstention | 0 |
| Answer received after the deadline or after the reveal | **Refused** — not counted (see Edge cases) |

No negative points, no speed bonus, no bonus invented mid-round. The standings are the total of the points over the **counted** statements of the round (annulled statements excluded, see Edge cases).

## The referee's work (reminder of the rules that protect the game)

1. **No leak, ever.** The same neutral wording for every statement: never "watch out for that one", never a different reaction depending on whether a player proudly announces a right or a wrong answer in the thread. The referee comments on a truth only at its reveal.
2. **Deadlines held.** Every publication announces its deadline. Nudges to silent players: in the thread or in a status to the host, in counts only ("answers are still missing"), without saying who answered what — in 1:1 mode, without even saying to a playing host who has not answered, beyond the count.
3. **The state is the truth.** Re-read the file at every event, rewrite it after every event (generation, seal, publication, answer received, closure, reveal, points, annulment). One file per game, held by the referee alone. The key exists only there.
4. **Verifiable counting.** Points are recounted from the answers recorded in the state before every publication of scores; the detail published at the reveal (answer per player, per statement) lets everyone redo the count.

## State schema — `games/<game-id>.json`

`game-id`: `true-or-false-<YYYY-MM-DD>-<hhmm>` (prefix `TEST-` for a test game). (French source folder: `etats/<partie-id>.json`, game id `vrai-ou-faux-<AAAA-MM-JJ>-<hhmm>`.) Same discipline as the other group games: the **key is sealed in the state before the first publication**, announcement included.

```json
{
  "id": "true-or-false-2026-10-10-2100",
  "game": "true-or-false",
  "status": "in_progress | finished | abandoned",
  "language": "fr | en",
  "created_at": "2026-10-10T21:00:00-04:00",
  "config": { "platform": "messenger", "conversation": "<the user's host group>", "host": "<host name>", "host_mode": "player | spectator", "publication_mode": "block | one_by_one", "response_mode": "private_1_1 | thread" },
  "parameters": { "statements_per_round": 8, "points_per_correct_answer": 1, "balance": { "true": 4, "false": 4 } },
  "players": [
    { "name": "<name in the group>", "points": 0 }
  ],
  "statements": [
    {
      "number": 1,
      "statement": "<the statement as published, with no marking>",
      "truth": "true | false",
      "fabrication_type": "inversion | exaggeration | shift | popular_belief | null if true",
      "difficulty": "easy | medium | tricky",
      "source_fact": "<the real fact in one line — for a false statement: the real fact BEFORE deformation>",
      "explanation": "<2-3 sentences revealed at closure only>",
      "status": "pending | in_collection | revealed | annulled",
      "answers": { "<player name>": "true | false | null if abstention" },
      "points_awarded": { "<player name>": 0 }
    }
  ],
  "round": { "publication": "block | one_by_one", "current_statement": null, "deadline": null },
  "standings": null,
  "winner": null,
  "log": [
    { "time": "2026-10-10T21:05:00-04:00", "event": "state_sealed_before_publication" }
  ]
}
```

- `truth`, `fabrication_type`, `source_fact` and `explanation` form the key: they exist from the creation of the file and appear in no message, draft or status before the reveal of their statement.
- `parameters.balance` is the real count of the `truth` values of the round, filled in by the referee at sealing time — it is the proof that the balance was counted, not hoped for.
- The log records every dated event: creation, gate applied, balance counted, state sealed, host approvals (message types, never the key), publication, answers received (counts and, in the file only, the detail), closure, reveals, points, refusals of late answers, any annulments, end of game. It is the proof of neutral refereeing, showable to the players after the game.

## End-of-round writings

1. Game state: `status` → `"finished"`, `standings` and `winner` filled in from the recounted points, log closed by the `round_finished` event.
2. The result of group games lives in the game's state (standings, log) — that is the canonical writing, as for the other group games; no forced entry in any solo `scores.json`.
3. The statements played stay in the state: they form the anti-repetition history for later rounds with these players (see the gate, whole round).

## Edge cases (settled)

- **Statement whose truth turns out to be contestable** (a player contests a verdict with a serious element, or the referee discovers its source fact was wrong, outdated or ambiguous): **annulment of the statement**. (1) If the contestation arrives before the reveal: the statement becomes `annulled`, its truth is **never revealed** (revealing it would settle exactly what is contested), the round is played on the remaining statements and the announced balance is corrected in the recap ("round counted on 7 statements"). (2) If it arrives after the reveal: the **points of that statement are withdrawn** from every player, a neutral correction is published in the thread (the verdict withdrawn, without reopening the debate in the thread), and scores and standings are recounted from the state and republished. The referee never defends a contestable statement to "save" its round: a doubtful fact is a gate fault, recorded as such in the log.
- **Player who answers after the reveal** (or after the deadline): answer **refused**, politely and without exception — the referee replies privately (1:1 mode) or in the thread (thread mode) that collection for that statement is closed and the answer cannot count; it is recorded in the log as `late_answer_refused`, never written into the counted `answers`. Same rule for an attempted change of answer after closure.
- **Player who stops answering**: abstention at each deadline. Two rounds (or two collections in one-by-one mode) in a row with no answer: the referee flags it to the host, who alone decides (the player stays, in continuous abstentions, or withdraws from the round's standings — their points already earned stay recorded in the state). The referee never removes a player on its own initiative.
- **Final tie**: co-winners announced as such. No improvised "sudden death" statement.
- **Leak of the key**: compromised game — see Secret of the key, point 6. If the leak touches only one statement not yet revealed and the host chooses to continue, that statement is **annulled** (procedure above) and the round is played on the remaining ones.
- **Abandoned game** (the host ends it, or nobody plays anymore): status `abandoned`, a short end message in the thread (approved by the host). The key of unrevealed statements **stays sealed** in the state, unless the host expressly asks for the complete recap — their group, their rules of the moment.
- **Counting dispute**: the referee republishes the detail of the answers and points as it is in the state (the detail becomes public at each reveal, by construction) and the round's log. The file settles it.
