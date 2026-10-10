# Word Chain, refereed — group game template

Runs on the generic mechanism in `references/group-messaging.md` (the user's connection, designated host group, host approvals, state held in a file) — this document defines only the game's rules and the referee's work. Unlike the secret-based games, this one has **no hidden information between players**: everything is played in the public thread of the group, and that is precisely what makes it simple to referee. No group, account, or proper name is hardcoded here.

## The game in one sentence

In the group thread, the players chain words of **one imposed category** for the round: each word must start with the **last letter of the previous word**. The referee validates every link (attack letter, membership in the category, non-repetition), signals faults kindly, holds the group's **collective lives** and the **record** of the longest chain. The group plays together against the chain stopping — not against each other.

## Parameters of a round

| Parameter | Settled rule |
|---|---|
| Players | **2 to 8 registered players** in the host group's config. Below 2, chaining has no game in it; above 8, the thread becomes unreadable. Outside those bounds: the referee tells the host before the announcement. |
| Category | **One single category per round**, chosen by the host (or drawn by the referee from the list below if the host asks) and announced before the starting word. It never changes mid-round. |
| Starting word | Supplied by the referee: a word of the category, common, ending on a playable letter (see "impossible attack letter"). It counts as the **first link** of the chain. |
| Collective lives | **3 lives for the whole group**, per round. Each fault validated as such costs 1 life. At 0 lives, the chain stops: immediate end of round. Lives are neither individual nor rechargeable mid-round, except the letter joker (see Edge cases), which is an expense of a life, not a gain. |
| Order of play | **Free, in the thread**: any registered player may propose the next link, but **never two valid proposals in a row from the same player** (see Edge cases). No imposed turn: asynchronous play rewards whoever passes through the thread, not whoever waits for a turn. |
| Chain length | Number of valid words chained, **starting word included**. That number is what is compared to the record. |
| Host | The host picks their mode (**player** or **spectator**, see `group-messaging.md`, section b bis); the choice is recorded in the state (`config.host_mode`). In spectator mode, the host proposes no word. |

### Starting categories (template list)

Cities, animals, jobs, first names, fruits and vegetables, household objects, sports, countries, rivers and mountains, musical instruments, brands and models known to everyone. The host may propose another category if it meets two conditions, checked by the referee before the announcement: (1) a common vocabulary shared by the players (no specialist category), (2) enough words starting with varied letters for a chain to live. A category that is too narrow is refused before launch, never discovered to be narrow mid-round.

## Attack letter and normalization — mechanical rules

Letter validation is **purely mechanical**: it depends on no dictionary and is never given the benefit of the doubt (see Dispute).

1. **Expected letter**: the **last alphabetic letter** of the last valid word of the chain.
2. **Attack letter**: the **first alphabetic letter** of the proposed word.
3. **Accents do not change the letter**: `é`, `è`, `ê`, `ë` count as `e`; `â`, `à` as `a`; `î`, `ï` as `i`; `ô` as `o`; `û`, `ù`, `ü` as `u`; `ç` as `c`; `ÿ` as `y`. Example: after a word ending in `e`, "éléphant" is a valid attack.
4. **Case is ignored**: "Lyon", "LYON" and "lyon" are the same word.
5. **Compound words and hyphens**: the word counts as a single word. Its attack letter is the first letter of its first element, its last letter is the last letter of its last element. Example: "orang-outan" attacks on `o` and ends on `n`; "chauve-souris" attacks on `c` and ends on `s`. The apostrophe follows the same logic ("l'hôtellerie" is not a category word in itself: the proposed word must be the full noun, without an article).
6. **Articles and determiners forbidden**: propose the word alone ("lyon", not "the city of Lyon"). A message that contains the word unambiguously ("I propose: Lyon!") is read in good faith: the referee extracts the proposed word and recalls it in the validation.
7. **Reference form of a word**: singular, without article, usual spelling. The plural of a word already played counts as a repetition ("lion" then "lions" = the same word, see Non-repetition). Two genuinely different words, however, are never merged by the referee ("lion" and "lionne" are two distinct words).

## How a round runs — in the public thread

1. **Announcement** (referee's message, approved by the host per the mechanism): the game, the category of the round, the registered players, the 3 collective lives, the reminder of the three possible faults (letter, category, repetition), the "never twice in a row the same player" rule, and the inactivity deadline (see Edge cases). No information is distributed privately: this game has no secrets.
2. **Starting word**: the referee publishes the starting word, its category and the expected letter for the next link. Example: "Starting word: **panda** (animals). Over to you: an animal starting with **A**. Lives: 3."
3. **Proposal**: a registered player writes **a single word** in the thread (in a message that contains it unambiguously). Discussion, jokes and encouragement in the thread are free and welcome, but they do not count as proposals: only the first message a player presents as their proposal — or that contains only one word of the apparent category — is judged. In case of real ambiguity, the referee asks in the thread "is that your proposal?" **before** judging; the answer settles it, with no possible fault on the clarification.
4. **Public validation**: the referee answers in the thread, after each judged proposal, with a short message that says: the word, the verdict, and — if the word is valid — the new expected letter, the current length of the chain and the lives remaining. If the word is refused: the reason in one sentence, kindly, the lives remaining, and the reminder that the chain still waits for a word starting with the same letter (the last valid word does not change).
5. **Chaining**: as soon as the validation is published, the hand is open for the next link. **Simultaneous proposals**: if two proposals arrive before the referee has validated the first, only the **first in thread order** is judged. The second becomes a **stale proposal**: it is neither valid nor a fault (its author was playing on the old last word, in good faith); its author may re-propose it — or propose another — once the new expected letter is known. No life is ever lost on a stale proposal.
6. **End of round**: the round ends in one of these cases, and in no other improvised one — lives exhausted (3 faults), inactivity deadline reached, or the host ends it. See "End of round and writings".

## Validating a link — the three checks, in this order

The referee applies the three checks **in this order**, and announces the first one that fails (a single ground of refusal per proposal: reproaches are never cumulated).

### 1. Attack letter (mechanical)

The normalized first letter of the proposed word must be the expected letter (normalized last letter of the last valid word). Otherwise: **letter fault**, 1 life lost, the word does not enter the chain. There is nothing to discuss: the letter is observed, not interpreted (see Dispute).

### 2. Non-repetition (factual, from the state)

The proposed word — in its normalized form (lowercase, without accents, singular) — must not already appear among the **valid words of this round's chain** (starting word included). Otherwise: **repetition fault**, 1 life lost, the word does not enter the chain.

- Only **valid** words consume a word. A word refused earlier in the round (for letter or for category) **may be re-proposed later** if, at that moment, it passes the three checks: a refusal does not burn the word, only the chain can.
- Repetition is judged round by round: a word played in a previous round may come back in a new round.

### 3. Membership in the category (the referee's judgement)

The word must designate something that belongs to the round's category, in its common sense. The referee judges **with their own lexicon**: no guaranteed external dictionary is connected to the game, and this reference does not claim otherwise. Concretely:

- A common word clearly in the category: accepted.
- A common word clearly outside the category: **category fault**, 1 life lost.
- A rare, regional, specialized word or one at the boundary of the category: the referee applies the **benefit of the doubt for the category** (see Dispute): on a real, documentable hesitation, the word is **accepted**, and the referee says so in the validation ("borderline word, accepted on the benefit of the doubt: sponges are animals, even if one first thinks of the object"). The hesitation is not a fault and costs no life.
- A word accepted on the benefit of the doubt enters the chain and is consumed like any valid word: it cannot be played again in the round.

### What is NEVER a fault

- A stale proposal (see How a round runs, point 5).
- A clarification request, a dispute (see Dispute) or a discussion message in the thread.
- A word proposed by an unregistered player or by a spectator: the referee notes it kindly ("only registered players propose links"), with no life lost; the word is not judged and is not consumed.
- A proposal from the same player as the previous valid link: it is **not judged** (see Edge cases, "same player twice in a row"), with no life lost.

## Collective lives — accounting

- Start: **3 lives**, displayed at the announcement and after every validation.
- Each fault (letter, repetition, clear category) costs **exactly 1 life**, announced in the validation message that records it.
- At **0 lives**: the referee immediately announces the end of the chain, in the same thread: final length, the complete chain, and the fate of the record (see End of round). No later proposal is judged for this round.
- Lives are **collective**: a fault costs the group, never a named player. The referee's messages never designate a "responsible" party for the end of the chain; they thank the players for the links, faults included — faults are part of the game and often its funniest moments.

## The group's record — persisted, per category

**Settled decision: the record is kept per category** (longest chain in "animals", longest chain in "cities", etc.), not as a single general record. Justification: categories do not have the same difficulty nor the same available vocabulary; a general record would crush every round toward the easiest category and make the other records invisible. The end-of-round recap may mention, for information, the longest chain across all categories — but that is a display derived from the per-category records, not a separate record to maintain.

### File and schema

The record lives in the **user's data** (never in the skill), in a dedicated file: `records-word-chain.json`, at the root of the skill's data folder (French source name: `records-chaine-de-mots.json`). It survives between games: each finished round re-reads it, compares, and rewrites it only if its category record is beaten.

```json
{
  "game": "word-chain",
  "records": {
    "animals": {
      "length": 14,
      "chain": ["panda", "antilope", "éléphant"],
      "game_id": "word-chain-2026-10-10-2100",
      "date": "2026-10-10",
      "players": ["<names of the players of the round>"]
    }
  }
}
```

- `length` = number of words in `chain` (starting word included) — the two values check each other.
- `chain` keeps the words as they were validated (the players' spelling, accents included): the record is also a souvenir of the round.
- A round that does not beat its category's record writes **nothing** in this file; its result lives in its own state (see the state schema). A round that ties does not replace the record in place: the first arrival keeps the record, and the tie is noted in the end-of-round recap.
- For a test game, the record file carries the `-TEST` suffix (`records-word-chain-TEST.json`): a test never beats the group's real record.

## Dispute — written procedure

The referee judges with their lexicon, with no guaranteed external dictionary: they can therefore be wrong, and the players may dispute them. The procedure is the same for a disputed refusal ("this word is in the category") and for a disputed acceptance ("this word is not").

1. **Who and when**: any registered player may dispute, in the thread, **before the next link is validated**. After the next link is validated, the dispute is late — except if it reveals a mechanical error (letter or repetition), which is corrected at any time (see point 4).
2. **Suspension**: as soon as a dispute is filed, the chain pauses: no new proposal is judged until the verdict. The referee announces it in one sentence.
3. **Who settles it**: **the host settles it**, after hearing the disputing player's argument (a short message: why the word is, or is not, in the category) and the referee's position (they say what their judgement rested on). The host does not have to justify themselves in the thread; their verdict is published by the referee and closes the dispute.
4. **Verdict rules, by ground**:
   - **Category**: the **benefit of the doubt** plays in favour of the word. If membership is genuinely debatable (rare word, double meaning, category boundary), the word is **accepted** — whether the dispute targets a refusal (the word enters the chain) or an acceptance (the word stays in it). At the verdict, the host may refuse only a word whose outsideness to the category is clear.
   - **Letter**: **never any benefit of the doubt**. The letter is checked mechanically under the normalization rules written above; if the referee got the letter wrong, they acknowledge it, correct the verdict and **restore the life** if a letter fault had been wrongly counted.
   - **Repetition**: the file settles it. The referee republishes the list of the round's valid words from the state; if the word is in it, the fault stands; otherwise, verdict corrected and life restored if applicable.
5. **Effects of the verdict**:
   - Refusal overturned (the word is accepted): the word enters the chain in its place, the life lost for its fault is **restored**, and the expected letter becomes the last letter of that word.
   - Acceptance overturned (possible only for a clear outsideness to the category): the word leaves the chain. If no link has yet been built on it, the chain restarts from the previous valid word, **with no life lost or restored** (the error is the referee's, not the group's). If a next link has already been validated on it, see Edge cases, "late dispute".
   - Verdict confirming the referee: play resumes exactly where the dispute had suspended it. Disputing in good faith never costs a life, whatever the verdict.
6. **One single dispute per link.** The same verdict is not re-disputed; the round continues. The host may end a round that turns into an endless argument; that is an ordinary end of round (see End of round).

## The referee's work (reminder of the rules that protect the game)

1. **Validation after every proposal, with no hidden refereeing delay.** The referee never lets two links chain without a validation between them: the validation is what advances the expected letter.
2. **Kindness of form, firmness of substance.** Refusals are short, without reproach, and always say what to play next ("we still need a word in T"). No message mocks a player, compares players to each other, or designates anyone responsible for a lost life.
3. **The state is the truth.** After every event (judged proposal, fault, lost life, dispute, verdict, end of round), the referee re-reads and rewrites the state file: chain of valid words, refused proposals and their grounds, lives remaining. Repetition counts and the length are always recomputed from the file, never from memory.
4. **No disguised hint.** The referee never suggests a word, never gives an example that would amount to a proposal ("for example an animal in T like…" is forbidden mid-round) and never comments on the difficulty of the expected letter beyond the fact ("expected letter: K — good luck" is allowed, it is a public fact).
5. **The host approves the sends** per the generic mechanism; in host-player mode, the host sees in the previews only what the whole thread will see — this game has no secret content to protect, and it is said as such at the announcement.

## State schema — `games/<game-id>.json`

`game-id`: `word-chain-<YYYY-MM-DD>-<hhmm>` (prefix `TEST-` for a test game). One file per round. (French source folder: `etats/<partie-id>.json`.)

```json
{
  "id": "word-chain-2026-10-10-2100",
  "game": "word-chain",
  "status": "in_progress | finished | abandoned",
  "language": "en | fr",
  "created_at": "2026-10-10T21:00:00-04:00",
  "config": { "platform": "messenger", "conversation": "<the user's host group>", "host": "<host name>", "host_mode": "player | spectator" },
  "parameters": { "category": "animals", "initial_lives": 3, "inactivity_deadline": "<duration or deadline announced>" },
  "players": [ { "name": "<name in the group>" } ],
  "starting_word": "<word supplied by the referee>",
  "chain": [
    { "position": 0, "word": "<starting word>", "player": null, "expected_letter": null, "status": "start" },
    { "position": 1, "word": "<validated word>", "player": "<player name>", "expected_letter": "<normalized letter required>", "status": "valid | valid_benefit_of_doubt" }
  ],
  "proposals": [
    { "player": "<name>", "word": "<proposed word>", "verdict": "valid | valid_benefit_of_doubt | letter_fault | repetition_fault | category_fault | stale | not_judged_same_player", "expected_letter": "<letter at the time of the proposal>", "time": "2026-10-10T21:05:00-04:00" }
  ],
  "lives_remaining": 3,
  "last_valid_player": null,
  "letter_joker_used": false,
  "record_before": { "category": "animals", "length": 0, "game_id": null },
  "record_after": null,
  "record_beaten": false,
  "log": [
    { "time": "2026-10-10T21:00:00-04:00", "event": "round_created" }
  ]
}
```

- `chain` contains only the **valid** words (start included): it is the reference list for the repetition check and for the length. `proposals` contains **everything** that was judged or set aside, with its verdict: it is the refereeing proof, showable to the players after the round.
- `record_before` is read from the records file at launch and copied into the state; `record_after` and `record_beaten` are filled at the end of the round, at the moment of the possible writing (see End of round).
- The log records every dated event: creation, announcement, starting word, every validation and every fault (with its ground), disputes and verdicts, recourse to the joker, end of round and its ground, record writing if applicable.

## End of round and writings

The round ends when the lives fall to 0, when the announced inactivity deadline is reached without a new valid link, or when the host ends it. In every case:

1. **Final message in the thread** (approved by the host): the ground of the end, the **final length**, the **complete chain** word by word, the lives remaining if any remain, and the fate of the record: beaten (new category record, with the old figure), tied, or not beaten (with the standing record and its figure). Warm and brief; no fault is attributed by name in it.
2. **State**: `status` becomes `finished` (or `abandoned` if the host ended a round nobody was playing anymore, per the generic mechanism), `record_after` and `record_beaten` are filled, and the log is closed by the end event.
3. **Record**: if the final length strictly exceeds the category's record, the referee rewrites `records-word-chain.json` (or its `-TEST` version) with the complete new entry (length, chain, game, date, players). Otherwise, the records file is not touched.
4. **No entry in `scores.json`**: as for the other group games, the result lives in the game's state; the records file is the only persistent writing specific to this game.

## Variants (chosen by the host BEFORE the round, written in the state, never mid-round)

- **Last syllable** (designed for spoken French): the next word must start with the **last syllable** of the previous word, judged by ear ("éléphant" → a word starting with the sound "fant"… the rarity of possible attacks makes the variant short and funny rather than long: lives kept at 3 as in the base game, but the referee announces an express round). The syllable is judged on common pronunciation; in case of disagreement on the syllable split, the dispute follows the ordinary procedure and the host settles it — it is the only variant where even "the letter" becomes a question of interpretation, and the announcement says so.
- **Two last letters**: the next word must start with the **two last letters** of the previous word (identical normalization). Hard variant: many word endings have no possible attack; the letter joker (Edge cases) then becomes a **pair joker**, under the same conditions. The referee chooses a starting word whose ending opens at least a few known attacks, and says so at the announcement.
- **Free category**: no imposed category; only the letter and non-repetition constrain. The record, in this variant, is kept under the `free_category` key of the records file. The category fault disappears; the letter and repetition faults remain, lives unchanged.
- **One variant per round only**: variants are combinable one by one — a single variant per round (combining them would make the rules unreadable in a thread) — the host chooses, the referee announces which one, in full words.

## Edge cases (settled)

- **Same player twice in a row**: **forbidden**. A proposal from the player who supplied the last valid link is not judged: the referee answers in the thread "you just played the previous link — over to the next player to propose", with no life lost and without consuming the proposed word (the player may re-propose it later if the expected letter then allows it and another player has played in between). A player whose proposal was **refused** (fault) is not "the last valid player": they may re-propose immediately, and another player may also take the hand. If only one registered player remains active and they are the last valid player, the round ends by the inactivity deadline or by the host's decision: the rule is never waived for a lone player.
- **Impossible or near-impossible attack letter in the category** (e.g. the chain arrives on a word ending in `k` in the "animals" category, or in `w` in "cities"): the chain does not die in silence. The referee announces the letter and the apparent blockage ("expected letter: K"). The group then has **one letter joker per round**: a player claims it in the thread, the group pays **1 collective life**, and the referee designates a **new attack letter** drawn among the letters that open common words of the category — the last valid word stays the same, only the expected letter changes, and the joker used is recorded in the state. With no life remaining, or the joker already used in the round: no recourse, the chain stops as soon as the group notes the blockage or at the inactivity deadline, and the end of round follows the ordinary procedure. The joker never resurrects an already finished round.
- **Compound word, hyphen, apostrophe, accents**: see "Attack letter and normalization" — accents neutralized (`é` = `e`), a compound read as one block (first letter of the first element, last letter of the last element), an article never counted in the word.
- **Borderline out-of-category word**: benefit of the doubt for the category (see Validation, check 3, and Dispute): accepted if membership is genuinely debatable, refused only if outsideness is clear. The referee gives the reason in one sentence in the validation when accepting a borderline word, so the group sees the rule being applied, not a favour being done.
- **Late dispute that overturns an acceptance already built on**: if a valid link was built on the overturned word, the chain is **rewound** to the last undisputed word: the overturned link and the link built on it leave the chain, their words become available again, no life is lost or restored for this rewinding (the error is the referee's), and play resumes at the letter of the last undisputed word. It is the only permitted form of rollback, and the log records it in full words.
- **Inactivity deadline**: announced at the opening (by default, the duration the host sets for their asynchronous games; failing that, 24 h without a valid link or a judged proposal). Reached: ordinary end of round, the record counts as for any end of round — a long but abandoned chain remains a long chain.
- **Player who stops playing or leaves the group**: the round continues without them; their already validated links stay in the chain (they were played). If all players but one desert, see "same player twice in a row".
- **Word proposed in another language**: the round is played in the announced language (the group's language, see the generic mechanism). A common foreign word that has passed into usage in that language is judged normally; otherwise, a category fault in the broad sense ("this word is not in the round's vocabulary"), 1 life — except on the first occurrence in the game, where the referee may content themselves with a reminder without a fault, said as such in the thread. This gracious reminder is granted only once per round, all players combined.
- **Abandoned game**: status `abandoned`, a short end message in the thread (approved by the host). The record **still counts** if the abandoned chain was beating it: the length was reached in play, in front of everyone; the record writing follows the ordinary procedure and the state log says why the round stopped.
- **Counting dispute** (length, lives, record): the referee republishes, from the state, the chain of valid words, the list of proposals and their verdicts, and the records file. The file settles it.

## Message templates (adapt to the language of the game)

- **Announcement**: "Word Chain — new round! Category: **[CATEGORY]**. Rule: each word starts with the last letter of the previous word, in the category, without ever repeating a word of the chain. The group has **3 collective lives**: a letter, category or repetition fault costs one. Never two links in a row by the same player. Category record: **[LENGTH]** — to beat."
- **Starting word**: "Starting word: **[WORD]**. Over to you: a word of the category starting with **[LETTER]**. Length: 1. Lives: 3."
- **Validation of a link**: "✅ **[WORD]** ([PLAYER]) — chain: [LENGTH]. Next: a word starting with **[LETTER]**. Lives remaining: [N]."
- **Refusal**: "❌ **[WORD]** — [GROUND IN ONE SENTENCE, KINDLY]. The chain stays on **[LAST VALID WORD]**: a word starting with **[LETTER]** is still needed. Lives remaining: [N]."
- **Borderline word accepted**: "✅ **[WORD]** ([PLAYER]) — borderline word, accepted on the benefit of the doubt for the category: [REASON IN ONE SENTENCE]. Chain: [LENGTH]. Next: **[LETTER]**. Lives remaining: [N]."
- **End of round**: "🏁 End of the chain! Final length: **[LENGTH]** words. The chain: [WORD 1 → WORD 2 → …]. [RECORD: beaten / tied / category record still at LENGTH]. Thanks to all the players — we start again on another category whenever you want."
