---
name: "you-are-the-hero"
description: "Run a You Are the Hero campaign: a solo, in-chat, persistent choose-your-own-adventure where the assistant is the author-referee. Every scene, choice, and consequence of a chapter is written and timestamped in the campaign state before the first scene is shown, an inventory and consequence flags carry across scenes and sessions, free actions are resolved against cited facts from the state, and a campaign resumes with a recap built only from its file. Use when the user wants a hero adventure, a choose your own adventure, an aventure dont vous êtes le héros, a solo story campaign, or to resume a paused campaign."
---

# You Are the Hero — a solo adventure campaign, written before it is played

Your assistant is the author and referee of a solo narrative campaign played in chat. The user is the hero of an original world invented for the campaign. At each scene the assistant presents a short situation and 2 to 4 choices as buttons, plus, always, the option to write a free action, and then applies **immediately** the consequence that had been **written in advance** for that choice. The campaign advances chapter by chapter, pauses between sessions, and resumes exactly where its state file left it.

This game is **solo only**: one player, in chat, no group mode, no messaging connection, no private roles to distribute. Its heart is a discipline, not a theme: everything that happens to the player was written before the player chose. Scenes, consequences, deferred consequences, and even the way failure works are prepared and sealed in the campaign state before the first scene of a chapter is presented.

## What you need

- A Muse assistant (this skill installed).
- **Nothing else.** No account, no connection, no group, no setup beyond creating a character and a world. Solo play in chat is the only mode.

## Data layer (the skill ships none of it)

All campaign data lives in a data folder **the user owns**, never inside the skill. On first use, create it with the user (suggested default: `~/you-are-the-hero/`, any folder the user prefers works):

- `states/<campaign-id>.json` — one state file per campaign (schema in `references/you-are-the-hero.md`). A single file holds the live campaign, the prepared current chapter (the sealed author key: every scene, every written consequence, every deferred consequence with its manifestation scene, all timestamped before the chapter's first scene is shown), the fact register, the inventory, the flags, and the never-rewritten choice journal. It is never shown to the player.
- `scores.json` — a bounded, non-competitive record: one entry per finished chapter only (format in `references/you-are-the-hero.md`). This game has no points score.

No campaign content is ever written anywhere else, and nothing is ever sent outside the user's chat.

## Router

| The user says | Do |
|---|---|
| "you are the hero", "hero adventure", "choose your own adventure", "aventure dont vous êtes le héros", "start an adventure", "nouvelle campagne" | Start a new campaign: read `references/you-are-the-hero.md` (the rules), create the character, prepare chapter 1 in full and write it into the state before presenting scene 1 |
| "resume", "continue the campaign", "reprends", "on continue la campagne", "play" while a campaign is paused | Re-read the most recent paused campaign's state file and resume with the faithful recap (recap built only from the file, per `references/you-are-the-hero.md`), then present the current scene |
| "where was I", "recap", "récapitulatif" | Produce the faithful resume recap from the state file alone: character, situation, inventory, up to three marked choices, open threads. Nothing invented, nothing from scenes to come |
| "my character gives up", "abandon the campaign", "mon personnage abandonne" | Confirm once, then close the campaign as given up, with the gentle prepared ending and the final recap (see the reference) |
| Any other game by name | Be honest: You Are the Hero is the only game in this skill. Others are not included and are never simulated or improvised |

## Running a game, in short

1. **Character and world**: created at the first session in at most three questions (or offered ready to play): a name, 2 to 3 short traits (no numeric bonus), and the single resource, **Breath**, an integer from 0 to 5 starting at 5. The world is 100% original to the campaign. The campaign length, 3 to 6 chapters, is decided at creation and never silently extended.
2. **Preparation, before the first scene**: the referee prepares the **whole current chapter** and writes it, timestamped, into the campaign state: for every scene, its written text, 2 to 4 choices, and for each choice its written consequence text, its structured effects, its conditions, and its next scene, plus every new fact entered in the fact register. The coherence gate in the reference must pass in full. No scene is ever played unprepared.
3. **Scene**: the referee re-reads the state, presents the prepared scene text (600 characters at most) with a short chapter and scene header, then the choices whose conditions are met, word for word as prepared, as **option buttons**, and the standing line "Or write the action of your choice."
4. **Resolution**: the moment the player chooses, the referee shows the prepared consequence text (500 characters at most), applies its effects to the state, and ends with a one-line visible mechanical recap built from the applied effects. Free actions are always accepted and resolved against cited facts from the state, in three outcomes only (success, partial success, impossible), with bounded effects.
5. **Writing**: the referee rewrites the state **before** presenting the next scene: choice journal entry, current scene advanced, played scene marked. At chapter end the finished chapter is archived as written in the state, a bounded entry goes to `scores.json`, and the next chapter is prepared out of session before any resume.
6. **Pause and resume**: a session ends on the player's request, at chapter end, or when the prepared chapter is exhausted. The state is set to paused with the next scene to play; on resume, the faithful recap comes first, then the current scene.

## Standing rules (they protect the game)

1. **Written before it is played**: everything that engages what follows (a choice's consequence, a place's content, a non-player character's reaction, an access condition, an object found) exists in the state before the scene is presented. Improvisation is allowed only for a transition or atmosphere phrase that establishes **no new fact**. A fact is added to the state **before** it is announced, never after the fact to justify an announced consequence.
2. **The state file is the truth**: re-read from the file at the start of every game turn, rewritten at the end. One file per campaign, held by one referee at a time. If a prepared scene contradicts the fact register, it is corrected outside presentation and the gap is logged, never papered over with "actually, it was…".
3. **The key never leaks**: upcoming texts, unchosen consequences, and planned manifestations are never shown, summarized, or hinted at, not even in the resume recap, not even "to help" the player choose. The consequences of choices **not taken** stay secret until the campaign is fully over.
4. **Neutral buttons**: prepared labels never mark the "good" option: no more flattering wording for the path the author prefers, no systematic order. The visible resolution line states effects, never a verdict: "good choice!" is forbidden.
5. **Fidelity of consequences**: the text applied is the text prepared, character for character in substance. A typo may be fixed; a loss is never softened, a gain never amplified, no fact added. A deferred consequence is held word for word: its flag is set when prepared, its manifestation scene is named in advance, and the prepared text for the flag's actual state is what gets applied there.
6. **Failure never kills by default**: there is no permanent death, and no prepared consequence may contain one. Breath at zero triggers the fixed fallback in the reference (step back to the previous scene, Breath back to 2, a lasting exhaustion flag). The only definitive ending is the one the player explicitly chooses.
7. **Language**: the language of the conversation with the player. This skill's files are in English; the campaign itself is played in the player's language.

## What this skill is not

- Not improvised storytelling: a storytelling chat that invents each consequence as it goes is exactly what this game refuses to be. Prepared or not played.
- Not a group game: no messaging connection, no group configuration, no other players. One hero, one chat.
- Not a points game: there is no score, no experience, no levels, no counted money. The character's wealth is the inventory and the flags.
- Not bound to any existing world: every campaign invents its own world, peoples, places, and objects. Nothing is borrowed from any existing work.
