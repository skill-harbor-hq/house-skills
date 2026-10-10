# Group play through the user's connected messaging — the generic mechanism

How every group game in this skill plugs into the user's messaging. Written for any user of the skill: no group, account, platform, or real name is hardcoded anywhere. Game templates (e.g. `references/werewolf.md`) build on this mechanism and do not repeat it.

## Principle

The user's assistant runs the game as **referee**: it holds the complete, sealed game state in a file, publishes to the group only what everyone must know, and passes secret information only by private message to the one player concerned. The host group belongs to the user; the assistant never writes in it on its own initiative.

## (a) Connection and configuration

1. **The user connects their messaging** to their Muse assistant — Messenger first (a "Companion"-style connection: the assistant reads and writes in the user's personal conversations, in their name). Other platforms follow the same model when connected.
2. **The user designates THE host conversation**: the group (or thread) where games will be played. One active host group per game; it can change between games, never mid-game.
3. **The configuration lives in the USER's data, never in the skill.** The skill ships only an empty template (shown in `SKILL.md`, Data layer) for the user to copy into their data folder and fill there:
   - `players` = the group members who take part in games (a member can spectate: just leave them off the list).
   - No real identifier is written in the skill or in any shared file: only in the user's private data folder.
   - With no filled config, no group game starts: the assistant asks the user to designate the group and the players, then writes the config into their data.

## (b) The three roles of the system

| Role | Who | Powers and limits |
|---|---|---|
| **The host** | The user who owns the connection | Designates the group and the players; **approves every send** the assistant makes in their group under their connection's rules (exact message preview + explicit confirmation right before sending); can end a game at any time. |
| **The referee** | The assistant | Holds the sealed state (file), deals secrets privately, runs the phases, keeps deadlines, counts votes, rules by the game template. Takes no side: it does not play. |
| **The players** | The group members listed in the config | Receive their secrets privately, act in the thread or privately depending on the phase, vote. They never see the state or anyone else's secrets. |

## (b bis) Host-player mode — the host hosts AND plays (built in, not an exception)

A normal, designed-for case: the host wants to play in their own game. At launch, the host picks their mode: **player** or **spectator**. If they play, the problem to solve is approval: the general rule (exact preview of every send) would show them everyone else's secrets and spoil their game. Host-player mode settles it like this:

1. **Public messages** (announcement, phase openings, results, recap): unchanged — exact preview + the host's confirmation before every send.
2. **Secret messages** (role distribution, private action requests for a role, private results of a night action, relays between teammates): each secret message type has its own template; the host approves **once, before the first send of that type, the exact template**, with a marked slot (e.g. `[YOUR ROLE]`, `[RESULT]`). The referee fills the slot for each player and sends in 1:1 **without ever showing the filled version to the host**. The approved text is otherwise character-for-character what goes out.
3. **The referee shows a playing host statuses, never contents**: "night actions received: 2/2", never who did what. The host's own secret reaches them in 1:1 like any other player — that is where, and only where, they learn their own role.
4. **Honest limit, told to the players in the announcement**: the referee's messages leave from the host's account (it is their connection); protection of roles against a playing host is therefore procedural, not technical — the referee shows them nothing, and the host pledges not to go read other players' private threads. A game among people who trust each other, announced as such.
5. **If a secret reaches the playing host by accident** (wrong preview, wrong recipient): the referee declares it to the host immediately, without naming more of the content than necessary, and follows the game template's "compromised game" conduct (the referee stops everything; the host decides: restart the game with a new draw, or continue knowingly — never concealment).
6. **Spectator mode**: the host does not play; exact-preview approval applies to every send, secrets included — players are told in the announcement that the host sees what the referee sends from their account pass by.

## (c) Flow of a game

1. **Announcement** — The host asks for a game (game, target player count) and picks their mode (player or spectator, section b bis). The referee prepares the announcement message; the host approves it; it goes to the host thread: proposed game, number of seats, signup deadline, and — matching the host's mode — either the honest limit of host-player mode (procedural protection, see b bis point 4) or, in spectator mode, the fact that the host sees the referee's secret sends pass by.
2. **Signups** — Players sign up by replying in the thread (or by reaction, depending on the platform). The referee keeps the list in the state. When the count is right, the host confirms the launch.
3. **Dealing the secrets** — If the game has secret information (roles, cards, answers), the referee sends it **one by one, in a private 1:1 message to each player concerned**, through the host's connection. Never in the thread, never in bulk, never to the host for "manual relay". **If the host plays: apply host-player mode (section b bis) — one template per secret message type, approved once before its first send, filled versions never shown to the host.**
4. **Phases** — The game alternates per its template: public messages in the thread (phase openings/closings, debates, votes per the template) and private actions collected in 1:1 by the referee (secret actions). Each phase has a **deadline announced in the thread**; the referee closes the phase at the deadline, not before, unless every expected action has been received.
5. **Results** — The referee publishes the results in the thread (host-approved message): what the template's rules make public, and nothing more. Still-live secrets are never revealed by an intermediate result.
6. **End of game** — The referee publishes the final recap required by the template (only then may secrets be revealed, if the template provides for it), writes the result into the data (scores/history) and marks the state finished.

At every phase, the referee **re-reads the state from the file** and **rewrites it after every event** (the same discipline as solo play: the file is the truth, not conversation memory).

## (d) Standing rules

1. **The sealed state stays in the referee's file.** No draft, summary, or message prepared for the host contains live secrets (undealt roles, upcoming answers): if the host also plays, they must never see the key in a draft.
2. **The thread only ever receives public information.** The assistant writes in the group only what the referee must publish: announcements, phase openings/closings, results the template provides for. Never a secret, never a hint about a secret, never a confirmation or denial of a game rumor.
3. **Every send follows the host's connection rules.** On Messenger (Companion): sending on explicit request, **exact message preview shown to the host and explicit confirmation right before every send**; the assistant writes as the host's account — messages it drafts carry the 🤖 marker under the host's transparency rule. No unapproved background sending: this channel never delivers cron results, notifications, or monitoring output — the referee proposes, the host approves, then it goes.
4. **Secrets travel only in 1:1 to the player concerned.** A private message contains only its recipient's secret (and, if the template provides for it, team information that player is entitled to know — e.g. the identity of their teammates). The referee checks the recipient before every private send: a wrong recipient = a leak = the game is compromised (see the template for the conduct to follow).
5. **Deadlines and silence.** Phases close at the announced deadline. The referee may ask the host to nudge a silent player (in the thread, without ever saying what is awaited from them privately). Actions not received by the deadline count as abstentions, per the template.
6. **The host can stop everything.** On the host's request: the game is marked abandoned, the referee publishes a short closing message (approved) and nothing else; secrets may then be revealed in the final recap since the game no longer exists.
7. **Language**: the host group's language, as the host sets it in the config or at the announcement.

## (e) Platform variants

The model does not change: one connected user, one designated conversation, a referee-file, secrets in 1:1, host approvals. What varies by connected platform:

| Aspect | Messenger | WhatsApp (or other connected messaging) |
|---|---|---|
| Connection | Companion (the user's personal account) | The platform's equivalent connection, always in the user's name |
| Sends in the group | Exact preview + the host's explicit confirmation before every send; 🤖 on the assistant's messages | Same rules if the connection imposes them; otherwise the host approves every referee message before sending, with no exception invented by the skill |
| Votes | In the thread (replies) or a group poll if the platform offers one at play time | Same: native poll if available, otherwise written votes in the thread counted by the referee |
| Private messages to players | Existing 1:1 conversation with each player (resolve the 1:1 thread, never the group) | Same: always the player's individual thread on that platform |
| Automatic delivery | Forbidden: no cron/notification results through this channel | Same ban, all platforms |

If a capability is missing on the platform of the moment (no polls, no reachable 1:1), the referee tells the host BEFORE launch and proposes the template's fallback (hand-counted written votes) — never silent improvisation mid-game.
