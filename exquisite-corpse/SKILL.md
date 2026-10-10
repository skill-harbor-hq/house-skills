---
name: "exquisite-corpse"
description: "Run an Exquisite Corpse group game refereed by the assistant inside the user's own connected messaging group (Messenger first): each player writes one segment of a text in private, blind, without ever seeing the others' segments, the referee collects the segments in 1:1, assembles them word for word and publishes the complete text at once, and a silent player's segment stays a marked gap that the referee never fills in. Includes the Complete the Sentence variant, where every player privately writes an ending for one public opening and the endings are published together, with an anonymous vote for the best ending and no self-vote. Use when the user wants an exquisite corpse game, a cadavre exquis, a complete the sentence game, a compléter la phrase, a blind writing game, a partie de groupe, or a group writing game with their group."
---

# Exquisite Corpse — a blind collective writing game for your group chat

Your assistant referees a game of Exquisite Corpse inside a group chat **the user owns and connects**. Each player writes **one segment of a text without ever seeing the others' segments**: the referee collects every contribution **in private, in 1:1**, seals it in the game state, then publishes the assembled text **all at once**. The fun is entirely in the collision: pieces written blind that, put end to end, tell something nobody had planned.

The blind is the game, and it is proved by the mechanic, not promised: contributions travel only in 1:1, nothing about a round is read, quoted, summarized, or even hinted at before publication, and the only statuses anyone ever sees are content-free ("contributions received: 3/4"). A player who stays silent leaves a **gap, marked as such in the published text**: the referee **never** writes, completes, or fixes a segment in anyone's place. The referee's own public messages (announcement, publication, results) are host-approved like every send (see `references/group-messaging.md`).

Two variants share the same blind collection (full rules in `references/exquisite-corpse.md`): **Exquisite Corpse** (3 to 6 players, one imposed segment type each, segments assembled in schema order, no points by default, an optional "best ending" vote) and **Complete the Sentence** (2 to 12 players, one public opening, one private ending each, endings published side by side, the vote for the best ending active by default). The game is asynchronous on purpose: one collection deadline per round, fixed by the host, and the text appears only when the collection closes.

## What you need

- A Muse assistant (this skill installed).
- **To actually play**: a messaging account **the user connects to their own assistant** and one group conversation on it that the user designates as the game host. Messenger is the first supported connection; the model is platform-generic (see `references/group-messaging.md`, platform variants). Installing the skill files needs nothing else.
- The assistant writes in the group **from the user's account** (that is how the connection works), and every public message needs the host's approval before it is sent. The complete assembled text in particular is published **only after the host approves it**. There is no fully automatic mode, and there never will be: the host approves, then it goes.

## Data layer (the skill ships none of it)

All game data lives in a data folder **the user owns**, never inside the skill. On first use, create it with the user (suggested default: `~/exquisite-corpse/`, any folder the user prefers works):

- `config.json` — the host configuration: platform, designated conversation, host name, host mode, player list. Template:

```json
{
  "platform": "messenger",
  "conversation": "<the group the user designates>",
  "host": "<the user's name>",
  "host_mode": "player | spectator",
  "players": [
    { "name": "<name or nickname in the group>", "identifier": "<identifier in the conversation, if known>" }
  ]
}
```

- `games/<game-id>.json` — one state file per game (schema in `references/exquisite-corpse.md`; the French source template names this folder `etats/`). It holds the game in progress: the players and their scores, and one entry per round with its variant, its sealed contributions (text, author, moment, `published: false` until publication), the assembled text, the votes, and the points. The contributions are the sealed key of the game: they exist in this file from the moment they are received and become public only at their round's publication.

There is **no separate scores file**: points, when a round has a vote, live in the game's state, and so does the game's result. No real identifier is ever written into the skill or a shared file: only into the user's private data folder. With no filled config, no group game starts: ask the user to designate the group and the players first.

## Router

| The user says | Do |
|---|---|
| "exquisite corpse", "cadavre exquis", "complete the sentence", "complète la phrase", "compléter la phrase", "blind writing game", "jeu d'écriture", "partie de groupe", "play with my group", "jouer avec mon groupe" | Run a group game: read `references/group-messaging.md` (connection, configuration, approvals, host-player mode), then `references/exquisite-corpse.md` (the rules, both variants). No filled config → set it up first (see Data layer) |
| "continue the game", "on continue la partie", "next round", "nouvelle manche" | Re-read the current game's state file and resume from it — the file, not conversation memory, is the truth |
| "what is the score", "c'est quoi le score" | Read the current game's state file in the user's data folder and answer from the file. Points exist only for rounds that had a vote; a game with no vote has no ranking, and the answer says so plainly |
| Any other group game by name | Be honest: Exquisite Corpse and its Complete the Sentence variant are the only group games in this skill. Others are not included and are never simulated or improvised |

## Running a round, in short

1. **Setup**: host designates the group and the players in the config (Exquisite Corpse: 3 to 6 players, one segment each; Complete the Sentence: 2 to 12 players, one ending each); the host picks their mode, **player** or **spectator** (host-player mode, `references/group-messaging.md` section b bis), recorded in the state. Each round declares its variant, and the host sets the round's options **at the announcement, never later**: the optional theme and the segment schema (Exquisite Corpse), the public opening (Complete the Sentence), whether the vote is active, and the single collection deadline.
2. **Announcement** in the group (host-approved): the variant, the theme if any (or, for Complete the Sentence, the opening published as-is), the number of players, and the collection deadline. For Exquisite Corpse the announcement contains **no segment** and never says who holds which segment type: the assignment is private.
3. **Private requests, in 1:1 only**: for Exquisite Corpse, the referee first draws one segment type per player and writes the full assignment, sealed, in the state **before any send**, then asks each player privately for only their own type, with its grammatical note, the length bound (15 words at most) and the deadline. For Complete the Sentence, each player privately gets the same request: the public opening, the bound (30 words at most, a single sentence) and the deadline. In host-player mode, a secret request goes out on a template the host approved once, filled slots never shown to the host (see `references/exquisite-corpse.md`).
4. **Blind collection**: each contribution arrives in 1:1, is sealed in the state the moment it lands, and gets the same bare acknowledgement everywhere: "Received." — no comment, no different tone per segment. One contribution per player; a correction sent before the deadline replaces it (the last version received is the one that counts). Anything arriving after the collection closes is refused, politely, in private. Only content-free statuses are ever announced.
5. **Close and assembly**: at the deadline, or earlier once every expected contribution is in, the collection closes. For Exquisite Corpse the referee assembles the segments **word for word, in schema order**: joined by a space, first letter capitalized, final punctuation ensured, and **nothing else corrected** — no grammar, no agreement, no word. A missing segment is replaced in its place by a bracketed marker (for example `[missing ending — contribution not received]`); if the marker lands in final position, the received sentence is closed with a period before it, because the marker is the referee's signal, not a piece of the sentence. The assembled text is written in the state before publication. For Complete the Sentence there is no assembly: the endings are prepared side by side under the same opening — anonymous, lettered, in a shuffled order when the vote is active; signed, in signup order, when the host disabled it.
6. **Publication** in the group (host-approved, and only after that approval): for Exquisite Corpse, the complete assembled text, then the attribution of every segment by type and author, the missing one named as missing — unless the "best ending" vote is active, in which case the text goes out **without attribution**, segments labelled by type only. For Complete the Sentence, the opening and all the endings in one message; a round needs at least 2 endings received, below that it is postponed or cancelled and recorded as such.
7. **Vote, when active**: players vote **in private, in 1:1**, before the vote deadline announced at publication — never in the thread, where a visible vote would anchor the next ones. **No self-vote**: a vote for one's own contribution is invalid, its author is told in private and may vote again for another contribution before the deadline. The winning contribution scores **1 point** for its author; a tie at the top is a **shared point**, 1 point to each tied author, with no tiebreak and no replayed round. At the close, the referee publishes the tally per letter or segment (never who voted for what) and reveals **all** authors.
8. **End of game**: after the last planned round, or when the host ends the game, the referee publishes a short recap (host-approved): the assembled texts, or the openings and winning endings, of the rounds played, and the points standings **only if at least one round had a vote** — a game of pure Exquisite Corpse without a vote has no winner and no ranking, and the recap says so simply. The state is marked finished; the result lives in the state file.

## Standing rules (they protect the game)

1. **The blind, whole**: contributions are collected **in 1:1 only, never in the group thread**, and nothing of a round is published, read aloud, quoted, summarized, or described before its publication — not even "someone wrote something very funny". Only content-free statuses are allowed ("contributions received: 3/4"). If the blind breaks, there is no game left.
2. **The referee never writes the text**: no invented segment, no completed gap, no shortened or corrected contribution. An overlong contribution is sent back to its author in private, before the deadline, to be shortened by them; the referee never shortens it. A contribution of the wrong type is likewise sent back naming the expected type; the referee never reclassifies a text or moves it in the assembly.
3. **A silent player leaves a marked gap, never a filled one**: at the deadline, a contribution not received (or set aside) stays missing. In Exquisite Corpse it is signalled in place, between brackets, and the publication is not delayed to wait for a substitute; in Complete the Sentence the ending is simply absent and the count is stated as-is ("3 endings received out of 4"). The gap is part of the result — often its funniest part.
4. **One deadline, held for everyone**: the collection closes at the announced deadline, or earlier if everything expected is in. A contribution arriving after the close is refused in private even if publication has not happened yet: one exception would destroy the deadline for every later round.
5. **Assembly is mechanical, presentation is settled**: segments joined word for word in schema order, a space between them, a capital on the first letter, final punctuation ensured, nothing else touched. Publication shows the complete text first, then the attribution; with the "best ending" vote, no attribution until the vote closes, and segments labelled by type only.
6. **Voting is anonymous and honest**: when a vote is active, publication is anonymous (shuffled, lettered endings for Complete the Sentence; unattributed segments for Exquisite Corpse), votes are private, self-voting is forbidden and controlled by the referee from the sealed state, a tie at the top shares the point, and every author is revealed at the close. The vote option is set at the round's announcement, never after collection.
7. **Set-asides are sober**: a contribution inappropriate for the host group (an insult aimed at a member, content plainly outside the group's limits) is not published; its author is told in private in one neutral sentence and may offer another before the deadline; the round continues, the contribution counts as missing. No public explanation, no detailed justification, no penalty points: the game has no tribunal.
8. **The state file is the truth**: every contribution is written into the state the moment it is received (text, author, moment, `published: false`), the full segment assignment is sealed there before the first private request goes out, and the referee re-reads the state before every send and rewrites it after every event. A dispute (assembly, tally, attribution of a point) is settled by republishing the texts and the tally **as they are in the state** — an assembly is redone aloud from the contributions, in schema order, never from conversation memory.
9. **Every send follows the host's connection rules**: exact preview + the host's explicit confirmation right before each public send; the assembled text is published only after the host approves it. In host-player mode, secret requests go out on templates approved once before their first send, filled versions never shown to the host, and the host receives statuses only.
10. **The host can stop everything** at any time: the game is marked abandoned, a short closing message goes out (host-approved), and the contributions of unpublished rounds **stay sealed** — they were never promised to the public and are not revealed in the closing message unless the host expressly asks.
11. **Language**: the group's language, as the host sets it in the config or at the announcement. This skill's files are in English; the game itself is played in the group's language.

## What this skill is not

- Not a ghostwriter: the referee referees, collects, and assembles — the text is written by the players alone, blind, and the referee adds nothing to it beyond capitalization, final punctuation, and the bracketed marker of a missing segment.
- Not real-time: there is no session to attend; a round is one collection against one deadline, at the group's pace, and the reveal happens in a single publication.
- Not a bot account: the referee writes from the host's own connected account, with the host's approvals. Players are told so in the announcement, including the honest note on host-player mode (see `references/group-messaging.md`, section b bis).
