---
name: "twenty-questions-reversed"
description: "Run a Twenty Questions, Reversed game: a solo yes/no deduction game in chat, in two phases. In Phase A the user thinks of a secret subject in one of six announced categories and the assistant guesses it in at most 20 closed questions answered by Yes / No / I do not know buttons, with no guess attempt before the 8th counted exchange. In Phase B the roles reverse: the assistant seals its subject in a written card in the game state before the phase starts, and the user guesses it in at most 20 closed questions in free text. An I do not know answer counts in the 20, and a guess attempt counts as a question in both phases. Use when the user wants twenty questions, a reversed guessing game, 20 questions inversé, vingt questions, or a yes/no deduction game."
---

# Twenty Questions, Reversed — two crossed deductions, 20 questions each

Your assistant referees a solo deduction game, played right in chat, in two phases around the same announced perimeter. **Phase A**: the user thinks of a secret subject and announces only its category; the assistant guesses it in at most **20 closed questions**, answered with **Yes / No / I do not know** buttons. **Phase B**: the roles reverse. The assistant chooses a subject, writes it into a **sealed card** in the game state **before** the phase starts, announces only its category, and the user guesses it in at most **20 closed questions** asked in free text. Each phase is won by naming the subject inside the bound; the score rewards speed.

A complete game is the two phases chained, A then B. That is the default format and the only one that feeds the combined reading and the streaks. At framing, the user may choose a single phase (A only or B only); the choice is written into the state before the game starts and never changes mid-game.

This game is **solo only**: one player, in chat, no group mode, no roles handed out to anyone else, no messages to anyone.

## What you need

- A Muse assistant (this skill installed).
- **Nothing else.** No account, no connection, no messaging group, no setup. The game is played solo, in chat, in the language of the conversation.

## Data layer (the skill ships none of it)

All game data lives in a data folder **the user owns**, never inside the skill. On first use, create it with the user (suggested default: `~/twenty-questions-reversed/`, any folder the user prefers works):

- `games/<game-id>.json` — one state file per game (schema in `references/twenty-questions-reversed.md`). It holds the framing, the Phase A journal (questions, answers, counter, live hypotheses, ruled-out families, incoherences), and, for Phase B, the **sealed card**: the assistant's subject, its 12 to 20 written attributes, its predefined answers and its supporting facts, written in full before the phase opens and never changed afterwards. Phase A never holds the user's subject during the phase; it is written in only at the reveal.
- `scores.json` — the persistent history of finished games (entry format in `references/twenty-questions-reversed.md`). Each entry carries both phase results, both scores, and the Phase B streak after the game, recomputed from the file at every writing, never held from memory. Subjects enter it only at the end of a game, once revealed on both sides.

No real identifier is ever written into the skill or a shared file: only into the user's private data folder. There is no configuration to fill in: a game can start as soon as the user asks.

## Router

| The user says | Do |
|---|---|
| "twenty questions reversed", "20 questions inversé", "vingt questions", "twenty questions", "yes/no deduction", "jeu de déduction oui/non", "play a guessing game" | Run a solo game in chat: read `references/twenty-questions-reversed.md` (the rules) and follow it |
| "continue the game", "reprends la partie", "on continue" | Re-read the most recent in-progress game's state file and resume from it, with no leak (resume announcement per `references/twenty-questions-reversed.md`) |
| "what is my streak", "c'est quoi ma série", "my scores", "mes scores", "mon historique" | Read `scores.json` in the user's data folder and answer from the file: Phase B streak, phase results, games played |
| Any other game by name | Be honest: Twenty Questions, Reversed is the only game in this skill. Others are not included and are never simulated or improvised |

## Running a game, in short

1. **Framing**: at most one framing question, the format (complete, A only, or B only), written into the state before anything starts. The language is the conversation's language.
2. **The perimeter, announced at the start of each phase**: a valid subject belongs to exactly one of six categories: **animal, object, trade or profession, place, fictional character, food**. No abstract concept, no word or expression, no event, no real person, no private person, no private address. Whoever chooses the subject announces **its category only, never the subject**: knowing the category is the help that makes 20 questions enough.
3. **Phase A, the assistant guesses**: the state is created, the user announces a category, and the assistant asks **one closed question at a time**, numbered ("Question 4/20"), answered by the three buttons **Yes / No / I do not know**, always in that order, always all three. After each answer the assistant updates the state (journal, counter, ruled-out hypotheses with dated reasons, live leads) before the next question. The assistant's questions ask about perceptible traits or commonly known facts, never encyclopedia detail the chooser has no reason to know.
4. **Phase A attempts, threshold settled**: the assistant may name a subject to guess only **from the 8th counted exchange** onward. Before that, trait questions only, even if it believes it already knows. A failed attempt counts, and the attempted subject is ruled out in the state.
5. **Phase B, roles reversed**: before announcing the category, the assistant chooses its subject inside the perimeter and writes the complete sealed card into the state: subject, category, **12 to 20 verifiable attributes** (including predictable negations), predefined answers to the most predictable questions, and one or two supporting facts. Only the category is announced. The user then asks closed questions in free text, one at a time; the assistant answers **only** "Yes", "No" or "I do not know", plus the counter, with no comment and no differentiated reaction.
6. **Phase B answering discipline**: the assistant answers strictly from the sealed card. A covered question gets the card's answer; a question whose answer follows unambiguously from a written attribute gets the deduced answer, with the attribute logged; anything else gets "I do not know", which counts in the user's 20. A hole in the card is never filled by improvisation, and a given answer is never corrected mid-phase.
7. **Phase B attempts**: the user may guess **at any time**, from the first exchange onward. Each attempt counts, right or wrong, and a wrong one rules that subject out.
8. **End of a phase**: a correct attempt ends the phase at once. At 20 counted exchanges with no correct attempt, the subject is revealed and written into the state. Score per phase: found in N exchanges scores **21 − N** points; a failure at 20 scores **0**. Before closing a complete game, every Phase B answer is rechecked line by line against the sealed card and the result is logged and told to the user in one sentence.

## Standing rules (they protect the game)

1. **Closed questions only**: every question must call for exactly "yes", "no" or "I do not know". A compound question joining two facts is not closed (see the edge cases in the reference for each phase).
2. **20 counted exchanges per phase, no exceptions**: the counter lives in the state and is shown at every turn. An "I do not know" answer **counts** in the 20, in both phases: 20 questions measure 20 exchanges, not 20 useful pieces of information. An "I do not know" authorizes **no elimination**: the question is logged as carrying no information, and the unknown is never treated as a "no".
3. **A guess attempt counts as a question, in both phases**: naming a precise subject to ask "is it this?" consumes one exchange, right or wrong. A category or trait question ("is it a sea animal?") is not an attempt: it is an ordinary question.
4. **The state file is the truth**: re-read at the start of every turn, rewritten at the end of every turn (questions, answers, counter, hypotheses). One file per game. No deduction lives only in the conversation.
5. **No leak, either way**: in Phase B, nothing from the sealed card (subject, attributes, facts) appears in any message before the final reveal, not even as a hint, a summary, or a warmer tone after a good question; the referee's tone stays neutral after good and bad questions alike. In Phase A, the assistant never claims to know the subject before attempting it, and never publishes its full candidate list: hypotheses live in the state.
6. **Phase A threshold**: no guess attempt before the 8th counted exchange. The rule blocks luck disguised as strategy and keeps scores comparable between games.
7. **The sealed card governs Phase B**: written in full before the phase opens, never rewritten afterwards, holes and errors included. Holes are logged, told frankly at the reveal, and every answer is rechecked against the card at the end.
8. **The first answer stands (Phase A incoherences)**: if the user's answers contradict each other, the assistant flags it once, kindly, naming both answers, and deduction continues on the **first** version; the second is logged in the incoherences list. The single exception is an explicit button mistake corrected by the user before the next question, which replaces the first version and is logged as a correction, with no change to the counter.
9. **Score exactly as written**: found in N scores 21 − N, failure scores 0, no bonus, no negative points, no points for a good question. The two phase scores are always named separately, never merged into one game score. The Phase B streak counts consecutive complete or B-only games where the user found the subject in Phase B; a Phase B failure resets it to 0, an A-only game neither raises nor resets it, and it is always recomputed from `scores.json`.
10. **The user can stop everything** at any time: the game is marked abandoned. In Phase B, the sealed card is not revealed in an abandon recap unless the user explicitly asks. A game abandoned before the end of its first phase writes no `scores.json` entry.
11. **Language**: the language of the conversation, fixed in the state at framing. This skill's files are in English; the game itself is played in the player's language.

## What this skill is not

- Not a group game: there is no group mode, no messaging connection, no roles and no private distribution. One player, in chat.
- Not a trivia quiz: the assistant never answers from general knowledge in Phase B, only from the sealed card written before the phase, so that every answer can be rechecked after the game.
- Not flexible on its frame: 20 counted exchanges per phase, the attempt threshold of Phase A, the counting of "I do not know", and the scoring scale are the game. Variants are other games, and they are not improvised here.
