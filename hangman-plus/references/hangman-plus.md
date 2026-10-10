# Hangman Plus — solo hangman with a sealed word and two bounded tokens: full rules

Reference for the `hangman-plus` skill. A **solo game, played in chat**: the assistant picks a secret word, the player proposes letters or the whole word, and mistakes cost lives. The "Plus" is **two additional mechanics, written and bounded** (a definition token and a rescue letter), decided here and never improvised mid-game. Hangman is a public-domain game in its principle; the rules below are rewritten and adapted to chat.

## The game in one sentence

The assistant seals a word from an announced category (for example animals) in the state file **before the first letter**. The player sees only the mask (`_ A _ _ _ E _ E`), the category, their lives, and the letters already proposed. On each turn the player proposes **one letter or the whole word**. **7 lives**: each absent letter costs 1 life, each wrong whole word costs 2. Victory if the word is fully revealed or guessed before the last life; defeat at 0 lives, and the word is then revealed in the final recap, never before.

## Setting up a game

At the start, three parameters are fixed and written into the state **before** the draw; they never change during the game:

1. **Language** — the language of the conversation (`fr` or `en`). All of the game's vocabulary (target word, proposals, definitions) is in that language.
2. **Category** — proposed by the player or drawn from the curated categories below; it is **announced publicly** from the opening (it is legitimate game information, not a disguised hint: it bounds the set without reducing the word to one or two candidates).
3. **Lives: 7, fixed.** No adjustable difficulty in this template: changing the number of lives would change the value of the score (see Score), so a 5-life game and a 7-life game would not be comparable in the history.

### Curated categories

| Category | Set (examples of form, never the word of a game in progress) | Note |
|---|---|---|
| `animals` | common animal names (giraffe, panther, hedgehog, in normalized form) | never a proper name of an animal |
| `jobs` | jobs and professions (baker, plumber, architect, truncated to 9 letters at most) | masculine singular forms, by list convention in French |
| `geography` | common geographical nouns (river, desert, peninsula) and very common place names **only if the category is played in an announced "places" mode** | see the proper-name rule below |
| `food` | common foods and dishes (croissant, chocolate) | |
| `nature` | plants, trees, phenomena (sunflower, avalanche) | |
| `objects` | everyday objects (umbrella, staircase) | |
| `sports-leisure` | sports, games, instruments (violin, climbing) | |
| `sciences` | common scientific terms (gravity, molecule, in normalized form) | no obscure term |
| `proper-names` (dedicated category) | very well known first names, countries, capitals | the **only** category where proper names are allowed, and only if the player explicitly chooses it |

**Proper-name rule (settled)**: outside the dedicated `proper-names` category, no proper name is a valid target: a country or a capital never slips into `geography`, whose targets are common nouns. Justification: a proper name cannot be deduced from the letters already seen in the same way (arbitrary spelling, no dictionary definition); mixing it with common nouns without announcing it would distort the game.

## The words — curated FR and EN lists, validation at the draw

There is no dictionary embedded in the skill: curation is a **verifiable drawing procedure**, not a fixed list copied here. For each game:

1. **Target length: 5 to 9 letters** (after normalization, see below). Below 5, the word falls too fast; above 9, the mask becomes unreadable in chat and errors pile up without information.
2. **Form**: a single word, letters `A` to `Z` only after normalization. Excluded at curation: compound words, words with a hyphen or an apostrophe, acronyms, abbreviations, plurals when the singular exists at the same length (keep the singular), conjugated forms.
3. **Accent normalization (FR, settled)**: the stored and displayed form is **without accents** — `É/È/Ê/Ë → E`, `À/Â → A`, `Î/Ï → I`, `Ô → O`, `Ù/Û → U`, `Ç → C`, `Ÿ → Y`. A word whose usual form carries an accent is kept only in its normalized form, and only if it remains the recognizable form of the word (for example `ELEPHANT`, `PANTHERE`, `ECOLE`). EN: `A` to `Z` only, no word with a foreign letter.
4. **Existence validated at the draw (gate)**: before writing the state, the assistant checks that the word **exists in the language of the game** in the sense of a common dictionary (FR: a usual dictionary such as Larousse/Robert or a common lexicon; EN: a common word list such as ENABLE or a usual dictionary). The word must be a **common** word: known to an ordinary speaker, definable in one sentence without resorting to a rarer term than itself. **At the slightest doubt (rare, archaic, or narrowly technical word, uncertain spelling), the word is discarded and another is drawn**, the same discipline as a trivia quality gate. The definition used for the Plus token is written at that moment and stored in the state (field `definition`), never invented at the moment the player asks for it.
5. **No offensive word**: insults, vulgar, discriminatory, or gratuitously sexual or violent terms are excluded at curation. In case of doubt, exclude.
6. **Soft anti-repetition**: before the draw, re-read the recent finished states of the same game in the data; a word already played in the player's last 20 finished games is set aside if another valid candidate exists. The history of hangman lives in `scores.json` and the states.

Once drawn, the word, its category, and its definition are written into the state **before** the opening announcement: that is the game's **sealed key** (field `word`, see the schema). The assistant never picks the word "in its head" during the game.

## Turn-by-turn flow

1. **Opening** — The assistant announces: the game, the category, the language, the number of letters, the lives (7), and the initial mask (one `_` slot per letter, separated by spaces). No letter is ever revealed for free, not even an "obvious" vowel.
2. **Player's turn** — The player sends, at their choice:
   - **one letter** (a single one; case does not matter; in FR, an accented letter is normalized before comparison, so proposing `É` is the same as proposing `E`);
   - **the whole word** (see its own cost below);
   - **a request for a Plus token** (see the dedicated section): the request takes the turn for display purposes, but by itself it neither advances nor moves back the mask, apart from the token's own effect;
   - or an abandonment (see Edge cases).
   Any other input (several letters at once without claiming the whole word, text with no identifiable letter) is **invalid**: the assistant says so, restates the format, and the turn is **not consumed**: no life lost, nothing written as a proposal.
3. **Resolving a letter** — The assistant re-reads the state, then:
   - Letter **present**: all of its positions are revealed in the mask. No life lost.
   - Letter **absent**: **−1 life**, and the letter joins the missed letters.
   - Letter **already proposed** (present or absent) or **already revealed by the rescue letter**: the repeated-proposal case, see below, **never counted again**.
4. **Resolving the whole word** — The proposal is normalized (uppercase, accents removed), then compared with the sealed word:
   - **Different length from the target word**: **invalid** proposal, rejected at no cost; the assistant says so without confirming or denying any letter ("that is not the right length" is the only information given, and it is already public from the mask).
   - **Word already tried** (and wrong): repeated proposal, **no additional cost**, see below.
   - **Exact word**: **immediate victory**, even if letters were still hidden; the mask is completed in the recap.
   - **Wrong word of the right length**: **−2 lives** (floor 0). The risk is the price of the information: a wrong whole word teaches nothing about positions, unlike a letter. No letter of the wrong proposal is revealed or marked as tried; only the word proposal is recorded (`words_tried`).
5. **Display after each turn** — A public state block, always in the same order: mask, lives remaining, letters found, letters missed, whole words already tried, Plus tokens remaining, and the potential score if the player stops spending (see Score; showing the potential score is optional, but if it is shown it is computed from the state, never estimated). **Never** the word, an unrevealed letter, or the definition (outside a spent token).
6. **End of turn** — The state is rewritten (proposal, effect, lives, log) before the next turn. The state is the truth, not the memory of the conversation.

### Repeated proposal — settled rule

**A proposal already made is never counted again as an error, in any form.** Concretely:

- Letter already proposed and missed: the assistant answers "already proposed" (recalling its result: absent), **no life lost**, and the player **proposes again in the same turn**; the game does not advance on a repetition.
- Letter already proposed and found, or letter revealed by the rescue token: same treatment ("already known").
- Whole word already tried: same treatment ("already tried"), no cost.

Justification: in chat, over a game that can stretch out, asking for a letter again is a memory slip, not a playing fault; punishing it twice for the same information would destroy the game without teaching the player anything. The public recap permanently displays the letters and words already played precisely so that repetition is avoidable, and free when it happens.

## The "Plus" — two bounded mechanics

Each token is used **at most once per game**, only during the player's turn and **before** that turn's proposal, never after the end of the game, never retroactively. These are the game's only two aids: **no other hint exists**: no "first letter for…", no summary of the remaining letters, no partial definition offered outside a token. If the player asks for an aid that is not provided for, the assistant refuses it while recalling the two tokens, without inventing a third one.

### Token 1 — Definition

- **Effect**: the assistant reveals the `definition` written into the state at the draw: a dictionary definition, short (one sentence), containing **neither the word, nor a word of the same family, nor its letters in order**. It may recall the category, never replace it with a near-unique synonym that would hand over the word.
- **Cost**: **−15 points** on the victory score (see Score; no effect if the game is lost, since a defeat scores 0 anyway). No life lost, no letter revealed.
- **Bounds**: once per game. The spent token is written into the state (`tokens.definition_used: true`, dated log entry) at the moment of use.

### Token 2 — Rescue letter

- **Effect**: the assistant reveals **one letter that is present and not yet revealed**, in all of its positions at once. The choice is **deterministic and verifiable**: among the word's not-yet-revealed letters, the one whose **first occurrence is furthest to the left** in the word. (Settled this way so that a post-game check can redo the choice from the state: no "the assistant picked the most useful letter", which would be an unbounded discretionary power.)
- **Cost**: **−25 points** on the victory score. No life lost.
- **Bounds**: once per game. The revealed letter joins the **known** letters: it is noted separately in the state (`rescue_letters`), shown in the mask like any found letter, and proposing it afterwards counts as a **repeated proposal** ("already known", free). It does not count as a letter "proposed" by the player in the game's statistics.

Order of costs: the two tokens can be combined (a game can spend both, −40 points in total); the order of spending does not matter, the cost is flat.

## Victory, defeat, score, streak

### End conditions

- **Victory**: the mask is complete (all letters revealed, player proposals and rescue letter combined), **or** the whole word is proposed exactly, at any time before the last life.
- **Defeat**: lives fall to **0** (absent letter with 1 life remaining, or wrong whole word costing 2 lives with 1 or 2 lives remaining; lives never go below 0). The word is revealed in the final recap, with its definition: the game is over, the secret no longer has a purpose, and learning the word is part of the game.
- The end check happens **after each resolution**, before any display of the next turn.

### Score (settled, no other points exist)

- **Victory**: `100 + 10 × lives_remaining − 15 × (definition used) − 25 × (rescue letter used)`, with a **floor of 10** (a victory is always worth at least 10, even if both tokens are spent with 1 life remaining: 100 + 10 − 40 = 70 in practice; the floor is only a safeguard if the formula ever changes).
- **Defeat or abandonment: 0.**
- No points per letter found, no speed bonus (the game is asynchronous in chat: time does not count), no negative points.

### Streak — persistence

The streak is the number of **consecutive victories by the player in this game** (`game: "hangman-plus"`), independent of other games: the hangman streak and the streak of any other game never mix.

- Victory: `streak_after = streak_before + 1`. Defeat or abandonment: `streak_after = 0`.
- `streak_before` is read from the data at setup: it is the `streak_after` of the **last finished game of the same game** in `scores.json` (0 if there is none). It is written into the state at creation; the streak is never recalculated from memory at the end of the game.
- `best_streak_after`: the largest `streak_after` ever reached in this game, recalculated at the end writing from the whole history of the same game in `scores.json` (current entry included).
- The fields are carried by **each entry** of `scores.json` (see End-of-game writings) and by the state (`streak_before`, `streak_after`): the streak therefore survives the loss of a state file, and an interrupted state does not corrupt it (a game left `in_progress`, or an `abandoned` state with no end writing, does not count; see Edge cases for abandonment, which does write its end).

## State schema — `states/<game-id>.json`

`game-id`: `hangman-plus-<YYYY-MM-DD>-<hhmm>` (prefix `TEST-` for a test game). Same discipline as everywhere in this skill: the word is the sealed key, written before the opening announcement; the state is re-read at the start of each turn and rewritten at the end of each turn, by one agent at a time.

```json
{
  "id": "hangman-plus-2026-10-10-2100",
  "game": "hangman-plus",
  "status": "in_progress | finished | abandoned",
  "language": "fr | en",
  "created_at": "2026-10-10T21:00:00-04:00",
  "category": "animals",
  "word": "<SEALED WORD, normalized, uppercase>",
  "definition": "<definition written at the draw, for the definition token>",
  "lives_max": 7,
  "lives_remaining": 7,
  "letters_proposed": { "<letter>": "found | missed" },
  "rescue_letters": ["<letter revealed by the token, or empty>"],
  "words_tried": ["<wrong whole words already proposed>"],
  "tokens": { "definition_used": false, "rescue_letter_used": false },
  "score": null,
  "streak_before": 0,
  "streak_after": null,
  "outcome": null,
  "log": [
    { "at": "2026-10-10T21:00:00-04:00", "event": "game_created_word_sealed" }
  ]
}
```

- The **mask is not stored**: it is recalculated at each display from `word`, `letters_proposed` (those marked `found`), and `rescue_letters`. Storing the mask would create a second source of truth that could diverge from the sealed word.
- `letters_proposed` contains only the letters actually proposed by the player (never the rescue letter, never the letters of a wrong whole word). Repetition is detected by the simple presence of the key.
- `score`, `streak_after`, and `outcome` (`"victory" | "defeat" | "abandon"`) stay `null` while the game is `in_progress`; they are filled at the end writing, at the same time as `status`.
- The log records each dated event: creation (word sealed), each proposal and its effect, each token spent, each repeated or invalid proposal (it does not change the game, but it happened), the end and its outcome. It is the post-game proof that the word never changed and that lives were counted by the rules.

## End-of-game writings

1. `scores.json` — add: `{ "date", "game_id", "game": "hangman-plus", "language", "category", "outcome", "score", "lives_remaining", "tokens_used": { "definition": true|false, "rescue_letter": true|false }, "streak_before", "streak_after", "best_streak_after", "test": true|false }`. The word itself does **not** go into `scores.json` (the score history does not need the secret; the kept game state carries it).
2. Game state: `status` → `"finished"` (or `"abandoned"`), `score`, `streak_after`, and `outcome` filled.
3. No writing to any question library: this is not a question game.

## Resuming a game

On the trigger "resume" (or "play" while a hangman game is `in_progress`): re-read the most recent `in_progress` state of this game and announce a **strictly public recap**: category, language, mask recalculated, lives remaining, letters found and missed, whole words already tried, tokens remaining, current streak (`streak_before` of the state). **Never** the word, an unrevealed letter, or the unspent definition. Resume at the next turn. The re-read state is the truth, not the memory of the conversation.

## Edge cases (settled)

- **Repeated proposal**: see the settled rule above, never counted again, and the player proposes again in the same turn. It applies to letters (found, missed, or revealed by the rescue token) and to whole words already tried.
- **Invalid proposal** (several letters without claiming the word, whole word of the wrong length, input with no letter): rejected, explained in one sentence, **no cost**, and the turn is not consumed. Three invalid proposals in a row change nothing: there is no hidden penalty.
- **Accented letter or lowercase**: normalized (accents removed per the curation table, uppercase) before any comparison: `é`, `E`, and `e` are the same proposal, including for repetition detection.
- **Whole word proposed with only 1 life left**: allowed. If it is wrong, lives fall to 0 (floor) and the game is lost; the 2-life cost is never a ban on trying.
- **Tokens requested after the end, or the same one twice**: politely refused; a finished game does not reopen, and a spent token is not spent again. Asking for the definition token **after** seeing the defeat makes no sense: the definition is given for free in the defeat recap (and in the victory recap if the player asks; the game is over).
- **The player guesses the "obvious" category and proposes the whole word on the very first turn**: perfectly legal, immediate victory, full score (100 + 70 = 170 if no life was lost and no token spent). The game does not punish good deduction.
- **Abandonment** (the player says "stop", "I give up", or stops answering and asks to close): status `abandoned`, `outcome: "abandon"`, score 0, **streak reset to 0** (end writing done as for a defeat, with a distinct `outcome` so the history distinguishes losing from quitting). The word is revealed in the abandonment recap if the player asks; otherwise it stays in the file. A game simply left `in_progress` (no closing request) writes nothing and does not affect the streak until it is closed.
- **Word discovered invalid mid-game** (the assistant realizes the sealed word breaks curation: proper name outside the dedicated category, nonexistent word, length out of bounds): the assistant's fault, never the player's. The game is **frankly cancelled**: the assistant says so, the game writes **no** score and does **not** affect the streak, the state becomes `abandoned` with a log event `game_cancelled_invalid_word` (without copying the faulty word outside its intended field), and a new game is offered. No silent correction of the word mid-game, under any pretext: changing the word after letters have been revealed would be referee cheating.
- **Contesting a life count**: the assistant republishes, from the state, the list of missed letters and wrong whole words with their cost, and redoes the calculation out loud (`7 − missed letters − 2 × wrong words`). The file decides.

## Message templates (adapt to the language of the game)

- **Opening**: "Hangman Plus — category: [CATEGORY]. A word of [N] letters, 7 lives. Mask: [_ _ _ …]. Propose a letter, the whole word (a wrong word costs 2 lives), or spend a token: definition (−15 points on a victory) or rescue letter (−25 points on a victory), once each."
- **After a turn**: "[MASK] — Lives: [N]. Found: [LETTERS]. Missed: [LETTERS]. Words tried: [LIST OR "none"]. Tokens remaining: [DEFINITION / RESCUE LETTER / NONE]."
- **Repetition**: "Already [proposed / known / tried] — no cost. Propose something else."
- **Victory**: "Found it: [WORD]! Score: [CALCULATION DETAIL]. Victory streak: [STREAK_AFTER]."
- **Defeat**: "No lives left. The word was: [WORD] — [DEFINITION]. Score: 0, streak reset to 0."
