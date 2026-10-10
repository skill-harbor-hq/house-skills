---
name: "who-said-that"
description: "Run a 'Who Said That?' group guessing game refereed by the assistant inside the user's own connected messaging group: real quotes drawn only from that group's history, screened and cleaned by the referee, published one by one, guessed privately by 3 to 8 consenting players, with the author answering too on a camouflage ballot and attribution revealed only after all answers are in. Use when the user wants a group game, a quote-guessing game, a 'who said that' game, a partie de groupe, or a partie de devine qui a dit ça with their group."
---

# Who Said That? — a quote-guessing game for your group chat

Your assistant referees a game of Who Said That? inside a group chat **the user owns and connects**. The referee draws real lines from that group's own history, screens out anything sensitive, cleans and anonymizes what remains, and publishes the quotes one by one. Each player privately guesses who wrote each quote. The author answers too, on a camouflage ballot that can never earn them a point on their own quote. Nobody learns who said what until every answer is in.

The game is asynchronous on purpose: each quote runs against an announced deadline, so a round takes hours, not minutes, and a real group can play around real life. 3 to 8 consenting players (4 to 6 recommended), 5 quotes per round by default.

This game quotes real words from real people, so its protections are not optional and are never negotiated mid-game. If a protection cannot be held, the game does not start, or the quote in question is discarded, or the round is cancelled (see `references/who-said-that.md`, edge cases).

## What you need

- A Muse assistant (this skill installed).
- **To actually play**: a messaging account **the user connects to their own assistant** and one group conversation on it that the user designates as the game host. Messenger is the first supported connection; the model is platform-generic (see `references/group-messaging.md`, platform variants). Installing the skill files needs nothing else.
- The assistant writes in the group **from the user's account** (that is how the connection works), and every public message needs the host's approval before it is sent. There is no fully automatic mode, and there never will be: the host approves, then it goes.

## Data layer (the skill ships none of it)

All game data lives in a data folder **the user owns**, never inside the skill. On first use, create it with the user (suggested default: `~/who-said-that/`, any folder the user prefers works):

- `config.json` — the host configuration: platform, designated conversation, host name, host mode, player list. Template:

```json
{
  "platform": "messenger",
  "conversation": "<the group the user designates>",
  "host": "<the user's name>",
  "host_mode": "player | spectator",
  "source_history": "history of the designated host group only",
  "players": [
    { "name": "<name or nickname in the group>", "identifier": "<identifier in the conversation, if known>", "consenting": true }
  ]
}
```

- `games/<game-id>.json` — one sealed state file per game (schema in `references/who-said-that.md`). Drawn quotes, their cleaned text, and **each quote's attribution** live only there, written before any publication.
- `history.json` — finished games and scores (date, players, scores, winner), if the user wants a record.

No real identifier is ever written into the skill or a shared file: only into the user's private data folder. With no filled config, no group game starts: ask the user to designate the group and the players first.

## Router

| The user says | Do |
|---|---|
| "who said that game", "devine qui a dit ça", "quote game", "partie de groupe", "play with my group", "jouer avec mon groupe" | Run a group game: read `references/group-messaging.md` (connection, configuration, approvals, host-player mode), then `references/who-said-that.md` (the rules and protections). No filled config → set it up first (see Data layer) |
| "continue the game", "on continue la partie" | Re-read the current game's state file and resume at the current quote — the file, not conversation memory, is the truth |
| Any other group game by name | Be honest: Who Said That? is the only group game in this skill. Others are not included and are never simulated or improvised |

## Running a game, in short

1. **Setup**: host designates the group and players in the config; the host picks their mode, **player** or **spectator** (host-player mode, `references/group-messaging.md` section b bis). Signing up is explicit consent to be quoted (cleaned quotes, from the host group only) and to be listed among the possible authors; the announcement says so in plain words, before signups.
2. **Draw, screen, clean**: before launch, the referee draws candidate lines only from the designated host group's history and only from consenting players, discards anything touching a sensitive topic (screening first, definitively, never justified, discarded text never shown to anyone), cleans each kept quote, and writes the complete sealed state — cleaned quotes and their attributions — **before any publication**.
3. **Host review**: each cleaned quote is read by the host before publication, as part of the usual send approval. The host may veto a quote without justifying it in the thread. Previews shown to a playing host never contain the attribution.
4. **Publication, one quote at a time**: number, cleaned text in quotes, "who said that?", and the collection deadline. Nothing else: no original length, no date, no context.
5. **Collection in private 1:1**: each player sends one player name per quote to the referee privately. The author answers too, on a camouflage ballot (any player, including themselves; it can never earn an attribution point on their own quote). A ballot can be changed until the deadline; only the last one counts. Silence at the deadline is an abstention.
6. **Reveal, only after collection closes**: attribution, the ballot detail (camouflage labelled as such, now that there is nothing left to protect), the quote's points, and the running scores. Before that moment: no confirmation, no denial, no hint, no differentiated reaction, in public or in private.
7. **End**: after the last quote, a final recap in the thread (final scores, winner, quotes nobody found), the result written to the data history, state marked finished. A tie at the top means co-winners; no tiebreaker is invented.

Scoring is fixed and announced in advance: a correct guess by a non-author is +1; a wrong guess or an abstention is 0; the author's camouflage ballot is always 0; and a camouflage bonus of +1 goes to the author when no non-author found them on that quote **and** the author submitted their camouflage ballot. No negative points, no invented bonuses mid-round.

## Standing rules (they protect the game)

1. **One source only**: quotes come **only** from the history of the user's own connected, designated host group. Never another group, never another account, **never a 1:1 thread** — words said in private never become a group quote.
2. **Possible authors are consenting players only**: a quote may be drawn only from a member who is a consenting player in the current game, and the proposed answers cover only those players. Someone who is not playing — a spectating group member, an absent member, a former member — is **never quoted and never proposed as an answer**, even if their lines are in the history.
3. **Protective screening, before any publication**: at selection, the referee discards any quote touching a sensitive topic (the full list is in `references/who-said-that.md`: health, money, conflicts between members, private life, minors, confidential work, and the rest of the prudent list). The discard happens **before** cleaning and **before** publication, it is definitive for the game, and it is **never justified** — not to the players, not in the thread, not to a playing host. Discarded quotes are **never shown** to anyone; in the state, the referee records only their count and a **generic category**, never their text. In doubt between harmless and sensitive: discard.
4. **Mandatory cleaning**: no raw quote is ever published. Every kept quote goes through the written cleaning procedure in `references/who-said-that.md` (names and identifying nicknames replaced or removed, mentions and identifiers removed, at most 200 characters and 2 sentences, and a de-anonymization re-read). If cleaning cannot make it safe, it is discarded like a sensitive quote.
5. **Host review**: each cleaned quote is read by the host before publication, as part of their send approval — the extra safety net of a human eye on every line, one by one. A vetoed quote goes back to the discarded stock, with no public justification.
6. **Late reveal, always**: a quote's attribution is revealed only **after its collection closes** (all answers received or the deadline passed). Before that moment: no confirmation, no denial, no hint, no differentiated reaction from the referee — in public or in private.
7. **Withdrawal of consent takes effect immediately**: a player who withdraws stops being quoted at once; their not-yet-published quotes are pulled from the round's stock (see `references/who-said-that.md`, edge cases).
8. **Sealed state**: drawn quotes and their attributions exist only in the game's state file, written before the first publication. No draft, summary, or message prepared for the host ever contains an unrevealed attribution; a playing host sees cleaned quotes without authors, like the players, and the sealed state stays out of their view in drafts and everywhere else.
9. **Every send follows the host's connection rules**: exact preview + the host's explicit confirmation right before each public send. In host-player mode, previews never contain attributions (see Standing rule 8).
10. **Deadlines hold**: each publication announces its deadline; reminders never say what is awaited from whom. The referee re-reads the state file at every event and rewrites it after every event.
11. **The host can stop everything** at any time: the game is marked abandoned, a short closing message goes out (host-approved), and the attributions of unrevealed quotes stay sealed unless the host expressly asks for the complete recap.
12. **Language**: the group's language, as the host sets it in the config or at the announcement. This skill's files are in English; the game itself is played in the group's language.

## What this skill is not

- Not a quote archive: the referee never copies discarded or sensitive originals anywhere, and never fills a short round with lines from another group, a 1:1 thread, a non-player, or its own invention. An invented quote is a refereeing fault, not a variant.
- Not a bot account: the referee writes from the host's own connected account, with the host's approvals. Players are told so in the announcement, including the honest limit of host-player mode (secrecy toward a playing host is procedural, not technical — the referee shows them nothing, and they pledge not to open other players' private threads).
