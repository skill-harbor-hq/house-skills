---
name: "true-or-false"
description: "Run a True or False group game refereed by the assistant inside the user's own connected messaging group (Messenger first): the referee composes a round of statements, about half true and half fabricated to look true, seals the answer key in its state file before publishing anything, collects True or False answers before a deadline, then reveals the truth statement by statement, 1 point per correct answer. Use when the user wants a true or false game, a vrai ou faux, a partie de groupe, or a group quiz game with their group."
---

# True or False — a fabricated-edition quiz for your group chat

Your assistant referees a game of True or False inside a group chat **the user owns and connects**. The referee composes a whole round of statements before anything is published: about half are true, and the other half are false statements the referee has fabricated itself to be plausible, by inversion, exaggeration, a one-step shift, or a popular belief. The answer key, which statement is true and which is false, with the real fact behind each one, is **sealed in the state file before the first publication**. Nobody knows the key in advance, not even the host when the host plays: the host learns each truth in the thread, at the same time as everyone else.

The game is asynchronous on purpose: a round is published, answers are collected until an announced deadline, and the truth is revealed only once collection is closed. 2 to 10 registered players. A round is 8 statements by default (5 for an express round, 12 for a long one, if the host asks), published in one block by default, or one by one if the host chooses that variant at the announcement, never mid-round.

## What you need

- A Muse assistant (this skill installed).
- **To actually play**: a messaging account **the user connects to their own assistant** and one group conversation on it that the user designates as the game host. Messenger is the first supported connection; the model is platform-generic (see `references/group-messaging.md`, platform variants). Installing the skill files needs nothing else.
- The assistant writes in the group **from the user's account** (that is how the connection works), and every public message needs the host's approval before it is sent. There is no fully automatic mode, and there never will be: the host approves, then it goes.

## Data layer (the skill ships none of it)

All game data lives in a data folder **the user owns**, never inside the skill. On first use, create it with the user (suggested default: `~/true-or-false/`, any folder the user prefers works):

- `config.json` — the host configuration: platform, designated conversation, host name, host mode, publication mode, response mode, player list. Template:

```json
{
  "platform": "messenger",
  "conversation": "<the group the user designates>",
  "host": "<the user's name>",
  "host_mode": "player | spectator",
  "publication_mode": "block | one_by_one",
  "response_mode": "private_1_1 | thread",
  "players": [
    { "name": "<name or nickname in the group>", "identifier": "<identifier in the conversation, if known>" }
  ]
}
```

- `games/<game-id>.json` — one state file per round (schema in `references/true-or-false.md`; the French source template names this folder `etats/`). It holds the round in progress: the published statements and the sealed key (each statement's truth, its source fact and, for a fabricated false, its fabrication type), the answers collected, and the points. The key is written there before any publication and lives only there until the reveal of each statement. Finished states are kept: they are the anti-repetition history for later rounds with the same players.

No real identifier is ever written into the skill or a shared file: only into the user's private data folder. With no filled config, no group game starts: ask the user to designate the group and the players first.

## Router

| The user says | Do |
|---|---|
| "true or false", "vrai ou faux", "group quiz", "quiz de groupe", "partie de groupe", "play with my group", "jouer avec mon groupe" | Run a group game: read `references/group-messaging.md` (connection, configuration, approvals, host-player mode), then `references/true-or-false.md` (the rules). No filled config → set it up first (see Data layer) |
| "continue the game", "on continue la partie", "next round", "nouvelle manche" | Re-read the current round's state file and resume from it — the file, not conversation memory, is the truth |
| "what are the scores", "c'est quoi les scores" | Read the current or finished round's state file in the user's data folder and answer from the file |
| Any other group game by name | Be honest: True or False is the only group game in this skill. Others are not included and are never simulated or improvised |

## Running a round, in short

1. **Setup**: host designates the group and the players (2 to 10 registered) in the config; the host picks their mode, **player** or **spectator** (host-player mode, `references/group-messaging.md` section b bis), recorded in the state. The host also picks, at the announcement and never mid-round, the round size (8 by default, 5 express, 12 long) and the publication mode (block by default, or one by one).
2. **Announcement** in the group (host-approved): the game, the round size, the fact that about half the statements are true and the other half are false statements fabricated by the referee to look true, the publication mode, the response mode (see step 4), the deadline, the scoring (1 point per correct answer), and — if the host plays — the honest limit of host-player mode (protection of the key is procedural, `references/group-messaging.md` b bis point 4) plus the fact that the truth of each statement is revealed only at the end of collection.
3. **Generation and sealed state**: the referee composes the whole round, applies the quality gate in `references/true-or-false.md` (stable, verifiable true facts with an unambiguous scope; fabricated false statements that are plausible, never absurd, never on a sensitive topic, in the same length, tone and apparent precision as the true ones), **counts the balance** (8 statements means 4 true and 4 false; 5 means 3 and 2; 12 means 6 and 6), shuffles the order so no pattern is guessable, and writes the complete state, key included, **before** the publication. The log records the seal.
4. **Publication and collection — the response mode is settled by the host's mode**:
   - **Host plays → answers privately, in 1:1 to the referee. Mandatory, not an option.** In public, early answers appearing in the thread the host frequents and approves would influence the host's own answers, and the host's visible answer would influence the following ones. In 1:1, collected at the same time, nobody sees anyone's answer before the reveal, the playing host included, and the round is played on equal terms.
   - **Host spectates → answers in the thread, by default.** The host does not play: there is nothing to protect on their side, and answering in the thread is simpler and livelier for the group. The copying effect between players (late answers see the early ones) is then **assumed and announced at the announcement**; if a spectating host prefers rigour, they choose 1:1 collection at the announcement — the choice is recorded in the state (`config.response_mode`) and never changes mid-round.
   - In both modes: a player may **change an answer until the deadline**; only the last one counts. Silence at the deadline is an **abstention** on the statement or round concerned (0 points, counts neither for nor against).
5. **Closure**: at the deadline (or as soon as every answer is in), the referee closes collection, re-reads the state, and recounts the points from the file, never from memory, before preparing any reveal.
6. **Reveal**: a message from the referee in the thread, approved by the host (the reveal draft is prepared only after closure, see Standing rules): for each statement, in number order, the verdict, a short explanation anchored on the source fact, the detail of the answers and the points; then the current or final scores. In one-by-one publication, each statement is revealed at the closure of its own collection.
7. **End of round**: final recap in the thread (complete standings, best guesser named as first in the standings, statements nobody got right), result written into the state, state marked finished. A tie at the top means **co-winners**, with no invented tiebreaker; a full tiebreaker round may be proposed by the host, as a new game.

## Standing rules (they protect the game)

1. **The key is sealed before publication**: for each statement, its truth, its source fact, its explanation and, for a false, its fabrication type. It is written into the state file before the first message, announcement included, and it never leaves that file before the reveal of its statement.
2. **Public messages contain only the statements**: announcement, publication (block or one by one), deadline reminders and statuses contain no key, no marking (no check mark, asterisk or differentiated bold), no partial count of correct answers per statement, and no hint of tone ("that one is easy"). Statements are published **bare and numbered**, all formatted identically. Intermediate drafts and recaps shown to a playing host contain neither the key of statements still to come or in collection, nor the correct answers: a global current score is allowed (it is a total, not an answer), a per-statement detail before its reveal is not.
3. **The playing host answers like a player**: in 1:1 to the referee, before the deadline, with no prior access to the state or to the other players' answers. A playing host's possibly poor score is the ordinary proof that the protection held; the referee does not comment on it otherwise.
4. **Fixed scoring, announced in advance**: a correct answer (True on a true statement, False on a false one) scores **+1**; a wrong answer or an abstention scores 0. No negative points, no speed bonus, no bonus invented mid-round. The standings are the total of the points over the **counted** statements of the round (annulled statements excluded, see `references/true-or-false.md`, edge cases). An answer received after the deadline or after the reveal is **refused**, politely and without exception, and logged as such, never written into the counted answers.
5. **No leak, ever**: the same neutral wording for every statement; never "watch out for that one", never a different reaction depending on whether a player proudly announces a right or a wrong answer in the thread. The referee comments on a truth only at its reveal. Before that moment, no confirmation or denial, in public or in private, even to a player who is "sure", even to the host.
6. **A leak compromises the round**: if the key (or the verdict of a single unrevealed statement) reaches a player or the playing host by accident (wrong preview, wrong recipient, one detail too many in a status), the referee stops everything, declares it frankly to the host in private without naming more content than necessary, and follows the compromised-game conduct in `references/group-messaging.md` (section b bis, point 5): the host decides, restart the round with fresh statements or continue knowingly. Never concealment. If the leak touches only one unrevealed statement and the host chooses to continue, that statement is annulled and the round is played on the remaining ones.
7. **Deadlines are held**: every publication announces its deadline. Nudges to silent players go in the thread or in a status to the host, in counts only ("answers are still missing"), without saying who answered what — in 1:1 mode, without even saying to a playing host who has not answered, beyond the count.
8. **The state file is the truth**: re-read at every event, rewritten after every event (generation, seal, publication, answer received, closure, reveal, points, annulment). One file per round, held by the referee alone. The key exists only there. Points are recounted from the answers recorded in the state before every publication of scores; the detail published at the reveal (answer per player, per statement) lets everyone redo the count.
9. **A contestable statement is annulled, never defended**: if a verdict turns out to be contestable (a player contests it with a serious element, or the referee discovers its source fact was wrong, outdated or ambiguous), the statement is annulled under the procedure in `references/true-or-false.md`: before its reveal, its truth is never revealed and the round is counted on the remaining statements; after its reveal, its points are withdrawn from every player, a neutral correction is published, and scores and standings are recounted and republished.
10. **Every send follows the host's connection rules**: exact preview + the host's explicit confirmation right before each public send. In host-player mode, the approval previews are blind by construction: the preview is the public message itself, which by rule 2 contains nothing of the key.
11. **The host can stop everything** at any time: the round is marked abandoned, a short closing message goes out (host-approved), and the key of unrevealed statements stays sealed in the state unless the host expressly asks for the complete recap.
12. **Language**: the group's language, as the host sets it in the config or at the announcement. This skill's files are in English; the game itself is played in the group's language.

## What this skill is not

- Not real-time: there is no session to attend and no answer is ever revealed before its collection closes; the round advances in the thread, at the group's pace, until the deadline.
- Not a bot account: the referee writes from the host's own connected account, with the host's approvals. Players are told so in the announcement, including the honest limit of host-player mode (protection of the key toward a playing host is procedural, not technical — the referee shows them nothing, and they pledge not to go read the state or other players' private threads).
