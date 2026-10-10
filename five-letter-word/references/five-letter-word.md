# Five-Letter Word — sealed five-letter word, 6 guesses, letter-by-letter feedback

Reference for the `five-letter-word` skill. A **solo game, in chat**: the assistant seals a five-letter word, the player has **6 guesses** to find it, and each valid guess receives letter-by-letter feedback (right place / present elsewhere / absent) in **one single format, settled below**. The principle (guessing a word from coloured feedback) is that of a classic letter game, public domain in its mechanics; the rules below are rewritten and adapted to chat, in French as in English. There is no group mode in this game.

## The game in one sentence

One five-letter word, sealed in the state file **before the first guess**. At each **valid** guess, the assistant answers with the grid of the 5 letters topped by 5 squares: 🟩 right place, 🟨 present elsewhere, ⬜ absent (with the duplicate rule below, which is part of the game). A win if a guess is entirely 🟩🟩🟩🟩🟩 within at most 6 valid guesses; otherwise, the word is revealed in the final recap — never before.

## Framing of a game

Fixed and written into the state **before** the draw, immutable during the game:

1. **Language** — the language of the conversation (`fr` or `en`). The target word and every valid guess are in that language.
2. **Guesses: 6, fixed.** No bonus guess, no extension "for one letter": 6 is the bound that gives the score its value (see Score).
3. **No category, no starting hint.** Unlike some other chat games, this one gives neither a theme nor a purchasable definition: the only information is the feedback of the guesses. No additional help exists in this template — if the player asks for some, the assistant declines by restating the rule, without inventing any.

## The target word — curated list, validation at draw time

1. **Exactly 5 letters**, letters `A`–`Z` after normalization. One single word, no apostrophe, no hyphen, no proper noun, ever: a five-letter proper noun cannot be deduced from feedback the way a common word can, and its spelling is arbitrary.
2. **Accents — settled rule (FR)**: the stored form of the target word is **without accents**. Normalization is: `É/È/Ê/Ë → E`, `À/Â → A`, `Î/Ï → I`, `Ô → O`, `Ù/Û → U`, `Ç → C`, `Ÿ → Y`. A word whose usual form carries an accent is kept only in its normalized form, and only if it remains the recognizable form of the word (e.g. `ECOLE`, `ETANG`, `CRANE` for crâne). EN: `A`–`Z` only.
3. **Common word, validated at draw time (gate)**: before writing the state, the assistant checks that the word **exists in the language of the game** (FR: usual dictionary or common lexicon; EN: a common word list such as ENABLE, or a usual dictionary) **and** that it is **common** — known to an ordinary speaker. Targets are therefore drawn from a frequent vocabulary: never a rare, archaic, narrowly technical word, or one with a contested spelling. **At the slightest doubt, the word is discarded and another is drawn.** This is an assumed asymmetric curation: the target is always a frequent word, but a player's **guess** is valid as soon as it is an existing word, even a less frequent one (see Validation of guesses) — the player is never punished for knowing a word the assistant would not have chosen as a target.
4. **No offensive word** as a target: insults and vulgar or discriminatory terms are excluded at curation; in case of doubt, exclude.
5. **Gentle anti-repetition**: a word that was already the target in any of the last 20 finished games of this game (states and `scores.json` of the data) is set aside if another valid candidate exists.

The drawn word is written into the state **before** the opening announcement: it is the **sealed key** (field `word`). It never leaves the file before the end of the game.

## Validation of guesses — complete procedure

A guess is the player's message during their turn. Procedure, in order:

1. **Normalization**: uppercase, accents removed following the table above (a FR guess typed with accents, e.g. `ÉTANG`, is therefore accepted and compared in the form `ETANG` — the assistant always displays the normalized form in the grid). Any character that is not a letter (`A`–`Z` after normalization) makes the guess invalid.
2. **Length**: exactly 5 letters, otherwise **invalid**.
3. **Word already tried** (identical, after normalization, to an earlier valid guess of the same game): **rejected without consuming a guess** — see Repeated proposal.
4. **Existence**: the word must **exist in the language of the game**, in the same standard as at draw time (usual dictionary / common word list). A pronounceable but nonexistent letter assembly (e.g. `XYZZY`, `BLORP` in FR) is **invalid**. At the slightest doubt of the assistant about existence, the rule is: **accept** if the word is attested in at least one usual dictionary or one common list of the language, **reject** only if the assistant can affirm that it does not exist; the doubt benefits the player, because wrongly rejecting a real word burns trust, not only a guess — and in any case a rejection does not consume a guess (see below), so the player can always propose again.

**Invalid guess — one single, total consequence**: the assistant rejects the guess in one sentence naming the reason (`length`, `characters`, `word nonexistent in the language of the game`, `already tried`), **the guess is NOT consumed** (the guess counter does not move), **nothing is returned** about the target word (no letter of the invalid guess receives any feedback, even partial — returning a letter of an invalid word would give free information outside the counter), the event is recorded in the state's log, and the player **proposes again in the same turn**. There is neither a limit nor a penalty on invalid guesses: they teach nothing and cost nothing, in both directions.

**Valid guess**: it consumes one guess, receives the complete feedback (next section), is written into the state (normalized word + feedback), and the counter advances.

## The feedback — exact format (settled, to be held at every guess)

For each valid guess, the assistant answers **exactly** in this form, without variant:

```
A R B R E
🟨🟨⬜🟨⬜
🟩 0 · 🟨 3 · ⬜ 2 — Guess 1/6.
```

- **Line 1**: the 5 letters of the guess, normalized, in uppercase, separated by one space.
- **Line 2**: 5 squares **with no space between them**, one per position, in the order of the letters: 🟩 = letter correct and **in the right place**; 🟨 = letter **present elsewhere** in the word (subject to the duplicate rule); ⬜ = letter **absent** (or already fully counted, see the duplicates).
- **Line 3**: the count of the three colours, then the counter of **valid** guesses (`Guess n/6`).
- No other format is used in the game: no substitute text notation (`[X]`, `(?)`, "right place" letter by letter in prose), no partial grid. Only in the final recap may past grids be recopied, identically.
- After the grid, the assistant may add **one single letter-state line** (see below) and nothing else: no comment on closeness ("you're getting warm"), no letter of the target word cited outside the grid.

### The duplicate rule (the heart of the feedback — two-pass algorithm)

The feedback is **always** computed this way, from the sealed word in the state, never from memory:

1. **🟩 pass**: for each position where the guess's letter equals the target word's letter at the same position → 🟩. Each 🟩 **consumes** the corresponding occurrence of the target word.
2. **🟨/⬜ pass, left to right**: for each non-green position, count the **not yet consumed** occurrences of that letter in the target word (total occurrences minus 🟩 already attributed to that letter, minus 🟨 already attributed to that same letter in this pass). If at least one remains → 🟨 and consume one. Otherwise → ⬜.

Consequence to state to the player if they contest: a letter can be ⬜ at one position and 🟨 or 🟩 at another in the same guess (e.g. the target word contains the letter once: a guess proposing it twice receives at most one non-grey feedback for that letter — the right-place position first, then the leftmost). The number of non-grey squares for a letter in one guess **never** exceeds its number of occurrences in the target word.

**Worked example (canonical)** — target `RADAR`, guess `ARBRE`:
- 🟩 pass: no position matches (`A≠R, R≠A, B≠D, R≠A, E≠R`) → 0 green.
- Occurrences of the target: `R×2, A×2, D×1`. Left to right: `A` → `A` remaining (2) → 🟨 (1 left); `R` → `R` remaining (2) → 🟨 (1 left); `B` → absent → ⬜; `R` → `R` remaining (1) → 🟨 (0 left); `E` → absent → ⬜.
- Feedback: `🟨🟨⬜🟨⬜`, count 🟩 0 · 🟨 3 · ⬜ 2.

### Letter state (public recap)

The assistant keeps in the state, per letter, the **best known status** deduced from feedback already published: 🟩 (seen in the right place) takes precedence over 🟨 (seen present), which takes precedence over ⬜ (seen absent). This state is **entirely public** (it only summarizes grids already shown) and may be displayed in one line after the grid: "Letters: 🟩 R, A · 🟨 — · ⬜ B, E, U, L…". Rules: a letter seen 🟨 then ⬜ in a duplicate guess **stays 🟨** in the state (the duplicate ⬜ does not mean "absent", it means "already fully counted" — the letter state must never contradict this by demoting a present letter to "absent"); a letter never goes down in status over the course of the game.

## Turn-by-turn flow

1. **Opening** — The assistant announces: the game, the language, "five-letter word, 6 guesses", and the feedback format in one **neutral** example (an example that uses neither the target word nor its letters in an informative combination — the canonical example above may serve as the opening only if it is not the current target; by default, the opening cites only the three squares and their meaning). No letter of the word is given.
2. **Player's turn** — The player sends a word. Validation following the procedure above. Invalid → rejection at no cost and a new proposal in the same turn. Valid → feedback in the exact format, state rewritten (guess, feedback, letter state, counter), before the next turn.
3. **End check after each feedback**: a fully green guess → immediate **win**; counter at 6 without a win → **loss**. No seventh guess "just to see": after the loss, the word is revealed in the recap and the game is closed.
4. **Final recap**: the outcome, the score (calculation shown), the streak after the game, the target word (always revealed at the end, win or loss — in a win it is already known), and the complete grid of the guesses in order.

## Win, loss, score, streak

- **Win**: a valid guess obtains 🟩🟩🟩🟩🟩. **Loss**: 6 valid guesses used up without a fully green guess. **Abandon**: see Edge cases.
- **Score (settled, no other points exist)**: a win at guess `n` (1 to 6, **valid** guesses only): `(7 − n) × 20` — that is 120, 100, 80, 60, 40, 20 depending on the winning guess. Loss or abandon: **0**. No partial points for letters found ("4 letters out of 5" is worth nothing in the score: the game rewards the word found, not the approach), no bonus, no negative points.
- **Streak**: the number of **consecutive wins of the player in this game** (`game: "five-letter-word"`), independent of other games. Win: `streak_after = streak_before + 1`; loss or abandon: `streak_after = 0`. `streak_before` is read at framing from the data: the `streak_after` of the last finished game of the same game in `scores.json` (0 if none), written into the state from its creation. `best_streak_after`: the largest `streak_after` reached in this game, recomputed at the end writing from the whole history of the same game (current entry included). Same discipline as everywhere in this skill: the fields live in each `scores.json` entry and in the state (`streak_before`, `streak_after`), never recomputed from memory.

### Repeated proposal — settled rule

A word **already tried** (earlier valid guess, compared after normalization) is **rejected without consuming a guess**, with the mention "already tried" and the reminder of its past feedback (the assistant may recopy its grid: it is public). Justification: proposing the same word again teaches strictly nothing (the feedback would be identical, computed from the same sealed word); consuming it would burn a guess for zero information — repetition is a memory slip, not a play.

## State schema — `games/<game-id>.json`

`game-id`: `five-letter-word-<YYYY-MM-DD>-<hhmm>` (prefix `TEST-` for a test game). The word is the sealed key, written before the opening announcement; the state is re-read at the start of each turn and rewritten at the end of each turn, by one agent at a time.

```json
{
  "id": "five-letter-word-2026-10-10-2100",
  "game": "five-letter-word",
  "status": "in_progress | finished | abandoned",
  "language": "fr | en",
  "created_at": "2026-10-10T21:00:00-04:00",
  "word": "<SEALED WORD, 5 letters, normalized, uppercase>",
  "max_guesses": 6,
  "guesses": [
    { "number": 1, "guessed_word": "ARBRE", "feedback": ["yellow", "yellow", "grey", "yellow", "grey"] }
  ],
  "letter_state": { "A": "yellow", "R": "yellow", "B": "grey" },
  "score": null,
  "streak_before": 0,
  "streak_after": null,
  "outcome": null,
  "log": [
    { "at": "2026-10-10T21:00:00-04:00", "event": "game_created_word_sealed" }
  ]
}
```

- `feedback` is stored in words (`"green" | "yellow" | "grey"`, per position) and **rendered** as squares in the exact format at display time — the text storage avoids any encoding ambiguity in the file, and the rendering stays unique because the word-to-square correspondence is fixed by the feedback section.
- `guesses` contains only **valid** guesses (invalid ones and repetitions live in the log, with their reason: they happened, but they are not guesses). `number` = position among the valid guesses, from 1 to 6.
- `letter_state`: best known status per letter (`"green" | "yellow" | "grey"`), updated after each feedback following the non-demotion rule. It contains only letters already publicly returned.
- `score`, `streak_after`, `outcome` (`"win" | "loss" | "abandon"`): `null` while the game is `in_progress`, filled at the end writing along with `status`.
- The log records every dated event: creation (word sealed), each valid guess and its feedback, each rejection (invalid or repetition, with the reason), the end and its outcome. It is the proof, after the game, that the word never changed and that every feedback was computed from it.

## End-of-game writings

1. `scores.json` — append: `{ "date", "game_id", "game": "five-letter-word", "language", "outcome", "score", "guesses_used": <valid guesses played>, "streak_before", "streak_after", "best_streak_after", "test": true|false }`. The target word does **not** enter `scores.json`; it stays in the game state, which is kept.
2. Game state: `status` → `"finished"` (or `"abandoned"`), `score`, `streak_after`, `outcome` filled.
3. No writing anywhere else: this is not a question game and it has no other persistent file.

## Resuming a game

On the trigger "resume" (or "play" while a five-letter word game is `in_progress`): re-read the most recent `in_progress` state of this game and announce a **strictly public recap** — language, valid guesses already played with their grids (in the exact format, recopied from the state), guesses remaining, letter state, current streak (`streak_before`). **Never** the target word. Resume at the next turn. The re-read state rules, not the memory of the conversation.

## Edge cases (settled)

- **Invalid guess** (length other than 5, non-letter characters, word nonexistent in the language, word already tried): rejected in one sentence with the reason, **never consumed**, no partial feedback, new proposal in the same turn. See the validation procedure — it is the central edge case of this game, not an exception.
- **Accents in a guess (FR)**: normalized before validation and comparison; the assistant displays the normalized form and says so if the typed form carried an accent ("I keep ETANG"). Proposing the same word with then without an accent counts as a **repetition** (the comparison is made after normalization).
- **Case**: indifferent everywhere (entry, comparison, repetition detection).
- **Word existing only in the other language** (e.g. an English word proposed in a FR game): **invalid** in the language of the game — validation is made against the language written in the state, never against "any dictionary". The assistant says so ("nonexistent in French, the language of the game").
- **The player proposes several words at once** ("TABLE or CHAISE?"): neither of them is a guess; the assistant asks for just one to be sent, turn not consumed. The first word of a list is never kept by default.
- **Sixth guess**: treated like the others, complete feedback published **before** the loss announcement if any (the player is entitled to the feedback of their last guess, then the recap reveals the word).
- **Abandon** (the player says "stop", "I give up", or asks to close): status `abandoned`, `outcome: "abandon"`, score 0, **streak reset to 0**, end writing as for a loss with a distinct `outcome`. The word is revealed in the abandon recap if the player asks; otherwise it stays in the file. A game left `in_progress` with no closing request writes nothing and does not affect the streak.
- **Target word discovered invalid mid-game** (curation violation discovered after the fact: nonexistent word, proper noun, wrong length): the assistant's fault. Game **cancelled openly**: no score written, streak unchanged, state `abandoned` with a log event `game_cancelled_invalid_word`, a new game proposed. Never a silent replacement of the word mid-game — every feedback already published would become a lie.
- **Contesting a feedback**: the assistant recomputes aloud, position by position, from the word in the state **revealed for the occasion if the game is finished**; if the game is still `in_progress`, it recomputes citing only the letters of the contested guess and the occurrence counts that the feedback implies (those counts are already implied by the public grids), without unveiling unreturned positions. The file settles it: if the published feedback contradicts the computation, the assistant acknowledges it, corrects the state and the log, and the game continues on the corrected feedback.

## Message templates (to adapt to the language of the game)

- **Opening**: "Five-Letter Word — I seal a five-letter word, you have 6 guesses. After each valid word: 🟩 right place, 🟨 present elsewhere, ⬜ absent. An invalid word (wrong length, nonexistent, already tried) does not consume a guess. Send your first word."
- **Guess feedback**: the grid in the exact format (3 lines), then at most the letter-state line.
- **Rejection**: "Rejected — [REASON]. Guess not consumed, you are still at [N] guess(es) played out of 6. Propose another word."
- **Win**: "🟩🟩🟩🟩🟩 — [WORD], found at guess [N]. Score: (7 − [N]) × 20 = [SCORE]. Winning streak: [STREAK_AFTER]."
- **Loss**: "Six guesses used up. The word was: [WORD]. Score: 0, streak reset to 0." followed by the complete grid of the guesses.
