---
name: "tournament-bracket"
description: "Run Tournament Bracket, a single-elimination group tournament refereed by the assistant inside the user's own connected messaging group (Messenger first): 4 to 16 players, each duel an asynchronous private mini-quiz with different questions per player and a sealed answer key written before the duel, sudden-death then earliest-complete-series tiebreaks, byes for the earliest signups, and an updated bracket published after every round. Use when the user wants a tournament, a bracket, un tournoi en tableau, or a knockout quiz tournament with their group."
---

# Tournament Bracket — a knockout quiz tournament for your group chat

Your assistant referees a single-elimination tournament inside a group chat **the user owns and connects**. The entrants face each other in a bracket: every duel is an asynchronous mini-quiz played separately in private by the two opponents, on different but comparable questions whose answer key is sealed in the state file before the duel starts. The better score advances, the updated bracket is published after every round, and the final crowns a champion.

The tournament is fair because it is sealed before it is played. No player ever sees their opponent's questions, and the referee cannot favour anyone: for each duel, all of both players' questions, their answers (the key), and each player's reserve question are written into the state file before the first question of that duel is sent. After the duel, its key becomes public with the result — anyone can recount. A bracket holds 4 to 16 players.

## What you need

- A Muse assistant (this skill installed).
- **To actually play**: a messaging account **the user connects to their own assistant** and one group conversation on it that the user designates as the game host. Messenger is the first supported connection; the model is platform-generic (see `references/group-messaging.md`, platform variants). Installing the skill files needs nothing else.
- The assistant writes in the group **from the user's account** (that is how the connection works), and every public message needs the host's approval before it is sent. There is no fully automatic mode, and there never will be: the host approves, then it goes.

## Data layer (the skill ships none of it)

All tournament data lives in a data folder **the user owns**, never inside the skill. On first use, create it with the user (suggested default: `~/tournament-bracket/`, any folder the user prefers works):

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

- `games/<game-id>.json` — one sealed state file per tournament (schema in `references/tournament-bracket.md`). It holds the bracket, the rounds and duels, and, duel by duel, each duel's sealed keys: both players' question sets with their complete keys, each player's sealed reserve question, the deadlines, the receptions and scores, any tiebreak, and the results and final ranking as the tournament goes.
- `library/questions.json` — the shared question library the referee checks before every duel (anti-repetition: an answer + dimension pair already in the library is never reused) and appends every question actually asked to at the end (see `references/tournament-bracket.md`, End writings). Unused reserves never enter it.
- No entry is ever made in a solo scores file for a tournament: the result lives in the tournament's state (`final_ranking`, `champion`, `history`).

No real identifier is ever written into the skill or a shared file: only into the user's private data folder. With no filled config, no tournament starts: ask the user to designate the group and the players first.

## Router

| The user says | Do |
|---|---|
| "tournament", "bracket", "tournoi", "tournoi en tableau", "knockout tournament", "tournoi avec mon groupe" | Run a group tournament: read `references/group-messaging.md` (connection, configuration, approvals, host-player mode), then `references/tournament-bracket.md` (the rules). No filled config → set it up first (see Data layer) |
| "continue the tournament", "on continue le tournoi" | Re-read the current tournament's state file and resume at the current round — the file, not conversation memory, is the truth |
| Any other group game by name | Be honest: Tournament Bracket is the only group game in this skill. Others are not included and are never simulated or improvised |

## Running a tournament, in short

1. **Setup**: host designates the group and players in the config; the host picks their mode, **player** or **spectator** (host-player mode, `references/group-messaging.md` section b bis). The tournament parameters are fixed at the announcement and written into the state: questions per player (3 by default, 5 if the host wants longer duels), round period, and the tiebreak deadline (120 minutes by default).
2. **Announcement and signups** in the group (host-approved): the places (bracket of 4, 8 or 16), the byes for the earliest signups if any, the duel format, the tiebreak rule, and that silence at a deadline is a forfeit. Signups are timestamped in the state: signup order is the seeding, and the earliest signups receive the byes.
3. **Bracket**: the bracket size is the smallest power of 2 at or above the number of entrants; byes = bracket size − entrants, given to the earliest signups in timestamped signup order. Round 1 pairings are crossed (highest seed still in play against the lowest), and the full round 1 bracket is published in the thread **before** the first duel.
4. **Each duel, sealed first**: the referee generates two different question sets (one per player, comparable difficulty, full quality gate, anti-repetition checked against the shared library), plus one sealed reserve question per player, and writes everything — questions, complete keys, reserves, deadline — into the state **before** any question of that duel is sent. Each player then plays their own set in private 1:1, before the shared round deadline.
5. **Scoring and publication**: score = number of correct answers, counted from the sealed key after the deadline or once both complete sets are in. The referee publishes the duel result in the thread (both scores, the full detail of both sets — the finished duel's key is no longer secret — the winner and how they won), and republishes the updated bracket once the round is complete. The next round is generated and sealed only after the previous round is fully published; two rounds are never played at once.
6. **Ties, byes and forfeits** follow `references/tournament-bracket.md` exactly: a tie is settled first by sudden death (one new sealed question per player), then by the earliest timestamp of the complete initial series — never at random. A silent player forfeits; a double silence eliminates both; a bye advances its holder without a duel.
7. **End**: the champion (or, after a double-forfeit final, honestly no champion) and the final ranking are published in the thread, the state is marked finished, and every question actually asked is appended to the shared library.

## Standing rules (they protect the tournament)

1. **Sealed key per duel**: no question of a duel is sent before that duel's entire key — both sets, both reserves, the deadline — is in the state file, with its sealing time logged. Later rounds are not written in advance: each round is generated and sealed after the previous round is published.
2. **Different questions per player, always**: the two opponents of a duel never receive the same question. Each plays only their own set, in private 1:1, and never sees the other's set or answers before the duel result is published.
3. **Comparable difficulty, gated**: every question — sets, reserves and tiebreak questions alike — passes the full quality gate in `references/tournament-bracket.md` before it is written into the state, and the two sets of a duel are balanced at generation (same family of effort, varied dimensions, no two questions on the same dimension for one player in one duel).
4. **The tiebreak order is fixed and announced before play**: sudden death first, then the earliest complete-series reception timestamp of the initial duel, then the tiebreak fallbacks written in the reference. A tie never sends both players through and is never settled by chance.
5. **Sealed state**: while a duel is open, its questions and key are shown to no one except each question's own recipient, and never leave the state file. In host-player mode, duel messages go out on a template the host approves once per message type; filled versions are never shown to a playing host, who only ever sees statuses.
6. **Every send follows the host's connection rules**: exact preview + the host's explicit confirmation right before each public send, with the host-player template exception above.
7. **Deadlines hold**: all duels of a round share the same announced deadline; a duel may close early only once both complete sets are in — never early against a player who has not finished. Receipts are acknowledged with a bare status, with no comment on the answers, and reminders never reveal content.
8. **The state is the truth**: the referee re-reads the state file at every event and rewrites it after every event; scores, timestamps and the published bracket are always recounted from the state, never from memory.
9. **The host can stop everything** at any time: the tournament is marked abandoned, a short closing message goes out (host-approved), and no champion is declared for an interrupted tournament.
10. **Language**: the group's language, as the host sets it in the config or at the announcement. This skill's files are in English; the tournament itself is played in the group's language.

## What this skill is not

- Not a shared quiz: the two opponents of a duel never answer the same questions, and there is no live, simultaneous play — each duel is asynchronous, in private, against a deadline.
- Not a bot account: the referee writes from the host's own connected account, with the host's approvals. Players are told so in the announcement, including the honest limit of host-player mode (secrecy toward a playing host is procedural, not technical — the referee shows them nothing filled, and they pledge not to open other players' private threads).
- No third-place match by default: the semi-final losers are joint third, unless a ranking match was announced before round 1.
