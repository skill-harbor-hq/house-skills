# You Are the Hero — persistent solo adventure campaign: full rules

Reference for the `you-are-the-hero` skill. Solo game, in chat, played by the user alone through a narrative choice campaign that continues from one session to the next. This document defines the author's discipline, the mechanics of a scene, the campaign state, and resume. It imposes no world: each campaign invents its own (see Tone and world).

## The game in one sentence

The player embodies a character in an original world; at each scene, the assistant-author presents a short situation and 2 to 4 choices as buttons, plus, always, the possibility of writing a free action, then applies **immediately** the consequence that had been **written in advance** for that choice. The campaign advances chapter by chapter, pauses between sessions, and resumes exactly where the state left it.

## Tone and world

- **All audiences**: danger and suspense allowed, no gore, no detailed violence, no adult content. A failure wounds or delays the character; it never mutilates them in the telling.
- **A 100% original world for every campaign**: places, peoples, trades, creatures, and objects invented for the campaign. Never a universe, character, place, or proper term borrowed from an existing work, licensed or not. If an invented name happens to resemble a known one, the author changes it before preparing the chapter.
- **Language**: the language of the conversation with the player.
- **Target duration**: a session lasts 15 to 30 minutes, that is **6 to 9 scenes**; a chapter counts **6 to 10 scenes** and fits in one or two sessions. A campaign counts 3 to 6 chapters, decided at creation, never silently lengthened along the way.

## The heart of the game: the generation discipline

This game holds together by one rule, which overrides all others:

> **Everything that happens to the player was written before the player chose.**

Improvisation mid-scene is forbidden for everything that engages what follows: the consequence of a choice, the content of a place, the reaction of a non-player character (NPC), an access condition, an object found. The author may improvise a transition phrase or an atmosphere description that establishes **no new fact**; the moment a phrase establishes a fact (a name, an object, a promise, a danger), that fact had to already exist in the state, or the author adds it to the state **before** announcing it and logs it as a fact added in preparation of the next scene, never after the fact to justify a consequence already announced.

### Preparing a chapter, before the first scene

Before presenting the first scene of a chapter, the author prepares **the whole current chapter** and writes it into the campaign state (see Schema). The preparation contains, for **each** scene of the chapter:

1. the scene's `id` and `title`;
2. `text`: the presentation text, already written, within the length bound (see Flow of a scene);
3. `choices`: the list of offered choices (2 to 4), each with:
   - a stable `id` within the scene (e.g. `s3-a`);
   - `button_text`: the short label shown to the player;
   - `consequence_text`: the consequence text, already written, that will be shown if the player picks this option; **this text, and no other, is what will be applied**;
   - `effects`: the mechanical effects of the consequence, in structured form (see Inventory and flags): objects gained / lost / used, flags set or cleared, resource modified, next scene;
   - `conditions`: the conditions for offering the choice (required flag, required object, required resource), or `null` if the choice is always offered;
   - `next_scene`: the id of the scene that follows if this choice is taken; the branches are written, not guessed.
4. an optional `failure_outcome`: what happens if the scene ends in failure (see Failure);
5. the **new facts** the scene establishes, added to the fact register (see below) at preparation time.

Preparing a chapter is not preparing the whole campaign: later chapters may exist only as a one-line intention in the state (`planned_chapters`). But **no scene is played if it has not been prepared according to the 5 points above**. When the player reaches the last prepared scene and the next chapter is not prepared, the session closes cleanly (see Sessions) and the author prepares the next chapter **out of session**, before any resume.

### Register of established facts

The state holds a `fact_register`: a dated list of truths of the world that the story has made canonical. Each entry: `{ "id", "fact", "established_in": "<scene or preparation>", "at": "<timestamp>" }`. Recorded there, at the moment they are prepared, or, for a fact born of a free action, at the moment they are applied:

- the truths of the world (geography, rules of a place, how a mechanism works);
- every NPC met: name, role, disposition toward the character at the end of the encounter;
- every promise made **by** the character or **to** the character, with its beneficiary;
- every place visited and its lasting state (open / closed, safe / dangerous);
- every singular object and where it is when it leaves the inventory.

**Re-read rule**: before presenting a scene, the author re-reads the whole register, the inventory, and the flags from the file. If the scene's prepared text contradicts a fact in the register, the prepared scene is **corrected outside presentation** (the gap is logged in the journal) or, if the contradiction is discovered after presentation, handled under the "contradiction discovered" edge case, never disguised as "actually, it was…".

### Coherence gate, applied to EVERY chapter before it is written into the state

- [ ] Every scene has a written text, 2 to 4 written choices, and **one written consequence per choice**
- [ ] Every consequence has its structured `effects`, coherent with its text (the text says an object gained if and only if the effects add it; the text mentions no effect absent from `effects`)
- [ ] Every `next_scene` points to a scene that exists in the chapter, or to an explicitly marked chapter end
- [ ] Every `conditions` references only flags, objects, or resource thresholds that already exist in the state or that this chapter can set **before** the scene concerned
- [ ] No choice requires an object the player cannot have obtained by this point through at least one prepared path, and if that path is missable, a **path without the object** is also prepared for the same scene (see Inventory, the missable key rule)
- [ ] Every announced or prepared deferred consequence ("this will have a sequel") has a named **manifestation scene** in this chapter or the next, with its written condition; no narrative debt without a written due date
- [ ] The fact register already contains every fact the chapter's texts take for granted (names, places, mechanisms, earlier promises honored or recalled)
- [ ] No text contradicts the register, the chapter's starting inventory, or an earlier consequence recorded in the choice journal
- [ ] The chapter has an identifiable end: last scene marked, the state of the world after the chapter described in one sentence in the state (`planned_chapter_end_summary`)
- [ ] Nothing borrowed from an existing work; all-audiences tone checked on every text

One unchecked item = chapter not ready. Fix the preparation, rewrite the state, **and only then** present the first scene.

## Character

Created at the first session, in at most three questions (or offered ready to play if the player prefers to start right away):

- `name`: the one the player chooses or accepts;
- `traits`: 2 to 3 short traits (e.g. "curious", "deft hands", "afraid of heights"). Traits grant **no numeric bonus**; they serve the author at preparation time: a trait may motivate an additional prepared choice in a scene, and the resume recap recalls them. A trait never creates an improvised effect mid-scene.
- `resource`: **settled: one single simple resource, Breath.** An integer bounded **0 to 5**, starting at 5. A prepared effect may cost 1 (effort, fear, small wound, sleepless night) or give back 1 (rest, meal, encouragement), never more than 1 per consequence. At 0, the character does not die: see Failure. No other gauge (no experience, no levels, no counted money beyond named objects): the character's wealth is the inventory and the flags.

The character never changes retroactively: a trait is added or removed only at a chapter end, with the player's agreement, and the change is logged in the journal.

## Flow of a scene

1. **Re-read**: the author re-reads the state from the file: current prepared scene, fact register, inventory, flags, Breath. No presentation from memory.
2. **Presentation**: the author sends:
   - a short header: chapter and scene number (e.g. "Chapter 1, Scene 3/7") and, if Breath changed at the previous scene, its value;
   - the scene's prepared `text`, **bounded to 600 characters, spaces included** (about 90 to 110 words): one situation, one place, one legible stake; no wall of text, no second scene hidden inside the first;
   - nothing else before the choices: no summary of the plan, no name of scenes to come.
3. **Choices by buttons**: the choices whose `conditions` are met by the current state are presented by **option buttons**, 2 to 4 labels taken **word for word** from the prepared `button_text`. A choice whose condition is unmet is simply not presented (the player does not need to know it existed), except a choice locked by a specific object, which may be shown greyed in the text ("the door asks for a key you do not have") if its prepared text provides for that.
   Under the buttons, one standing line, always present: "Or write the action of your choice." The player must know at every scene that the free action exists (see Choices and free actions).
4. **Wait**: one choice per scene. The player answers by a button or by a written free action. Any discussion, question, or hesitation from the player before choosing does not advance the scene and costs nothing.
5. **Immediate resolution**: as soon as the choice is received, the author applies **the prepared consequence** of that choice:
   - shows the prepared `consequence_text`, **bounded to 500 characters**, spaces included;
   - applies the `effects` in the state (inventory, flags, Breath, new facts);
   - makes the consequence **visible**: the resolution line ends with a one-line mechanical recap built from the applied effects (e.g. "Inventory: + bent brass key · Flag: mara_grateful · Breath: 5/5"). No applied effect stays silent, no announced effect is omitted from the state.
6. **Writing**: the author rewrites the state **before** presenting the next scene: entry in the choice journal (see Inventory and flags), `current_scene` advanced to the taken choice's `next_scene`, played scene marked `played` with the choice taken. Then the author moves on to presenting the next scene, or closes the session if the player asks or if the chapter is finished.

## Choices and free actions, settled rule

**The free action is always accepted.** At each scene, on top of the buttons, the player may write any action plausible for their character. The free action does not short-circuit the discipline; it is resolved inside it as follows:

1. **Feasibility from the state**: the author judges the action only from the fact register, the inventory, the flags, and the current scene's text. Possible / impossible / possible at a cost: the judgment rests on a cited fact of the state ("the pipe links the storeroom to the lantern, register, fact f-07"), never on a narrative wish.
2. **Resolution in three outcomes only**:
   - **Success**: the action works. Its effects are those, already prepared, of the button choice closest in intent, **or**, if no prepared choice comes close, a bounded, new effect, limited to: a new fact recorded in the register, a new flag, or advancing to the same `next_scene` as the closest choice. A free action **never** grants an object, a Breath gain, or a shortcut to a distant scene that did not exist in the preparation; if the player aims exactly at that, the outcome is "partial success".
   - **Partial success**: the action works in part, or at a cost prepared by analogy (at most 1 Breath point, or a named inconvenience flag). The resolution text says what worked, what did not, and the cost, in **500 characters at most**.
   - **Impossible**: a fact of the state opposes it. The author says so in one sentence, citing the fact, **at no cost and without advancing the scene**: the player then picks a button or another free action. Impossible is never a punishment.
3. **Recording**: the free action, its outcome, and its effects are written into the choice journal with `type: "free"`, the state fact that grounded the judgment, and the effects actually applied. If it created a new fact, that fact enters the register **at the same moment**, dated; it becomes canonical for every later scene, prepared or to prepare (the preparation of later chapters must respect it; the gate will check).
4. **Gentle anti-derailment**: a free action can neither kill a named NPC, nor destroy a place or a singular object of the register, nor leave the zone of the current chapter. The author then resolves it as a bounded partial success ("you move away, but…") that brings the character back to the current scene or its normal `next_scene`. The campaign does not break for a player's idea; it does not rewrite itself for it either.

## Inventory and flags

### Inventory

- A list of named objects: `{ "id", "name", "state": "carried | used | lost | consumed", "obtained_in": "<scene>", "note": "<what it is for, per the register>" }`. No generically stacked unnamed objects; a prepared consumable may carry a `quantity` (bounded to 3 at preparation).
- An object is obtained, lost, consumed, or used **only** through the `effects` of a prepared consequence or through the recorded resolution of a free action within the bounds above. The author never makes an object appear in a text if it is not in the effects.
- **Use**: a choice may carry the condition `required_object`. When the player takes it, the `object_used` effect moves the object to `state: "used"` (it stays in the inventory, it has served, its text says so) or `"consumed"` if it disappears in serving; the preparation settles it, the applied consequence does not subtract from it.
- **The missable key rule**: no object obtained by an optional choice may be the only path through a chapter. Every scene locked by an object also prepares the path without the object: costlier (Breath, inconvenience flag, detour through another prepared scene), never blocking.

### Consequence flags

- Flags named in `snake_case`, booleans, set only by prepared `effects` or a recorded free resolution: `{ "name", "set_in": "<scene>", "at": "<timestamp>", "description": "<what it changes, in one sentence>" }`.
- A flag serves three things, all written: offering or withdrawing a choice (`conditions`), modifying the text of a prepared consequence that provides two variants (`variant_if_flag`; **both** texts are written at preparation), and manifesting a deferred consequence (see below).
- **Deferred consequence**: when a consequence prepares a distant sequel, its `effects` set the flag **and** name the `manifestation`: the scene where it will manifest and what will happen there if the flag is present (and, if useful, what will happen in its absence; two prepared texts). At the manifestation scene, the author applies the prepared text matching the flags' real state. A deferred consequence with no named manifestation fails the gate.
- No flag is ever cleared in silence: if an effect clears it, the journal says so and the visible resolution line shows it.

### Choice journal

An appendix of the state, one entry per played scene, **never rewritten**:

```json
{ "at": "…", "scene": "s3", "type": "button | free", "choice_id": "s3-a or null", "free_action": "<the player's text, if free>", "consequence_applied": "<id or one-line summary>", "effects": { "inventory": [], "flags": [], "breath_delta": 0 }, "next_scene": "s4" }
```

The journal is the proof of the discipline: set against the prepared chapter (kept intact in the state, see Schema), it shows that every applied consequence is a pre-written consequence, and that every announced effect appears in the prepared `effects` of the choice taken.

## Failure, never permanent death by default

There is **no permanent character death by default**, and no prepared consequence may contain one. Failure takes two forms, both prepared:

1. **Scene failure**: a prepared consequence may be bad (Breath loss, object lost, inconvenience flag, detour). It applies like the others: visible, recorded, and the campaign continues. A chapter prepares at most **two** frankly bad consequences; the adventure stays all-audiences and fair.
2. **Breath at zero**: the character collapses from exhaustion (never a described death). Fixed procedure, announced to the player at character creation:
   - the author **steps back to the previous scene** (the last scene whose outcome was not a failure);
   - a cost written in advance, always the same: Breath goes back up to **2**, and a lasting flag `exhaustion` is set (it may close the chapter's most athletic choices, if the preparation provides for that); consumed objects stay consumed, the register's facts stay true, only position and Breath step back;
   - the fallback is recorded in the journal (`type: "fallback"`), the failing scene stays marked `played_failure` and is not replayed identically: its resume variant, if the preparation provides one, applies; otherwise the player resumes at the previous scene and makes another choice, a different one if possible.
3. **Deliberate end of campaign**: if the player **explicitly chooses** to stop for good (in session: "my character gives up", confirmed once by the author), the campaign becomes `finished_given_up`: the author narrates, in **600 characters at most**, a gentle ending prepared by the campaign's tone (the character goes home, renounces, passes on their task; never a death), writes the final recap, and closes the state. It is the only definitive ending, and it belongs to the player.

No other mechanism ends a campaign against the player's will: no hidden timer, no NPC who "decides" in their place in an improvised text.

## Sessions and resume

### End of session

A session ends when the player asks, when the chapter ends, or when the prepared chapter is exhausted. The author then:

1. finishes the resolution in progress, if any (never a closing in the middle of a half-applied consequence: either the scene is resolved and written, or it was not presented);
2. rewrites the state: `status: "paused"`, `current_scene` = next scene to play, `last_session_at` filled, journal up to date;
3. tells the player, in a few lines built **from the state**: where the character stops, their Breath, and the promise of resume ("we will resume at scene X of chapter N"), without revealing any text to come;
4. if a chapter has ended: writes the bounded scores entry (see Writings).

### Resume, the faithful recap

On resume ("resume", "let's continue the campaign", or "play" while a campaign is `paused`), the author:

1. scans the states folder, re-reads the most recent `paused` campaign **from the file**; the re-read state is authoritative, not the memory of the conversation;
2. produces a **faithful recap**, built only from the state, in this order:
   - the character: name, traits, current Breath;
   - the situation: current chapter, where the character is and what they are seeking, **drawing only on facts of the register and scenes already played**;
   - the inventory: objects carried, with their state (a `used` object is said to be used, an absent object is not mentioned);
   - the marked choices: at most **three**, drawn from the choice journal (those that set a flag whose manifestation is still to come, gained an object still carried, or cost Breath), with their consequence **as recorded**, never embellished or completed;
   - the open threads: flags whose manifestation has not yet happened, named in story language ("someone owes you a service"), without saying where or how it will manifest.
3. **Resume prohibitions**: invent nothing (no place, NPC, object, promise, or event absent from the state); no text, title, or hint of scenes to come; no already-applied consequence presented otherwise than as the journal records it. If an expected element is missing from the state, the author says so as is ("the state does not say…") instead of filling it in.
4. After the recap, the author checks that what follows is prepared (current chapter prepared in full in the state, gate passed): if yes, presents the current scene; if the next chapter is not prepared, prepares it in full first, then presents the scene; never the reverse.

Resume is part of the game, not a side matter: a campaign whose recap invents is a campaign whose discipline is broken, exactly like an improvised consequence.

## State schema, `states/<campaign-id>.json`

`campaign-id`: `adventure-<world-slug>-<YYYY-MM-DD>-<hhmm>` (prefix `TEST-` for a test campaign). **One single file per campaign**: it holds at once the live campaign, the prepared chapter (the author's key, never shown to the player), and the journal. The campaign lives in the **user's data** (`~/you-are-the-hero/states/`), never in the skill.

```json
{
  "id": "adventure-auremist-valley-2026-10-10-2100",
  "game": "you-are-the-hero",
  "status": "in_progress | paused | finished | finished_given_up",
  "language": "fr | en",
  "world": { "name": "<name of the world>", "summary": "<two sentences, tone and principle of the world>" },
  "created_at": "2026-10-10T21:00:00-04:00",
  "last_session_at": null,
  "character": {
    "name": "<name>",
    "traits": ["<trait>", "<trait>"],
    "breath": 5,
    "breath_max": 5
  },
  "current_chapter": 1,
  "current_scene": "s1",
  "planned_chapters": [ { "number": 1, "title": "<title>", "intention": "<one line>" } ],
  "prepared_chapter": {
    "number": 1,
    "title": "<chapter title>",
    "prepared_at": "2026-10-10T20:55:00-04:00",
    "coherence_gate": "passed",
    "planned_chapter_end_summary": "<one sentence>",
    "scenes": [
      {
        "id": "s1",
        "title": "<internal title, never shown>",
        "text": "<presentation text, 600 characters at most>",
        "choices": [
          {
            "id": "s1-a",
            "button_text": "<short label>",
            "conditions": null,
            "consequence_text": "<consequence text, 500 characters at most>",
            "effects": {
              "inventory_gain": [],
              "inventory_loss": [],
              "object_used": null,
              "flags_set": [],
              "flags_cleared": [],
              "breath_delta": 0,
              "new_facts": [],
              "manifestation": null
            },
            "next_scene": "s2"
          }
        ],
        "failure_outcome": null,
        "status": "upcoming | current | played | played_failure"
      }
    ]
  },
  "inventory": [
    { "id": "watchbook", "name": "Watch notebook", "state": "carried", "obtained_in": "creation", "note": "<what it is for>" }
  ],
  "flags": [
    { "name": "<snake_case>", "set_in": "s2", "at": "…", "description": "<one sentence>" }
  ],
  "fact_register": [
    { "id": "f-01", "fact": "<canonical truth, one sentence>", "established_in": "preparation_ch1", "at": "…" }
  ],
  "choice_journal": [],
  "finished_chapters": [],
  "journal": [ { "at": "…", "event": "campaign_created" } ]
}
```

- `prepared_chapter` is this game's **sealed key**: it exists in full, with all its consequences, **before** the presentation of the chapter's first scene (its `prepared_at` is earlier than the journal's first `scene_presented` event of the chapter; that is verifiable in the file). It is never shown, summarized, or hinted at to the player; a resume recap draws **nothing** from it.
- When a chapter ends, its prepared content is **archived as written** into `finished_chapters` (with the list of choices taken), then replaced by the next prepared chapter. The archive is never rewritten: it is what allows checking afterward that the consequences applied were the consequences written.
- `manifestation` in `effects`: `null`, or `{ "scene": "s6", "flag": "<name>", "if_present": "<prepared text>", "if_absent": "<prepared text or null>" }`.
- `variant_if_flag` on a choice: `{ "flag": "<name>", "variant_consequence_text": "…", "variant_effects": { } }`, written at preparation, never composed at play time.
- The `journal` records every dated event: creation, preparation of the chapter (gate passed), every scene presentation, every choice, every free resolution, every fallback, every session closing, every resume and the recap it issued.

## Writings

1. **Campaign state**: rewritten at every resolved scene and every session closing (see above). It is the only place the campaign lives.
2. **`scores.json`, bounded, non-competitive.** This game has **no points score**. A single writing, at the end of each finished chapter, in `~/you-are-the-hero/scores.json`:
   ```json
   { "date": "YYYY-MM-DD", "game_id": "<campaign-id>", "game": "you-are-the-hero", "world": "<name of the world>", "language": "fr", "chapter": 1, "chapter_title": "<title>", "scenes_played": 7, "breath_at_chapter_end": 4, "test": false }
   ```
   No entry mid-chapter, no entry for a chapter abandoned midway (a `finished_given_up` campaign receives a single entry with `"chapter": null, "given_up": true`). Nothing else is written anywhere: no question library, no ranking.
3. **No external send**: this game never leaves the user's chat. No group message, no artifact, no publication.

## The author-referee's work (reminder of the rules that protect the game)

1. **Prepared or not played.** No scene without complete preparation and a passed gate, written into the state before its presentation. The temptation to "just invent this consequence" is this game's central fault.
2. **The state is authoritative.** File re-read at the start of every game turn, rewritten at the end of the turn. One file per campaign, held by one agent at a time.
3. **The key does not leak.** Neither upcoming texts, nor unchosen consequences, nor planned manifestations are shown, summarized, or hinted at, not even in the resume recap, not even "to help" the player choose. The consequences of choices **not taken** stay secret until the complete end of the campaign; the player will never know what they missed, unless a second character replays the chapter.
4. **Button neutrality.** Prepared labels do not mark the "good" option: no more flattering wording for the path the author prefers, no systematic order (the safe path is not always first). The visible resolution line states the effects, never a judgment ("good choice!" is forbidden; "the key opens the door" is the story, not a verdict).
5. **Fidelity of consequences.** The text applied is the text prepared, character for character in substance: the author may fix a typo, never soften a loss, amplify a gain, or add a fact. If the prepared consequence turns out incoherent with the real state at the moment of applying it (see Edge cases), the author stops and handles the gap in the open, in the journal, never in silence.

## Edge cases (settled)

- **The player picks a button whose condition has just lapsed** (state re-read different from the one at presentation, e.g. a resume in between): the author says so, spends nothing, and re-presents the scene from the re-read state. The file decides.
- **Free action that reproduces a button**: handled as the corresponding button (same prepared consequence, `type: "free"` in the journal with the note "equivalent to <choice_id>"). The player neither loses nor gains anything by it.
- **Incomprehensible or out-of-world free action** (deliberate anachronism, meta-gaming): the author asks for a clarification in one sentence, at no cost and without advancing the scene. Two clarifications with no playable action = the scene stays waiting; the session may close cleanly on this unplayed scene.
- **Contradiction discovered after presentation** (a prepared text contradicts the register, spotted by the author or the player): the author admits it in the chat, the faulty scene is **suspended**: if no consequence has yet been applied for it, it is corrected in the state (journal: `scene_corrected`, old and new facts named) and re-presented; if a consequence has already been applied on the basis of the false fact, the consequence **stands** (the character's past is not rewritten), the register is corrected for the future, and the complete incident is recorded. Never "you misunderstood".
- **The player asks what would have happened with another choice**: polite and firm refusal, in game as out of session; the key is shown only at the complete end of the campaign, and even then only if the player asks again at that moment. Mid-campaign: "that door stays closed".
- **Two `paused` campaigns coexist**: on resume, the author names both (world + chapter + date of last session, drawn from the states) and asks which one to resume. Never a silent choice for the player.
- **Unreadable or incomplete state at resume** (corrupted file, prepared chapter missing while `current_scene` assumes it): the author says so, reconstructs **nothing** from memory, and offers: either restart from the last chapter archived in `finished_chapters`, or close the campaign as `finished_given_up` with the recap the state still allows. No invented scene as a "fix".
- **Session interrupted mid-scene** (the player disappears after the presentation, before choosing): the scene stays `current`, no effect applied; on resume, the recap precedes the re-presentation of the same scene, from its intact prepared text.
- **The player wants to change character mid-campaign**: refused mid-chapter; possible between two chapters, as a new character taking over the world's sequel (new state, the world's register is copied, not the choice journal nor the former character's inventory, except an explicitly handed-over object, recorded).
- **Contesting a consequence** ("that is not what the button said"): the author republishes, from the chapter archive in the state, the prepared `button_text` and `consequence_text` of the choice taken, and the journal entry. The file decides.
