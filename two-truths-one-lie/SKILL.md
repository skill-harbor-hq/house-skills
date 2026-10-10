---
name: "two-truths-one-lie"
description: "Run a 'Two Truths, One Lie' group game refereed by the assistant inside the user's own connected messaging group (Messenger first): a rotating featured player privately gives two true statements and one lie, the key stays sealed in the referee's state file, the other players vote privately, and the featured player scores 1 point per fooled voter capped at 2. Use when the user wants a group game, a two truths one lie game, a partie de groupe, or a partie de deux vérités un mensonge with their group."
---

# Two Truths, One Lie — a bluffing game for your group chat

Your assistant referees a game of Two Truths, One Lie inside a group chat **the user owns and connects**. In turn, each player is the featured player: they privately give the referee three short statements about themselves, two true and one false, and say which one is the lie. The referee checks the statements, seals which one is the lie in its state file before anything is published, then publishes the three statements in a shuffled order. The other players vote privately for the statement they believe is the lie. At the deadline the referee reveals the lie, the votes, and the points.

The game is asynchronous on purpose: a turn takes hours, not minutes, so a real group can play around real life. Minimum 3 players, recommended 4 to 8. One game is one complete cycle: every registered player is featured exactly once, in the order of the rotation queue recorded in the state.

## What you need

- A Muse assistant (this skill installed).
- **To actually play**: a messaging account **the user connects to their own assistant** and one group conversation on it that the user designates as the game host. Messenger is the first supported connection; the model is platform-generic (see `references/group-messaging.md`, platform variants). Installing the skill files needs nothing else.
- The assistant writes in the group **from the user's account** (that is how the connection works), and every public message needs the host's approval before it is sent. There is no fully automatic mode, and there never will be: the host approves, then it goes.

## Data layer (the skill ships none of it)

All game data lives in a data folder **the user owns**, never inside the skill. On first use, create it with the user (suggested default: `~/two-truths-one-lie/`, any folder the user prefers works):

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

- `games/<game-id>.json` — one sealed state file per game (schema in `references/two-truths-one-lie.md`). It holds, per turn: the rotation queue, the featured player's final statements and the sealed key (which published statement is the lie), the private votes, and the scores. The key is written there before any publication and lives only there until the reveal.
- `history.json` — finished games (date, players, scores, winners), if the user wants a record.

No real identifier is ever written into the skill or a shared file: only into the user's private data folder. With no filled config, no group game starts: ask the user to designate the group and the players first.

## Router

| The user says | Do |
|---|---|
| "two truths one lie", "deux vérités un mensonge", "partie de groupe", "play with my group", "jouer avec mon groupe" | Run a group game: read `references/group-messaging.md` (connection, configuration, approvals, host-player mode), then `references/two-truths-one-lie.md` (the rules). No filled config → set it up first (see Data layer) |
| "continue the game", "on continue la partie" | Re-read the current game's state file and resume at the current turn and phase — the file, not conversation memory, is the truth |
| Any other group game by name | Be honest: Two Truths, One Lie is the only group game in this skill. Others are not included and are never simulated or improvised |

## Running a game, in short

1. **Setup**: host designates the group and players in the config; the host picks their mode, **player** or **spectator** (host-player mode, `references/group-messaging.md` section b bis). The rotation queue is the registration order, frozen in the state at launch. Default deadlines, adjustable by the host at the announcement and written into the state: 24 hours to collect the featured player's statements, 12 hours to vote.
2. **Announcement** in the group (host-approved): the game, the rotation order, the scoring (correct guesser +1; featured player +1 per fooled voter, capped at 2 per turn), the honour rule (a player who already knows a statement is true or false declares it privately to the referee and abstains on that turn, with no reason given in the thread), and the deadlines.
3. **Collection, privately**: the referee asks the featured player in 1:1 for 3 short statements, 2 true and 1 false, and the featured player designates, in that same private reply, which one is the lie. No other player ever sees the collection.
4. **Quality gate, before anything is published**: the referee checks plausibility, comparable level of detail, verifiability in principle, absence of anything sensitive, and short self-contained form. A sensitive or unverifiable statement is blocking: it is replaced before publication, privately, without revealing anything about which statement is the lie. A statement that is too obvious, or noticeably less detailed than the other two, is advisory: the referee asks once, and the featured player may keep it at their own points risk. At most one adjustment is requested per turn. A replaced statement is never kept in the state and never circulates anywhere.
5. **Sealed key, then publication**: the referee shuffles the order, writes the final statements, the numbered publication order, and the key into the state — the seal happens before the publication message, never after — then publishes the 3 numbered statements in the thread with the voting instruction and the deadline. From publication on, neither the statements nor the key changes.
6. **Votes, privately**: every registered player except the featured player votes in 1:1, one number only. Votes are private so a visible vote cannot anchor the following ones. A vote may be changed until the deadline; only the last ballot counts. The referee acknowledges each vote with a bare "received" and may announce in the thread only a bare count ("votes received: 2/3"), never a content. Silence at the deadline is an abstention.
7. **Reveal at the deadline** (or as soon as every expected vote is in): the referee publishes, in one message, the lie, the detail of the votes with abstentions named as abstentions, the turn's points, and the cumulative standings; updates the state before asking the next featured player. The featured player may then recount their two truths in the thread if they wish; the referee never does it for them.
8. **End**: after the last turn of the cycle, the final standings are published and written into the state; a tie at the top means co-winners, with no improvised tiebreaker.

Scoring is fixed before the game and never changed during a cycle: a correct guesser scores **+1**; a fooled guesser scores 0; the featured player scores **+1 per fooled voter, capped at 2 points per turn**; an abstention scores 0 and earns the featured player nothing; a skipped or cancelled turn scores nothing for anyone.

## Standing rules (they protect the game)

1. **Private collection, sealed key**: the three statements are collected privately from the featured player, who designates the lie in that same private exchange. The key — which published statement is the lie — is written into the sealed state file before any publication and never leaves it until the reveal. The referee never reveals, notes in public, or comments on which statement is the lie, at any moment before the reveal, including in a gate adjustment request, a message to the host, or a recap.
2. **Private votes**: votes are cast in 1:1 to the referee, never in the thread, so no vote can anchor the next ones. No vote content is visible to anyone before the simultaneous reveal.
3. **The gate protects the turn**: an unverifiable statement (a pure taste, opinion, or feeling nobody could be right or wrong about) or a sensitive statement (health, money, intimate life, conflicts, third parties) is replaced before publication; the replacement request names only the gate reason, in the private collection thread, and reveals nothing about the lie. The discarded statement is not kept in the state and is shown nowhere.
4. **Capped featured score**: the featured player earns 1 point per voter fooled into picking a true statement, capped at 2 per turn, for every featured player whatever the group size, so no single bluff can win a whole cycle.
5. **The featured player never votes on their own turn**, not even for fun: their ballot would distort the count of the fooled.
6. **Honour rule**: a player who already knows, outside the game, that a statement is true or false declares it privately to the referee before voting and abstains on that turn; the abstention is announced at the reveal as an ordinary abstention, without a reason. A declaration after voting but before the reveal withdraws the ballot.
7. **Sealed state, thread gets only public information**: statements awaiting publication, the key, and unrevealed votes exist only in the game's state file. No draft, summary, or message prepared for the host ever contains the key or an unrevealed vote; in host-player mode, the collection instruction goes out on a template the host approves once, filled versions never shown to a playing host.
8. **Every send follows the host's connection rules**: exact preview + the host's explicit confirmation right before each public send. Exception, by design: in host-player mode, secret messages go out on a **template the host approves once per message type**, filled by the referee and never shown filled to the host (see `references/group-messaging.md`, b bis).
9. **Deadlines hold**: phases close at the announced deadline; silence is an abstention. The referee re-reads the state file at every event and rewrites it after every event.
10. **The host can stop everything** at any time: the game is marked abandoned, a short closing message goes out (host-approved), and the keys of unrevealed turns are revealed in it only if the host expressly asks.
11. **Language**: the group's language, as the host sets it in the config or at the announcement. This skill's files are in English; the game itself is played in the group's language.

## What this skill is not

- Not real-time: if your group wants a fast, same-evening game around a table, this is the wrong tool.
- Not a bot account: the referee writes from the host's own connected account, with the host's approvals. Players are told so in the announcement, including the honest limit of host-player mode (secrecy toward a playing host is procedural, not technical — the referee shows them nothing, and they pledge not to open other players' private threads).
