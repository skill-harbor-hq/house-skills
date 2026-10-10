---
name: "five-letter-word"
description: "Run a Five-Letter Word game: a solo word guessing game in chat, refereed by the assistant. A common five-letter word is chosen from a curated vocabulary and sealed in the game state before the first guess; the player gets 6 valid guesses, each answered with exact letter-by-letter feedback (right letter in the right place, right letter in the wrong place, absent), with duplicate letters settled by a strict two-pass rule. An invalid guess is rejected and never consumes a try. Game history and the winning streak persist in the user's own data folder. Use when the user wants a five-letter word game, a word guessing game, a mot en 5, a jeu de mot en cinq lettres, or to resume a game in progress."
---

# Five-Letter Word — one sealed word, six guesses

Your assistant referees a solo word guessing game, played right in chat. Before the first guess, the assistant picks a common five-letter word in the language of the conversation, from a curated everyday vocabulary, and writes it into a sealed game state file: that word never changes during the game and is never revealed before the end. The player then has **6 valid guesses** to find it. Each valid guess gets exact letter-by-letter feedback: 🟩 right letter in the right place, 🟨 right letter in the wrong place, ⬜ absent — with duplicate letters settled by a strict **two-pass rule**, so a letter is never credited more times in one guess than it actually appears in the target word.

This game is **solo only**: one player, in chat, no group mode, no private roles, no messages to anyone. Guesses that are not real words of the game's language, have the wrong length, contain non-letters, or repeat an earlier guess are **rejected and never consume a try**: the player simply proposes again in the same turn. A win scores `(7 − winning guess number) × 20`; a loss or an abandon scores 0; wins in a row build a persistent **streak**.

## What you need

- A Muse assistant (this skill installed).
- **Nothing else.** No account, no connection, no messaging group, no setup. The game is played solo, in chat, in the language of the conversation (French or English).

## Data layer (the skill ships none of it)

All game data lives in a data folder **the user owns**, never inside the skill. On first use, create it with the user (suggested default: `~/five-letter-word/`, any folder the user prefers works):

- `games/<game-id>.json` — one state file per game (schema in `references/five-letter-word.md`). The sealed target word lives only there, written before the opening announcement; the file also holds the valid guesses with their feedback, the public letter state, the score, the streak counters, and the event log.
- `scores.json` — the persistent history of finished games (entry format in `references/five-letter-word.md`). Each entry carries the outcome, the score, the number of valid guesses played, and the streak before and after, so the current streak and the best streak are always read from the file, never from memory. The target word never enters `scores.json`; it stays in the game state.

No real identifier is ever written into the skill or a shared file: only into the user's private data folder. There is no configuration to fill in: a game can start as soon as the user asks.

## Router

| The user says | Do |
|---|---|
| "five-letter word", "mot en 5", "word guessing game", "jeu de mot", "play a word game", "nouvelle partie" | Run a solo game in chat: read `references/five-letter-word.md` (the rules) and follow it |
| "continue the game", "reprends la partie", "on continue" | Re-read the most recent in-progress game's state file and resume from it — the file, not conversation memory, is the truth (resume announcement per `references/five-letter-word.md`) |
| "what is my streak", "c'est quoi ma série", "my history", "mon historique" | Read `scores.json` in the user's data folder and answer from the file: current streak, best streak, games played |
| Any other game by name | Be honest: Five-Letter Word is the only game in this skill. Others are not included and are never simulated or improvised |

## Running a game, in short

1. **Framing, written before the draw**: the language (the conversation's language), 6 guesses fixed, no starting category and no starting hint. These never change mid-game.
2. **The sealed word**: the referee picks a target from a curated everyday vocabulary and validates it at draw time — exactly 5 letters after normalization, a common word of the game's language, no proper noun, no offensive term, and not a target of any of the last 20 finished games if another valid candidate exists. The word is written into the state file **before** the opening announcement.
3. **Opening**: the referee announces the game, the language, "a five-letter word, 6 guesses", and the meaning of the three squares. No letter of the word is given, and there is no purchasable hint: the feedback of the guesses is the only information in this game.
4. **Each turn**: the player sends one word. The referee validates it (normalization, length, not already tried, exists in the game's language). Invalid → rejected in one sentence naming the reason, **no try consumed, no feedback given on any letter**, and the player proposes again in the same turn. Valid → the guess consumes a try and receives the feedback in the one exact grid format of the reference, computed from the sealed word by the two-pass rule; the state is rewritten before the next turn.
5. **End check after every feedback**: a fully green guess is an immediate win; 6 valid guesses without a full green is a loss. There is no seventh guess.
6. **Final recap**: the outcome, the score with its calculation shown, the streak after the game, the target word (always revealed at the end), and the complete grid of the guesses in order. The result is appended to `scores.json` and the state is closed.

## Standing rules (they protect the game)

1. **Sealed word, written before the first guess**: the target word is written into the game state before the opening announcement. It never leaves the file before the end of the game, and it never changes mid-game — if it is discovered invalid mid-game, the game is cancelled openly, with no score written and the streak unchanged, never silently replaced (see `references/five-letter-word.md`).
2. **The state file is the truth**: the referee re-reads it at the start of every turn and rewrites it after every event (valid guess, rejection, end of game). Every feedback grid is computed from the sealed word in the file, never from memory.
3. **The two-pass rule for duplicates**: greens are marked first, each one consuming its occurrence of the target word; then, left to right, a non-green position gets 🟨 only if an unconsumed occurrence of that letter remains in the target. The number of non-grey squares for a letter in one guess never exceeds that letter's count in the target word.
4. **One feedback format only**: the 3-line grid of the reference — the 5 normalized letters spaced on line 1, the 5 squares with no spaces on line 2, the colour counts and the valid-guess counter on line 3. No substitute notation, no partial grid, no comment on closeness ("you're getting warm" is forbidden), and no letter of the target cited outside the grid. After the grid, at most one public letter-state line.
5. **Invalid guesses cost nothing and teach nothing**: wrong length, non-letter characters, a word that does not exist in the game's language, or a word already tried — rejected with the reason named, never counted, never given any letter feedback, and re-proposable in the same turn, with no limit and no penalty. When in doubt about a word's existence, the doubt benefits the player: accept if the word is attested in a usual dictionary or a common word list of the language.
6. **No help beyond the feedback**: no starting category, no hint, no definition. If the player asks for extra help, the referee declines by restating the rule, without inventing one.
7. **Score and streak, exactly as written**: a win at valid guess `n` scores `(7 − n) × 20` (120, 100, 80, 60, 40, 20); a loss or an abandon scores 0; no partial points for letters found, no bonus, no negative points. The streak counts consecutive wins in this game only: a win adds 1, a loss or an abandon resets it to 0, and the best streak is recomputed from the full history at the end-of-game writing.
8. **The user can stop everything** at any time: the game is marked abandoned, score 0, streak reset to 0, with the end-of-game writings of a loss under a distinct outcome. The word is revealed in the abandon recap only if the user asks. A game left in progress with no closing request writes nothing and does not affect the streak.
9. **Language**: the language of the conversation, fixed in the state before the draw. The target word and every valid guess are in that language; a word that exists only in the other language is invalid here. This skill's files are in English; the game itself is played in the player's language.

## What this skill is not

- Not a group game: there is no group mode, no messaging connection, no roles and no private information. One player, in chat.
- Not a word list or a solver: the curated vocabulary is a draw-time quality gate applied by the referee, not a file shipped with the skill, and the skill never helps crack a word game played elsewhere.
- Not flexible on its frame: 6 guesses, one feedback format, the two-pass duplicate rule, and the scoring scale are the game. Variants are other games, and they are not improvised here.
