---
name: "five-locks-escape"
description: "Run a Five Locks Escape game: five chained puzzles on one theme, refereed by the assistant, playable solo in chat or cooperatively by a group in the user's own connected messaging group (Messenger first). The full answer key is written and sealed in the game state before the first puzzle, the team shares 3 hints for the whole game, and any lock can be forced at a points cost instead of blocking the game. Use when the user wants an escape game, a puzzle chain, an escape-5-cadenas, or a cooperative group puzzle."
---

# Five Locks Escape — five chained puzzles, one way out

Your assistant referees an escape game made of five locks in a chain, all on one theme. Each solved puzzle gives the code, word, or key that opens the next lock, and the solution of lock N always serves lock N+1 in a documented, mechanical way. The players advance together, share **3 hints for the whole game**, and no lock can block the game for good: a lock that resists too long can be **forced**, at the price of its points.

Play it solo, in chat with the user, or cooperatively, with a whole group against the game, inside a group chat **the user owns and connects**. This game has no individual secrets: no roles, no private actions. In group mode, every proposal, hint request, and force request happens in the public thread.

## What you need

- A Muse assistant (this skill installed).
- **For solo play: nothing else.** No account, no connection, no setup beyond choosing a theme.
- **For cooperative group play**: a messaging account **the user connects to their own assistant** and one group conversation on it that the user designates as the game host. Messenger is the first supported connection; the model is platform-generic (see `references/group-messaging.md`, platform variants).
- The assistant writes in the group **from the user's account** (that is how the connection works), and every public message needs the host's approval before it is sent. There is no fully automatic mode, and there never will be: the host approves, then it goes.

## Data layer (the skill ships none of it)

All game data lives in a data folder **the user owns**, never inside the skill. On first use, create it with the user (suggested default: `~/five-locks-escape/`, any folder the user prefers works):

- `config.json` — only needed for group play: platform, designated conversation, host name, player list. Template:

```json
{
  "platform": "messenger",
  "conversation": "<the group the user designates>",
  "host": "<the user's name>",
  "players": [
    { "name": "<name or nickname in the group>", "identifier": "<identifier in the conversation, if known>" }
  ]
}
```

- `games/<game-id>.json` — one state file per game (schema in `references/five-locks-escape.md`). The sealed key — all five solutions, accepted variants, hint texts, and chain links — lives only there, written in full before the first puzzle is shown.
- `scores.json` — solo results only, if the user wants a record (entry format in `references/five-locks-escape.md`). Group results live in the game state only.

No real identifier is ever written into the skill or a shared file: only into the user's private data folder. Solo play needs no config at all. Group play with no filled config does not start: ask the user to designate the group and the players first.

## Router

| The user says | Do |
|---|---|
| "escape game", "five locks", "évasion", "5 cadenas", "puzzle chain", "play solo" | Run a solo game in chat: read `references/five-locks-escape.md` (the rules) and follow it |
| "escape game with my group", "escape coopératif", "jouer en groupe" | Run a cooperative group game: read `references/group-messaging.md` (connection, configuration, approvals), then `references/five-locks-escape.md` (the rules). No filled config → set it up first (see Data layer) |
| "continue the game", "reprends la partie", "on continue" | Re-read the most recent in-progress game's state file and resume from it — the file, not conversation memory, is the truth (resume announcement per `references/five-locks-escape.md`) |
| Any other game by name | Be honest: Five Locks Escape is the only game in this skill. Others are not included and are never simulated or improvised |

## Running a game, in short

1. **Theme**: chosen by the user or the players, or drawn by the referee and announced.
2. **Generation, all at once, before departure**: the referee generates all 5 puzzles in one pass, applies the quality gate to every lock, and writes the complete state file immediately — public statement, solution, accepted variants, hint text, and chain link to the next lock, for every lock. That is the **sealed key** (see Standing rules).
3. **Opening**: the referee announces the theme, the principle (5 locks in a chain), the hint counter (3 for the whole game), the scoring scale, and the forcing rule, then the statement of **lock 1 only**.
4. **One lock at a time**: the team discusses freely; a counted proposal is explicit (`PROPOSITION: <answer>`); the referee checks it against the sealed state (solution + listed variants, after normalization) and answers with the same neutral wording every time — correct or incorrect, nothing more.
5. **Hints**: 3 for the whole game, one per lock at most, the sealed hint text given as written, −5 points each.
6. **Forcing**: after 4 counted failed attempts the referee offers forcing; the team may ask earlier, from 2 counted failed attempts. A forced lock opens, scores 0, and its chain element is transmitted publicly as a mechanism so the next lock stays playable.
7. **End**: after lock 5 (solved or forced), the referee publishes the final grade and the full recap — decomposition of the score, forced locks, hints used, elapsed time if timestamped, and every solution revealed with its reasoning step. Solo: a result entry goes to `scores.json`. Group: the result lives in the state only.

## Standing rules (they protect the game)

1. **Sealed key, written before the first puzzle**: the complete key for all 5 locks — solutions, accepted variants, hint texts, chain links — is written into the game state **before** the first puzzle is presented. It never leaves the file, never appears in a draft shown to the host or the players, and no puzzle is presented before the previous lock is solved or forced.
2. **The state file is the truth**: the referee re-reads it at the start of every turn and rewrites it after every event. The provisional score is always recalculated from the state, never from memory.
3. **Neutral referee**: every counted proposal gets the same neutral wording ("Proposition received: incorrect." / "Proposition received: correct — the lock opens."). No warm/cold, no "almost", no comment on content, ever. A nearly-right answer gets exactly the same "incorrect" as an absurd one.
4. **3 hints per game, total**: one shared counter for the whole team in group mode, one hint per lock at most, −5 points per hint spent. A hint is the sealed text, as written — never the solution, never a summary that contains it.
5. **No lock blocks the game**: any lock can be forced instead of solved, under the conditions in `references/five-locks-escape.md` (thresholds, second-player confirmation in group mode). A forced lock scores 0 and no further penalty.
6. **No improvised equivalence**: an answer counts only if, after the normalization defined in the reference, it matches the solution or a variant listed in the state at generation time. The referee never accepts an unlisted equivalence mid-game.
7. **The thread only gets public information** (group mode): lock openings, verdicts, score announcements, force offers, recap. Every send follows the host's approval rules (`references/group-messaging.md`). This game has no individual secrets and no 1:1 play: a proposal sent privately does not count — the referee redirects it to the thread.
8. **The host can stop everything** at any time (in solo, the user): the game is marked abandoned, which is terminal. Solutions are revealed in an abandon recap only if the user or the host asks.
9. **Language**: the language of the chat or of the group, as the user or host sets it. This skill's files are in English; the game itself is played in the players' language.

## What this skill is not

- Not a puzzle generator for other uses: the chain is generated for one game, sealed, and played — not exported, not reused across games.
- Not a bot account: in group mode the referee writes from the host's own connected account, with the host's approvals.
- Not blocking by design: if a team is stuck, its options are always the same — keep trying, spend a hint if one remains for that lock, or force the lock. The game always ends.
