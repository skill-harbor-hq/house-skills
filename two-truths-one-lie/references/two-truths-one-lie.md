# Two Truths, One Lie — rotating featured player (group game)

Group game template for this skill. It runs on the generic mechanism in `references/group-messaging.md` (the user's connection, designated host group, host approvals, secrets in 1:1) — this document defines only the game's rules and the referee's work. No group, account, or real name is hardcoded here. The "two truths, one lie" principle is a classic icebreaker game in the public domain as a principle; the rules below are written for this skill and adapted to asynchronous play by messaging.

## The game in one sentence

In turn, one group member is the **featured player**: they privately give the referee three statements about themselves — **two true and one false**. The referee publishes the three statements, in a shuffled order, without saying which one is the lie. The other players each vote for the statement they believe is false. At the deadline, the referee reveals the lie: the players who found it score, and the featured player scores for each player they fooled, within the cap in the scoring scale below. Then the next featured player takes their turn.

The pleasure of the game: learning true (and surprising) things about the others, and discovering who can bluff with plausible details.

## Players, duration, rotation

- **Minimum 3 players** (1 featured player + 2 voters), **recommended 4 to 8**. Above 8, turns get longer and votes get diluted: the referee tells the host before the announcement and proposes splitting the game or waiting.
- **One game = one complete cycle**: every registered player is featured **exactly once**, in the order of the **rotation queue** (see below). The host may decide at the announcement on a shorter game (a number of turns fixed in advance); the decision is written into the state before the first turn and never changes during the game.
- **Rotation queue**: the order of featured players is the order in which players registered, recorded in the state (`rotation_queue`) from the launch. It changes only through the "skipped turn" procedure (see Edge cases) — never by preference of the referee or of a player during a cycle. The queue and the scores live in the state and persist there from one turn to the next: a game can stretch over several days, one turn per deadline, without losing anything.
- **Default deadlines** (the host may adjust them at the announcement, they are then written into the state): collection of the featured player's statements, **24 hours** after their private request; voting, **12 hours** after publication of the statements. The referee may close a phase earlier if everything expected has been received.
- The host plays or referees as a spectator according to the mode chosen at the announcement (see `group-messaging.md`, section b bis); if they play, they are a player like the others: featured in their turn in the queue, voting on the others' turns.

## The referee's work — overview of a turn

A complete turn always follows the same order, without exception:

1. **Collection in 1:1** — the referee privately asks the featured player; they give their 3 statements **and designate, in the same private message, which one is the lie**.
2. **Quality gate** — the referee checks the 3 statements (see the gate below) and may request **one** adjustment, privately, before any publication.
3. **Sealed key** — the referee writes into the state, **before any publication**, the final statements, the shuffled publication order, and the identity of the lie (the key). From that moment, the key never leaves the file until the reveal.
4. **Publication** — the referee publishes the 3 numbered statements in the thread, in the shuffled order, with no marker.
5. **Votes in 1:1** — each other player votes privately for one number. No vote is visible before the reveal.
6. **Reveal and points** — at the deadline, the referee publishes the lie, the detail of the votes, and the turn's points, updates the scores in the state, then opens the next featured player's turn.

## Step 1 — Collecting the statements (privately, always)

1. The referee sends the featured player, **in 1:1**, the collection instruction (template below): 3 short statements about themselves, 2 true, 1 false, with the deadline. If the host plays, this secret message follows the host-player mode of the mechanism: template approved once by the host before its first send, filled version never shown to the host — and when the host is themselves the featured player, they receive and fill in the instruction in 1:1 like any other player.
2. The featured player replies **in that same private thread**: their 3 statements, **and they explicitly indicate which of the three is the lie**. Without that designation, the collection is incomplete: the referee asks for it privately, once, before the deadline.
3. No other player ever sees the collection. Unpublished statements (drafts, a statement replaced at the gate) circulate nowhere: not in the thread, not in a preview intended for the playing host, not in a recap.

## Step 2 — Quality gate (written, applied before the seal)

The referee checks the 3 statements, one by one. A statement that fails a **blocking** criterion is never published as is.

### Criteria

- [ ] **Plausible, all three** — each statement, true or false, must be believable to someone who knows the featured player a little. An absurd lie ("I have walked on the Moon") or an implausible truth with no supporting detail ruins the turn: the lie must be the most **ordinary** of the three, not the most spectacular.
- [ ] **Comparable difficulty** — the 3 statements are in the same register of precision (concrete details of the same density: a place, a period, a number, when there is one). A vague statement next to two very detailed ones points to the culprit by its form, not by its content.
- [ ] **Verifiable in principle by the featured player** — a fact, an event, an observable habit: the featured player must be able, if a player contests it after the reveal, to recount the true fact or acknowledge the false one without evasion. Pure tastes, opinions, and feelings ("I hate such-and-such a dish", "I love such-and-such a season") are **unverifiable** and are set aside: nobody can be right or wrong about them, the vote becomes a lottery.
- [ ] **No sensitive statement** — same hygiene as the other games in this skill family: health, money and personal finances, intimate life, family or professional conflicts, identities or situations of third parties, anything that would make the featured player or someone else uncomfortable once published is **set aside**. The lie and the truths are subject to the same rule: a false sensitive statement is still a sensitive statement published in the thread.
- [ ] **Self-contained and short** — each statement fits in one or two sentences, is understood without context, and names no other player (a statement that involves a third party puts them in a position to confirm or deny: see the honour rule below).

### The referee's power of adjustment

- The referee may ask the featured player to adjust **one** statement per turn: the one that is **too obvious** (the lie that gives itself away, or the truth the whole group already knows) or **unverifiable** in the sense of the gate. The request is made **privately, in the collection thread**, naming the statement by its text or its rank **in the collection** — the featured player knows which one is their lie; the referee does not need to know it to formulate the request, and never comments on it.
- **The referee never reveals or notes in public, at any moment, which statement is the lie** — not in the adjustment request, not in a message to the host, not in the log of a recap shown to the players before the end of the game. The adjustment request states only the gate reason (too obvious, unverifiable, sensitive, difficulty not comparable), never a judgement on the truth of the statement.
- **Blocking or advisory**: sensitive or unverifiable = **blocking** — no publication until the statement is replaced; if the replacement does not arrive within the extended deadline granted by the referee (by default 12 hours), the turn is skipped (see Edge cases). Too obvious or difficulty not comparable = **advisory** — the referee asks once; if the featured player keeps their statement, the referee publishes it as is: that is the featured player's points risk, not a fault.
- The replaced statement is **not kept** in the state: only the final text enters it. The state log records the event ("gate adjustment, collection statement no. 2, reason: unverifiable"), without copying the discarded text and without its nature (true or false).

## Step 3 — Sealed key and publication

1. Once the gate is passed, the referee **shuffles the order** of the 3 statements (draw recorded in the log: the published order must owe nothing to the collection order — otherwise the collection rank would become a clue over games) and writes **immediately** into the state: the final statements, their publication order numbered 1-2-3, and the key (`published_number_of_the_lie`). **That is the seal: it takes place before the publication message, never after.**
2. The referee publishes in the thread (message approved by the host under the mechanism — public content, ordinary approval, even if the host plays: this message contains nothing secret):
   - the name of the turn's featured player and the turn number in the cycle;
   - the 3 statements, numbered, in the shuffled order;
   - the voting instruction (privately to the referee, a single number) and the deadline.
3. From publication on, **no further modification** of the statements or of the key. A material error by the referee (truncated text, a changed word that alters the meaning) follows the publication-error procedure in Edge cases — never a silent correction.

## Step 4 — Votes

- **Who votes**: all registered players **except the turn's featured player**. The featured player does not vote on their own turn, not even "for fun": their ballot would distort the count of the fooled.
- **How**: **privately, in 1:1 to the referee**, a single number (1, 2, or 3) — the statement the voter believes is the lie. A short reason is welcome but optional; the referee never comments on it before the reveal (neither "interesting", nor any different tone depending on whether the vote is right or wrong).
- **Why private**: a visible vote anchors the following ones (people follow the first voter instead of judging the statements). The simultaneous reveal of all votes is part of the game. The referee may announce in the thread a bare status ("votes received: 2/3"), never a content.
- **Changing a vote**: allowed until the deadline; only the last ballot received counts, the state keeps a trace of the replacement.
- **Silence at the deadline = abstention**: no point possible for the voter, and the abstention counts **neither as a fooled vote nor as a correct vote** for the featured player's scale (see below).
- The referee acknowledges each vote privately with a bare status ("received").

## Step 5 — Reveal and points

At the deadline (or as soon as all expected votes are received), the referee, **from the state**:

1. Re-reads the sealed key and the recorded votes; recounts the turn's points according to the scale.
2. Publishes in the thread, in a single message: the number and text of the lie; the detail of the votes (who voted what, abstentions named as abstentions); the turn's points (guessers, featured player); the game's cumulative standings.
3. Updates the state (turn `revealed`, points, player scores, log) **before** asking the next featured player.
4. The featured player may then, if they wish, recount their two truths in the thread — that is the social moment of the game, never an obligation, and the referee never recounts in their place.

## Scoring scale (settled, written before the game, never changed during a cycle)

- **Correct guesser** (vote = number of the lie): **+1 point**. Every correct guesser scores, whatever the number of correct guessers.
- **Fooled guesser** (vote = number of a true statement): **0 points**.
- **Featured player**: **+1 point per fooled voter**, **capped at 2 points per turn**. Justification for the cap: without it, a single perfect-bluff turn would be worth more than the rest of the cycle combined (with 7 voters, 7 points against 1 point per correct answer elsewhere); with it, the featured player has the best possible gain in the game (2) without being able to win the game on a single turn. The cap is the same for every featured player, whatever the size of the group.
- **Abstention** (silence, or abstention declared under the honour rule): 0 points to the voter, and **earns the featured player nothing** — one is "fooled" only by voting for a true statement; not playing is not falling for it.
- **Skipped or cancelled turn**: no points, for anyone.
- **End of game**: the player or players at the top of the final standings are **co-winners** in case of a tie — no improvised tiebreaker (neither "more successful featured turns", nor "registered first"). The host may ask for a complete additional cycle, which is a new game announced as such, scores reset to zero in a new state.

### Why there is no "tie of votes" to settle

Each vote is **individual**: there is neither collective elimination nor a candidate in the sense of a group vote. That two statements receive the same number of votes, or that the votes split 1-1-1, changes nothing — the lie is the one in the sealed key, each correct ballot scores its point, each false ballot counts one fooled voter for the featured player. The only "tie" that exists in this game is a tie **in the standings**, handled above (co-winners).

## Honour rule — knowing the truth in advance

It happens that a player already **knows**, outside the game, that a statement is true or false: they were there, the featured player had told them, they lived the episode together. Playing that knowledge as an "intuition" distorts the turn for everyone. The rule, stated at the game's announcement:

1. A player who recognizes with certainty the truth or falsity of a statement in the turn **declares it privately to the referee before voting** (one message is enough: "I know about statement 2"). They **abstain** on this turn.
2. The declared abstention is recorded in the state (`declared_abstentions`) and announced at the reveal as an ordinary abstention, **without a reason**: the thread will never know who abstained by silence and who by honour.
3. Declaration **after voting but before the reveal**: the ballot is withdrawn, it scores nothing and earns the featured player nothing; the incident is recorded in the log.
4. Knowledge discovered **after the reveal**: the turn's points stand (a public reveal is not rewritten), the referee records it in the log and privately reminds the player of the rule. In case of repetition, the host alone decides what follows (the player may be removed from following cycles — never by the referee on their own initiative).
5. Corollary for the featured player: do not build a statement on an episode that **the whole group** lived together — that is no longer bluff, it is a collective-memory quiz, and the gate will treat it as "too obvious".

## State schema — `games/<game-id>.json`

`game-id`: `two-truths-<YYYY-MM-DD>-<hhmm>` (prefix `TEST-` for a test game). Same discipline as the other games: the key (which published statement is the lie) is written into the state **before each publication**.

```json
{
  "id": "two-truths-2026-10-10-2100",
  "game": "two-truths-one-lie",
  "status": "in_progress | finished | abandoned",
  "language": "fr | en",
  "created_at": "2026-10-10T21:00:00-04:00",
  "config": { "platform": "messenger", "conversation": "<the user's host group>", "host": "<host name>", "host_mode": "player | spectator" },
  "scale": { "correct_guesser": 1, "featured_per_fooled": 1, "featured_cap_per_turn": 2 },
  "deadlines": { "collection_hours": 24, "vote_hours": 12 },
  "players": [
    { "name": "<player name>", "score": 0 }
  ],
  "rotation_queue": ["<featured 1>", "<featured 2>", "..."],
  "current_turn": 1,
  "turns": [
    {
      "number": 1,
      "featured": "<featured player name>",
      "status": "collection | gate | sealed | published | votes | revealed | skipped | cancelled",
      "collection_deadline": "2026-10-11T21:00:00-04:00",
      "vote_deadline": null,
      "final_statements": [
        { "collection_rank": 1, "text": "<final statement>", "nature": "truth | lie", "adjusted_at_gate": false }
      ],
      "publication_order": [2, 3, 1],
      "published_statements": [
        { "number": 1, "text": "<published statement>", "is_lie": false }
      ],
      "key": { "published_number_of_the_lie": 1 },
      "votes": { "<voter name>": 1 },
      "abstentions": ["<name>"],
      "declared_abstentions": ["<name>"],
      "points": { "guessers": { "<name>": 1 }, "featured": 0, "fooled": 0 },
      "sealed_at": "2026-10-10T22:05:00-04:00",
      "published_at": null,
      "revealed_at": null
    }
  ],
  "winners": null,
  "log": [
    { "moment": "2026-10-10T21:00:00-04:00", "event": "game_created_rotation_queue_frozen" }
  ]
}
```

- The turn's **key** = `key.published_number_of_the_lie` (doubled, for checking, by the `is_lie` field of `published_statements`). The two writings must always agree; in case of a divergence noticed before the reveal, the referee follows the "compromised game" conduct of the mechanism (they stop the turn, tell the host, the host decides) — never a silent choice of one over the other.
- `final_statements` contains only the **final** texts, after the gate: a statement replaced at the gate leaves there only the trace `adjusted_at_gate: true` on its replacement and a log event with a generic reason — never the discarded text, never its nature.
- `sealed_at` must be **earlier** than `published_at` for each turn; that order, readable in the state, is the proof of the seal.
- `rotation_queue` is frozen at creation; the skipped-turn procedure moves the defaulting featured player there to the end of the queue (the event is logged, the original queue remains reconstructible from the log).
- The `players` scores are the sum of the points of the `revealed` turns; they are recounted from the turns' `points`, never from memory.
- The log records each dated event: creation and frozen queue, collection request, collection received, gate adjustment (generic reason only), seal, publication, votes received (statuses), abstentions and declared abstentions, reveal and points, skipped or cancelled turn, end of game. It is the proof of neutral refereeing, showable to the players after the game — provided that, as long as a turn is not revealed, only the events of already-revealed turns are shown from it.

## Edge cases (settled)

- **Featured player who does not provide their statements by the deadline** (or incomplete collection: statements without designation of the lie, blocking gate replacement not provided within the extended deadline granted):
  1. A private reminder goes out at mid-deadline ("you have until [time] for your three statements"), with no detail in the thread.
  2. Deadline passed: the turn is **skipped**. The referee announces in the thread, in neutral terms and without a reason: "the turn of [featured] is postponed, we move to the next featured player." No statement, even partial, is published.
  3. The defaulting featured player is moved **to the end of the queue of the current cycle**, once only. If they default a second time in the same cycle, their turn is **lost for this cycle** (removed from the queue, event logged); they remain a voter on the other turns.
  4. No points are awarded for a skipped turn; the cycle continues. If the queue empties before the end of the cycle (several turns lost), the game ends on the turns played and the standings as they stand.
- **Tie of votes on a turn**: not applicable — each vote scores or not, individually (see Scoring scale). Tie **in the final standings**: co-winners.
- **Player who knows the truth in advance**: honour rule above (private declaration, abstention, no public reason).
- **The featured player reveals their lie in the thread during the vote** (joke, clumsiness, or provocation): the turn is **cancelled** — the key is public before its time, no vote can be honest any more. No points. The referee publishes a neutral cancellation message (approved by the host), records the incident, and the featured player may be placed back at the end of the queue with **entirely new** statements if the host so decides; it is never automatic.
- **Late vote** (after the deadline, before the reveal): refused, politely, privately. The deadline is what makes the simultaneous reveal possible.
- **A voter publishes their vote in the thread by mistake**: unlike estimation games, the error here is **recoverable without distorting the turn** if it is caught in time — procedure: (1) the referee confirms nothing in the thread; (2) they privately ask the voter for a **new private ballot**, reminding them that their first choice is public and that they vote in full knowledge; the final private ballot alone counts; (3) the incident is mentioned honestly at the reveal ("a vote was visible in the thread before the reveal; its author re-voted privately") and logged. If the host judges the turn distorted (e.g. the published vote argued at length and steered the debate), **the host alone** may ask for the turn to be cancelled before the reveal.
- **Referee publication error** (text of a statement altered to the point of changing its meaning, wrong order announced in the state): voting is **suspended immediately**, the referee publishes the complete correct version (approved), reopens a full voting deadline, and privately asks voters already received to **confirm or change** their ballot on the corrected version. The incident and the republication are logged; the key, however, never changes.
- **Contestation after the reveal** (the featured player denies that a "true" statement is true, a voter contests the count): the referee republishes the detail of the votes and the points as they are in the state — the file settles the count. For the truth of the statements: it is the featured player's word that was sealed at collection; if the featured player acknowledges having been mistaken about one of their "true" statements, the turn is **cancelled retroactively** (the turn's points withdrawn from everyone, standings recalculated, event logged and announced in the thread); if they maintain it, the turn stands.
- **Player who no longer responds at all** (neither featured nor voter): abstention at each deadline. If they miss two turns in a row, the referee reports it to the host, who alone decides on their removal from the rotation queue (their remaining featured turns are removed, their acquired points stay in the standings with the mention "removed", announced in the thread without further detail). The referee never removes a player on their own initiative.
- **Abandoned game** (the host ends it, or nobody plays any more): status `abandoned`, short closing message in the thread (approved by the host); the keys of unrevealed turns **are not revealed** in that message, unless the host expressly asks for it; acquired scores stay in the state.

## Writings

1. **During the game**: the state is re-read at the start of each phase and rewritten after each event (collection, gate, seal, publication, each vote, reveal, skipped turn) — one file per game, kept by the referee alone.
2. **End of game (cycle finished)**: the referee publishes the complete final standings (scores, successful featured turns, number of lies found per player), fills in `winners` in the state, and marks the status `finished`.
3. **No entry in `scores.json`**: that file stays dedicated to scored solo rounds; the result of a group game lives in the game's state (`status`, player scores, `winners`, log), as for the other group games. No entry either in the question library: this game asks no question from the referee, it consumes only the players' statements, which are never reused.

## Message templates (adapt to the game's language)

- **Game announcement**: "Two Truths, One Lie — rotating featured player. Every player will be featured once, in this order: [ROTATION QUEUE]. When it is your turn, you will privately give the referee 3 statements about yourself: 2 true, 1 false. The others will vote, privately, for the one they believe is false. Correct guesser: +1. Featured player: +1 per fooled player, capped at 2 per turn. Honour rule: if you already KNOW that a statement is true or false because you were there or you were told it, tell the referee privately and abstain on this turn — without saying why in the thread. Deadlines: collection 24 h, vote 12 h."
- **Collection instruction (private, to the featured player)**: "Two Truths, One Lie — it is your turn as featured player. Send me here, privately, 3 short statements about yourself: 2 true, 1 false, and tell me which one is the false one. Plausible, roughly as detailed as each other, nothing sensitive (health, money, intimate life, conflicts) and nothing that cannot be verified in principle: no tastes or opinions. Deadline: [DEADLINE]. If a statement does not pass the gate, I will ask you for another one right here — nothing will be published before that." — if the host plays, this template is approved once by the host before its first send (host-player mode), the filled version of each featured player is never shown to them.
- **Collection acknowledgement (private)**: "Received. I will check and come back to you here if a statement needs adjusting; otherwise, publication in the thread at the planned time."
- **Gate adjustment request (private)**: "Two Truths, One Lie — one adjustment before publication. Statement no. [RANK IN THE COLLECTION] ("[START OF THE STATEMENT]…"): [REASON: unverifiable / sensitive / too obvious / less detailed than the other two]. Can you replace it with a statement in the same register? Nothing is published in the meantime."
- **Publication (thread)**: "Turn [N] — featured: [NAME]. Their three statements: 1) [STATEMENT] 2) [STATEMENT] 3) [STATEMENT]. Two are true, one is false. Vote privately to the referee: the number you believe is false, before [DEADLINE]. [NAME] does not vote on this turn."
- **Vote acknowledgement (private)**: "Received for turn [N]." (nothing else — no comment on the choice.)
- **Reveal (thread)**: "Turn [N] — reveal. The lie of [FEATURED] was no. [NUMBER]: "[STATEMENT]". Your votes: [NAME] → [NUMBER] (found / fooled); …; abstentions: [NAMES OR "none"]. Points for the turn: [GUESSERS] +1; [FEATURED] +[POINTS] ([NUMBER] fooled, cap 2). Standings: [CUMULATIVE SCORES]."
- **Skipped turn (thread)**: "Turn [N] — the turn of [FEATURED] is postponed; we move to the next featured player: [NAME]."
