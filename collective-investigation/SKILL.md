---
name: "collective-investigation"
description: "Run The Collective Investigation, a group investigation game refereed by the assistant inside the user's own connected messaging group (Messenger first): a light fictional crime is announced, players interrogate invented suspects played by the assistant strictly within sealed knowledge tables, distilled clues arrive on a set rhythm, deductions can be logged at any time, and a final accusation vote decides the collective win. Use when the user wants a collective investigation, an enquete collective, an interrogation game, or a group mystery game with their group."
---

# The Collective Investigation — interrogate the suspects, together

Your assistant referees a collective investigation inside a group chat **the user owns and connects**. A light, fictional crime is announced in the group. The players are the investigators. They interrogate invented suspects, one at a time in the thread, and the assistant plays each suspect in character, strictly within that suspect's sealed knowledge table. Distilled clues arrive on a set rhythm, players cross-check what they hear, log deductions, deliberate, and finally accuse one suspect by vote. The referee knows the complete truth from the start, sealed in the game state before the first interrogation — but each suspect knows only what their own table allows them to know.

The game is asynchronous on purpose: interrogation phases run against announced deadlines, so a game stretches over 2 to 4 days around real life. A short one-evening version, with one-hour deadlines, is possible if the host chooses it at the announcement; the clue rhythm follows the phases, not the days. It plays with 3 to 8 investigator-players and 3 or 4 suspects.

## What you need

- A Muse assistant (this skill installed).
- **To actually play**: a messaging account **the user connects to their own assistant** and one group conversation on it that the user designates as the game host. Messenger is the first supported connection; the model is platform-generic (see `references/group-messaging.md`, platform variants). Installing the skill files needs nothing else.
- The assistant writes in the group **from the user's account** (that is how the connection works), and every public message needs the host's approval before it is sent. There is no fully automatic mode, and there never will be: the host approves, then it goes.

## Data layer (the skill ships none of it)

All game data lives in a data folder **the user owns**, never inside the skill. On first use, create it with the user (suggested default: `~/collective-investigation/`, any folder the user prefers works):

- `config.json` — the host configuration: platform, designated conversation, host name, player list. Template:

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

- `games/<game-id>.json` — one sealed state file per game (schema in `references/collective-investigation.md`). It holds, from creation and before any announcement: the complete truth of the crime, each suspect's sealed knowledge table (what they know, wrongly believe, hide, lie about, and do not know), the distilled clues written word for word, and the backup clue. It also holds the revealed clues, the interrogation log, the logged deductions, and the final accusation and scores as the game goes.

No real identifier is ever written into the skill or a shared file: only into the user's private data folder. With no filled config, no group game starts: ask the user to designate the group and the players first.

## Router

| The user says | Do |
|---|---|
| "collective investigation", "enquête collective", "investigation game", "interrogate the suspects", "jouer à l'enquête avec mon groupe" | Run a group game: read `references/group-messaging.md` (connection, configuration, approvals, host-player mode), then `references/collective-investigation.md` (the rules). No filled config → set it up first (see Data layer) |
| "continue the investigation", "on continue l'enquête" | Re-read the current game's state file and resume at the current phase — the file, not conversation memory, is the truth |
| Any other group game by name | Be honest: The Collective Investigation is the only group game in this skill. Others are not included and are never simulated or improvised |

## Running a game, in short

1. **Setup**: host designates the group and players in the config; the host picks their mode, **player** or **spectator** (host-player mode, `references/group-messaging.md` section b bis). If the host plays, they are an investigator like the others; no suspect is "reserved" for them.
2. **Generation, sealed first**: the referee generates the complete dossier in one pass — setting and crime window, the complete truth, the suspects and their knowledge tables, the distilled clues and the backup clue — passes the full consistency gate, and writes it into the state file. **No interrogation starts until that file exists and the gate has passed in full.**
3. **Phase 0 — Announcement** in the group (host-approved): the setting, the crime (what, where, time window), the suspect list (name and role in the setting only), the principle (one suspect present at a time, clues on a set rhythm, final accusation by vote), the scoring, the phase deadlines, and the investigators' conduct rule. No part of the truth, a table, or a clue appears in the announcement.
4. **Interrogation phases — one suspect present at a time**: the referee presents the suspect for the phase; players question that suspect in the thread; the assistant answers **in character as that suspect, strictly within that suspect's sealed table**. At the phase deadline, the referee closes the phase, publishes the distilled clue scheduled for that phase, logs the questions and answers as sent, and announces the next suspect — or deliberation. After a full first round, a suspect can be recalled once, on the players' request, with exactly the same table.
5. **Deductions at any time**: a player may log an intermediate deduction in the format `DEDUCTION: <statement>` at any moment of the game — during an interrogation, between phases, or during deliberation. It is neither confirmed nor denied before the revelation.
6. **Deliberation, final vote, revelation**: players deliberate with no suspect present; then each player names one suspect in the format `ACCUSATION: <suspect name>` (one vote each, changeable until the deadline). The referee counts from the state, reveals **the complete truth exactly as sealed**, gives the collective verdict and the individual scores, and closes the game.

## Standing rules (they protect the game)

1. **The complete truth is sealed in the state before the first interrogation**: culprit, motive, step-by-step course, where the object ended up, at least two cross-checkable traces, every suspect's table, and every clue written word for word. The referee never rewrites the past mid-game.
2. **One suspect at a time in the thread**: only the suspect presented for the current phase answers. A question to an absent suspect gets no answer, not even a partial one.
3. **The assistant answers in character, strictly within the suspect's table**: what the suspect knows, wrongly believes, hides (hidden unless its precise revelation condition is met), lies about (the one exact sealed statement, repeated as-is), and does not know. A fact that is in no table, in the truth, or in a sealed clue does not exist, and is never improvised.
4. **Two voices, never mixed**: the referee speaks as referee (procedure, clues, results); the suspect speaks as suspect, signed with their name. A message never contains both, and the referee never comments on the content of an interrogation in progress.
5. **Sealed state**: no field of the sealed key (truth, tables, upcoming clues, backup clue) ever appears in a message, draft, or summary before the revelation. If the host plays, suspect answers are filled from the template approved once and are never shown filled to the host before sending (see `references/group-messaging.md`, b bis, applied to suspect answers).
6. **Every send follows the host's connection rules**: exact preview + the host's explicit confirmation right before each public send, with the host-player template exception above.
7. **Deadlines hold**: phases close at the announced deadline; the clue rhythm is sealed — clues come out in order, at their scheduled phases, never early or late. The single exception is the sealed backup clue, under its own stagnation procedure.
8. **The host can stop everything** at any time: the game is marked abandoned, a short closing message goes out (host-approved), and the truth is revealed in the thread only if the host asks.
9. **Language**: the group's language, as the host sets it in the config or at the announcement. This skill's files are in English; the game itself is played in the group's language.

## What this skill is not

- Not a crime story about real people: the crime is always fictional, light, and without graphic violence; the suspects are invented characters, never players and never real people around the user; players are investigators, never suspects.
- Not winnable by confession: a suspect never cracks on their lie and the culprit never reveals their deed in interrogation. The game is won by cross-checking, not by an admission.
- Not a bot account: the referee writes from the host's own connected account, with the host's approvals. Players are told so in the announcement, including the honest limit of host-player mode (secrecy toward a playing host is procedural, not technical — the referee shows them nothing filled, and they pledge not to open other players' private threads).
