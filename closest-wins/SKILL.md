---
name: "closest-wins"
description: "Run a Closest Wins numeric estimation game refereed by the assistant: a question whose answer is a number, every value sealed in the game state before the first question, each player estimates without seeing the others' numbers, and the closest answer scores 1 point, ties sharing the point. Playable solo in chat, the user against a sealed 20 percent tolerance, or in a group in the user's own connected messaging group (Messenger first), answers collected in private in 1:1 and revealed all at once. Use when the user wants a closest wins game, a le plus proche gagne, an estimation game, a guessing numbers game, or a partie d'estimations with their group."
---

# Closest Wins: the estimation game where the closest number takes the point

Your assistant referees a game of numeric estimation. The referee asks a question whose answer is a number, in a named unit. Everyone estimates, **without seeing anyone else's number**, and when the answers are in, the referee reveals the true value: **the closest answer scores 1 point**. The default game is **5 rounds**. The pleasure is not in knowing the figure: it is in approaching it by order-of-magnitude reasoning, and in sensing where the others will go wrong.

The fairness is in the sealing. **Every true value, with its source, is written into the game state before the first question is asked**, and no value ever leaves that file before its round's reveal. In group play, answers are collected **in private, in 1:1**, never in the thread, because a visible number anchors every answer after it; the reveal publishes the true value, every answer, every distance, and the running score **all at once**. Full rules in `references/closest-wins.md`.

Play it solo, right in chat: the user plays alone against a **sealed tolerance of 20 percent by default**, written in the state before the game and never changed during it: an answer within plus or minus 20 percent of the true value scores the point. Or play it in a group, inside a group chat **the user owns and connects**: 2 or more players, the closest scoring, ties sharing the point, and a tie in the final standings making co-winners.

## What you need

- A Muse assistant (this skill installed).
- **For solo play: nothing else.** No account, no connection, no setup.
- **For group play**: a messaging account **the user connects to their own assistant** and one group conversation on it that the user designates as the game host. Messenger is the first supported connection; the model is platform-generic (see `references/group-messaging.md`, platform variants). Installing the skill files needs nothing else.
- The assistant writes in the group **from the user's account** (that is how the connection works), and every public message needs the host's approval before it is sent. There is no fully automatic mode, and there never will be: the host approves, then it goes.

## Data layer (the skill ships none of it)

All game data lives in a data folder **the user owns**, never inside the skill. On first use, create it with the user (suggested default: `~/closest-wins/`, any folder the user prefers works):

- `config.json` — only needed for group play: platform, designated conversation, host name, host mode, player list. Template:

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

- `games/<game-id>.json` — one state file per game (schema in `references/closest-wins.md`). The sealed key lives only there: every round's true value and its `fact_source`, written in full before the first question, plus the solo tolerance or the group variant flag, the answers, the distances, the points, and the log.
- `scores.json` — solo results only (entry format in `references/closest-wins.md`). Group results live in the game state only.
- `library/questions.json` — the shared anti-repetition library: one entry per round played, in both modes, with `game: "closest-wins"` (format in `references/closest-wins.md`). A cancelled round never enters it.

No real identifier is ever written into the skill or a shared file: only into the user's private data folder. Solo play needs no config at all. Group play with no filled config does not start: ask the user to designate the group and the players first.

## Router

| The user says | Do |
|---|---|
| "closest wins", "le plus proche gagne", "estimation game", "jeu d'estimations", "guess the number", "play solo" | Run a solo game in chat: read `references/closest-wins.md` (the rules) and follow it |
| "closest wins with my group", "le plus proche gagne en groupe", "jouer en groupe" | Run a group game: read `references/group-messaging.md` (connection, configuration, approvals, host-player mode), then `references/closest-wins.md` (the rules). No filled config → set it up first (see Data layer) |
| "continue the game", "on continue la partie", "next round", "manche suivante" | Re-read the current game's state file and resume from it: the file, not conversation memory, is the truth |
| "what is the score", "c'est quoi le score" | Read the current game's state file in the user's data folder and answer from the file: in group, the players' scores and winners; in solo, the score out of the rounds played |
| Any other game by name | Be honest: Closest Wins is the only game in this skill. Others are not included and are never simulated or improvised |

## Running a game, in short

1. **Generation, all at once, before departure**: the referee composes all 5 rounds (the express default) in one pass, applies the quality gate of `references/closest-wins.md` to every question (stable verifiable fact, one true value with its unit and any needed date in the question, unknown but approachable, no famous figure recited by heart, no clue in the wording, anti-repetition against `library/questions.json`), and writes the complete state at once: question, sealed value, unit, and `fact_source` for every round, plus the solo tolerance (20 percent by default) or, in group, the optional "without going over" variant if the host chose it before the game. That is the **sealed key**.
2. **Opening of a round**: solo, the question is asked in chat, alone, with its unit. Group, the referee publishes in the thread (host-approved): the round number, the question with its unit, the deadline, and the reminder that answers go **in private to the referee, never in the thread**.
3. **Answers**: solo, the user answers in chat with one number. Group, each player sends their number in 1:1 before the deadline and gets the same bare acknowledgement ("Received."), with no comment on the value, ever. One answer per player: the first counts, an explicit correction before the deadline replaces it. Silence at the deadline means the round is skipped for that player; a late answer is refused in private.
4. **Reveal**: solo, immediate correction: the true value, the distance (absolute and relative), the point or not under the sealed tolerance, a short explanation from `fact_source`, and the running score. Group, at the deadline (or earlier once every answer is in), one single message: the true value with its source in one sentence, **all** the answers, each distance, the round winner(s), and the cumulative scores. The state is updated before the next round opens.
5. **End**: group, the complete final standings are published (host-approved): scores, rounds won, exact answers highlighted, and co-winners on a tie. Solo, a recap with the missed rounds' true values. Solo results go to `scores.json`; both modes add their played rounds to `library/questions.json`; the state is marked finished.

## Standing rules (they protect the game)

1. **Sealed key, written before the first question**: every round's value and source is in the state from the game's creation. The key never leaves the file before its round's reveal, and no value is ever corrected silently mid-round: a fact discovered false or ambiguous cancels its round, with no points, and the game continues on the remaining rounds.
2. **Private answers in group, reveal all at once**: an answer visible early anchors the others, so group answers live in 1:1 and in the state only, and become public together at the reveal, with the true value and every distance. Only content-free statuses are ever announced ("answers received: 3/4"). If a player posts their answer in the public thread by mistake, **the answer counts and the round continues**: the referee comments on nothing in the thread, privately reminds the players still to answer to play their own estimation, mentions the incident honestly in the reveal, and logs it; the host alone may ask for that round's cancellation before the reveal.
3. **Distance decides, nothing else**: distance is the absolute gap to the true value, in the question's unit. The closest scores **1 point**; an exact answer scores the same 1 point, celebrated in words, never bonused. **A tie at the minimal distance is a shared point**: each tied player scores 1, with no tiebreak and no replayed round. No negative points, no proportional points, no points invented mid-game, and no "without going over" elimination unless the host chose that variant before the game and it is written in the state.
4. **Solo tolerance is sealed too**: 20 percent by default, written in the state before the game, never adjusted after an answer. Within the tolerance scores 1, outside scores 0.
5. **Units and numbers are read in good faith, never silently**: a decimal comma and a decimal point are the same number; an obvious, unambiguous conversion (a value given in kilometres for a question in metres, "37 million" for a count) is accepted and confirmed to the player in private before the deadline; an ambiguous answer (no unit where it matters, no identifiable number, two numbers) gets one private clarification request before the deadline, and with no clarification by the deadline it is invalid, announced as such at the reveal, with no distance and no point.
6. **The state file is the truth**: the referee re-reads it before every step and rewrites it after every event. A dispute over a calculation is settled by republishing the answers, the value, and the distances as they are in the state and redoing the calculation aloud, never from conversation memory.
7. **Every group send follows the host's connection rules**: exact preview plus the host's explicit confirmation right before each public send. In host-player mode, the host answers in 1:1 like every player and is shown statuses only, never the other players' answers before the reveal; that protection is procedural, a matter of trust, and the opening announcement says so plainly.
8. **The host can stop everything** at any time (in solo, the user): the game is marked abandoned, a short closing message goes out in group mode (host-approved), and unrevealed rounds stay unrevealed unless the host asks for their values in the closing message.
9. **Language**: the language of the chat or of the group, as the user or host sets it. This skill's files are in English; the game itself is played in the players' language.

## What this skill is not

- Not a quiz of knowledge: the values are chosen to be unknown but approachable by reasoning; a question everyone can recite exactly, or nobody can approach at all, fails the quality gate and is never asked.
- Not a bidding game: going over the true value does not eliminate anyone, unless the host chose the "without going over" variant before the game.
- Not a bot account: in group mode the referee writes from the host's own connected account, with the host's approvals.
