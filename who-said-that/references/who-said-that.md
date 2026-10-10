# Who Said That? — group game template

Runs on the generic mechanism in `references/group-messaging.md` (the user's connection, designated host group, host approvals, private messages in 1:1) — this document defines only the game's rules, its own protections, and the referee's work. The principle "guess who said this line" is a classic of party and board games; the rules below are written for this skill and adapted to asynchronous play.

## The game in one sentence

The referee draws real lines from the host group's history, anonymizes and cleans them, then publishes them one by one: each player privately guesses who wrote them. Attribution is revealed only once all the answers have been collected. The spice of the game: everyone knows these voices, nobody is sure of anything — and the author, who answers like everyone else, can muddy the trail.

## Players and round

| Parameter | Rule |
|---|---|
| Players | **3 to 8 consenting players** (recommended: 4 to 6). Below 3, guessing has no game left in it; above 8, the private collection gets heavy for the referee. Outside those bounds: the referee tells the host before the announcement and proposes waiting for more signups or launching another game. |
| Round | **5 quotes by default**; 3 = express, 8 = long, if the host asks. A round is played quote by quote, never as a block. |
| Consent | Signing up for the game is explicit consent to be quoted (cleaned quotes, drawn from the host group only) and to appear among the possible authors. The game announcement says so in plain words, before signups. |
| Host | The host picks their mode (**player** or **spectator**, see `group-messaging.md`, section b bis); the choice is recorded in the state (`config.host_mode`). |

## Protections — dedicated section, NON-NEGOTIABLE rules

This game quotes real words from real people. Its protections are neither optional nor negotiable mid-game; if one of them cannot be held, the game does not start (or the quote in question is discarded, or the round is cancelled — see Edge cases).

1. **Single source.** Quotes come **only from the history of the connected host group belonging to the skill's user**, the one designated in THEIR config (see `group-messaging.md`). Never another group, never another account, **never a 1:1 thread** — a line said in private never becomes a group quote.
2. **Possible authors = consenting players only.** A quote may be drawn only from a member who is a **consenting player in the current game**, and the proposed answers cover only those players. Someone who is not playing — a spectating group member, an absent member, or a former member — **is never quoted and never proposed as an answer**, even if their lines are in the history.
3. **Protective screening, before any publication.** At selection time, the referee **discards** any quote touching a sensitive topic, according to the list below. The discard happens **before** cleaning and **before** publication, it is **definitive** for the game, and it is **never justified** — not to the players, not in the thread, not to a playing host. Discarded quotes are **never shown** to anyone; in the state, the referee records only their number and a **generic category** (see the schema) — never their text.
4. **Mandatory cleaning.** No raw quote ever appears. Each kept quote goes through the cleaning procedure written below; if cleaning is not enough to make it safe, it is discarded as in point 3.
5. **Host review.** Each cleaned quote is **read by the host before publication**, as part of their usual send approval (`group-messaging.md`, rule d (3)) — that is the extra safety net: the host's human eye on every line, one by one. The host may veto a quote, without having to justify it in the thread; the referee draws another one or plays the round on the remaining quotes.
6. **Late reveal, always.** A quote's attribution is revealed only **after its collection closes** (all answers received or deadline passed). Before that moment: no confirmation, no denial, no hint, no differentiated reaction from the referee — in public and in private alike.
7. **Withdrawal of consent = immediate effect.** A player who withdraws stops being quoted at once: their not-yet-published quotes are pulled from the round's stock (see Edge cases).

### Sensitive topics list — systematic discard at screening

The referee discards any quote that touches, even indirectly, even as a joke, on:

- **Health**: illness, diagnosis, symptoms, medication, medical appointments, mental health, fatigue or distress expressed seriously;
- **Money**: debts, loans between members, salaries, prices paid that anger someone, financial difficulties, any amount that commits someone;
- **Conflicts between members**: reproaches, real disagreements, tensions, sarcasm aimed at a member, any line that would replay a dispute;
- **Private life**: family and intimate relationships, romantic situation, address, precise location, schedules that locate someone, identifiers of any kind;
- **Minors**: anything concerning an identifiable child — their school, their health, their activities, their reported words;
- **Confidential work**: non-public information about an employer, clients, files, named colleagues;
- **The rest of the prudent list**: grief, religion or intimate opinions, alcohol or substance use, personal legal or administrative proceedings, embarrassing remarks or mockery whose republication could wound.

In doubt between "harmless" and "sensitive": **discarded**. The game never runs out of harmless lines; it does not survive one line too many.

## Selection and cleaning — written procedure

Done by the referee, before launch, in this order:

1. **Draw frame.** The referee goes through the host group's history (and only that group's) and keeps as candidates only lines from the game's **consenting players**.
2. **Protective screening.** Each candidate is passed against the sensitive topics list above. Discarded = out of the stock, recorded in the state by generic category only.
3. **Cleaning** of each kept candidate, in this order:
   - **First names and proper names removed**: any first name or name of a person (player or not) is replaced by `[someone]` when the line stays natural, otherwise the mention is deleted. Identifying nicknames get the same treatment.
   - **Mentions and identifiers removed**: mentions (@…), addresses, phone numbers, emails, identifying links, precise place names when they identify someone.
   - **Bounded length**: at most **200 characters** and **2 sentences**. Beyond that: truncate at a clean sentence end, or discard if the truncation distorts the line or leaves a sensitive fragment.
   - **De-anonymization re-read**: the referee re-reads the result and asks "can a player identify someone *otherwise* than by style and by memory of the conversation?" (a unique detail, a context recognizable by a third party, a reference to a private event). If yes: clean further, or discard.
   - A cleaned quote that becomes incomprehensible or uninteresting is discarded too — the game comes first.
4. **Round stock.** The referee keeps the round's number of quotes (5 by default), ideally spread across the players with no announced guarantee (never promise "one quote per person": that would be an attribution hint). It may keep 1 to 2 replacement quotes, put through the same screening, cleaning, and review, for cancellations (see Edge cases).
5. **Sealed state.** The referee writes the **complete state into the game file immediately** — cleaned quotes, **each one's attribution**, internal source references — **before any publication** (see the schema). The original text lives only in the group history; the state contains only the cleaned version and the source reference, never an extra copy of sensitive or discarded originals.
6. **Host review** (protection 5): each cleaned quote is submitted to the host in their send approval before its publication. A vetoed quote goes back to the discarded stock, with no public justification.

### Announcement template — compliant example (adapt to the game's language)

- **Announcement**: "Who Said That? — new game! [N] consenting players: [NAMES]. A round of [N] quotes drawn from the history of THIS group, anonymized and cleaned. The possible authors are only the players. Answer the referee privately, one name per quote, before the announced deadline. The author answers too, like everyone else. Reveal only once all answers are received (or the deadline has passed)."

If the host plays: apply the host-player mode of `group-messaging.md` (section b bis) — the announcement then also carries its honest limit (protection of sends is procedural, not technical), and the previews submitted to a playing host **never contain the attribution**: quotes are shown to them cleaned and authorless, like to the players; the sealed state stays out of their view, in drafts as elsewhere (rule d (1) of the mechanism).

## How a round runs

For each quote, in stock order:

1. **Publication** (referee's message in the thread, approved by the host, quote reviewed — protection 5): the quote's number, its cleaned text in quotation marks, the instruction "who said that?", and the collection **deadline**. Nothing else: not the original's length, not its date, no context at all.
2. **Collection — answers in private, in 1:1 to the referee.** A settled choice, and its justification: in public, the first answer would influence all the following ones (copying, group effect) and the author could adjust their bluff in plain sight; in private and simultaneously, each player answers from their own memory alone, the collection stays sealed to the end, and the reveal keeps its effect. Debate and theories stay free in the thread — only the **ballot** (one player name) is deposited in private. A player may change their ballot until the deadline; only the last one counts. Silence at the deadline = **abstention** (0 points, counts neither for nor against).
3. **The author answers too — camouflage ballot (settled).** Recognizing their own quote is unavoidable for the author; the question was what to make of their ballot. Options rejected: forced abstention by the author (it would point them out — the only silent player on a quote would be suspect every round) and a self-attribution point (they know the answer, that would not be a game). Rule kept: **the author deposits a ballot like everyone else, which may name any player, including themselves; that ballot is called a "camouflage" ballot — it can never earn them an attribution point on their own quote.** The referee counts received ballots uniformly ("answers received: 3/4") without ever singling out the author's ballot before the reveal.
4. **Closure and reveal.** At the deadline — or as soon as all ballots are received — the referee closes the collection, **and only then** publishes in the thread: the attribution, the answer detail (ballot by player, camouflage labelled as such now that there is nothing left to protect), the quote's points, and the running scores. Before that publication, nothing: not in public, not in private to a curious player, not in a status to a playing host beyond the ballot count.
5. **End of round.** After the last quote: a final recap in the thread (final scores, winner, quotes nobody found), the result written into the state (and into the data's score history, per the skill's convention), state marked `finished`. A tie at the top: **co-winners**, no invented tiebreaker.

## Points — fixed scale, announced in advance

| Event | Points |
|---|---|
| Correct attribution (ballot of a **non-author** naming the author) | **+1** |
| Wrong attribution, abstention | 0 |
| Author's ballot on their own quote (camouflage), whatever its content | 0 (never a self-attribution point) |
| **Camouflage bonus**: no non-author found the author on this quote (abstentions count as "not found") **and** the author deposited their camouflage ballot | **+1 to the author** |

No negative points, no bonuses invented mid-round. The camouflage bonus rewards a line well disguised by the luck of the draw — and gives the author a reason to bluff rather than name themselves. A silent author (abstention) does not collect the bonus: you win nothing by not playing.

## The referee's work (reminder of the rules that protect the game)

1. **No leak, ever.** The same neutral wording for every quote and every player: never "that one is easy", never a different reaction depending on whether a theory in the thread is right or wrong. The referee comments neither on styles nor on memories raised in the debate.
2. **Screening is not discussed.** A player who asks why a given line never appears, or who requests a specific quote, gets the same answer: "the referee draws and screens according to the rules, with no comment on the discards." Never a confirmation that a specific line was discarded.
3. **Deadlines held.** Each publication announces its deadline. Nudges to the silent: in the thread, without detail ("answers are still missing for the current quote"), or in private to the player concerned, with no game element beyond the already-public quote.
4. **The state is the truth.** Re-read the file at every event, rewrite it after every event (selection, screening, publication, ballot received, closure, reveal, points). One file per game, kept by the referee alone. Attributions exist only there — and in the original history, which the referee does not copy.

## State schema — `games/<game-id>.json`

`game-id`: `who-said-that-<YYYY-MM-DD>-<hhmm>` (prefix `TEST-` for a test game). Same discipline as Werewolf: the **attributions are the sealed key**, written into the state **before the first publication**.

```json
{
  "id": "who-said-that-2026-10-10-2100",
  "game": "who-said-that",
  "status": "in_progress | finished | abandoned",
  "language": "en | fr",
  "created_at": "2026-10-10T21:00:00-04:00",
  "config": { "platform": "messenger", "conversation": "<the user's host group>", "host": "<host name>", "host_mode": "player | spectator", "source_history": "history of the designated host group only" },
  "parameters": { "quotes_per_round": 5, "points_correct_attribution": 1, "camouflage_bonus": 1, "quote_length_limit_characters": 200 },
  "players": [
    { "name": "<name in the group>", "consenting": true, "active": true, "points": 0 }
  ],
  "protective_screening": {
    "messages_examined": 0,
    "discarded": [ { "source_ref": "<internal reference of the message>", "category": "health | money | conflict | private_life | minors | confidential_work | other_sensitive" } ],
    "note": "Categories only: the text of a discarded quote is copied neither here, nor in the thread, nor anywhere."
  },
  "quotes": [
    {
      "number": 1,
      "source_ref": "<internal reference of the original message in the host group history>",
      "cleaned_text": "<the quote as published>",
      "cleaning": ["<operations applied: name_replaced, mention_removed, length_bounded…>"],
      "author": "<player name — SEALED KEY, written before publication>",
      "status": "pending | collecting | revealed | cancelled",
      "answers": { "<player name>": "<guessed name | null if abstention>" },
      "points_awarded": { "<player name>": 0 },
      "camouflage_bonus_awarded_to": null
    }
  ],
  "round": { "current_quote": null, "deadline": null },
  "winner": null,
  "log": [
    { "time": "2026-10-10T21:05:00-04:00", "event": "state_sealed_before_publication" }
  ]
}
```

- `source_ref` is an internal reference (position or identifier of the message in the host group's history): it lets the referee — and only the referee — find the original again for verification after the game; it is never published.
- The author's ballot is recorded in `answers` like the others, with its camouflage nature noted in the log at reveal time only — in the state, the referee's private file, it may be marked on receipt; it never is in a message.
- The log records every dated event: creation, screening (counts and categories only), cleaning, sealed state, host review, publications, ballots received (counts), closures, reveals, points, cancellations, end of game. It is the proof of neutral refereeing and applied protections, showable to the players after the game — purged of unrevealed attributions if the game is still in progress.

## Edge cases (settled)

- **Quote recognized by its author**: the normal case, provided for by the camouflage ballot (see How a round runs, point 3). The author may name themselves or bluff toward another player; in both cases, no attribution point for them on this quote, and the camouflage bonus stays possible if nobody else finds them and they deposited their ballot.
- **A player contests a quote as badly cleaned** (they recognize themselves as identifiable in it, or see an identifying or sensitive element that slipped through): the contest is made **in private to the referee**, never by debating the content in the thread. **Quote cancellation procedure**: (1) the referee **immediately suspends** collection of that quote; (2) it publishes in the thread a neutral message — "quote [N] is cancelled and replaced, with no points" — without repeating the element in question, without saying who contested or why; (3) the cancelled quote's attribution **is never revealed** (revealing it would aggravate exactly what the contest flags) and its status becomes `cancelled` in the state; (4) no point is awarded for that quote, to anyone (neither attribution nor bonus); (5) the round continues with a replacement quote (same screening, same cleaning, same host review) if the stock has one, otherwise it is played on the remaining quotes and the scores stand on that reduced total. If the contest arrives **after** the reveal: that quote's points are **withdrawn** retroactively, a neutral correction is published in the thread (without repeating the element in question), and the host decides whether the game continues.
- **Author who leaves the game mid-round** (withdrawal of consent, leaving the group, or the host's request): their **already revealed** quotes stay played and their points count (they were played in good faith, with the consent of the moment); their **not-yet-published** quotes are pulled from the stock and replaced if possible, otherwise the round gets shorter; their quotes **in collection** have their collection closed without reveal if no ballot has yet been publicly counted — otherwise (collection closed, reveal done) they stay counted as revealed. The player leaves the possible authors and the final standings (their points are archived in the state, not published); the other players keep being guessable normally. If the player count falls below 3, the round ends: recap on the revealed quotes, state `finished` with the reason noted in the log.
- **Final tie**: co-winners announced as such. No tiebreaker, no improvised "sudden death" quote — a full tiebreaker round may be proposed by the host, as a new game.
- **Player who stops answering**: abstention at each deadline. Two collections in a row without a ballot: the referee reports it to the host, who alone decides (the player stays, in continued abstentions, or withdraws — see the departure case above). The referee never removes a player on its own initiative.
- **The author confesses in the thread** ("that's me!") during collection: the referee neither confirms nor denies — the same neutral answer as for any thread theory. If the confession is credible enough to kill the quote (the thread agrees on it), the host may ask for its cancellation: same procedure as a contested quote, but the attribution is not revealed by the referee either way — the players keep their conviction, the referee keeps its rule.
- **Quote not found or insufficient history**: if screening and consents leave fewer quotes than the round asked for, the referee tells the host **before** the announcement (a numbered shortened round, or no game) — never any filling with lines from another group, a 1:1 thread, non-players, or invented lines. A quote invented by the referee is a refereeing fault, not a variant.
- **Publication error** (wrong quote, attribution revealed too early, message sent to the wrong thread): the game is compromised in the sense of `group-messaging.md`. The referee stops everything and says so frankly to the host in private; the host decides: cancel the affected quote and continue, restart the round with a new draw, or abandon. Never concealment.
- **Abandoned game** (the host ends it, or nobody plays anymore): status `abandoned`, a short end message in the thread (approved by the host). The attributions of unrevealed quotes **stay sealed** in the state, unless the host expressly asks for the complete recap — their group, their rules of the moment.
- **Counting dispute**: the referee republishes the answer and points detail exactly as it stands in the state (the detail becomes public at each reveal, by construction) and the round's log. The file settles it.
