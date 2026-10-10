# Five Locks Escape — chained cooperative puzzle: full rules

Reference for the `five-locks-escape` skill. Two modes: **solo** in chat with the user, or **cooperative group** — the whole team against the game — through the generic mechanism in `references/group-messaging.md` (the user's connection, a designated host group, host-approved sends). This document defines only the rules of the game and the referee's work; it does not repeat the sending mechanism.

## The game in one sentence

Five locks in a chain on one theme: each solved puzzle gives the code, word, or key that opens the next lock, and the solution of lock N always serves lock N+1 in a documented way. The team advances together, has **3 hints for the whole game**, and no lock can block the game for good: a lock that resists too long can be **forced**, at the price of its points.

## Modes

| Aspect | Solo (in chat) | Cooperative group (messaging) |
|---|---|---|
| Players | The user alone | The players listed in the host group's config; the team is **one single counter** for attempts, hints, and score |
| Where it is played | The user's chat | The host group's thread; every proposal, hint request, and force request happens **in the public thread** (this game has no individual secret: no 1:1) |
| Who decides a hint | The user | Any team player, by explicit request in the thread (see Hints) — no vote, the team is one counter |
| Who decides a force | The user | Explicit request from one player **+ confirmation from a second player** (see Forcing) |
| Role of the host | They play | They approve every referee send under the generic mechanism; if they also play, they are a team member like the others (no team secret to protect from them: the key lives in the file, never in the thread) |
| End writing | Entry in `scores.json` | Result in the game state only (see End of game) |

Group player count is not bounded by this template: minimum 2 players, so that confirmation of a force by a second player makes sense; below that, play solo.

## Generation in advance — the complete chain, before departure

The referee generates **all 5 puzzles in one pass, before the first game message**, chooses a theme (proposed by the user or the players, or drawn by the referee and announced), and writes the complete state **immediately** into `games/<game-id>.json`: for each lock, the public statement, the **solution**, the **accepted answer variants**, the **hint text**, and the **chain-link type** toward the next lock. This is the **sealed key**: it never leaves the file, it appears in no draft shown to the host or the players, and no puzzle is presented until the previous lock is solved or forced.

### Admitted puzzle types

Logic (deduction with testable conditions), calculation (arithmetic or deciphering **whose complete rule is given in the statement**), wordplay (initials, assembly, guided anagram), observation of a described scene (the statement describes the scene; everything needed is in it). **Never**: a moving or recent fact, an opinion, pointed external knowledge not supplied in the statement, a riddle with no reasoning path. If the answer requires a convention (reading order, alphabet numbering, direction of travel), the convention is written in the statement.

### Chaining — the chain must be real

The solution of lock N **serves** lock N+1. Recognized chain-link types (one per junction, documented in the state in `chain_link_to_next`):

| Type | Principle |
|---|---|
| `cryptographic keyword` | The word solution of N is the decryption key of puzzle N+1 |
| `orientation word (selection)` | The word solution of N designates which part of a described set (row, column, category) to read in N+1 |
| `order code` | The code solution of N gives the reading or assembly order of the elements of N+1 |
| `reused code` | The code solution of N is reused as-is (combination, coordinates, positions to pick) in N+1 |
| `untangling keyword` | The word solution of N is the padding, template, or mask to remove/apply in N+1 |

A simple "well done, here is the next puzzle about the same decor" is **not** a chain link: the link must be mechanical and necessary — without solution N, puzzle N+1 is unsolvable or unreadable. Continuity exception: after a **force**, the chain element is transmitted by the forcing mechanism (see Forcing, point 4).

### Quality gate — applied to EVERY lock before it is written into the state

- [ ] **One single verifiable solution**: the referee can redo the reasoning or calculation step by step and reach a unique answer; edge cases are settled in the statement (what is counted, in what order, from where)
- [ ] Everything needed to solve is **in the statement** (scene, grid, calculation rule, convention) — no external research, no moving fact, no opinion
- [ ] The solution is a **short word or short code** (a word, a number, a short digit sequence): it is what travels as the tool of the next lock
- [ ] The chain link toward the next lock is one of the recognized types above and **tested**: the referee really used solution N to build or solve N+1
- [ ] **Accepted variants listed**: case, accents, article, digit separators, predictable equivalent forms (see Normalization) — written in the state, never improvised mid-game
- [ ] **Hint text written**: one reasoning step, never the solution nor a step that contains it in plain form (see Hints)
- [ ] The public statement contains neither the lock's solution, nor a later lock's solution, nor a fragment that assembles them on its own
- [ ] Difficulty broadly increasing along the chain (lock 1 is an entry point, lock 5 the most demanding)

**Calibration**: a *selection* puzzle whose statement gives the complete instruction ("the previous word tells you which row to read") is easy by construction — a player who follows the inscription solves it on the first try, with no deduction. This puzzle type belongs at the start of the chain (locks 1-2) or as a breather between two demanding locks, never as a "resistant" lock in the middle or at the end of the chain.

One unchecked item = the lock is discarded and regenerated **before departure** — never repaired mid-game.

## Normalization and variants — what counts as "the right answer"

A proposal is **correct** if, after normalization, it equals the solution or one of the variants listed in the state:

- **Normalization always applied**: case ignored; accents ignored (é = e); leading/trailing spaces and punctuation ignored; a leading definite article tolerated ("le", "la", "les", "l'", "the"); for a digit code, separators ignored ("2-3-1", "2 3 1", and "231" are the same answer).
- **Variants**: any other predictable equivalent form (accepted spelling, word order of a two-part code, etc.) must be **listed in the state at generation time**. The referee **never** accepts an equivalence improvised during the game: a form that is neither listed nor covered by normalization counts as a failed attempt, even if it "meant" the right thing — the rule is hard, but it is the same for everyone, and it protects the referee from any suspicion of arbitrariness. If the team contests, the log and the state's variant list settle it after the game.

## Flow

1. **Opening** — The referee announces in the thread (or the chat): the theme, the principle (5 locks in a chain), the hint counter (3 for the whole game), the scoring scale, and the forcing rule, then the statement of **lock 1 only**.
2. **One lock at a time** — The team discusses freely in the thread. The referee never presents a lock's statement before the previous one is solved or forced: the puzzles to come are part of the key.
3. **Proposal** — A player proposes an answer in the explicit format (see Attempts). The referee checks it against the state (solution + variants, after normalization) and answers **correct** or **incorrect**, with no orienting comment (see Neutrality).
4. **Resolution** — Correct answer: the referee announces the lock opening, the points earned, the provisional score and, if the chain link requires it, presents the next lock's statement. The referee rewrites the state at every event (same discipline as everywhere in this skill: the state is the truth, re-read at the start of each turn, rewritten at the end).
5. **End** — After lock 5 (solved or forced), the referee publishes the final grade and the complete recap (see End of game).

## Attempts — what counts, what does not

A lock is played neither by silent grinding nor by misunderstanding. The distinction is procedural:

- **Counted attempt**: an **explicit proposal, addressed as such**: the player writes `PROPOSITION: <answer>` (recommended format, announced at the opening) or phrases unambiguously "our answer is <answer>". It is logged in the state (`attempts` of the lock, with the player's name in group mode) and increments the lock's counter. The template shown at the opening, with its placeholder (`PROPOSITION: <answer>`), is obviously not a proposal — only players' messages count.
- **Do NOT count as attempts**: discussion hypotheses ("wouldn't it rather be a sea animal?"), questions between players, jokes and off-topic answers (an answer that visibly does not target the current lock — a dish, a song, an unrelated proper name), drafts struck through or withdrawn by their author before verdict.
- **Ambiguous case**: if the referee cannot decide whether a message is a proposal or discussion, they **ask** ("do you want me to count that as a proposal?") and count nothing until the player has confirmed. One clarification request per ambiguous message; the player's confirmation turns the message into a counted attempt, their denial cancels it with no trace in the counter.
- **Proposal targeting a lock that is not the current one** (already opened, or guessed for a lock not yet presented): not counted; the referee answers only "that is not the current lock" — **without ever confirming or denying** whether the answer would be worth anything for another lock. Confirming would be a free hint.
- **Ceiling**: there is no attempt ceiling. Counted attempts serve two purposes: triggering the **force offer** (see Forcing) and appearing in the log. They cost no points by themselves.

### Referee neutrality — no free hint

The referee answers every counted attempt with the **same neutral wording**: "Proposition received: incorrect." / "Proposition received: correct — the lock opens." Absolute prohibitions:

- **Warm/cold** ("you're getting warm", "almost", "you're nearly there", "good direction") — forbidden in all its forms, including for an answer one letter off. A nearly-right answer receives exactly the same "incorrect" as an absurd one.
- Any comment on the content ("interesting lead", implicit eyebrow-raising), any reaction that differs according to proximity to the solution.
- **One single exception**: if the mechanic of a hint **written in the key** is itself gradual (e.g. the sealed hint describes an intermediate step to validate), spending that hint entitles the team to what its text provides — nothing more, and only against spending one hint from the counter.

## Hints — 3 for the whole game

1. **Stock**: **3 hints for the entire game**, all locks combined — not 3 per lock. The counter is **single for the team** in group mode: a hint spent by one player is spent for all.
2. **Spending**:
   - *Solo*: the user explicitly asks for a hint for the current lock.
   - *Group*: **any player** can spend a hint by an **explicit request addressed to the referee** in the thread (e.g. "Referee, hint." or `HINT` at the head of the message). The explicit request **is enough and the spending is immediate**: no vote, no retraction delay — the team organizes among itself, the referee executes. In exchange, the referee is strict on form: a **mention in discussion** ("a hint would help us", "we should maybe…") is **not** a request; faced with an ambiguous phrasing, the referee asks for confirmation before spending, exactly as for ambiguous attempts.
3. **One hint per lock at most**: the hint text is unique and sealed in the state. A second hint request on the same lock is refused with no spending ("this lock's hint has already been given"); the remaining stock serves the following locks.
4. **Content**: the referee gives **the sealed hint text** of the current lock, as written. Never the solution, never a summary that would contain it, never a second reasoning step. If the team stays blocked after the hint, its options are: keep trying, or force.
5. **Cost**: **−5 points per hint spent**, deducted once, at the moment of spending (the provisional score announced afterward already includes it). Stock at zero: no more hints; the referee says so at the next request and spends nothing.

## Forcing — never a dead block

1. **Automatic threshold**: after **4 counted failed attempts** on the current lock, the referee **offers** forcing in the thread: "This lock resists (4 attempts). You can force it: it will open, but it will score 0 points. To force: one player asks for the force and a second confirms. You can also keep trying." The team may refuse and continue; the referee re-offers forcing after each further batch of **2 failed attempts** (6, 8, 10…).
2. **Early forcing**: from **2 counted failed attempts** on the current lock, the team may ask for forcing without waiting for the referee's offer, under the same acceptance procedure. Before 2 attempts, a force request is refused ("this lock has not been tried yet"): a puzzle that has not been attempted is not skipped.
3. **Acceptance**: *group* — explicit request from one player + explicit confirmation from a **second** player, in the thread; without confirmation, nothing happens (the request alone has no effect and is not logged as a game event). *Solo* — the user decides alone. On the referee's **automatic offer** (point 1), acceptance follows the same procedure: one "let's force" + one confirmation.
4. **Effects**: the lock is marked `forced` in the state, scores **0 points**, and no additional penalty applies beyond the 0 (hints already spent stay deducted, that is all). The team moves to the next lock. **Chain element**: if the forced lock's solution is needed by the next lock (the case by construction of the chain), the referee then transmits it publicly **as a mechanism, not as an answer**: "By forcing the lock, you free the mechanism: engraved underneath, <element>." This transmission happens **after** the force decision, never before; it scores no points and is not a hint. If, exceptionally, a forced lock does not feed the next one, its solution stays sealed until the final recap.
5. **Forcing lock 5** is allowed under the same conditions: the game ends, the final grade mentions it ("door forced"), the score is computed normally.

## Score

- **Base**: 20 points per solved lock, i.e. **100 points** for the complete chain. A forced lock is worth **0**. A lock solved after a hint is still worth its 20 points — the hint cost is global, below.
- **Hint penalty**: **−5 points per hint spent** (maximum −15).
- **Formula**: `total = (20 × locks solved) − (5 × hints spent)`, with a **floor at 0** — no negative score, ever.
- Failed attempts cost nothing. There is no speed bonus, no first-attempt bonus, and no points invented mid-game.
- **Provisional score**: after each lock and each hint spending, the referee announces the score recomputed **from the state** (points of closed locks − penalty of hints already spent), never from memory.
- **Final grade**: the total out of 100, the list of forced locks if any, the number of hints used, and — if the game is timestamped (state with `started_at` / `finished_at`) — the **elapsed time**. Reading example: 4 locks solved (80), 2 hints (−10), 1 lock forced (0) → **70/100**.

## Abandon and resume

- **Resume**: on request ("resume", "let's continue"), the referee re-reads the most recent `in_progress` state and announces: the theme, the **current lock** (number and statement, re-read from the state), the **provisional score**, the **hints remaining**, and the number of **attempts already counted** on the current lock — **with no solution, no unspent hint text, no statement of locks to come**. The re-read state is the truth, not conversation memory. In group mode, this announcement is made in the thread, by a send approved under the generic mechanism.
- **Abandon**: on the user's request (solo) or the host's (group), the game becomes `abandoned`. In group mode, the referee publishes a short approved closing message. Solutions are revealed in the abandon recap only if the user or the host asks; otherwise they stay in the file.

## End of game and writings

1. **Final recap** (chat or thread, according to mode): final grade and its decomposition (points per lock, hint penalty), forced locks named, hints used, elapsed time if timestamped, and **revelation of all solutions** with, for each, the reasoning step that leads to it — the game is over, the secret no longer has a purpose.
2. **Writings**:
   - *Solo*: add an entry to `~/five-locks-escape/scores.json` (in the user's data folder):
     ```json
     { "date": "YYYY-MM-DD", "game_id": "<id>", "game": "five-locks-escape", "theme": "<theme>", "language": "fr | en", "score": 70, "locks": 5, "hints_used": 2, "forced_locks": [3], "test": false }
     ```
   - *Group*: **no** entry in `scores.json` (reserved to scored solo rounds); the result lives in the state: `status: "finished"`, `score.total`, `finished_at`, and the complete log.
   - Game state: `status` → `"finished"`, `finished_at` filled, last log event `game_finished` with the final score.

## State schema — `games/<game-id>.json`

`game-id`: `five-locks-escape-<YYYY-MM-DD>-<hhmm>` (prefix `TEST-` for a test game). The sealed key — solutions, variants, hints, chain links — exists from the file's creation, before the first game message.

```json
{
  "id": "five-locks-escape-2026-10-10-2100",
  "game": "five-locks-escape",
  "status": "in_progress | finished | abandoned",
  "mode": "solo | cooperative_group",
  "language": "fr | en",
  "theme": "<theme of the chain>",
  "created_at": "2026-10-10T21:00:00-04:00",
  "started_at": "2026-10-10T21:00:00-04:00",
  "finished_at": null,
  "config": {
    "platform": "<platform of the host group, or "chat" in solo>",
    "conversation": "<the user's host group, in group mode>",
    "host_mode": "player | spectator | null in solo",
    "players": ["<name>", "..."]
  },
  "current_lock": 1,
  "hints": { "total": 3, "remaining": 3, "spent": [ { "lock": 2, "by": "<name of the requesting player, in group mode>", "at": "…" } ] },
  "score": { "lock_points": 0, "hint_penalty": 0, "total": 0 },
  "locks": [
    {
      "number": 1,
      "title": "<public title of the lock>",
      "type": "logic | calculation | wordplay | observation of a described scene",
      "puzzle": "<complete public statement>",
      "solution": "<sealed solution>",
      "accepted_variants": ["<form>", "<form>"],
      "hint": "<sealed hint text>",
      "chain_link_to_next": { "type": "cryptographic keyword | orientation word (selection) | order code | reused code | untangling keyword", "description": "<how the solution serves the next lock>" },
      "status": "upcoming | current | solved | forced",
      "attempts": [ { "player": "<name or user>", "proposal": "<as normalized>", "at": "…" } ],
      "counted_attempts": 0,
      "points": null
    }
  ],
  "log": [ { "at": "…", "event": "game_created_key_sealed" } ]
}
```

- `chain_link_to_next` is `null` for lock 5. `points` is `null` until the lock is closed, then `20` (solved) or `0` (forced). `score` is recomputed and rewritten at every lock closing and every hint spending, from the locks' fields and `hints.spent` — never held "in the head".
- The log records every dated event: creation (key sealed), opening of each lock, every counted attempt (player + proposal), every hint spent, force offer and acceptance, chain-element transmission after a force, end of game. It is the proof of neutral refereeing, showable to the players after the game.

## The referee's work (reminder of the rules that protect the game)

1. **Sealed key, zero leak.** No solution — of the current lock or of later ones — appears in a message, a draft, or a recap before its resolution, its forcing (chain element only, after the decision), or the end of the game. Same neutral wording for every attempt (see Neutrality).
2. **The state is the truth.** File re-read at each turn, rewritten after every event. One file per game, held by the referee alone.
3. **The thread receives only public content** (in group mode): lock openings, verdicts, score announcements, force offers, recap. Everything goes through the host's approval under the generic mechanism; the referee sends nothing on its own initiative.
4. **No individual secret in this game**: no roles, no 1:1. If a player writes a proposal to the referee privately, the referee redirects them to the thread: a private proposal does not count — in cooperative play, the team plays open-book among its members.

## Edge cases (settled)

- **Two counted proposals almost simultaneous** (group): the referee processes them in the order of arrival in the thread, one at a time, rewriting the state between the two. If the first one solves the lock, the second targets an already-opened lock: not counted, handled by the "not the current lock" rule.
- **Correct answer drowned in a sentence** ("I'm sure it's X, otherwise Y"): ambiguous by construction (two answers) — the referee asks which one is the proposal; nothing is counted before the answer.
- **A player proposes while a hint has just been requested**: the order in the thread decides; the attempt is judged normally, the hint stays spent even if the attempt, arriving right after, solves the lock.
- **Hint requested while the stock is at zero**: net refusal, no spending possible, the referee restates the remaining options (try, or force if the conditions are met).
- **Force request without confirmation** (group): it expires at the end of the current game turn (change of lock or closing of the session); it does not "float" to the next lock.
- **Lock judged defective mid-game** (real ambiguity discovered, two defensible answers): the referee admits it, the lock is **cancelled**: it counts **20 points** (the failure is the referee's, not the team's), its chain element is transmitted as after a force, and the incident is logged and told to the players. Never a silent repair of the statement mid-game.
- **Player who no longer plays** (group): no mechanical effect — the game is cooperative, with no elimination; attempts, hints, and forces remain possible for the players present. Force confirmation always requires a second **present** player; if only one active player remains, the host may close the game or convert it to solo (logged).
- **Contest of a verdict or the score**: the referee republishes, from the state, the lock's logged attempts, the variant list, and the score decomposition. The file decides.
- **Resume after a requested abandon**: impossible — `abandoned` is terminal. A new game = a new state, a new chain.
