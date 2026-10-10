# Werewolf, asynchronous — group game template

Runs on the generic mechanism in `references/group-messaging.md` (the user's connection, designated host group, approvals, secrets in 1:1) — this document defines only the game's rules and the referee's work. Werewolf is a public-domain social-deduction classic in principle; the rules below are rewritten and adapted to asynchronous play.

## The game in one sentence

A village, werewolves hidden among the villagers. At night, the wolves pick a victim and the seer probes one player. By day, the village debates and votes to eliminate a suspect. The referee (the assistant) holds every role in secret and runs the phases on fixed deadlines — nobody can accuse it of cheating, and no human needs to know the roles to host.

## Lineup by player count

A deliberately simple role set: **wolves, villagers, seer** from the start; **hunter** from 8 players; **witch** from 11 players only. Justification: each special role adds private exchanges per night (more refereeing time, more waiting risk); the witch, with two decisions a night, is the heaviest role — she only joins big games, where her impact is worth the complexity. The hunter is designed never to block the game (see his rule).

| Players | Wolves | Seer | Hunter | Witch | Villagers |
|---|---|---|---|---|---|
| 5 | 1 | 1 | — | — | 3 |
| 6 | 2 | 1 | — | — | 3 |
| 7 | 2 | 1 | — | — | 4 |
| 8 | 2 | 1 | 1 | — | 4 |
| 9 | 3 | 1 | 1 | — | 4 |
| 10 | 3 | 1 | 1 | — | 5 |
| 11 | 3 | 1 | 1 | 1 | 5 |
| 12 | 4 | 1 | 1 | 1 | 5 |

Minimum 5, maximum 12 for this template. Outside that range: the referee tells the host before the announcement and proposes waiting for more signups or launching another game.

## Dealing the roles — IN PRIVATE, always

1. Signups closed and list confirmed by the host (see `group-messaging.md`, flow of a game). At launch, the host picks their mode: **player** or **spectator** (see `group-messaging.md`, section b bis, host-player mode); the choice is recorded in the state (`config.host_mode`). If they play, the host is on the player list like everyone else.
2. The referee draws the roles at random and writes the **complete state into the game's file immediately** (sealed roles, see the schema) — **before any dealing message**.
3. **If the host plays**: apply host-player mode (`group-messaging.md`, section b bis) — before any dealing send, the referee submits to the host the **exact template** of the role message, with a marked slot (e.g. `[YOUR ROLE]`), for **one-time approval**. The referee then fills the template for each player and sends it in 1:1 **without ever showing the filled versions to the host**; the host receives their own role in 1:1 like any other player. The same rule applies to every other secret message type in the game (a role's private action request, the seer's probe result, the victim revealed to the witch, relays between wolves): one template per message type, approved once before its first send, filled versions never shown to a playing host. If the host is a spectator, the exact preview of each secret send applies, as for public messages.
4. The referee sends each player, **in 1:1**, a message containing only THEIR role (and its power, in one sentence):
   - Wolf: their role + the names of their fellow wolves (wolves know each other — legitimate team information, not a leak). A lone wolf in the game: the message says exactly that ("you are the only wolf"), without inventing a teammate.
   - Seer, hunter, witch, villager: their role alone. No other name, no other role.
5. Each player confirms privately ("received"). With no confirmation by the deadline the host set, the referee reports it to the host (never in the thread with details; if the host plays, only as a status — e.g. "confirmations received: 4/5" — with no secret content) before starting the first night.

### Secret templates — compliant examples (adapt to the game's language, never to the drawn roles)

Starting texts for the templates to have approved (host-player mode: once per type, before its first send; spectator mode: they serve as the basis for exact previews). The marked slots are the only elements that change from one send to the next.

- **Role**: "Werewolf — your secret role. You are: [YOUR ROLE]. [POWER IN ONE SENTENCE] [TEAM INFORMATION, OR NOTHING] Reply "received" in this private thread to confirm. Do not share this message."
- **Action request, wolf**: "Werewolf — night [NUMBER]. Send the referee, privately, the name of your victim for tonight, before [DEADLINE]."
- **Action request, seer**: "Werewolf — night [NUMBER]. Send the referee, privately, the name of the player you want to probe, before [DEADLINE]."
- **Probe result**: "Werewolf — your probe result. [PROBED PLAYER]: ["wolf" OR "not a wolf"]"
- **Witch request**: "Werewolf — night [NUMBER]. The wolves' victim is: [VICTIM]. Reply privately: "save", "kill [NAME]", or "nothing", before [DEADLINE]."
- **Wolf relay**: "Werewolf — night [NUMBER]. The pack's proposals are: [PROPOSED TARGETS]. Confirm your final choice privately, before [DEADLINE]."

## NIGHT phase (everything happens in private, through the referee)

Fixed order, each step collected in 1:1 against the same announced deadline:

1. **The wolves choose a victim — "private votes + relay" mechanism.** No discussion thread between wolves (one more thread = one more leak risk, and private threads between players are not guaranteed on every platform). Instead:
   - Each wolf privately sends the referee the name of their proposed target.
   - The referee **relays** to each wolf the targets proposed by the pack (target names only: "the proposals are: X, Y"), then each wolf privately confirms their final choice.
   - **Aggregation rule**: final unanimity → that victim. Persistent disagreement after the relay (with 3–4 wolves: no majority) → the referee breaks it by **drawing lots among the proposed targets**, and records it in the state log (a draw that can be verified after the game — the referee is neutral, the log proves it). A single wolf (5-player game): their choice stands, no relay.
   - A silent wolf at the deadline = abstention; if no wolf proposes, **no victim that night** (in the morning the referee announces the village had a quiet night, with no further detail).
2. **The seer probes one player.** They send a name privately to the referee; the referee answers privately, only: "wolf" or "not a wolf". No other information, ever. Silence = no probe.
3. **The witch (if in play) decides.** The referee privately reveals to her the name of the wolves' victim (that is HER role information). She replies privately: `save` (life potion, once per game), `kill <name>` (death potion, once per game), or `nothing`. Silence = `nothing`. Used potions are recorded in the state.
4. **The hunter does not act at night**, but their **standing target** (see below) must be current.

The referee closes the night at the deadline (or as soon as every expected action has been received) and applies the effects in the state: the wolves' victim (unless saved), the death potion's target if any.

## DAY phase (in the public thread)

1. **Morning announcement** (referee's message, host-approved): who was eliminated during the night — or a quiet night — **and the role of each eliminated player is revealed** (the rule decided below), then the number of players remaining, without saying how many wolves are left.
2. **Debate** — in the thread, until the announced vote deadline. The referee does not take part in the debate: it neither confirms nor denies ANY claim about a role, even a false one, even an obvious one. Its only public messages: deadline reminders (via the host) and the vote closing.
3. **Vote** — public, in the thread: each living player names one living player. If the group's platform offers a poll, the referee may use it (options = living players) if the host chose it at the announcement. One vote per player; a vote can be changed until the deadline, only the last one counts. Silence = abstention (counts neither for nor against anyone).
4. **Result** — at the deadline, the referee counts (from the state, not from memory), publishes the vote detail and the eliminated player's name, **reveals their role**, and applies chain effects (hunter, see below) before checking for a win.

### The revelation rule (decided)

**Every eliminated player — by night, vote, potion, or the hunter's shot — has their role publicly revealed by the referee.** Justification: in an asynchronous text game stretching over days, the information revealed at each elimination is the fuel of deduction; without it, debate runs dry and players drop off. Strict corollary: while a player is alive, the referee neither reveals nor lets slip their role, in any circumstance — not privately to another player (outside the wolves' team information), not in a summary to the host if the host plays.

## The hunter — standing target (asynchronous adaptation)

An eliminated hunter "fires one last shot". To never suspend the game waiting for the reaction of a player who has just been eliminated (and may be away for hours), the rule is adapted:

- From the deal onward, the hunter gives the referee, privately, the name of their **standing target**; they can change it at any time by a new private message, without justification.
- When the hunter is eliminated (night, vote, or potion), the referee **immediately** applies their current standing target: that player is eliminated, their role is revealed, and the event is announced in the same result message.
- With no standing target recorded: no shot (the referee reminded the hunter privately at the start of every night — the log shows it).

## Win conditions (checked after EVERY elimination, chains included)

- **The village wins** as soon as no wolf is left alive.
- **The wolves win** as soon as living wolves are as many as, or more than, living non-wolves (they control the day vote).
- On a win: the referee publishes the result, reveals **all** the roles (the game is over, secrecy has no object anymore), writes the result into the data history, and marks the state finished.

## The referee's work (reminder of the rules that protect the game)

1. **No leak, ever.** Same neutral wording for everyone: never "good lead", never a different reaction depending on whether an accusation targets a wolf or an innocent. In private as in public, the referee gives only the information the recipient's role provides for.
2. **Deadlines kept.** Every phase opening announces its deadline. Nudges to silent players: via the host, in the thread ("some night actions are still missing", never saying whose or what) or privately to the player concerned ("your werewolf game is waiting for your action before 9 pm" — with no game detail).
3. **Eliminated player = spectator.** They can read the thread; by the game rule announced at the start, they no longer debate, vote, or share anything they know or believe. The referee reminds them privately at elimination, politely, once.
4. **The state is the truth.** Re-read the file at every event, rewrite it after every event (role dealt, action received, vote, elimination, potion, draw). One file per game, kept by the referee alone.

## State schema — `games/<game-id>.json`

`game-id`: `werewolf-<YYYY-MM-DD>-<hhmm>` (prefix `TEST-` for a test game). Same discipline as a sealed key: roles are written before the first dealing message.

```json
{
  "id": "werewolf-2026-10-10-2100",
  "game": "werewolf",
  "status": "in_progress | finished | abandoned",
  "language": "en | fr",
  "created_at": "2026-10-10T21:00:00-04:00",
  "config": { "platform": "messenger", "conversation": "<the user's host group>", "host": "<host name>", "host_mode": "player | spectator" },
  "phase": { "type": "night | day", "number": 1, "deadline": "2026-10-10T23:00:00-04:00" },
  "players": [
    {
      "name": "<name in the group>",
      "role": "wolf | seer | hunter | witch | villager",
      "alive": true,
      "elimination": null,
      "hunter_target": null,
      "potions": { "life": true, "death": true }
    }
  ],
  "current_night": {
    "wolf_proposals": { "<wolf name>": "<proposed target>" },
    "wolf_final_choices": { "<wolf name>": "<final target>" },
    "wolf_victim": null,
    "seer_probe": { "target": null, "result": null },
    "witch_decision": null
  },
  "day_votes": { "<voter name>": "<voted name>" },
  "winner": null,
  "log": [
    { "time": "2026-10-10T21:05:00-04:00", "event": "roles_dealt" }
  ]
}
```

- `hunter_target` and `potions` only serve the roles concerned; `potions` stays `null` outside the witch (adapt the schema to the actual fill: do not invent empty fields elsewhere).
- The log records every dated event: dealing, actions received (without copying secrets outside the file — they exist ONLY there), relay, any draw, votes, eliminations, win. It is the proof of neutral refereeing, showable to the players after the game.

## Edge cases (decided)

- **Tie in the day vote**: immediate runoff between only the tied players (same short deadline announced by the referee, e.g. 2 h, or the end of day set at the announcement). Persistent tie → **nobody is eliminated that day**; play moves to the next night. (No host casting vote: the referee stays neutral.)
- **Tie or disagreement among the wolves**: see the night aggregation rule (relay, then a draw among the proposed targets, recorded in the log).
- **A player who stops answering**: their action counts as an abstention at each deadline. If they miss **two phases in a row**, the referee reports it to the host, who alone decides: the player stays (continued abstentions) or is **removed** from the game (announced in the thread with no role revelation; if the removal changes the balance, the referee checks for a win right away). The referee never removes a player on its own initiative.
- **Private send error** (a secret sent to the wrong recipient or into the thread): the game is compromised. The referee stops everything, says so frankly to the host in private, and the host decides: restart the game (new draw) or continue knowingly. Never concealment.
- **Abandoned game** (the host ends it, or nobody plays anymore): status `abandoned`, a short closing message in the thread (host-approved), roles revealed in that closing message only if the host asks — otherwise they stay in the file.
- **Counting dispute**: the referee republishes the vote detail as it stands in the state (the day vote detail is public by construction) and the log for night actions. The file settles it.
