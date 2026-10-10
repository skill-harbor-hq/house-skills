---
name: "hangman-plus"
description: "Run a Hangman Plus game: solo hangman in chat, refereed by the assistant. A word from an announced category is chosen from a curated list, written and sealed in the game state before the first letter, played with 7 lives (a wrong letter costs 1, a wrong whole word costs 2), with two bounded Plus tokens, a dictionary definition for 15 points and a rescue letter for 25 points, and a score and a victory streak persisted between games. Use when the user wants hangman, a word guessing game, a pendu, or a partie de pendu."
---

# Hangman Plus — solo hangman, a sealed word, two bounded tokens

Your assistant referees a game of hangman played **solo, in chat** with the user. The assistant seals a word from an announced category in the game state before the first letter; the player proposes one letter or the whole word per turn, with **7 lives** (a wrong letter costs 1 life, a wrong whole word costs 2). The "Plus" is two bounded aids, each usable once per game: a **definition token** (−15 points on a victory) and a **rescue letter** (−25 points on a victory). The score and the victory streak are persisted in the user's own data folder, so the streak survives from one game to the next.

This game is solo only: one player, the user, against the sealed word. There are no other players, no roles, and no group mode.

## What you need

- A Muse assistant (this skill installed).
- **Nothing else.** No account, no connection, no group, no setup beyond choosing (or accepting) a category. The word lists are curated by the drawing procedure in `references/hangman-plus.md` (curated FR and EN categories, validated at the draw); no dictionary file is required.

## Data layer (the skill ships none of it)

All game data lives in a data folder **the user owns**, never inside the skill. On first use, create it with the user (suggested default: `~/hangman-plus/`, any folder the user prefers works):

- `states/<game-id>.json` — one state file per game (schema in `references/hangman-plus.md`). The sealed word, its category, and its definition live only there, written in full before the opening announcement. The mask is never stored: it is recalculated from the state at each display.
- `scores.json` — the persistent record: one entry per finished game (entry format in `references/hangman-plus.md`), carrying the score, the outcome, the tokens used, and the streak fields (`streak_before`, `streak_after`, `best_streak_after`). The streak is read from this file at setup and never recalculated from memory. The sealed word itself never goes into `scores.json`.

No real identifier is ever written into the skill or a shared file: only into the user's private data folder.

## Router

| The user says | Do |
|---|---|
| "hangman", "pendu", "play hangman", "jouer au pendu", "word guessing game" | Run a solo game in chat: read `references/hangman-plus.md` (the rules) and follow it |
| "resume", "reprends la partie", "continue the game" | Re-read the most recent in-progress game's state file and resume from it — the file, not conversation memory, is the truth (resume announcement per `references/hangman-plus.md`: strictly public recap, never the word, an unrevealed letter, or the unspent definition) |
| "what is my streak", "c'est quoi ma série", "my score history" | Read `scores.json` in the user's data folder and answer from the file: current streak, best streak, recent results |
| Any other game by name | Be honest: Hangman Plus is the only game in this skill. Others are not included and are never simulated or improvised |

## Running a game, in short

1. **Setup, fixed before the draw**: the language (the conversation's language), the category (proposed by the player or drawn from the curated categories, announced publicly), and 7 lives, fixed. All three are written into the state before the word is drawn and never change mid-game.
2. **The draw, sealed**: the referee draws a word of 5 to 9 letters by the curation procedure (common word, validated existence, normalized form, no proper name outside the dedicated category, anti-repetition against the last 20 finished games), writes the word, its category, and its one-sentence definition into the state, and only then announces the opening: category, number of letters, 7 lives, the initial mask. No letter is ever revealed for free.
3. **One proposal per turn**: one letter (present: all its positions revealed, no life lost; absent: −1 life), or the whole word (exact: immediate victory; wrong at the right length: −2 lives; wrong length: invalid, no cost). An invalid input consumes no turn and costs nothing.
4. **Repeated proposals are free**: a letter or word already proposed is never counted again as an error; the assistant says "already proposed / known / tried" and the player proposes again in the same turn.
5. **The Plus tokens**: each at most once per game, requested before the turn's proposal. Definition: the sealed one-sentence definition is revealed, −15 points on a victory. Rescue letter: the not-yet-revealed letter whose first occurrence is furthest left is revealed in all its positions, −25 points on a victory. No other hint exists, ever.
6. **End**: victory when the mask is complete or the whole word is guessed exactly; defeat at 0 lives, with the word and its definition revealed in the final recap. Score on a victory: `100 + 10 × lives_remaining − 15 × (definition used) − 25 × (rescue letter used)`, floor 10; defeat or abandonment: 0. The end writing updates the state and appends the entry to `scores.json`, streak included (victory: streak +1; defeat or abandonment: streak reset to 0).

## Standing rules (they protect the game)

1. **Sealed word, written before the first letter**: the word, its category, and its definition are written into the game state **before** the opening announcement. The word never changes mid-game and is never revealed before the end, under any pretext. If the sealed word turns out to break curation, the game is frankly cancelled (no score, no streak effect) and a new game is offered — never a silent swap.
2. **The state file is the truth**: the referee re-reads it at the start of every turn and rewrites it after every event (proposal, token, repetition, end). The mask, the lives, and the potential score are always recalculated from the state, never from memory.
3. **7 lives, fixed**: an absent letter costs exactly 1 life, a wrong whole word of the right length costs exactly 2 lives (floor 0). Nothing else costs a life: not a repetition, not an invalid input, not a token.
4. **A repeated proposal is never counted twice**: letters found, missed, or revealed by the rescue token, and whole words already tried, are answered "already…" at no cost, and the player proposes again in the same turn.
5. **Two tokens, once each, and nothing else**: the definition token and the rescue letter are the game's only aids. No other hint is invented, offered, or sold for points: a request for any other aid is refused with a reminder of the two tokens.
6. **The rescue letter is deterministic**: among the word's unrevealed letters, the one whose first occurrence is furthest to the left. Never "the most useful letter": the choice must be redoable from the state after the game.
7. **The definition is the sealed one**: written at the draw, one sentence, containing neither the word, nor a word of its family, nor its letters in order. It is revealed only by spending the definition token (or in the final recap, when the game is over).
8. **Score and streak are settled**: the victory formula and the floor of 10, 0 for a defeat or an abandonment, the streak read from `scores.json` at setup and written at the end. No points per letter, no speed bonus, no points invented mid-game.
9. **The user can stop everything** at any time: the game is marked abandoned (score 0, streak reset to 0, end writing done), and the word is revealed in the abandonment recap only if the user asks. A game simply left in progress writes nothing and does not affect the streak.
10. **Language**: the language of the conversation (`fr` or `en`), set at setup; the whole game (word, proposals, definitions) is played in that language. This skill's files are in English; the game itself is played in the player's language.

## What this skill is not

- Not a group game: there is no group mode, no messaging connection, and no other player. One user, one chat, one sealed word.
- Not a dictionary or a word list: the curated lists are a drawing procedure applied at each game (categories, length, validation gate), not a file shipped with the skill, and the sealed word of a game in progress is never shown or exported.
- Not lenient by improvisation: lives, token costs, and the score formula are fixed by the rules. If a situation seems unfair, the settled edge cases in `references/hangman-plus.md` decide, not a mid-game invention.
