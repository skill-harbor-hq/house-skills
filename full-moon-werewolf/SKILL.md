---
name: "full-moon-werewolf"
description: "Run an asynchronous Werewolf (Loup-garou / Mafia-style social deduction) game for a group, refereed by the assistant inside the user's own connected messaging group (Messenger first): secret roles by private message, sealed state file, night and day phases on deadlines, public votes, and a built-in host-player mode for a host who also plays. Use when the user wants a group game, a werewolf game, a partie de groupe, or a partie de loup-garou with their group."
---

# Full Moon Werewolf — a werewolf game for your group chat

Your assistant referees an asynchronous game of Werewolf (the classic social-deduction game: hidden werewolves among villagers) inside a group chat **the user owns and connects**. The assistant holds every role in a sealed state file, sends secrets only by private 1:1 message, runs night and day phases against announced deadlines, counts the votes, and reveals each eliminated player's role. No human has to know the roles to host, and the referee cannot be accused of cheating: its state file and event log are the proof.

The game is asynchronous on purpose: a round takes hours, not minutes, so a real group can play around real life. Minimum 5 players, maximum 12.

## What you need

- A Muse assistant (this skill installed).
- **To actually play**: a messaging account **the user connects to their own assistant** and one group conversation on it that the user designates as the game host. Messenger is the first supported connection; the model is platform-generic (see `references/group-messaging.md`, platform variants). Installing the skill files needs nothing else.
- The assistant writes in the group **from the user's account** (that is how the connection works), and every public message needs the host's approval before it is sent. There is no fully automatic mode, and there never will be: the host approves, then it goes.

## Data layer (the skill ships none of it)

All game data lives in a data folder **the user owns**, never inside the skill. On first use, create it with the user (suggested default: `~/full-moon-werewolf/`, any folder the user prefers works):

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

- `games/<game-id>.json` — one sealed state file per game (schema in `references/werewolf.md`). Roles live only there.
- `history.json` — finished games (date, players, winner), if the user wants a record.

No real identifier is ever written into the skill or a shared file: only into the user's private data folder. With no filled config, no group game starts: ask the user to designate the group and the players first.

## Router

| The user says | Do |
|---|---|
| "werewolf game", "loup-garou", "partie de groupe", "play with my group", "jouer avec mon groupe" | Run a group game: read `references/group-messaging.md` (connection, configuration, approvals, host-player mode), then `references/werewolf.md` (the rules). No filled config → set it up first (see Data layer) |
| "continue the game", "on continue la partie" | Re-read the current game's state file and resume at the current phase — the file, not conversation memory, is the truth |
| Any other group game by name | Be honest: Werewolf is the only group game in this skill. Others are not included and are never simulated or improvised |

## Running a game, in short

1. **Setup**: host designates the group and players in the config; the host picks their mode, **player** or **spectator** (host-player mode, `references/group-messaging.md` section b bis).
2. **Announcement** in the group (host-approved): the game, seats, signup deadline, and the honesty note that matches the host's mode.
3. **Signups** in the thread; when the count is right, the host confirms the launch.
4. **Roles**: drawn at random, written **immediately** into the sealed state file, then sent one by one in private 1:1 messages — never in the thread.
5. **Night / day phases** on announced deadlines, per `references/werewolf.md`. The referee re-reads the state file at every event and rewrites it after every event.
6. **End**: final recap in the thread (all roles revealed only then), result written to the data history, state marked finished.

## Standing rules (they protect the game)

1. **Sealed state**: roles and pending secrets exist only in the game's state file. No draft, summary, or message prepared for the host ever contains a live secret.
2. **The thread only gets public information**: announcements, phase openings/closings, results the rules make public. Never a secret, never a hint, never a confirmation or denial of a game rumor.
3. **Every send follows the host's connection rules**: exact preview + the host's explicit confirmation right before each public send. Exception, by design: in host-player mode, secret messages go out on a **template the host approves once per message type**, filled by the referee and never shown filled to the host (see `references/group-messaging.md`, b bis).
4. **Secrets travel only in 1:1 to the player concerned**, and only their own secret (plus legitimate team information, e.g. a wolf's packmates). Check the recipient before every private send: a wrong recipient leaks the game.
5. **Deadlines hold**: phases close at the announced deadline; a missing action is an abstention. Reminders never say what is awaited from whom.
6. **The host can stop everything** at any time: the game is marked abandoned, a short closing message goes out (host-approved), and roles are revealed in it only if the host asks.
7. **Language**: the group's language, as the host sets it in the config or at the announcement. This skill's files are in English; the game itself is played in the group's language.

## What this skill is not

- Not real-time: if your group wants a fast, same-evening game around a table, this is the wrong tool.
- Not a bot account: the referee writes from the host's own connected account, with the host's approvals. Players are told so in the announcement, including the honest limit of host-player mode (secrecy toward a playing host is procedural, not technical — the referee shows him nothing, and he pledges not to open other players' private threads).
