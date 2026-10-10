# Caption Contest with blind voting — group game template

Reference for this skill. It is played through the generic mechanism in `references/group-messaging.md` (the user's connection, a host group designated by the user, host approvals, private 1:1 messages) — this document defines only the rules of the game and the referee's work. No group, account, or real name is hardcoded anywhere. The principle — write the funniest caption for a photo, then vote blind — is a party-game classic; the rules below are written for this skill and adapted to asynchronous play.

## The game in one sentence

A photo is shared in the group. Each player sends **their caption in private to the referee**, before the deadline. The referee publishes all captions **anonymized and shuffled**, with no name attached. The group votes — never for its own caption — then the referee reveals the author of the winning caption and the points in the standings. The fun of the game: laugh at the texts first, discover who wrote them afterwards — in fact, nobody signed them.

## Players and game

| Parameter | Rule |
|---|---|
| Players | **4 to 8 registered players** (recommended: 4 to 6). Below 4, the minimum of publishable captions (3, see below) becomes too fragile — one silence and the round collapses — and voting, deprived of the self-vote, turns on too few ballots. Above 8, private collection and publication become heavy. Out of bounds: the referee tells the host before the announcement and proposes waiting for signups or launching another game. |
| Rounds | **3 photos per game, by default**; 1 = express, 5 = long, if the host asks. One round = one photo, one collection, one publication, one vote, one revelation. Rounds are played one at a time, never in parallel. |
| Host | The host chooses their mode (**player** or **spectator**, see `group-messaging.md`, section b bis); the choice is recorded in the state (`config.host_mode`). If they play, they send their caption and vote like everyone else, in private. |
| Language | The host group's language, as the host defines it in the config or at the announcement. |

## The photo — admitted sources, and only those

Each round has exactly one photo, chosen **before** collection opens, from one of these two sources — never a third:

1. **Provided by the host.** The host transmits the photo to the referee (or designates it in their collection). Written conditions: (a) it is a photo the host has the right to share in their group; (b) it shows no person in a sensitive or embarrassing situation, and no identifiable minor without their parent's agreement — the contest laughs at a situation, never at a person behind their back; (c) the referee republishes it **under a neutral filename and without metadata** (EXIF, geolocation, original name): a filename like `family-photo-march.jpg` or a geolocation are clues about the source, and sometimes about a future caption's author.
2. **Generated or chosen by the assistant, at the host's request.** The host approves the exact image before its publication, like every send under the mechanism (preview + confirmation). A generated image is announced as such if it could pass for a real photograph of a real person — otherwise, no special mention: the group captions what it sees.

Forbidden as a source: a photo taken from a player's thread without their agreement for this game (a player who wants to propose a photo transmits it to the host, who then becomes the provider in the sense of point 1 — the chain stays clear, and no player is "the source" in the group's eyes during the game); a screenshot of a private conversation; an image whose origin the referee does not know.

**Round opening.** The referee publishes in the thread (a host-approved message): the photo, the round number, the **collection deadline**, the **voting mode of the round** (see Vote — chosen at the announcement, never changed afterwards), the maximum length of a caption, and the reminder of the three rules players confuse most: caption **in private to the referee**, **never in the thread**; **forbidden to vote for your own caption**; a caption that lets its author be identified will be **sent back for rewording** (see Collection, point 3).

## Collection of captions — in private, one per player

1. **Sent in 1:1 to the referee, before the deadline, and only there.** A caption received in the public thread is not a caption "in advance": it is burned (see Edge cases — caption published in the thread). The referee acknowledges receipt privately with a bare status ("received for round [N]"), with no comment on the text — neither "funny", nor a different tone depending on the caption. Public statuses allowed during collection: counts only ("captions received: 3/5"), never content, never a name associated with a receipt or a delay.
2. **One caption per player per round.** Maximum length: **200 characters, 2 sentences at most**, announced at the opening. A player may replace their caption with a new private message **before the deadline**: the last version received in time is authoritative, earlier ones are discarded and never published (the state keeps the trace of the replacement, not of the discarded texts — see the schema). After the deadline: no receipt, no replacement (see Edge cases — late caption).
3. **Anonymity check at receipt — the rewording procedure.** At receipt, before retaining a caption, the referee re-reads it with a single question: **"does this text let its author be identified by anything other than style or humour?"** What betrays an author includes:
   - a proper name, a first name, a nickname, a signature ("signed X", "as X would say" about oneself);
   - a reference to a private fact or an event that only the author can know or claim ("my dog", "at my place", "the photo I sent you");
   - any identifier (claimed initials, a player's habitual emoji-signature presented as a signature, a language or detail the group would mechanically associate with one single person and that the player slipped in as a signed wink).

   Style, on the other hand, is **not** a reason to send a caption back: writing "like so-and-so" is the game itself — authors are guessed by their humour, that is intended; they are not identified by a signature, that is forbidden.

   **Procedure, in order, always before the deadline:** (1) the referee returns the caption to its author **in private**, naming the **category** of the problem ("the caption contains a proper name / an identifying private reference") — no debate, no replacement text suggested; (2) the author may send a reworded version **before the same collection deadline** (no individual extension: extending for one player would reveal that a player had a problem); (3) the reworded version goes through the same check; if it passes, it is retained as the player's caption, and the initial version is **never published, never quoted, and its text is not kept in the state** — the state records only the category of the reason and the fact of the rewording (see the schema); (4) if no acceptable version arrives before the deadline — no rewording, or a rewording that still identifies — the player is **without a caption for this round**: they may still vote (for the others), they cannot score the round's author points. In the thread, nothing ever signals that a rewording took place: publication shows only the retained captions, and the number of published captions is never publicly compared with the number of players.
4. **Closing the collection.** At the deadline, collection closes. The referee counts the **retained** captions (acceptable, on time):
   - **3 retained captions or more**: the round continues to publication.
   - **Fewer than 3 retained captions**: the round **is not published** (see Edge cases — too few captions). Publishing 2 captions would be a duel where anonymity is illusory and the vote almost forced.

## Anonymization and shuffling — the referee's work before publication

This is the step that makes or breaks the game. It is done entirely in the state, **before** any publication message:

1. **Public codes.** The referee assigns each retained caption a neutral code — **L1, L2, L3…** — in a **random order**, with no relation to reception order, the alphabetical order of authors, or the order of players in the config. The draw and the retained order are recorded in the state's log.
2. **State sealed before publication.** The complete **code → author → text** table is written into the state file **before** the publication message (see the schema, fields `submissions` and `publication_order`). It is the key of the round: from that moment, the referee can no longer reorder, touch up a text, or "forget" a caption. Any draft shown to the host for approval contains only the texts under their codes — never the author table; if the host plays, it is the same rule as the mechanism's host-player mode: statuses and anonymized texts only.
3. **Presentation normalization — and nothing else.** Texts are published **exactly as written** by their authors (spelling, punctuation, humour intact — correcting a text is already signing it or distorting it), under uniform presentation: same prefix ("**L2** —"), same typography, no emoji or formatting carried over from a player's private message, uniform quotation marks added by the referee if the publication template uses them. Normalization is about the packaging, never the words.
4. **No ordering clue.** The referee never comments on a caption at publication ("this one will please you") and does not react differently depending on codes during the vote. The same neutral wording for all, from the first message to the count.

## Publication and vote

### Publication

The referee publishes the captions in the thread, all at once, as soon as collection has closed and the state is sealed:

- **Written-vote mode** (see below): a single message lists all captions under their codes, in code order.
- **Reaction-vote mode**: **one separate message per caption**, each containing only its code and its text — a reaction attaches to a message, not to a line of a list; publishing the list in a single message would make reaction voting impossible to count. The messages follow each other immediately, in code order, with no comment between them, then a final short message announces the opening of the vote and its deadline.

The vote-opening message recalls: the deadline, the voting mode of the round, the ban on self-voting and its exact regime depending on the mode (next point — the referee **says** it, they do not leave it to be guessed), and that authors are revealed only after counting.

### The vote — two modes, only one chosen per round, announced at the opening

The mode is chosen by the host **before the round opens**, written into the state (`vote_mode`), and it no longer changes for this round.

| | **Written vote in private (1:1)** — reference mode | **Reaction vote** — only if the platform really allows it |
|---|---|---|
| How to vote | Each player sends the referee in private the **code** of their favourite caption (e.g. "L3"), before the vote deadline. One ballot per player. | Each player places **one reaction** (the one announced at the opening, e.g. 👍) on the message of the chosen caption, before the vote deadline. One reaction-vote per player. |
| Changing your mind | Yes, until the deadline: the last private ballot counts, the state keeps the trace of the change. | Yes, until the deadline: remove the old reaction and place the new one. At the deadline, the referee records the state of reactions as it is — a player who leaves two reaction-votes has an **invalid** ballot (see Edge cases). |
| **Self-vote** | **Controllable, and controlled.** The referee knows the code → author table: a ballot naming the voter's own caption is **discarded**. The referee tells the voter **in private** ("ballot discarded: self-vote") and the voter may file another ballot **before the deadline**; with no new ballot at the deadline, they are an abstainer for this round. The discard is recorded in the state (`discarded_votes`), never announced in the thread with a name. | **Not reliably controllable — honour rule, stated as such.** Depending on the platform, the referee does not always see who placed which reaction, and therefore cannot guarantee discarding self-votes. The rule announced at the opening is therefore: "reaction vote = do not vote for your own caption, on honour; the referee will discard any self-vote they can actually detect, but cannot promise to detect them all." A self-vote detected after counting but before revelation follows the same rule as in written mode (discarded, recount); detected after revelation, it is recorded in the log and reported to the host — the round's points are not silently rewritten, the host decides. |
| Who may vote | Registered players of the game, including those with no retained caption in this round. Spectators and non-players do not vote: in written mode, the referee ignores their ballots; in reaction mode, their reactions are counted only if the referee can identify them as non-players — a limit of the mode, announced with it. | Same, with the limit written on the left. |
| Silence | Abstention: 0, counts neither for nor against. | Same. |

**Counting.** At the deadline, the referee counts **from the state** (written ballots recorded as they arrived; a dated record of reactions for reaction mode), discards self-votes and invalid ballots according to the mode, and obtains a number of **valid votes per code**. This count — detail per code, discarded ballots counted without names — is published in the thread with the revelation (see below). No partial result, no "L2 is leading" during the vote: the referee publishes nothing between the opening and the closing of the vote, apart from a neutral deadline reminder.

### Tie at the vote — settled tie-break

If there is a tie for first place between two or more captions after counting valid votes:

1. **Tie-break round, between the tied captions only.** The referee announces it in the thread (codes concerned, no author), with a **short deadline** set at the announcement (e.g. 2 hours, or the end of the game's day — never an open deadline).
2. **Who votes in the tie-break: only players who are authors of none of the tied captions.** Settled reason: a tied author cannot vote for their own caption and would therefore, facing a single opponent, have only a forced choice — their ballot would say nothing, and with two tied captions, the two authors would mechanically neutralize each other. Neutral players, on the other hand, really decide. The referee determines the eligible voters from the sealed state, and invites them **in private, one by one**, without ever telling the others who is neutral or why a given player is not invited (being invited or not would reveal who is not an author of a tied caption — the invitation therefore stays invisible in the thread; in the thread, the announcement says only "tie-break in progress, ballots in private").
3. **Mode of the tie-break: written vote in private, always** — even if the round was played in reactions. This is the round where the self-vote must be controllable without exception, and the number of voters is small: private costs nothing.
4. **Result of the tie-break:** the caption that receives the most valid votes there **wins the round**. The other finalist(s) of the tie-break take the finalist place in the round's standings (see Points).
5. **Persistent tie at the tie-break** (neutral ballots split, or no neutral ballot received by the deadline, or no neutral voter available — a possible case when all players are authors of a tied caption): **no third round, no draw** — breaking a humour tie at random would be false refereeing. The tied captions are **co-winners of the round**: each receives the co-winner points (see Points), and all are revealed as such.

## Revelation and points

### Revelation — after counting only

Once the vote is closed, discards made, and any tie-break finished, the referee publishes in the thread, in a single message:

- the **count per code** (valid votes for each caption, discarded ballots counted without names, the tie-break result if there was one);
- the **winning code and its author's name** — this is the central revelation of the round;
- the **authors of all the other captions**, code by code. Settled justification: the round is over, the vote is closed, there is nothing left to protect — and revealing all authors feeds the conversation ("that was you, L4?") that makes the pleasure of the game and the group's memory for the following rounds. What is **never** revealed, even at the end: the text of a discarded caption (identifying and not reworded, published in the thread, or late) and the identity of a player whose caption was discarded for an anonymity reason, linked to that reason (the revelation says "[Name] had no retained caption in this round" only if the player consents or if the fact is already public — otherwise, the revelation speaks only of the published captions, and the count of players without a caption stays an internal status);
- the **points of the round** and the **cumulative standings** of the game.

Before this message: no confirmation, no denial, no hint about an author — in public as in private, including to a playing host beyond the statuses provided by the mechanism.

### Points — fixed grid, announced in advance

| Event | Points |
|---|---|
| **Winning** caption of the round (most valid votes, or winner of the tie-break) | **+2 to its author** |
| **Finalist** caption: distinct second place at the count, or loser of a played tie-break | **+1 to its author** |
| **Co-winning** captions (persistent tie after the tie-break, see above) | **+1 to each tied author** (and no distinct finalist point on this round: the co-winners together occupy first place) |
| Any other published caption; player with no retained caption; abstention at the vote | 0 |

Settled precisions:

- The finalist point goes to the caption that came second **in the final result of the round**: after a won tie-break, the finalist is the caption beaten in the tie-break (the tie-break brings together only the captions tied for first; a caption outside the tie had strictly fewer votes and cannot claim that place). If, without a tie-break, two captions are tied for **second** place: each receives the finalist point (+1) — the grid rewards the place reached, not a podium forced to a single name.
- **No points for voters.** Voting right (having chosen the winner) earns nothing: the game rewards writing, not forecasting, and vote points would turn the vote into a calculation ("vote for the weak caption to protect mine") instead of a judgement of humour.
- No negative points, no bonuses invented mid-game (neither "shortest caption", nor a bonused "unanimous vote"): the grid above, announced at the opening of the game, is the only one.
- **Standings and end of game.** After the last round, the referee publishes the complete final standings (points of all players, rounds won by each). Tie at the top of the final standings: **co-champions**, announced as such — no improvised tie-break; the host may ask for an extra round, which is then a complete normal round (new photo), announced before being played.

## The referee's work (reminder of the rules that protect the game)

1. **No leak, ever.** The code → author table exists only in the state. The same neutrality for every code, in public as in private: never a comment on a specific caption before revelation, never a differentiated reaction depending on the real author.
2. **Deadlines kept.** Each opening (collection, vote, tie-break) announces its deadline. Reminders to the silent: in the thread, in counts only ("captions / ballots are still missing"), or in private to the player concerned, with no additional game element.
3. **The state is authoritative.** Re-read the file at every event, rewrite it after every event (caption received, rewording requested and received, collection closed, state sealed, publication, ballot received, self-vote discarded, count, tie-break, revelation, points). One file per game, kept by the referee alone. In case of a dispute, recount from the state — never from a memory of conversation.
4. **The host can stop everything** (mechanism, rule d (6)): game `abandoned`, short approved closing message; the authors of captions not yet revealed stay sealed in the state, unless the host expressly asks to publish the complete recap.

## State schema — `games/<game-id>.json`

`game-id`: `caption-contest-<YYYY-MM-DD>-<hhmm>` (prefix `TEST-` for a test game). Same discipline as the other group games: **the code → author table of each round is the sealed key of that round, written into the file before the publication message of that round.**

```json
{
  "id": "caption-contest-2026-10-10-2100",
  "game": "caption-contest",
  "status": "in_progress | finished | abandoned",
  "language": "fr | en",
  "created_at": "2026-10-10T21:00:00-04:00",
  "config": { "platform": "messenger", "conversation": "<the user's host group>", "host": "<host name>", "host_mode": "player | spectator" },
  "parameters": { "rounds_per_game": 3, "min_captions_publication": 3, "max_length_characters": 200, "points_winner": 2, "points_finalist": 1, "points_co_winner": 1 },
  "players": [
    { "name": "<name in the group>", "score": 0, "rounds_won": 0 }
  ],
  "current_round": 1,
  "rounds": [
    {
      "number": 1,
      "photo": { "source": "host | assistant", "internal_reference": "<neutral filename or internal reference, never published with metadata>", "internal_description": "<short factual description, for the referee only — in simulation, it is the substitute for the image>" },
      "vote_mode": "written_private | reactions",
      "collection_deadline": "2026-10-10T22:00:00-04:00",
      "vote_deadline": null,
      "status": "collection | sealed | published | vote | tie_break | revealed | postponed | cancelled",
      "submissions": {
        "<player name>": {
          "status": "received | rewording_requested | retained | no_caption | refused_late | burned_thread",
          "rewording_reason": null,
          "retained_text": "<text exactly as published, or null if no caption retained>",
          "public_code": "L1 | null"
        }
      },
      "publication_order": ["L1", "L2", "L3"],
      "authors_by_code": { "L1": "<player name — SEALED KEY, written before publication>" },
      "votes": { "<voter name>": "<code voted, last valid ballot>" },
      "discarded_votes": [ { "voter": "<name>", "code": "<code>", "reason": "self_vote | invalid_ballot | non_player" } ],
      "count": { "L1": 0 },
      "tie_break": null,
      "winning_code": null,
      "winning_author": null,
      "points_awarded": { "<player name>": 0 }
    }
  ],
  "winners": null,
  "log": [
    { "time": "2026-10-10T21:00:00-04:00", "event": "game_created" }
  ]
}
```

- `rewording_reason` contains only a **generic category** (`proper_name`, `private_reference`, `signature`, `identifier`) — never the offending passage nor the text of the discarded version. Same rule for a refused or burned caption: status and category only, no text kept apart from the retained and published text.
- `tie_break`, when it takes place, takes the form: `{ "codes": ["L1", "L2"], "neutral_voters": ["<name>"], "deadline": "<ISO>", "votes": { "<name>": "<code>" }, "winning_code": "<code | null if persistent tie>", "persistent_tie": false }`.
- `winners`: the list of names tied on score at the top at the end of the game (a single name if there is a unique winner); `null` while the game is not finished.
- The log records every dated event: creation, round opening (photo, voting mode, deadlines), captions received (counts and statuses — texts live only in `retained_text`), rewording requested (category only), collection closed and its count, draw of the order and **state sealed before publication**, publication, ballots received (counts), self-votes discarded (counts in public, detail in the state), count, tie-break and its result, revelation, points, postponement or cancellation of a round, end of game. It is the proof of neutral refereeing, showable to the players after the game — purged of authors not yet revealed if the game is in progress.

## End-of-game writings

1. **Game state**: `status` → `"finished"`, final player scores, `winners` filled, log closed by the end event. That is where the result lives.
2. **`scores.json` of the data: no entry.** As for the other group games of the skill, this file stays dedicated to scored solo rounds; the standings of a contest live in the game's state.
3. **No library to feed**: there is neither a question nor an answer to archive against repetition. The same photo can be replayed in another game — they will be other captions, other authors, another vote. The referee simply avoids re-proposing the previous round's photo in the same game, as game common sense, not as an archive rule.

## Edge cases (settled)

- **Late caption** (received after the collection deadline, before or after publication): **refused**, politely, in private ("received after the deadline, it cannot enter the round"). No exception: accepting a latecomer would destroy the equality of collection for all following rounds and, after publication, anonymity (a caption added after the fact would be identifiable as "the latecomer's" in the eyes of anyone who followed the counts). The refusal is recorded in the log (status `refused_late`, without text). If the lateness brings the retained captions below the minimum, the "too few captions" case applies, not a grace for the latecomer.
- **Identifying caption — rewording before the deadline only.** Complete procedure at Collection, point 3. Two settled precisions: (a) if the initial version is identifying but its author no longer materially has time to reword before the deadline (message received at the last minute), the rule does not change — no individual extension, the player is without a caption for the round and may vote; (b) the referee **never** signals publicly, during or after the round, that a specific player had to reword; in the log and in the state, generic category only, without the discarded text.
- **Tie at the vote**: tie-break between the tied captions only, neutral voters only, written private vote always, short deadline — complete procedure at the Vote section. Persistent tie: co-winners at +1 each, no third round, no draw.
- **Too few captions (fewer than 3 retained at closing)**: the round is **not published**. Procedure: (1) the referee announces in the thread, with no name or content: "not enough captions received for this round — it is postponed"; (2) **single postponement**: a new collection deadline is announced for the **same photo** (e.g. the next day, at the time set by the host); captions already retained **stay retained and sealed** for the postponement (their authors do not have to resend them, and they cannot replace them during the postponement except by asking the referee before the new deadline — same replacement rule as in ordinary collection); players without a caption may send one by the new deadline; (3) if, at the postponement, the minimum is still not reached: the round is **cancelled**, the photo is withdrawn from the game, and the captions retained for it are **never published** (publishing them outside a vote, or in a later round, would break their anonymity, which has become guessable by elimination); the game continues on the remaining rounds, or ends if it was the last one — the standings then hold on the rounds played. No points are awarded for a postponed or cancelled round.
- **Caption published in the public thread by its author (by mistake or by bravado).** Settled: the caption is **burned** for this round. It cannot enter the anonymized publication (the whole group saw it in fact signed by the message carrying it), nor is it counted as "published" in the sense of the minimum of 3 captions. Procedure: (1) the referee confirms nothing in the thread beyond what is necessary — a neutral message: "reminder: captions are played in private with the referee" — without naming or quoting the text; (2) the author may send **another** caption, different, in private before the deadline: it follows ordinary collection, anonymity check included (if the new caption refers to the one in the thread, it is identifying by reference and goes to rewording); (3) the incident is recorded in the log (status `burned_thread`, without text). If the author sends nothing back, they are without a caption for the round and may vote.
- **Self-vote.** In written mode: discarded, voter notified in private, new ballot possible before the deadline (see the modes table). In reaction mode: honour rule announced, discarding of every self-vote actually detected, no promise of complete detection — the referee settles it by **saying** so, never by pretending a control they do not have. A player who repeats it over several rounds: the referee reports it to the host in private; the host alone decides on a follow-up (a reminder in the group, without naming a specific ballot).
- **Invalid ballot at the vote** (nonexistent code, two codes in a single written ballot without correction before the deadline, two reaction-votes left simultaneously in reaction mode at the deadline): invalid, it counts for nobody. In written mode, the referee asks for a clarification in private if the deadline has not passed; without clarification at the deadline, invalid and recorded (`invalid_ballot`). No ballot is ever forcibly interpreted ("they surely meant L3") after the deadline.
- **Player who no longer responds** (neither caption, nor vote): abstention at each phase, with no points penalty. Two rounds in a row without any participation: the referee reports it to the host, who alone decides (the player stays, in continuous abstentions, or withdraws from the game — their already-revealed captions and already-scored points stay acquired in the state and in the standings published so far; they leave the following rounds). The referee never removes a player on their own initiative.
- **Photo contested after opening** (a player reports that the photo represents them, or someone close to them, in a situation they do not want captioned): the contestation is made in private to the referee or to the host. The host decides: if the photo is withdrawn, the round is **cancelled** (same regime as cancellation for too few captions: captions received are never published), another photo may open a replacement round. The referee never debates the reason in the thread; the public message is neutral: "the round is cancelled and replaced".
- **Abandoned game** (the host ends it, or nobody participates any more): status `abandoned`, short closing message in the thread (approved by the host). The authors of rounds already revealed stay public (they were); the tables of unrevealed rounds stay sealed in the state, unless the host asks for the complete recap — their group, their rules of the moment.
- **Dispute of a count**: the referee republishes the count as it is in the state — detail of valid votes per code (public since revelation), number of ballots discarded by reason, and, for written mode, the detail of ballots **per voter** if the disputant is the host or if the dispute concerns their own ballot; the code → author table of the round, already revealed, lets everyone verify the discarded self-votes. The file decides.

## Message templates (to adapt to the language of the game)

- **Game announcement**: "Caption Contest — new game! [N] players: [NAMES]. [N] rounds, one photo per round. For each photo: send your caption **in private to the referee** before the announced deadline (200 characters max, 2 sentences max). Captions will be published anonymous and shuffled; you will then vote, **without ever voting for your own**. The winning author of each round is revealed after the vote. Grid: winner +2, finalist +1."
- **Round opening**: "Round [N]/[TOTAL] — here is the photo. Captions in private to the referee before [COLLECTION DEADLINE]. Vote of the round: [MODE — "written, in private" OR "by reactions 👍 on the message of each caption"]. Never put your caption in the thread."
- **Private acknowledgement of receipt**: "Caption received for round [N]." (nothing else — no comment on the text.)
- **Private rewording request**: "Your caption for round [N] cannot be retained as it stands: it contains [CATEGORY: a proper name / an identifying private reference / a signature]. Send me another version before [COLLECTION DEADLINE] if you want to play this round. The original will be neither published nor kept."
- **Publication (written mode)**: "Round [N] — the captions, anonymous and shuffled: **L1** — "[TEXT]"; **L2** — "[TEXT]"; **L3** — "[TEXT]". Vote in private with the referee: the code of your favourite, before [VOTE DEADLINE]. Forbidden to vote for your own caption: in written mode, the referee discards self-votes."
- **Publication (reaction mode), per caption then opening**: "**L[N]** — "[TEXT]"" then, after the last one: "Round [N] — vote open: place a 👍 on THE message of your favourite caption, before [VOTE DEADLINE]. One reaction-vote per person. Forbidden to vote for your own caption — in reaction mode, it is an honour rule: the referee will discard what they can detect, without being able to promise to detect everything."
- **Tie-break announcement (thread)**: "Round [N] — tie for first place between [CODES]. Tie-break in progress: written ballots in private with the referee, before [SHORT DEADLINE]. Authors are still not revealed."
- **Revelation**: "Round [N] — results. Valid votes: [CODE]: [N]; … ([N] discarded ballot(s): [REASONS COUNTED, WITHOUT NAMES]). [TIE-BREAK, IF PLAYED: "Tie-break: [CODE] wins [N]–[M]."] **Winner: [CODE] — "[TEXT]", by [AUTHOR] (+2).** Finalist: [CODE], by [AUTHOR] (+1). All captions: [CODE] — [AUTHOR]; … Standings: [CUMULATIVE SCORES]."
