# Twenty Questions, Reversed — yes/no deduction, solo, in two phases: full rules

Reference for the `twenty-questions-reversed` skill. A **solo game, in chat only**. The principle of twenty questions is a classic of the public domain; the rules below are rewritten and adapted to chat: buttons in Phase A, free text in Phase B, state files and a sealed card under the discipline settled here (key written into the file before play, state re-read and rewritten at every turn). No real name, no group, no account is hardcoded in this document.

## The game in one sentence

One game, two crossed deductions around the same perimeter. **Phase A**: the player thinks of a secret subject, the assistant guesses it in at most 20 closed questions. **Phase B**: the roles reverse: the assistant chooses a subject, seals it in a card written into the state **before** the phase, and the player guesses it in at most 20 closed questions asked in free text. Each phase is won by finding the subject inside the bound; the score rewards speed.

## Presentation — settled

**A complete game = the two phases chained, A then B.** That is the default format and the only one that feeds the combined reading and the streaks (see Scores). At framing, the player may choose **a single phase** ("A only" or "B only"); the choice is written into the state (`format: "complete" | "a_only" | "b_only"`) **before** starting and never changes during the game. Justification: the two phases do not exercise the same role (guessing / being guessed), and comparing them requires the complete format; a single phase stays useful when time is short, but it is recorded as such and does not count in the streaks of complete games.

At most one framing question (the format), never an interrogation. The language is the conversation's language.

## The perimeter — announced at the start, always

At the start of each phase, the referee announces the perimeter **in writing**. A valid subject belongs to exactly one of these six categories, and the player (Phase A) as well as the assistant (Phase B) **announce the category, never the subject, at the start of the phase**. Knowing the category is the help that makes 20 questions sufficient; hiding the category too would make the bound arbitrary.

| Category | Definition | Valid examples | Out of perimeter |
|---|---|---|---|
| `animal` | A real animal species, identifiable by a common name | giraffe, emperor penguin, beaver | a named individual animal, an imaginary creature |
| `object` | A common or famous physical object, named by its generic name or its famous identity | umbrella, lighthouse, acoustic guitar | an obscure precise commercial model, an abstract object |
| `trade` | A recognizable trade or profession | baker, plumber, airline pilot | an invented job title, a company |
| `place` | A geographical place or a famous monument, named | Eiffel Tower, Sahara desert, Venice | a private address, a fictional place |
| `fictional_character` | A widely known fictional character (published and distributed work) | Sherlock Holmes, Mario | a character invented by the player, a disguised acquaintance |
| `food` | A known food or dish, named | croissant, Savoy fondue, banana | a home recipe with no public name, a brand |

General exclusions, announced with the perimeter: no abstract concept (justice, happiness), no word or expression, no event, no real person (living or dead: only fiction gets its character), no private person, no subject whose identity depends on a detail almost nobody knows. A subject on the border of two categories is filed by whoever chooses it into the category they announce; that announcement is what counts for the phase.

## Rules common to both phases

1. **Closed questions only**: each question calls for exactly "yes", "no" or "I do not know". A compound question (two questions in one, "and" / "or" joining two facts) is not closed: see the edge cases specific to each phase.
2. **Bound of 20 counted exchanges per phase.** The counter is held in the state and shown at every turn ("question 7/20"). What counts and what does not is settled below, phase by phase, never improvised.
3. **"I do not know" counts in the 20 — settled.** In Phase A as in Phase B, a question the questioned party answers "I do not know" **consumes an exchange**: the counter advances. Justification: 20 questions measure 20 exchanges, not 20 useful pieces of information; otherwise a phase could stretch indefinitely and scores would no longer be comparable from one game to the next. Written consequence on both sides: an "I do not know" authorizes **no elimination**: the state records the question with the mention `no_information`, and neither the assistant (Phase A) nor the player (Phase B) may treat the unknown as a "no". (On the assistant's side in Phase B, its "I do not know" answers are strictly framed: see "The sealed card".)
4. **A guess attempt counts as a question — settled, in both phases.** Naming a precise subject to ask "is it this?" consumes an exchange, whether it is right or wrong. A wrong attempt adds the attempted subject to the ruled-out list in the state. A category or trait question ("is it a sea animal?") is **not** an attempt: it is an ordinary question, treated as such.
5. **The state is the truth.** The state is re-read at the start of every turn and rewritten at the end of the turn (questions, answers, counter, hypotheses). One single file per game. No deduction lives only "in the conversation".
6. **No leak.** In Phase B, nothing from the sealed card (subject, attributes, facts) appears in a message before the final reveal, not even as a summary, an insinuation, or a differentiated reaction ("good lead!" is forbidden: the same neutral tone after a good and a bad question). In Phase A, the assistant never claims to know the subject before attempting it.

## Phase A — the assistant guesses

### Flow

1. **Opening.** The assistant announces the perimeter (the six categories and the exclusions, in summary), restates the bound and the counting rules (attempt = 1 exchange, "I do not know" = 1 exchange), and asks the player to think of a subject and announce **its category only**. The state is created at that moment, `current_phase: "A"`, counter at 0.
2. **Questions by buttons.** The assistant asks **one closed question at a time**, numbered ("Question 4/20 — …?"), and the player answers by option buttons: **"Yes" / "No" / "I do not know"** (three buttons, always in that order, always all three, even if the assistant judges "I do not know" unlikely: the button exists so the player is never forced to settle what they do not know). A free-text answer from the player ("rather yes", "well, yes…"): see edge cases.
3. **After each answer**, the assistant updates the state **before** the next question: the question and the answer in the phase journal, the counter, and the hypotheses (see "Holding the hypotheses"). In the same message as the next question, it may say in one neutral sentence where it stands ("I am narrowing in on African mammals"), never a complete public list of candidates: that list belongs to the state.
4. **Attempts — threshold settled.** The assistant may attempt a guess only **from the 8th counted exchange** onward (counter ≥ 8, the attempt included: the first possible attempt therefore carries number 8 at the earliest). Before that threshold, it has only trait questions, even if it believes it already has the answer: the rule prevents a luck guess disguised as strategy and makes scores comparable. Each failed attempt counts (common rule 4) and the attempted subject is ruled out in the state.
5. **Closing.** Two outcomes:
   - **Found**: an attempt names the subject and the player confirms "yes". The phase ends immediately; the number of exchanges used is the phase's result (see Scores). The player then reveals, if they have not already done so by confirming, the exact spelling of the subject, which is written into the state **at that moment only** (never before: the guesser's state does not contain the subject during the phase, see the schema).
   - **Failure at 20**: the counter reaches 20 with no correct attempt. The player reveals their subject; the assistant writes it into the state and records, in the `what_misled` field, one honest sentence on what misled it (the answer that closed the right branch, the candidate family never explored, the hypothesis held too long). No excuse invented after the fact: the cause is read in the journal of questions and hypotheses in the state.

### Holding the hypotheses (in the state, at every turn)

The Phase A state permanently holds:

- `questions`: the ordered list of counted exchanges: number, type (`question` | `attempt`), text, answer (`yes` | `no` | `i_do_not_know`), and, for an attempt, the attempted subject.
- `ruled_out_hypotheses`: each ruled-out family or subject with the **dated reason** ("felines — ruled out at Q5: not carnivorous"). A ruling-out founded on an "I do not know" is forbidden (common rule 3): the question is then marked `no_information` and rules nothing out.
- `live_leads`: the families or traits still open after the last answer ("large African herbivores", "trunk or no trunk, unsettled"). It is from this list, re-read in the file, that the assistant draws its next question, not from its memory of the conversation.
- `incoherences`: see the dedicated edge case.

Quality of the assistant's questions (rule drawn from testing): the assistant asks about **perceptible traits or commonly known facts** about the subject (size, habitat, diet, appearance, use), not encyclopedia facts the subject's chooser has no reason to know (internal anatomy, exact figures, fine taxonomy). Each "I do not know" provoked by an overly scholarly question is an exchange burned by the assistant, not by the player; testing showed this, and the rule is written for that reason.

## Phase B — roles reversed, sealed card

### The sealed card — written BEFORE the player's first question

Before announcing the category of Phase B, the assistant chooses its subject inside the perimeter and writes into the state the **complete sealed card** (`card_b`, see the schema):

- `subject` and `category` (the category alone is announced to the player; the subject never leaves the file).
- `attributes`: **12 to 20 key attributes**, each in the form of a verifiable fact ("built mainly of iron", "height over 300 metres"), enough to answer predictable questions without improvising. The list covers at minimum: living or not, origin / location, material or composition when relevant, relative size (bigger / smaller than a human, than a house), era or age, function or use, salient visual traits, and **predictable negations** ("is not made of stone", "is not permanently inhabited"): a question "is it made of stone?" is not answered from "it is made of iron" by mere elegance; the negation is written, or the answer must follow unambiguously, otherwise it is "I do not know".
- `predefined_answers`: the answers to the most predictable questions for this subject (fine location, century of creation, function, fame), each `yes` / `no` anchored on an attribute.
- `supporting_facts`: one or two stable, sourceable facts, one line each, justifying the sensitive attributes (dates, dimensions).

**Answering discipline.** The assistant answers **strictly** from the card:

- Question covered by an attribute or a predefined answer → the card's answer, with no added comment.
- Question not covered but whose answer **follows unambiguously** from a written attribute (e.g. card: "built in 1889"; question: "is it over 100 years old?" → yes) → the deduced answer, and the attribute used is recorded in the phase journal with the question.
- Question not covered and not deducible → **"I do not know"**, which counts in the player's 20 (common rule 3). The assistant never fills a hole in the card by improvisation, even an "obvious" one: an incomplete card is paid for in "I do not know", and the hole is recorded (`card_holes`) to improve the next card. That is the verifiability of the phase at stake: after the game, **every Phase B answer is rechecked against the card**, line by line (see "End-of-game writings").
- The assistant never corrects an answer already given during the phase, even if it spots a hole or a card error: it records it, the phase continues on the card as it is, and the error is told frankly at the reveal.

### Flow

1. **Opening.** The assistant announces: Phase B begins, the **category** of its subject, the bound of 20, and the player's counting rules (attempt = 1 exchange, the assistant's "I do not know" = 1 exchange, non-closed question = reformulation with no penalty, below). The card is already in the state at that instant (journal: `card_b_sealed`, dated, **before** the opening).
2. **Questions in free text.** The player writes their questions one by one. The assistant answers "Yes", "No" or "I do not know": that answer alone, plus the counter ("7/20"), no comment, no differentiated reaction (common rule 6). Each counted exchange is written into the state (`questions_b`: number, player's text, answer, source in the card: cited attribute or the mention `deduced` / `hole`).
3. **Player's attempts — at any time, settled.** Unlike the assistant in Phase A, the player may attempt a guess **whenever they want**, from the first exchange onward: it is their risk, and each failed attempt counts (common rule 4) and rules out the attempted subject (recorded in `attempts_b`). The asymmetry is deliberate: the Phase A threshold disciplines an assistant strategy that must stay comparable from one game to the next; the human player also plays on instinct, and the identical counting of attempts is enough for the fairness of the score.
4. **Closing.** **Found**: an attempt names the subject of the card → immediate reveal: the assistant unveils the subject, the number of exchanges used, and invites the player to contest any answer that seems wrong to them (verification against the card then happens out loud, from the file). **Failure at 20**: the assistant reveals the subject and the complete card; any answer of the phase can be rechecked against it in front of the player.

## Scores, scale and streaks

Scale per phase, identical on both sides (settled):

- **Found in N counted exchanges → `21 − N` points** (finding in 8 is worth 13, in 12 is worth 9, in 20 is worth 1). **Failure at 20 → 0 points.** No bonus, no negative points, no points for a "good question": the scale pays only for the speed of the deduction, to stay comparable between games.
- In Phase A, the points measure the assistant's performance; in Phase B, the player's. A complete game therefore produces two separately named scores, never merged into a single "game score" that would mix the two roles. The honest reading of a complete game: "the assistant found it in 12, the player in 11".

`scores.json` — one entry per game:

```json
{
  "date": "2026-10-10",
  "game_id": "twenty-questions-2026-10-10-2100",
  "game": "twenty-questions-reversed",
  "language": "en",
  "format": "complete | a_only | b_only",
  "found_a": true,
  "questions_a": 12,
  "score_a": 9,
  "subject_a": "giraffe",
  "found_b": true,
  "questions_b": 11,
  "score_b": 10,
  "subject_b": "Eiffel Tower",
  "streak_b_after_game": 3,
  "test": false
}
```

- In `a_only` format, the `*_b` fields and `streak_b_after_game` are `null`; in `b_only` format, the `*_a` fields are `null`.
- **Streak (`streak_b_after_game`)**: the number of consecutive games, in formats `complete` and `b_only` only, in the chronological order of the file, where the player **found the subject in Phase B**, counted after the current game. A failure in Phase B resets the streak to 0; an `a_only` game neither raises nor resets it (it is ignored by the calculation, and its entry carries `null`). The streak is **recomputed from the file** at every writing; it is never held "in the head" between games.
- The subjects (`subject_a`, `subject_b`) enter `scores.json` only at the end of the game, once revealed on both sides: the history is shared between player and assistant only at that moment.

## State schema — `games/<game-id>.json`

`game-id`: `twenty-questions-<YYYY-MM-DD>-<hhmm>` (prefix `TEST-` for a test game). One single file for both phases.

```json
{
  "id": "twenty-questions-2026-10-10-2100",
  "game": "twenty-questions-reversed",
  "status": "in_progress | finished | abandoned",
  "language": "fr | en",
  "created_at": "2026-10-10T21:00:00-04:00",
  "format": "complete | a_only | b_only",
  "current_phase": "A | B | null",
  "phase_a": {
    "announced_category": "animal",
    "counter": 0,
    "attempt_threshold": 8,
    "questions": [
      { "number": 1, "type": "question | attempt", "text": "…", "answer": "yes | no | i_do_not_know", "attempted_subject": null, "no_information": false }
    ],
    "ruled_out_hypotheses": [
      { "hypothesis": "felines", "reason": "Q5: not carnivorous", "at_question": 5 }
    ],
    "live_leads": ["large African herbivores"],
    "incoherences": [
      { "at_question": 9, "first_version": "no", "second_version": "yes", "stands": "first_version", "detail": "…" }
    ],
    "outcome": null,
    "revealed_subject": null,
    "what_misled": null,
    "score_a": null
  },
  "phase_b": {
    "card_b": {
      "subject": "…",
      "category": "place",
      "attributes": ["…"],
      "predefined_answers": [ { "question_type": "…", "answer": "yes | no" } ],
      "supporting_facts": ["…"],
      "sealed_at": "2026-10-10T21:20:00-04:00"
    },
    "announced_category": "place",
    "counter": 0,
    "questions_b": [
      { "number": 1, "text": "…", "answer": "yes | no | i_do_not_know", "card_source": "cited attribute | deduced | hole", "type": "question | attempt" }
    ],
    "attempts_b": [ { "number": 4, "attempted_subject": "…", "correct": false } ],
    "penalty_free_reformulations": 0,
    "card_holes": [],
    "outcome": null,
    "score_b": null
  },
  "log": [
    { "at": "2026-10-10T21:00:00-04:00", "event": "game_created" },
    { "at": "2026-10-10T21:20:00-04:00", "event": "card_b_sealed" }
  ]
}
```

- **`phase_a` never contains the player's subject during the phase**: no subject field, no disguised hint. `revealed_subject` is filled only at the closing of the phase, from the player's reveal. It is the exact equivalent of a sealed key, inverted: here, it is the assistant's ignorance that must be structural, not merely promised.
- `card_b` is written in full, subject included, **before** the opening of Phase B (event `card_b_sealed` dated in the log **before** the first exchange of the phase) and never changes afterwards, holes and errors included: they are recorded, never rewritten.
- Each phase's `counter` counts only counted exchanges: answered questions (including "I do not know") and attempts. The penalty-free reformulations of Phase B are counted separately (`penalty_free_reformulations`), never in `counter`.

## Resuming a game

On "resume": scan `games/`, re-read the most recent `in_progress` state of this game, and announce a recap **with no leak at all**: format, current phase, counter of the current phase, outcome of the finished phase if there is one (found in N, or failure), and, for a Phase B in progress, the category only, never the subject of the card, never an attribute. In Phase A, the recap may re-read the questions already asked and their answers (the player knows them: they gave them); it reveals no "warm" hypothesis beyond the neutral sentences already said. The resume starts again from the re-read state, not from the memory of the conversation.

## Edge cases (settled)

- **Player's answer incoherent with their previous answers (Phase A).** Example: "no" to "is it carnivorous?" then, later, answers that suppose a predator. Procedure: (1) the assistant **flags it kindly, once, at the moment the incoherence becomes visible**, naming both answers, without accusing (the flagging states the rule, it does not negotiate: the interrogative form that would invite rewriting history is forbidden); (2) **the first version stands — settled**: the deduction continues on the first answer, the second is recorded in `incoherences` with both versions and the mention `stands: "first_version"`. Justification: if the last answer crushed the previous ones, a player could, by mistake or by play, move their subject mid-phase with nothing showing it; the first answer is the one on which the assistant engaged its questions. Single exception: if the player says explicitly, **before the next question**, "I pressed the wrong button at Q5, the right answer is yes", the correction replaces the first version, the incoherence is recorded as `button_correction` with both versions, and the counter does not change (the exchange happened, only its answer is corrected). (3) At the final reveal, the recorded incoherences are re-read out loud: if the revealed subject makes the first version false, that is noted in `what_misled`, and the phase stays counted as it was played, with no replay.
- **Subject out of perimeter discovered in Phase A.** The assistant can only discover it through the answers (it does not know the subject): for example, the answers draw an abstract concept while the announced category was `object`. Settled, in two stages: **clear discovery before the 10th exchange** (the answers are incompatible with **every** category of the perimeter, not only with the announced one) → the phase is **cancelled** (`outcome: "cancelled_out_of_perimeter"`, no score, no streak entry), the assistant says so frankly and proposes starting again with a subject inside the perimeter. **Late discovery (exchange 10 or later) or simple category mismatch** (the subject is inside the perimeter, but not in the announced category: a place announced as a famous `object`, for example) → **the phase is played to the end**, marked `out_of_perimeter: true` in the state with the detail; if the assistant finds it, the result is told with its mark ("found in 14, on a subject outside the announced category") and the phase counts neither in the compared scores nor in any streak: it enters `scores.json` with its normal fields but the end log notes the gap, and in `complete` format, the whole game is excluded from the streak calculation. Justification: cancelling late would punish an almost finished deduction for a framing fault; playing it silently would falsify the scores.
- **Player's non-closed questions in Phase B.** Open question ("where is it?"), enumerated multiple-choice question, question compound of two facts: the assistant answers with the reformulation template, "Rephrase in yes/no, with no penalty", **the counter does not advance**, nothing is answered on the substance (not even a half-hint), and the event is counted in `penalty_free_reformulations`. The player may reformulate indefinitely; only the form counts. If the reformulation changes the meaning (the player splits their compound question into two distinct questions), those are two ordinary counted exchanges from there on.
- **Assistant's non-closed question in Phase A.** The assistant asks none: its questions are born closed. If the player answers "your question is not closed" to an ambiguous or double question, the assistant acknowledges it, reformulates into **one** closed question, and the exchange counts **once only**, at the moment of the answer to the closed version; the faulty version is recorded in the phase journal.
- **Player's answer outside the buttons in Phase A** ("rather yes", "it depends", free text). The assistant asks them to settle it with one of the three buttons, without advancing the counter as long as the answer is not one of the three; a repeated "it depends" answer is an invitation to answer "I do not know", which does count (common rule 3) as soon as it is clicked.
- **Vague attempt** ("is it a big animal?", "something in Paris?"): it is not an attempt (common rule 4), it is treated as an ordinary question in both phases, counted as such, never as a guess.
- **The player reveals their subject by accident in Phase A** (they name it in a message): Phase A ends on the spot, `outcome: "revealed_by_accident"`, score 0 for the assistant (it deduced nothing from that name), and the reveal is recorded. In `complete` format, Phase B is played normally.
- **The player changes subject during Phase A** (detectable only through chained incoherences): at the **second** recorded incoherence, the assistant says so and asks whether the subject stayed the same; if the player confirms a change, the phase is cancelled and restarted from zero on the new subject (new phase state, counter reset to 0, the old phase stays in the log as `cancelled_subject_change`). If they maintain it, the phase continues under the "first version stands" rule for each incoherence.
- **Card hole discovered in Phase B** (a given answer turns out false against the supporting facts, or two answers contradict each other): never a correction during the phase (see answering discipline); the hole is recorded in `card_holes`, told frankly at the reveal, and if the hole plausibly cost the player the phase (false answer on a central trait), Phase B is marked `outcome: "faulty_card"` with the player's score set to `null` (neither found nor an honest failure: the game does not count in the streak, in either direction).
- **Abandoned game** (the player ends it, or the conversation stops durably): status `abandoned`; in Phase B, the card **is not revealed** in an abandon recap: it will be if the player explicitly asks, or at the resume. No entry in `scores.json` for a game abandoned before the end of its first phase; a phase finished before the abandon of the second is recorded normally with the original format and the mention of the abandon in the log.
- **Contesting an answer (Phase B).** The file settles it: the assistant re-reads the card out loud (attribute cited for each contested answer); if the card proves the assistant wrong, the "card hole" edge case applies. In Phase A, contesting bears on the player's answers: the state shows them as they were recorded turn by turn.

## End-of-game writings

1. Game state: outcomes and scores of both phases filled (or `null` according to the format), status → `"finished"`.
2. `scores.json`: add the entry in the "Scores" format above, streak recomputed from the file if it applies.
3. **Verification of Phase B**: before closing, re-read `questions_b` against `card_b` line by line and record the result in the log (`phase_b_verification`: number of answers rechecked, number of gaps). In a real game, this verification is told to the player in one sentence ("11 answers rechecked against the card: no contradiction"), which is the proof that the sealed card governed the phase.
4. No entry in any reusable question library: this game generates no reusable questions, and writing the guessed subjects there would create an anti-repetition with no object here (the same subject may come back from one game to the next; only the players' memory remembers it).

## Message templates (to adapt to the language of the game)

- **Game opening**: "Twenty Questions, Reversed. Perimeter: animal, object, trade, place, well-known fictional character, food. No abstract concept, no real person, no private place. Phase A: you think of a subject, you tell me only its category; I ask you at most 20 closed questions, you answer with the Yes / No / I do not know buttons. An attempt of mine counts as a question, an 'I do not know' too. I may only attempt a name from the 8th question onward. Then we reverse: I seal my subject in writing before you start. Here we go: your category?"
- **Phase A question**: "Question [N]/20 — [CLOSED QUESTION]?" (followed by the three buttons, always Yes / No / I do not know).
- **Phase B answer**: "[Yes | No | I do not know]. ([N]/20)" — nothing else.
- **Reformulation (Phase B)**: "Rephrase in yes/no, with no penalty: I can only answer a closed question, one single fact at a time. ([N]/20, counter unchanged)"
- **Incoherence flagging (Phase A)**: "Flagging it for you: at question [N] you answered [FIRST VERSION], and this one seems to say the opposite. I continue on your first answer, that is the rule, it is written, and I record both versions; we will re-read them together at the end."
- **Phase B reveal**: "It was: [SUBJECT] ([CATEGORY]). Found in [N] exchanges [OR: not found in 20]. My card was written before your first question; every answer can be rechecked against it, ask me for any of them."
- **Complete game end**: "Game finished. Phase A: [found in N / failure] — [SUBJECT A]. Phase B: [found in N / failure] — [SUBJECT B]. Scores: assistant [SCORE A], you [SCORE B]. Phase B found streak: [STREAK]."
