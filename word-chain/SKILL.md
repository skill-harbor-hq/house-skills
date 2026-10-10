---
name: "word-chain"
description: "Run a Word Chain group game refereed by the assistant inside the user's own connected messaging group (Messenger first): in the public thread, 2 to 8 players chain words of one imposed category, each word starting with the last letter of the previous word, no word repeated, with 3 collective lives, one letter joker per round, and a persistent record kept per category. Use when the user wants a word chain game, a word game, a chaîne de mots, a partie de groupe, or a group word game with their group."
---

# Word Chain — a cooperative word game for your group chat

Your assistant referees a game of Word Chain inside a group chat **the user owns and connects**. In the public thread, the players chain words of **one imposed category** for the round: each word must start with the **last letter of the previous word**. The referee validates every link (attack letter, membership in the category, non-repetition), signals faults kindly, holds the group's **3 collective lives**, and keeps the **record** of the longest chain — per category. The group plays together against the chain stopping, not against each other.

This game has **no hidden information between players**: everything is played in the public thread of the group, and that is precisely what makes it simple to referee. The referee plays **by reading the thread**: a proposal counts because it appears in the thread, not because anyone forwarded it — no private send is needed for a proposal to be submitted or judged. The referee's own messages (announcement, validations, end of round) are public messages in the thread, host-approved like every send (see `references/group-messaging.md`).

The game is asynchronous on purpose: no imposed turn order, the chain advances whenever a registered player passes through the thread, against an announced inactivity deadline. 2 to 8 registered players.

## What you need

- A Muse assistant (this skill installed).
- **To actually play**: a messaging account **the user connects to their own assistant** and one group conversation on it that the user designates as the game host. Messenger is the first supported connection; the model is platform-generic (see `references/group-messaging.md`, platform variants). Installing the skill files needs nothing else.
- The assistant writes in the group **from the user's account** (that is how the connection works), and every public message needs the host's approval before it is sent. There is no fully automatic mode, and there never will be: the host approves, then it goes.

## Data layer (the skill ships none of it)

All game data lives in a data folder **the user owns**, never inside the skill. On first use, create it with the user (suggested default: `~/word-chain/`, any folder the user prefers works):

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

- `games/<game-id>.json` — one state file per round (schema in `references/word-chain.md`; the French source template names this folder `etats/`). It holds the round in progress: the category, the chain of valid words, every judged or set-aside proposal with its verdict, and the collective lives remaining.
- `records-word-chain.json` — the persistent records, **one record per category** (schema in `references/word-chain.md`; French source name: `records-chaine-de-mots.json`). It survives between rounds: a finished round is compared to its category's record and rewrites the file only if it beats it. For a test round, the file carries the `-TEST` suffix: a test never beats the group's real record.

No real identifier is ever written into the skill or a shared file: only into the user's private data folder. With no filled config, no group game starts: ask the user to designate the group and the players first.

## Router

| The user says | Do |
|---|---|
| "word chain", "chaîne de mots", "word game", "jeu de mots", "partie de groupe", "play with my group", "jouer avec mon groupe" | Run a group game: read `references/group-messaging.md` (connection, configuration, approvals, host-player mode), then `references/word-chain.md` (the rules). No filled config → set it up first (see Data layer) |
| "continue the game", "on continue la partie", "next round", "nouvelle manche" | Re-read the current round's state file and resume from it — the file, not conversation memory, is the truth |
| "what is the record", "c'est quoi le record" | Read `records-word-chain.json` in the user's data folder and answer from the file, per category |
| Any other group game by name | Be honest: Word Chain is the only group game in this skill. Others are not included and are never simulated or improvised |

## Running a round, in short

1. **Setup**: host designates the group and the players (2 to 8 registered) in the config; the host picks their mode, **player** or **spectator** (host-player mode, `references/group-messaging.md` section b bis), recorded in the state. The host picks the round's **one category** (or asks the referee to draw one from the template list in `references/word-chain.md`); it never changes mid-round.
2. **Announcement** in the group (host-approved): the game, the category, the registered players, the 3 collective lives, the three possible faults (letter, category, repetition), the "never twice in a row the same player" rule, and the inactivity deadline. No information is distributed privately: this game has no secrets.
3. **Starting word**: the referee publishes a starting word of the category, common, ending on a playable letter. It counts as the **first link** of the chain.
4. **Proposals in the thread**: any registered player proposes the next link directly in the thread — one word, starting with the last letter of the last valid word, in the category, never played before in this round. Free order, but **never two valid proposals in a row from the same player**. Discussion, jokes and encouragement in the thread are free and welcome; they do not count as proposals.
5. **Public validation after each proposal**: the referee answers in the thread with the word, the verdict, and — if valid — the new expected letter, the current chain length and the lives remaining. If refused: the reason in one kind sentence, the lives remaining, and the reminder that the chain still waits for a word starting with the same letter. The three checks are applied **in this order** — attack letter (mechanical), non-repetition (from the state), category (the referee's judgement, with the benefit of the doubt, see below) — and only the first failing check is announced.
6. **Faults and lives**: each validated fault (letter, repetition, clear category miss) costs the group **exactly 1 life**. At **0 lives**, the round ends immediately. A **letter joker** (once per round) lets the group change an impossible or near-impossible expected letter at the cost of 1 life (see `references/word-chain.md`, edge cases).
7. **Disputes**: any registered player may dispute a verdict in the thread **before the next link is validated**; the chain pauses and **the host settles it** before the next link (full procedure in `references/word-chain.md`). A reasoned doubt benefits the player: for the category, a genuinely debatable word is accepted.
8. **End of round**: lives exhausted, inactivity deadline reached, or the host ends it — and no other improvised case. Final message in the thread (host-approved): the reason, the final length, the complete chain word by word, the lives remaining if any, and the fate of the category record (beaten, tied, or standing). The record file is rewritten only if the round **strictly beats** its category's record.

## Standing rules (they protect the game)

1. **The chain rule, whole**: every word starts with the **last letter of the previous word** and respects the **imposed category**; **no word is ever repeated** in a round (the starting word included; a plural of a played word is the same word). Letter validation is purely mechanical, with the written normalization (accents do not change the letter, case is ignored, a hyphenated compound counts as one word — full rules in `references/word-chain.md`).
2. **3 collective lives, never individual**: a fault costs the group, never a named player. The referee's messages never designate anyone as "responsible" for the end of a chain; faults are part of the game and often its funniest moments.
3. **One letter joker per round, at 1 life**: claimed in the thread when the expected letter is impossible or near-impossible in the category, it changes only the expected letter — the last valid word stays. With no life left, or the joker already used, there is no recourse; the joker never resurrects a finished round.
4. **Never twice in a row the same player**: a proposal from the player who supplied the last valid link is **not judged** — no life lost, the word is not consumed — and the referee says so in the thread. A player whose proposal was refused may propose again immediately.
5. **Disputes are settled by the host before the next link**: the chain pauses on a dispute; the host decides after hearing the disputing player's argument and the referee's position. Category: the **benefit of the doubt goes to the word**. Letter: never any benefit of the doubt — the letter is checked mechanically, and a referee error is corrected with the life restored. Repetition: the state file settles it. Disputing in good faith never costs a life.
6. **The state file is the truth**: after every event (proposal judged, fault, life lost, dispute, verdict, joker, end of round), the referee re-reads and rewrites the state file: chain of valid words, refused proposals with their reasons, lives remaining. Repetition checks and the length are always recomputed from the file, never from memory. **No score file**: the result lives in the round's state; the records file is the only persistent writing specific to this game.
7. **Validation before the chain moves on**: the referee never lets two links chain without a validation between them — the validation is what advances the expected letter. Simultaneous proposals: only the **first in thread order** is judged; the second is a **stale proposal**, neither valid nor a fault, and no life is ever lost on one.
8. **Kindness of form, firmness of substance**: refusals are short, without reproach, and always say what to play next. No message mocks a player, compares players, or blames anyone for a lost life. The referee never suggests a word and never gives an example that would amount to a proposal.
9. **Every send follows the host's connection rules**: exact preview + the host's explicit confirmation right before each public send. In host-player mode, the host sees in the previews only what the whole thread will see — this game has no secret content to protect, and the announcement says so plainly.
10. **The host can stop everything** at any time: the round is marked abandoned, a short closing message goes out (host-approved), and the record still counts if the abandoned chain was beating it.
11. **Language**: the group's language, as the host sets it in the config or at the announcement. This skill's files are in English; the game itself is played in the group's language.

## What this skill is not

- Not real-time: there is no imposed turn and no session to attend; the chain advances in the thread, at the group's pace, until the lives run out or the inactivity deadline is reached.
- Not a bot account: the referee writes from the host's own connected account, with the host's approvals. Players are told so in the announcement, including the honest note that, this game having no secrets, host-player mode protects nothing here beyond what the whole thread already sees.
