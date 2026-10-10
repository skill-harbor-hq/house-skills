---
name: "photo-challenge"
description: "Run a Photo Challenge group game refereed by the assistant inside the user's own connected messaging group (Messenger first): on a rolling cycle, the referee announces a theme, players submit their own photo privately in 1:1, all accepted photos are republished together anonymized under letters for the vote, votes are reactions counted by the referee with self-votes discarded, and points build a season ranking. Use when the user wants a photo challenge, a défi photo, a photo contest, or a group photo game with their group."
---

# Photo Challenge — a rolling photo game for your group chat

Your assistant referees a Photo Challenge inside a group chat **the user owns and connects**. On a rolling cycle, the referee announces a **theme** ("something red", "my favourite corner"); each registered player photographs the theme in their own way and submits **one photo, taken by themselves**, privately to the referee. When submissions close, all accepted photos are republished **together**, under letters and without author names, and the group votes with **reactions**. The referee never judges anyone's taste: the voters judge the theme, the referee counts, and the host publishes. Points from each cycle build a **season ranking** that rewards regularity, not one evening of glory.

The game runs on an **honour system, announced as such**: a photo must be taken by the member who submits it, and the game promises **no technical verification** (no EXIF analysis, no detection of generated or found images). It is a game among people who trust each other, and the announcement says so.

The cycle is asynchronous and fixed in advance: by default **7 days** (submissions from day 1 to day 4 at 8 p.m., vote from day 5 at 9 a.m. to day 7 at 8 p.m., recap after). The next theme is announced the day after the recap is published, never before the current vote closes. 3 to 12 registered players; below 3 accepted submissions, a cycle does not go to a vote as it stands.

## What you need

- A Muse assistant (this skill installed).
- **To actually play**: a messaging account **the user connects to their own assistant** and one group conversation on it that the user designates as the game host. Messenger is the first supported connection; the model is platform-generic (see `references/group-messaging.md`, platform variants). Installing the skill files needs nothing else.
- The players' photos: each player takes and submits their own photo during the submission window.
- The assistant writes in the group **from the user's account** (that is how the connection works), and every public message needs the host's approval before it is sent. There is no fully automatic mode, and there never will be: the host approves, then it goes. The recap in particular only exists as a **prepared** text until the host approves it: the referee never declares a winner in the thread on their own initiative.

## Data layer (the skill ships none of it)

All game data lives in a data folder **the user owns**, never inside the skill. On first use, create it with the user (suggested default: `~/photo-challenge/`, any folder the user prefers works):

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

- `games/<cycle-id>.json` — one state file per cycle (schema in `references/photo-challenge.md`; the French source template names this folder `etats/`). It holds the cycle's config as written at creation, the approved theme, the windows and deadlines, every submission with its status (accepted, refused late, refused duplicate, exchanged, set aside off-topic, withdrawn for consent), the letter assigned to each accepted photo, the vote detail and count, the cycle ranking, and the recap status. The letter-to-author key lives **only** in this file until the recap.
- `photo-challenge-season.json` — the persistent season file (schema in `references/photo-challenge.md`; French source name: `defi-photo-saison.json`). It holds the planned number of cycles (8 by default), the themes already used, the finished cycles, and the cumulative ranking. It is updated **only when a cycle's recap is published**, never for a cycle still in progress. For a test season or cycle, ids carry the `TEST-` prefix.

No real identifier is ever written into the skill or a shared file: only into the user's private data folder. With no filled config, no group game starts: ask the user to designate the group and the players first.

## Router

| The user says | Do |
|---|---|
| "photo challenge", "défi photo", "photo contest", "concours photo", "partie de groupe", "play with my group", "jouer avec mon groupe" | Run a group game: read `references/group-messaging.md` (connection, configuration, approvals, host-player mode), then `references/photo-challenge.md` (the rules). No filled config → set it up first (see Data layer) |
| "continue the cycle", "on continue le cycle", "next theme", "prochain thème" | Re-read the current cycle's state file and resume from it — the file, not conversation memory, is the truth. Never announce the next theme while a recap is still waiting for approval |
| "what is the ranking", "c'est quoi le classement" | Read `photo-challenge-season.json` in the user's data folder and answer from the file |
| Any other group game by name | Be honest: Photo Challenge is the only group game in this skill. Others are not included and are never simulated or improvised |

## Running a cycle, in short

1. **Creation**: the referee writes the complete cycle state (config, theme approved by the host with the announcement, windows and deadlines) **before** the announcement. Nothing in the config changes mid-cycle. Defaults: 7-day cycle, deferred 1:1 collection, 2 reactions per voter, anonymity during the vote on, season points [5, 3, 2, 1].
2. **Announcement** in the group (host-approved): cycle number, theme, submission deadline, collection mode ("photo privately to the referee" by default), the coming vote deadline, and the rules in one line (one photo per member, taken by you, vote by reactions, no self-vote). Deadlines are written in words ("Thursday 8 p.m."), not only as timestamps.
3. **Collection**: each member sends their photo **privately, in 1:1, to the referee**, before the submission deadline, never in the thread during this window. The referee acknowledges receipt privately with a bare status ("received for cycle [N]"), with **no comment on the photo, ever**. Refusals are immediate and private: late (after the deadline), duplicate (the first photo received is kept; an explicit exchange before the deadline is allowed), or from an unregistered member. Every event is recorded in the state with its time.
4. **Close of submissions**: the referee freezes the list of accepted photos, draws the publication order at random (recorded in the log), assigns letters (A, B, C…), and prepares the vote-opening message. Any off-topic set-aside follows the bounded procedure in `references/photo-challenge.md` **before** this preparation (written reason in the state, host approval in private, the member warned privately, doubt keeps the photo). Below 3 accepted submissions: the referee tells the host before the vote opens and proposes a single 24-hour extension or merging with the next cycle.
5. **Opening of the vote** (host-approved): the accepted photos, **all together**, under their letters, **without author names** if anonymity is on, the vote deadline, and the budget reminder ("2 reactions, not on your own photo: it will not count"). The vote opens at that moment, not before: equal exposure is the point of the deferred collection.
6. **Vote**: voters place their reactions **on the photos themselves** in the thread, at most **1 per photo**, up to their budget (2 by default). **Any reaction counts for 1**; there is no emoji hierarchy. A member may vote without having submitted, and a member whose submission was refused votes normally. The referee says nothing in the thread during the vote, reacts to no photo, and may only send a deadline reminder if the host asks. If the platform cannot do reactions on the photos, the written fallback announced **in the vote-opening message itself** applies ("I vote for [LETTER(S)]" in the thread, same budget, same self-vote exclusion).
7. **Close and count**: at the deadline, the referee counts **from the thread re-read at closing and from the state**, never from memory: raw totals per photo, exclusion of self-votes (a photographer's reaction on their own photo is discarded at counting, recorded by name in the state only, **never named in the thread**), exclusion of out-of-window reactions (direct-thread mode) and of non-members, then the valid total per photo, which is the cycle score.
8. **Recap PREPARED**: the referee drafts the complete recap (winner, ranking with letters revealed, valid totals, season points, one line with the count detail: total reactions and exclusions by category, no names), submits it to the host **privately**, marked **waiting for approval**. **Nothing is published at this stage**, and the season file is not yet updated.
9. **Publication**: only after the host's explicit approval does the recap go to the thread; only then does the referee update the season file, mark the cycle finished, and log the publication.

## Standing rules (they protect the game)

1. **The voters judge the theme, not the referee.** Whether a photo embodies the theme well, is beautiful, funny or touching is what the vote says, never the referee. The referee comments on **no photo** before the end of the vote, in public, in private, or to the host: the same bare acknowledgement for everyone, the same wording.
2. **Equal exposure.** All photos of a cycle become visible **at the same time**, when the vote opens. Nobody collects reactions while the others are still photographing.
3. **Honour system, stated as such.** The photo must be taken by the member who submits it (an archive photo of one's own is allowed; the game asks for no proof of date). Light retouching (cropping, brightness) is allowed; a montage that fabricates the scene is no longer the theme's photo, and the voters will judge it anyway. No technical verification is promised or performed, and the referee runs no investigation and accuses nobody.
4. **One photo per member per cycle.** The first received is kept; a second is refused as a duplicate in private, unless the member explicitly asks to exchange it before the deadline, in which case the last requested version stands and the state keeps the trace of both. After the deadline, no exchange.
5. **Deadlines hold.** The windows close at the announced times. A submission one minute late is **refused, without exception and without negotiation**, recorded in the state (received time against deadline); the late member votes normally in the cycle. Reopening a window "just this once" would destroy the rule for every following cycle.
6. **Self-vote excluded, never denounced.** A photographer's reaction on their own photo is not counted. It is not a fault and is never named in the thread; the recap publishes the totals **after** exclusion and, in one line, the number of exclusions. Reactions beyond a voter's budget: only the first ones, in chronological order, count up to the budget.
7. **Bounded off-topic power.** The referee never judges the quality of an interpretation of the theme: a clever, distant or funny reading is exactly what the voters reward or not. A submission may be set aside only if it is **manifestly unrelated** to the theme, and only by the bounded procedure (reason written in the state before the vote opens, host approval in private with the photo and the reason, member warned privately before the vote opens, **doubt keeps the photo**). A photo that has gone to the vote can never be set aside afterwards.
8. **Consent comes first.** A member who submits guarantees that recognizable people in the photo agree to appear in the group. A photo reported before the vote opens as showing a non-consenting person is withdrawn without debate in the thread (the member may submit another before the deadline); after the vote opens, withdrawal stays possible at any time at the request of the person concerned, relayed by the host, and the recap notes it in one neutral line.
9. **Points and ties.** Cycle ranking by valid total, descending. Season points by rank: [5, 3, 2, 1] by default (1st 5, 2nd 3, 3rd 2, 4th and below with an accepted submission 1, no accepted submission 0). **A tie at the vote means tied winners**: same rank, same points for that rank, the next rank shifted by the number of tied photos (competition ranking: 1, 2, 2, 4). No tiebreak, no lightning round, no casting vote, in the lead as anywhere else, even in the season's last cycle.
10. **The state file is the truth.** The referee re-reads the state at every event and rewrites it after every event (submission, refusal, set-aside, opening, closing, count, recap status). The letter-to-author key and the set-aside reasons leave the state only at the recap (for the authors). No draft shown to the host for approval reveals an author while anonymity is active: the host approves the vote message exactly as the group will see it, letters included, without the key. **No entry in any scores file**: a cycle's result lives in its state and in the season file.
11. **The host publishes, the referee prepares.** Announcement, vote opening, recap: three public messages, three approvals. A recap waiting for approval for more than a cycle: the referee flags it to the host and does not announce the next theme until the ranking is published; the rolling game must not run ahead of its own results.
12. **The host can stop everything** at any time: the cycle is marked abandoned, a short closing message goes out (host-approved), no season points are awarded, and the season file is untouched; the theme may be proposed again later.
13. **Language**: the group's language, as the host sets it in the config or at the announcement. This skill's files are in English; the game itself is played in the group's language.

## What this skill is not

- Not a photography contest judged by an expert: there is no jury and no aesthetic verdict from the referee, only the group's reactions, counted by written rules.
- Not real-time: a cycle runs over days, at the group's pace, inside announced windows.
- Not a bot account: the referee writes from the host's own connected account, with the host's approvals. Players are told so in the announcement, including the honest note that, in host-player mode, the host approves the vote message exactly as the group sees it, without the letter-to-author key.
