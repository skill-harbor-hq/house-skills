---
name: "caption-contest"
description: "Run a Caption Contest for a group, refereed by the assistant inside the user's own connected messaging group (Messenger first): one photo per round, captions collected privately and published anonymized and shuffled, blind voting with no self-vote, authors revealed only after counting, and a fixed points grid. Use when the user wants a caption contest, a caption game, a concours de légendes, or a légendes game with their group."
---

# Caption Contest — a blind caption game for your group chat

Your assistant referees a Caption Contest inside a group chat **the user owns and connects**. A photo is posted in the group. Each player sends their funniest caption for it **in private to the referee**, before the deadline. The referee publishes every retained caption **anonymized and shuffled**, with no name attached. The group votes — never for its own caption — and only after counting does the referee reveal who wrote the winning caption, and every other caption. The fun is in laughing at the texts first and discovering their authors afterwards: in fact, nobody signed them.

The game is asynchronous on purpose: collection, publication, voting, and revelation each run against an announced deadline, so a real group can play around real life. Players: 4 to 8 registered players (recommended: 4 to 6). A game is 3 photos by default (1 = express, 5 = long, if the host asks); rounds are played one at a time, never in parallel.

## What you need

- A Muse assistant (this skill installed).
- **To actually play**: a messaging account **the user connects to their own assistant** and one group conversation on it that the user designates as the game host. Messenger is the first supported connection; the model is platform-generic (see `references/group-messaging.md`, platform variants). Installing the skill files needs nothing else.
- The assistant writes in the group **from the user's account** (that is how the connection works), and every public message needs the host's approval before it is sent. There is no fully automatic mode, and there never will be: the host approves, then it goes.

## Data layer (the skill ships none of it)

All game data lives in a data folder **the user owns**, never inside the skill. On first use, create it with the user (suggested default: `~/caption-contest/`, any folder the user prefers works):

- `config.json` — the host configuration: platform, designated conversation, host name, player list, and the host's mode. Template:

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

- `games/<game-id>.json` — one sealed state file per game (schema in `references/caption-contest.md`). The code-to-author table of each round lives only there, written before that round's publication.
- There is no separate scores file for this game: the contest standings live in the game's state file.

No real identifier is ever written into the skill or a shared file: only into the user's private data folder. With no filled config, no group game starts: ask the user to designate the group and the players first.

## Router

| The user says | Do |
|---|---|
| "caption contest", "concours de légendes", "caption game", "play caption contest with my group", "jouer au concours de légendes" | Run a group game: read `references/group-messaging.md` (connection, configuration, approvals, host-player mode), then `references/caption-contest.md` (the rules). No filled config → set it up first (see Data layer) |
| "continue the contest", "on continue le concours", "next round", "prochaine manche" | Re-read the current game's state file and resume at the current phase — the file, not conversation memory, is the truth |
| Any other group game by name | Be honest: Caption Contest is the only group game in this skill. Others are not included and are never simulated or improvised |

## Running a game, in short

1. **Setup**: host designates the group and players in the config; the host picks their mode, **player** or **spectator** (host-player mode, `references/group-messaging.md` section b bis); the number of rounds is set (3 by default). If the player count is outside 4 to 8, the referee says so to the host before any announcement and proposes waiting for signups or launching another game.
2. **Photo**: exactly one photo per round, chosen before collection opens, from one of only two admitted sources (see `references/caption-contest.md`): provided by the host (with the written conditions there — the right to share it, no one in a sensitive or embarrassing situation, no identifiable minor without a parent's agreement — republished under a neutral filename with no metadata), or generated or chosen by the assistant at the host's request, with the host approving the exact image before publication.
3. **Round opening** in the group (host-approved): the photo, the round number, the **collection deadline**, the **voting mode of the round** (chosen at the announcement, never changed afterwards), the maximum caption length (200 characters, 2 sentences at most), and the three reminders players confuse most: captions go **in private to the referee, never in the thread**; **never vote for your own caption**; a caption that identifies its author will be **sent back for rewording**.
4. **Collection — in private, one per player.** Each player sends one caption in 1:1 to the referee before the deadline. The referee acknowledges receipt privately with a bare status and no comment on the text. A player may replace their caption before the deadline; only the last version received in time counts. At reception, the referee runs the anonymity check (see Standing rules): a self-identifying caption is returned privately, by problem category only, for rewording before the same deadline, with no individual extension. At the deadline, collection closes: **3 retained captions or more** → the round goes to publication; **fewer than 3** → the round is not published (postponement procedure in `references/caption-contest.md`).
5. **Anonymization and shuffling**: the referee assigns each retained caption a neutral code — **L1, L2, L3…** — in a **random order** unrelated to reception order, alphabetical author order, or config order; writes the complete **code → author → text** table into the sealed state file **before** any publication message; and publishes the texts exactly as written, under uniform presentation only (same prefix, same typography, no formatting carried over from a private message).
6. **Publication and vote**: in written-vote mode, one message lists all captions under their codes; in reaction-vote mode, **one separate message per caption** (code and text only), followed by a short message opening the vote. The voting mode is chosen by the host before the round opens and never changes for that round. Written votes are private 1:1 ballots naming a code; reaction votes are one announced reaction per player on the chosen caption's message. No partial result is ever published during the vote.
7. **Tie-break**: if two or more captions tie for first place after counting valid votes, a tie-break round is held between the tied captions only, with a short deadline, **written private ballots always**, and **only players who are authors of none of the tied captions may vote** — the tied authors never break their own tie. If the tie persists (split neutral ballots, no neutral ballot received, or no neutral voter available), there is no third round and no draw: the tied captions are **co-winners**.
8. **Revelation and points**: only after counting (and any tie-break) does the referee publish, in one message: the count per code, the winning code and its author's name, the authors of all the other published captions, the round's points, and the cumulative standings. Points are fixed and announced in advance: winner **+2**, finalist **+1**, co-winners **+1 each** (see `references/caption-contest.md` for the exact finalist rules). No points for voters, no negative points, no invented bonuses.

## Standing rules (they protect the game)

1. **Sealed state**: the code-to-author table exists only in the game's state file, written before publication. No draft, summary, or message prepared for the host ever contains a live author mapping. Before revelation: no confirmation, no denial, no hint about an author — in public or in private, including to a playing host beyond the statuses the mechanism provides.
2. **Captions are collected in private and published anonymized.** Captions are received in 1:1 only; a caption posted in the public thread is burned for that round (procedure in `references/caption-contest.md`). Published captions carry codes only; authors are revealed only at the end of the round, after counting.
3. **A caption that identifies its author is reworded before publication.** At reception the referee asks one question: does this text identify its author by anything other than style or humour? A proper name, nickname, or signature; a reference to a private fact only the author could claim; any identifier slipped in as a signed wink — the caption is returned privately, naming only the category of the problem, with no replacement text suggested. Style is never a reason to send a caption back: guessing authors by their humour is the game itself. The discarded version is never published, never quoted, and its text is never kept in the state — only the generic category is logged. If no acceptable version arrives before the deadline, the player has no caption for that round but may still vote.
4. **No self-vote, ever.** In written mode it is controlled and controlled for real: a ballot naming the voter's own caption is discarded, the voter is told privately, and they may file another ballot before the deadline. In reaction mode it is an honour rule, stated as such at the announcement: the referee discards every self-vote it can actually detect but cannot promise to detect them all.
5. **Ties are broken by neutral voters only.** The tie-break voters are exactly the players who are authors of none of the tied captions; **the tied authors never vote in their own tie-break**. Neutral voters are invited privately, one by one — being invited or not would reveal who is not a tied author, so the invitation stays invisible in the thread.
6. **Every send follows the host's connection rules**: exact preview + the host's explicit confirmation right before each public send. Exception, by design: in host-player mode, secret messages go out on a **template the host approves once per message type**, filled by the referee and never shown filled to the host (see `references/group-messaging.md`, b bis). Publication drafts shown to a playing host contain the caption texts under their codes only — never the author table.
7. **Deadlines hold**: collection, vote, and tie-break each close at their announced deadline; a late caption is refused with no exception, and silence is an abstention. Reminders carry counts only ("captions received: 3/5"), never content, never a name tied to a receipt or a delay.
8. **The host can stop everything** at any time: the game is marked abandoned, a short closing message goes out (host-approved), and the authors of unrevealed captions stay sealed in the state unless the host expressly asks for the full recap.
9. **Language**: the group's language, as the host sets it in the config or at the announcement. This skill's files are in English; the game itself is played in the group's language.

## What this skill is not

- Not a public posting tool: captions are never published with their authors' names attached before the vote — anonymity until revelation is the game, not an option.
- Not real-time: collection and voting run on deadlines over hours, not in a live session around a table.
- Not a bot account: the referee writes from the host's own connected account, with the host's approvals. Players are told so in the announcement, including the honest limit of host-player mode (secrecy toward a playing host is procedural, not technical — the referee shows them nothing, and they pledge not to open other players' private threads).
