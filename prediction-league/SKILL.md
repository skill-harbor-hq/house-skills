---
name: "prediction-league"
description: "Run a Prediction League for a group, refereed by the assistant inside the user's own connected messaging group (Messenger first): over a season, players privately predict the outcomes of real upcoming events, the referee checks each result from a single source named in advance, scores with a fixed grid, doubles one confidence joker per round, and publishes the round and season standings. Use when the user wants a prediction league, a forecasting game, a ligue de pronostics, or a pronostics game with their group."
---

# Prediction League — a forecasting game for your group chat

Your assistant referees a season-long Prediction League inside a group chat **the user owns and connects**. Players predict, in private, the outcomes of real upcoming events (matches, weather, the winner of a show). For every event, one verification source is named in advance, and the referee checks the result from that source and that source only, never from memory. Points follow a fixed grid written down before play; one confidence joker per round doubles a single prediction. The season crowns the most consistent forecaster, not the luckiest player of a single evening.

The game is asynchronous on purpose: each event has its own deadline, typically 30 minutes before it starts, so a real group can play around real life. Players: 3 to 12.

## What you need

- A Muse assistant (this skill installed).
- **To actually play**: a messaging account **the user connects to their own assistant** and one group conversation on it that the user designates as the game host. Messenger is the first supported connection; the model is platform-generic (see `references/group-messaging.md`, platform variants). Installing the skill files needs nothing else.
- The assistant writes in the group **from the user's account** (that is how the connection works), and every public message needs the host's approval before it is sent. There is no fully automatic mode, and there never will be: the host approves, then it goes.

## Data layer (the skill ships none of it)

All game data lives in a data folder **the user owns**, never inside the skill. On first use, create it with the user (suggested default: `~/prediction-league/`, any folder the user prefers works):

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

- `rounds/<round-id>.json` — one state file per round (called `etats/` in the French source template; schema in `references/prediction-league.md`). It holds the events, their named sources, the accepted and refused predictions, the verified results, and the round's points.
- `league-season.json` — the persistent season standings file (schema in `references/prediction-league.md`). One file per season, updated only at the end of a finished round.

No real identifier is ever written into the skill or a shared file: only into the user's private data folder. With no filled config, no group game starts: ask the user to designate the group and the players first.

## Router

| The user says | Do |
|---|---|
| "prediction league", "ligue de pronostics", "forecasting game", "pronostics with my group", "jouer aux pronostics" | Run a group game: read `references/group-messaging.md` (connection, configuration, approvals, host-player mode), then `references/prediction-league.md` (the rules). No filled config → set it up first (see Data layer) |
| "continue the league", "on continue la ligue", "next round", "prochaine journée" | Re-read the current round's state file and the season file and resume from them — the files, not conversation memory, are the truth |
| Any other group game by name | Be honest: Prediction League is the only group game in this skill. Others are not included and are never simulated or improvised |

## Running a season, in short

1. **Setup**: host designates the group and players in the config; the host picks their mode, **player** or **spectator** (host-player mode, `references/group-messaging.md` section b bis); the host announces the season length (number of rounds) and it is written into the season file — it is not extended mid-season without the host's agreement.
2. **Round announcement** in the group (host-approved): round number, the events with, for each one, its type, its expected prediction format, **its named verification source**, **its own deadline**, and the points grid. The complete round state is written to its file **before** this announcement; none of it changes after the first prediction is received.
3. **Predictions — in private, always.** Each player sends their predictions to the referee **in 1:1**, never in the thread. Until an event's deadline passes, predictions already filed for that event stay invisible to the other players. The referee acknowledges receipt privately, with the recording time — that timestamp is what decides lateness.
4. **Deadline per event, not per round.** Each event has its own deadline (default: 30 minutes before its real start). A filing message is judged event by event: what arrives in time is accepted, what arrives after its event's deadline is refused — even inside the same message as on-time predictions. A player may change a prediction, or move their joker, until that event's deadline; only the last version received in time counts.
5. **Confidence joker**: one joker per player per round, declared when filing the prediction it applies to, before that event's deadline. That prediction's points — whatever they are, including 0 — are **doubled**. A joker placed on a refused prediction or a cancelled event is not consumed while another event of the round is still open; past the last open event, an unplaced joker is simply lost.
6. **Lock and publication**: at each event's deadline, the referee publishes the table of received predictions for that event in the thread, all at once, jokers flagged. From then on they are public and frozen.
7. **Verification**: after each event, the referee checks the result **from the named source only** (see Standing rules) and writes the verified result and the time of verification into the state.
8. **End of round**: when every event is verified or cancelled, the referee computes the points **from the state** (never from memory), publishes the per-event detail, the round standings, and the updated season standings, then writes both persistence files (round state marked finished, season file updated).

## Standing rules (they protect the game)

1. **The truth is named before the game.** For each event, the round state names a **single verification source** (a specific site, page, or publication) **before that event's prediction deadline**. After the event, the referee verifies the result **from that source, and that source only**: never from memory, never from another source, never from the referee's or a player's recollection. If the named source says something other than what everyone believed, the source is right — that is why it was named in advance.
2. **Deadlines hold, per event.** Late predictions are refused, with no exception and no negotiation — even by a minute, even if the event has not started. Refusals are announced privately to the player concerned, citing the deadline and the received time, and logged in the state without the content.
3. **Predictions are a temporary secret.** Nothing in the thread, nothing privately to another player, no hint, until the event's deadline has passed. If the host plays, apply host-player mode (`references/group-messaging.md` section b bis): the referee shows the host only statuses ("predictions received for E2: 4/5"), never contents before the scheduled publication.
4. **The state file is the truth.** Re-read the file at every event (filing, refusal, verification), rewrite it after every event. Points are computed from the state, and the published standings can be recomputed by anyone from the public table of predictions and the verified results.
5. **Silent or contradictory source: follow the written procedure** in `references/prediction-league.md` — postpone the verification and say so in the thread, recheck after an announced delay (default 24 h); if the named source itself cannot settle it, the event is cancelled (zero points for everyone). The named source is never replaced by another source after predictions are in.
6. **Neutral tone.** The same wording for everyone, no comment on the quality of a prediction before verification, no advice: the referee records, it does not play.
7. **Language**: the group's language, as the host sets it in the config or at the announcement. This skill's files are in English; the game itself is played in the group's language.

## What this skill is not

- Not a betting tool: no money, no odds, no stakes — points and standings only.
- Not real-time: predictions close before each event starts, and verification waits for the named source to publish.
- Not a bot account: the referee writes from the host's own connected account, with the host's approvals. Players are told so in the announcement, including the honest limit of host-player mode (secrecy toward a playing host is procedural, not technical — the referee shows them nothing, and they pledge not to open other players' private threads).
