# Exquisite Corpse, refereed — group game template

Runs on the generic mechanism in `references/group-messaging.md` (the user's connection, designated host group, host approvals, messages private in 1:1) — this document defines only the game's rules and the referee's work. Exquisite Corpse is a surrealist writing game, public domain in its principle; the rules below are rewritten and adapted to asynchronous play. No group, account, or proper name is hardcoded here.

## The game in one sentence

Players each write a piece of text **without ever seeing the others' pieces**: the referee (the assistant) collects each contribution in private, locks it into the game's sealed state, then publishes the assembled text all at once. The pleasure is entirely in the collision: pieces written blind that, put end to end, tell something nobody had planned.

## The two variants

One game can chain rounds of both variants; each round declares its variant in the state and in its announcement.

| | **Exquisite Corpse** | **Complete the Sentence** |
|---|---|---|
| Input | An optional **theme** (public) and an imposed segment schema | A **sentence opening** published in the thread (public) |
| What each player writes | **One single segment**, of the type assigned to them (e.g. the character, the action, the place, the ending) | **One complete ending** for the published opening — the same instruction for everyone |
| What the player sees | Their segment type and the theme. Never the others' segments, never their detailed types beyond their own | The opening (it is public). Never the others' endings |
| Assembly | The segments are put end to end **in schema order**, not in arrival order | No assembly: all endings are published side by side, attached to the same opening |
| Points | **None by default** — an atmosphere game (optional vote, see below) | **Vote option ON by default**: 1 point to the best ending (the host can disable it at the announcement, see below) |
| Players | 3 to 6 per round (one segment each) | 2 to 12 per round (one ending each) |
| Duration of a round | One collection + one publication | One collection + one publication (+ a vote if the option is active) |

## Common rules — the blind collection

These rules apply to both variants. They are the heart of the game: if the blind breaks, there is no game left.

1. **Contributions in 1:1 only.** Each player sends their contribution **in a private message to the referee**, never in the group thread. The referee publishes nothing of a round before its planned publication (see "Publication"). No contribution is read, quoted, summarized, counted aloud with its content, or even described ("someone wrote something very funny") before publication. Only **content-free statuses** are allowed: "contributions received: 3/4".
2. **One contribution per player per round.** Correction allowed before the deadline: the player sends a new version in the same private thread, the **last version received before the deadline** is the one that counts, and the state keeps the trace of the replacement (the two texts are never both published).
3. **One deadline per round**, set by the host at the announcement and repeated in every private request. The referee closes the collection at the deadline, or earlier if every expected contribution has been received. **Any contribution arriving after the close is refused**, politely, in private — even if publication has not happened yet: one exception would destroy the deadline for every later round.
4. **Bounded length, written in the private request.** Exquisite Corpse: **15 words at most per segment**. Complete the Sentence: **30 words at most, a single sentence**. A theme or an opening imposes no style: the absurd is welcome, it is the principle of the game.
   - Overlong contribution: the referee sends it back in private to its author, before the deadline, asking for a version within the bound ("too long: 15 words at most, send me a short version") — **the referee never shortens it themselves**. Still overlong at the deadline: it is set aside and counts as a missing segment / ending (see "Silent player").
5. **Content inappropriate for the group.** The referee may set aside a contribution they judge inappropriate for the host group (an insult aimed at a member, content plainly outside the group's limits). Sober procedure, no sermon: (1) the contribution is not published; (2) its author is told in private in one neutral sentence ("your contribution was set aside: it does not suit this group. The round continues without it."); (3) if the deadline has not passed, the author may offer another; (4) the round continues, the set-aside contribution counts as missing. No public explanation, no detailed justification, no penalty point — the game has no tribunal.
6. **Silent player — settled: the referee NEVER fills in.** At the deadline, a contribution not received (or set aside) stays missing:
   - *Exquisite Corpse*: the text is published **with the missing segment signalled in its place**, between brackets — e.g. `[missing ending — contribution not received]`. The referee does not invent the segment, does not ask another player to double it, and does not delay publication to wait for a substitute: the gap is part of the result, and is often its funniest part.
   - *Complete the Sentence*: the missing ending is simply absent from the publication, and the number of endings received is stated as-is ("3 endings received out of 4"). The round takes place only if **at least 2 endings** are received; below that, the round is postponed (new deadline announced by the host) or cancelled, and recorded as such in the state.
7. **The state is the truth.** Each contribution is written into the state file **the moment it is received** (that is the sealed contribution: text + author + moment, field `published: false`), before any publication. The referee re-reads the state before every send and rewrites it after every event, as for every group game in this skill.

## Variant 1 — Exquisite Corpse

### Segment schemas

The schema depends on the round's player count. The schema's order is the assembly order, always.

| Players | Segments, in order |
|---|---|
| 3 | `[character]` `[action]` `[ending]` |
| 4 (default) | `[character]` `[action]` `[place]` `[ending]` |
| 5 | `[character]` `[action]` `[place]` `[moment]` `[ending]` |
| 6 | `[character]` `[action]` `[companion or object]` `[place]` `[moment]` `[ending]` |

Reading the types: `[character]` = a noun phrase as subject ("a captain in yellow boots"); `[action]` = a verb phrase starting with a verb ("decided to repaint the storm"); `[place]` = a place complement ("on the harbour quay"); `[moment]` = a time complement ("one stormy evening"); `[companion or object]` = a noun phrase introduced by "with" ("with a sleeping parrot"); `[ending]` = the end of the sentence, a last piece that closes it, preferably unexpected ("and since then, nobody dares whistle on the harbour."). These grammatical notes are part of each type's private request: they are what makes the assembly readable despite the blind.

### How a round runs

1. **Announcement** (in the thread, message approved by the host per the mechanism): the variant, the optional theme, the number of players, the collection deadline. The announcement contains **no segment** and does not name who holds which type — the assignment is private.
2. **Assignment** — The referee draws one segment type per player at random, writes the complete assignment in the state (sealed) **before any send**, then sends each player, **in 1:1**, a request containing only: the theme (if any), **their** segment type with its grammatical note, the length bound and the deadline. Nothing else: neither the other detailed types nor — obviously — any segment already received.
   - *Host-player mode* (see `group-messaging.md`, section b bis): the segment request is a secret message; its template — with a `[SEGMENT TYPE]` slot and its variable grammatical note — is approved **once** by the host before the first send. Since the grammatical note changes with the type, the approved template contains the list of possible notes, one per type; the referee fills only the type slot and the matching note, and never shows the filled requests to the host-player. Only statuses come back to them ("assignments sent", "contributions received: 3/4").
3. **Collection** — Per the common rules. Private acknowledgement, identical everywhere: "Received." — no comment, no different tone depending on the segment.
4. **Assembly** — At the close, the referee assembles the texts **word for word** in schema order: joining the segments with a space, capitalizing the first letter, and ensuring the final punctuation. **Nothing else is corrected**: no grammar, no agreement, no word. A missing segment is replaced in its place by the bracketed marker of common rule 6; if the marker lands in final position, the received sentence is closed with a period before the marker — the marker is the referee's signal, not a piece of the sentence. The assembly is written in the state (`assembled_text`) before publication.
5. **Publication** (in the thread, message approved by the host): the complete assembled text, then — the round has no vote by default — **the attribution of the segments**: each type with its author's name, the missing segment named as such included. That is the end of the blind for this round: everything becomes public at once, segments and authors.
6. **Vote option — "best ending" (off by default).** If the host activates it **at the round's announcement** (never after collection): the publication gives the assembled text **without attribution**, each segment labelled by its type only. The players then vote (see "Voting" below) for the `[ending]` segment — a single segment is in competition, which is what keeps the vote readable. The winner scores 1 point; the complete attribution (every author) is revealed at the vote's close, at the same time as the result. If no ending was received, the vote does not take place and the round stays pointless.

## Variant 2 — Complete the Sentence

### How a round runs

1. **Announcement and opening** (in the thread, message approved by the host): the variant, **the sentence opening, published as-is**, the collection deadline, and whether the vote is active (yes by default). The opening is public information — it is the shared instruction, there is nothing to hide. Example opening: "When the bell rang at midnight, everyone understood that…". A good opening is open (several very different endings must be possible), grammatically welcoming (it ends so that an ending hooks onto it directly) and has no "right" answer: it is not a question.
2. **Private requests** — The referee sends each player, **in 1:1**, a reminder of the opening, the length bound and the deadline. This request contains no ending — at this stage the referee has received none, and will go on showing none: each player writes their ending knowing only the opening.
   - *Host-player mode*: the request is identical for every player and contains no secret proper to its recipient; the ordinary exact preview is enough, including for the host-player, who receives the same request as the others and answers in their own private thread.
3. **Collection** — Per the common rules. Endings arrive in 1:1, are sealed in the state on receipt, and are never shown to anyone before publication — not even as a word count or a hint.
4. **Publication** — At the close, the referee publishes in the thread, in a single message: the opening repeated, then every ending received.
   - **Vote active (default)**: endings are published **anonymous**, labelled with a letter (A, B, C…), in an **order shuffled** by the referee (draw recorded in the state's log — the publication order must be neither the signup order nor the arrival order, which would let authors be guessed). No author's name appears.
   - **Vote disabled by the host at the announcement**: endings are published **signed**, in signup order, and the round ends there — no points.
5. **Vote (if active)** — See the "Voting" section below. At its close: result, revelation of every ending's author, points.

## Voting — rules common to both variants

- **Who votes**: the round's players, each **one vote**. A spectator host does not vote; a host-player votes like the others.
- **How**: the vote is sent **in private (1:1) to the referee** before the vote deadline announced at publication (a short window: a few hours, set at publication). Private votes, not in the thread: a visible vote anchors the following ones, exactly like a visible contribution. At the close, the referee publishes the **tally per letter / per segment**, never the detail of who voted for what.
- **No self-vote**: a player cannot vote for their own contribution. A self-vote received is invalid: the referee says so in private to its author, who may vote again for another contribution before the deadline; with no new vote by the deadline, the player is counted as abstaining. The referee knows the authors (they are in the sealed state) — that control is precisely why publication anonymity does not apply to them.
- **Points**: the winning contribution scores **1 point** for its author. **Tie at the top: shared point** — each tied author scores 1 point, announced as such, with no tiebreak and no replayed round. Points accumulate in the state from round to round within the same game; there are no negative points.
- After the vote closes, **every author is revealed** — anonymity serves only an honest vote, it is not meant to last.

## End of game

After the last planned round (or on the host's decision): the referee publishes a short recap — the assembled texts / the openings and winning endings of the rounds played, and the points standings **only if at least one round had a vote** (a game of pure Exquisite Corpse with no vote has neither winner nor standings, and the recap simply says so). State marked `finished`, result recorded in the log. No writing into `scores.json`: as for the other group games, the result lives in the game's state.

## State schema — `games/<game-id>.json`

`game-id`: `exquisite-corpse-<YYYY-MM-DD>-<hhmm>` (prefix `TEST-` for a test game). One single schema for both variants; each round declares its own. The contributions are the sealed key: they exist in this file from the moment they are received, with `published: false`, and become public only at their round's publication. (French source folder and field names: `etats/<partie-id>.json`, e.g. `manches`, `echeance_collecte`, `texte_assemble`.)

```json
{
  "id": "exquisite-corpse-2026-10-10-2100",
  "game": "exquisite-corpse",
  "status": "in_progress | finished | abandoned",
  "language": "fr | en",
  "created_at": "2026-10-10T21:00:00-04:00",
  "config": { "platform": "messenger", "conversation": "<the user's host group>", "host": "<host name>", "host_mode": "player | spectator" },
  "players": [
    { "name": "<player name>", "score": 0 }
  ],
  "rounds": [
    {
      "number": 1,
      "variant": "exquisite-corpse | complete-the-sentence",
      "theme": "<optional theme, or null>",
      "opening": "<published opening, complete-the-sentence only, otherwise null>",
      "segment_schema": ["character", "action", "place", "ending"],
      "vote_active": false,
      "collection_deadline": "2026-10-10T23:00:00-04:00",
      "vote_deadline": null,
      "contributions": {
        "<player name>": {
          "segment_type": "character | action | place | moment | companion-or-object | ending | sentence-ending",
          "text": "<sealed text, or null if missing>",
          "status": "received | silent | set_aside_length | set_aside_content | refused_late",
          "received_at": null,
          "label": "<anonymous publication letter, active vote only, otherwise null>",
          "published": false
        }
      },
      "assembled_text": null,
      "votes": { "<voter name>": "<voted label>" },
      "points": { "<player name>": 0 },
      "status": "collection | published | vote | finished | cancelled"
    }
  ],
  "winners": null,
  "log": [
    { "time": "2026-10-10T21:00:00-04:00", "event": "game_created" }
  ]
}
```

- `segment_schema` serves Exquisite Corpse only; `opening` serves Complete the Sentence only. Both are written when the round opens, before the first private request.
- In Exquisite Corpse, the **type assignment** (which player holds which segment) is written in `contributions.<player>.segment_type` at the moment of the draw, with `text: null` and a pending status — the assignment is therefore sealed before the sends, and filling in the text never changes the type.
- `label` is assigned at the close of collection, in the shuffled publication order; before the close, it is `null` for everyone — the arrival order must never leak through.
- The log records every dated event: creation, announcement, assignments sent (statuses, no detail shown to the host-player), contributions received (statuses), any set-aside and its sober ground, close, assembly, publication, votes received (statuses), result, end. It is the proof of neutral refereeing and of a respected blind, showable to the players after the game.

## Edge cases (settled)

- **Contribution sent in the public thread by mistake.** It counts, and the round continues — cancelling would punish everyone for one clumsiness. But the blind is dented for that contribution: (1) the referee neither comments on it nor confirms anything about it in the thread; (2) they privately remind the players who have not yet contributed to write **their** piece, without leaning on the leaked one; (3) the incident is honestly mentioned in the publication message ("one contribution was posted in the thread by mistake before the close; it counts, the others were collected in private") and recorded in the log. In Exquisite Corpse, if a segment leaked, the remaining segments are not reassigned. If the host judges the round spoiled (e.g. the ending published right at the opening), **the host alone** may ask for its cancellation before publication; the referee never cancels it on their own initiative on this ground.
- **Contribution of the wrong type** (a `[place]` received for an `[action]`, an ending that does not hook onto the opening): the referee sends it back in private before the deadline, naming the expected type, without showing any other text; the player rewrites. Still the wrong type at the deadline: it counts as missing. The referee never reclassifies a text themselves — a segment never changes place in the assembly.
- **Tie at the vote**: shared point (see "Voting"). No second round: the game is light, a tie is a result, not a problem.
- **Vote with no votes at all** (nobody votes by the vote deadline): no points, authors revealed anyway, round `finished`. The referee says so as-is, with no after-the-fact nudge.
- **Fewer players than the schema mid-game** (a player withdraws after the assignment): their segment becomes missing at the deadline, silent-player rule; no replacement mid-round. Between rounds, the host may adjust the schema to the real number of players.
- **Private send error** (a contribution or an assignment gone to the wrong recipient, revealing a sealed text): the round's blind is compromised. The referee stops the round, says so frankly to the host in private, and the host decides: restart the round (new assignment / new opening) or continue knowingly. Never concealment (see also `group-messaging.md`, standing rule 4).
- **Abandoned game** (the host ends it, or nobody contributes anymore): status `abandoned`, a short closing message in the thread (approved by the host). The contributions of unpublished rounds **stay sealed** — they were never promised to the public and are not revealed in the closing message, unless the host expressly asks; rounds already published remain acquired in the state.
- **Dispute** (assembly, tally, attribution of a point): the referee republishes the texts and the tally **as they are in the state** — texts sealed on receipt, labels, votes. The file settles it: an assembly is redone aloud from `contributions`, in `segment_schema` order, never from conversation memory.

## Message templates (adapt to the language of the game)

- **Announcement, Exquisite Corpse**: "Exquisite Corpse — round [N]. Theme: [THEME, OR "free"]. [NUMBER] players, one segment each, in private. You will receive your segment type by private message; send your segment **in private to the referee** before [DEADLINE]. Do not put it in the thread: nobody will see the other segments before the complete text is published."
- **Private segment request**: "Exquisite Corpse — round [N]. Theme: [THEME]. Your segment: [SEGMENT TYPE] — [THE TYPE'S GRAMMATICAL NOTE]. [BOUND: 15 WORDS AT MOST]. Send it in private here before [DEADLINE]. You will not see the other segments: that is the game." (Host-player mode: template approved once, see Variant 1, step 2.)
- **Announcement and opening, Complete the Sentence**: "Complete the Sentence — round [N]. Here is the opening, to complete in private: "[OPENING]" Each person sends their ending **in private to the referee** before [DEADLINE] (30 words at most, one sentence). All endings will be published together [VOTE VERSION: anonymously, then you will vote for the best one / NO-VOTE VERSION: with your names]."
- **Private ending request**: "Complete the Sentence — round [N]. Opening: "[OPENING]" Send your ending in private here before [DEADLINE] (30 words at most, one sentence). Do not put it in the thread."
- **Private acknowledgement** (both variants): "Received." (nothing else — no comment on the text.)
- **Publication, Exquisite Corpse**: "Exquisite Corpse — round [N], the complete text: "[ASSEMBLED TEXT, MISSING SEGMENT SIGNALLED BETWEEN BRACKETS IF ANY]" [NO VOTE: Segments: [TYPE] — [AUTHOR]; … / WITH VOTE: vote in private for the best ending before [VOTE DEADLINE].]"
- **Publication, Complete the Sentence (vote active)**: "Complete the Sentence — round [N]. "[OPENING]" Your endings: A — [ENDING]; B — [ENDING]; … Vote in private for the letter of the best ending before [VOTE DEADLINE] (not for your own). The authors will be revealed at the close."
- **Vote result**: "Round [N] — result: [LABEL] wins ([TALLY PER LABEL]). Point for [AUTHOR(S)]. The endings were: A — [AUTHOR]; B — [AUTHOR]; … Scores: [CUMULATIVE SCORES]."
