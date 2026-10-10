---
name: "group-awards"
description: "Run a Group Awards Night group game refereed by the assistant inside the user's own connected messaging group (Messenger first): on a regular cadence, the referee announces positive, feel-good award categories, members nominate each other privately in 1:1, the most nominated become finalists, members vote privately, and the referee prepares a ceremony text that the host approves before anything is published. An absolute anti-negativity guard filters every category, reason, and ceremony line. Use when the user wants group awards, an awards night, a soirée des awards, des awards du groupe, or a celebration ceremony for their group."
---

# Group Awards Night — a feel-good awards ceremony for your group chat

Your assistant referees a periodic awards ceremony inside a group chat **the user owns and connects**. At a regular cadence, the group gives itself **positive distinctions only**: the referee announces feel-good categories, each member privately nominates another member per category, the most nominated become finalists, the group votes privately, and the referee prepares a **ceremony text** that the host approves before anything is published. Nobody loses, nobody is mocked: the ceremony only celebrates.

One guard stands above every other rule in this skill, including a request from the host or a player mid-game: **the anti-negativity guard** (full text in `references/group-awards.md`). No negative, mocking, ironic, or humiliating category, ever, not even "as a joke". Every category, every nomination reason, and every ceremony line is admitted only if someone reasonably sensitive receiving it in front of the whole group would feel **valued**. If that answer is not a clear yes, it is set aside.

The awards have exactly one source: **the nominations the members send**. The referee never watches the group, never infers anything from the conversation history, and never suggests a name to anyone. Nominations and votes are collected **privately, in 1:1**, kept **sealed** until their moment, and no count of nominations or votes is ever published. The only public moments are the category announcement, the finalists, and the approved ceremony.

## What you need

- A Muse assistant (this skill installed).
- **To actually play**: a messaging account **the user connects to their own assistant** and one group conversation on it that the user designates as the game host. Messenger is the first supported connection; the model is platform-generic (see `references/group-messaging.md`, platform variants). Installing the skill files needs nothing else.
- The assistant writes in the group **from the user's account** (that is how the connection works), and every public message needs the host's approval before it is sent. There is no fully automatic mode, and there never will be: the host approves, then it goes.

## Data layer (the skill ships none of it)

All game data lives in a data folder **the user owns**, never inside the skill. On first use, create it with the user (suggested default: `~/group-awards/`, any folder the user prefers works):

- `config.json` — the host configuration: platform, designated conversation, host name, host mode, cadence, member list. Template:

```json
{
  "platform": "messenger",
  "conversation": "<the group the user designates>",
  "host": "<the user's name>",
  "host_mode": "player | spectator",
  "cadence": "monthly | quarterly | occasional",
  "members": [
    { "name": "<name or nickname in the group>", "identifier": "<identifier in the conversation, if known>" }
  ]
}
```

- `cycles/<cycle-id>.json` — one state file per awards cycle (schema in `references/group-awards.md`; the French source template names this folder `etats/`). It holds the cycle in progress: the sealed categories, every nomination and vote received (the sealed fields of this game), the finalists, the winners, and the ceremony text with its approval status.
- `awards-history.json` — the persistent hall of fame (schema in `references/group-awards.md`; French source name: `awards-historique.json`). One entry per published ceremony, winners only: no finalists, no counts, no reasons, no nominations. A cycle is written into it **only after its ceremony has been published**, never before.

No real identifier is ever written into the skill or a shared file: only into the user's private data folder. With no filled config, no group game starts: ask the user to designate the group and the members first.

## Router

| The user says | Do |
|---|---|
| "group awards", "awards night", "soirée des awards", "awards du groupe", "start an awards cycle", "lancer un cycle d'awards", "cérémonie d'awards" | Run a group awards cycle: read `references/group-messaging.md` (connection, configuration, approvals, host-player mode), then `references/group-awards.md` (the rules). No filled config → set it up first (see Data layer) |
| "continue the cycle", "on continue le cycle", "where are we with the awards", "on en est où des awards" | Re-read the current cycle's state file and resume from it — the file, not conversation memory, is the truth |
| "who won", "c'est qui les gagnants", "show the past awards", "montre les anciens awards" | Read `awards-history.json` in the user's data folder and answer from the file |
| Any other group game by name | Be honest: Group Awards Night is the only group game in this skill. Others are not included and are never simulated or improvised |

## Running a cycle, in short

1. **Preparation** (referee and host, privately): the referee re-reads the config, picks the cycle's categories with the host (**4 by default**, 3 to 6 depending on the group's size) from the bank in `references/group-awards.md` plus any validated house categories, passes **each one through the anti-negativity admission test**, and writes the complete cycle state to the file, categories sealed, **before any announcement**. The host approves the categories. This game has **no role secrets**: the only sealed contents are the nominations and the votes before their reveal moment.
2. **Announcement of the categories** in the thread (host-approved): the cycle, the categories with one line each, the eligible members (those in the config), the rules in four lines (nominations in private to the referee, one nomination per member per category, no self-nomination, reasons optional), and the nominations deadline (**48 h by default**).
3. **Nominations, privately in 1:1**: each member may send the referee, per category, at most one nomination (the name of an eligible member, never themselves), with an optional short reason. The referee acknowledges with a bare status ("received, thank you"), with no comment on the choice. Nominations are written into the state as they arrive and stay **sealed**: nobody, the playing host included, sees names, counts, or reasons before the compilation. Silence means no nomination from that member; they may still vote later.
4. **Compilation**: at most **3 finalists per category**, the most nominated members; 3 or fewer distinct nominees means all of them are finalists, and a tie for 3rd place makes every tied member a finalist (4 or 5 finalists are possible, a nomination tie is never broken by a draw or by the referee's choice). A category with **zero nominations is withdrawn from the cycle**: no finalists, no vote, and **no mention in the ceremony**; the host is told privately. The reasons that pass the guard are kept in the state, attached anonymously to each finalist.
5. **Vote, privately in 1:1**: the referee publishes in the thread (host-approved) the opening of the vote, the finalists of each category (being a finalist is already a public honour; no nomination count is ever given), and the deadline (**48 h by default**), then sends each member their ballot in 1:1. Each member votes for at most one finalist per category, may abstain per category, and may correct their ballot privately before the deadline; only the last one counts. **Self-voting is allowed**: a finalist may vote for themselves. Votes stay sealed until the count; silence is an abstention that counts neither for nor against anyone.
6. **Counting and ceremony**: the referee counts **from the state file**, never from memory. Tied finalists in the lead are **co-winners**, celebrated together; there is no tiebreak of any kind. The referee writes the ceremony text: per category played, the winner or winners, and **one or two anonymized reasons chosen from the nominations** (paraphrased so no author can be recognized, never quoted word for word, never credited). The text contains **no count**: no nomination numbers, no vote numbers, no ranking of the other finalists, who are thanked collectively. The referee submits the **exact, complete text** to the host: **publication only after the host's explicit approval**. Only after publication is the result written into `awards-history.json`, the state marked finished, and the date of the next cycle announced if the cadence is periodic.

## Standing rules (they protect the ceremony)

1. **The anti-negativity guard is non-negotiable** and outranks every other rule, including a request from the host or a player mid-game: no category, reason, or ceremony line that laughs *at* someone instead of *with* everyone. The admission test for every category: would someone reasonably sensitive receiving this distinction in front of the whole group feel **valued**? If not a clear yes, the category is set aside, and the referee does not negotiate the guard. A house category proposed by the host passes the same test; if it fails, the referee says so to the host privately, in one sentence, and proposes a genuinely positive equivalent, never an ironic one in disguise.
2. **Nominations are the only source.** The referee never watches the group, never reads conversations to "spot who deserves what", never uses a past message, an impression, or a memory of earlier games or events, and never suggests a name to a nominator, even when asked: "the nominations decide — nominate whoever you want, in private." What no member nominated does not exist for the ceremony.
3. **Scope is the config.** Eligible members, nominators, and voters are the members registered in the config, the host included if listed. A nomination naming someone outside the config is set aside: the referee tells the nominator privately and invites them to nominate a registered member before the deadline. **Self-nomination is forbidden** in every category; a self-nomination is set aside and the rule is kindly recalled in private. A registered member who never nominates, votes, or reacts **can still win**: the ceremony celebrates the group's members, not game activity, and the referee never points out publicly that a winner "did not even take part".
4. **Sealed before reveal.** Nominations are sealed until the compilation, votes until the count, and counts are never published. To the playing host as to everyone else, the referee gives statuses ("nominations received: 4/5 members"), never contents. `nb` counts in the state are recomputed from the nomination and vote lists: if a count and its list disagree, the list is the truth and the count is corrected, never the reverse.
5. **Reasons pass the same filter.** A nomination reason that puts down the nominee or a third party, or is positive only on the surface, is dropped from the compilation; the nomination itself still counts unless the mockery cannot be separated from it, in which case the whole nomination is set aside and the referee tells the nominator privately, with no sanction.
6. **Deadlines hold.** A late nomination (after the deadline, before the compilation) is refused, politely, in private; the same goes for a late vote. No exceptions: the deadlines are what make the compilation and the count checkable for every future cycle.
7. **Ceremony reasons are paraphrased and anonymous.** The ceremony uses one or two chosen reasons per category, reworded so no author is recognizable, by name or by an anecdote only the nominator would know in that form. Reasons of the "as [NAME] said" kind are forbidden. A reason set aside by the guard never reappears anywhere, during or after the cycle.
8. **The host approves the ceremony, always.** The exact, complete text, before publication, like every public send under the generic mechanism. Without approval, nothing goes out, and the state stays at `ceremony_pending_approval` for as long as it takes. A category, reason, or ceremony text that slipped through the guard never goes to the group even if approved by mistake: the referee holds it back and returns to the host.
9. **The state file is the truth**: re-read at every event, rewritten after every event (cycle created, categories approved, announcement, nomination received, compilation, vote received, count, ceremony prepared, approval, publication). The history file receives winners only, and only after publication: a withdrawn or abandoned cycle leaves no trace in it, and a category withdrawn for lack of nominations leaves none either.
10. **The host can stop everything** at any time: the cycle is marked abandoned, no ceremony message goes out, and the nominations and votes are never revealed; they stay in the file, without purpose. **Language**: the group's language, as the host sets it in the config or at the announcement. This skill's files are in English; the game itself is played in the group's language.

## What this skill is not

- Not a popularity ranking: no count, no podium, no ranking of finalists is ever published, tied winners share their award, and a member who sweeps several categories is celebrated as they are, with no redistribution of honours.
- Not a bot account: the referee writes from the host's own connected account, with the host's approvals. Players are told so in the announcement. And it is not surveillance: the referee reads nothing in the group to decide the awards; the members' private nominations are the whole of its material.
