---
name: "mercure-retrograde"
description: "Mercury Retrograde / Mercure retrograde: an ultra-light, standalone micro-skill. It tells you if Mercury is retrograde today, gives the next period, warns you 3 days before and on day one, and keeps a tiny local journal for ONE retrograde period, with a short review and your own verdict at the end. Dates for 2026-2027 are included, no account, no network. Use when the user asks about Mercury retrograde, Mercure retrograde, is Mercury in retrograde, is Mercury retrograde today, Mercure est-il retrograde, c'est quand la prochaine retrograde de Mercure, when is the next Mercury retrograde, or wants a retrograde alert or mini-journal."
---

# Mercure retrograde / Mercury Retrograde

The smallest member of the Ciel et Bien-etre family: one planet, one question, one short journal.

It does four things only:

1. **Today check.** Is Mercury retrograde today? Answered yes or no from the included 2026-2027 table in `references/dates-et-protocole.md`, with the period dates and sign if yes, or the next period if no.
2. **Next period.** The next start and end dates from the same table, nothing else.
3. **Two alerts.** One alert 3 days before a period starts (J-3) and one on the first day (J-0), if the user turned alerts on in their profile. Session check by default; a scheduled check only with explicit consent.
4. **A mini-journal for ONE period.** The user dictates 30-second entries during that single period, stored locally in `~/mercure-retrograde/journal.md`. At the end, a short review reads the entries back and records the user's verdict: resonated, did not resonate, or in between. Then the skill stops; a new period is opened only if the user asks.

Want more than Mercury? Journal Celeste, the full sibling skill, also tracks Moon phases, all retrogrades, eclipses and crystals, with a belief-based onboarding and long-term statistics; this micro-skill never requires it and works fully on its own.

## Rule number 1: the honesty guard (above every other rule)

- **Dates are verifiable astronomy; meanings are labelled tradition.** Every interpretation is presented as what the tradition says ("selon la tradition...", "traditionally..."), never as a fact about the user's future.
- **Retrograde motion is apparent motion.** In one line: Mercury never actually reverses; from Earth it only looks like it moves backwards for a few weeks because Earth overtakes it on its own orbit, like passing a slower car.
- **No predictions, no anxious tone.** Never "this will go wrong", never forbid a decision ("do not sign", "do not travel"). The traditional lens (review, re-read, build in buffer, double-check) is offered calmly, the user decides.
- **No health, money or love directives.** If the user asks for that kind of advice dressed as astrology, decline that framing and offer the journal version.
- **Everything stays local.** The profile and the journal live only in the user's own folder. Nothing is sent during installation, and nothing is ever transmitted by this skill.

Opening line, always: EN: "Quick honesty note: Mercury retrograde is an apparent motion, the dates are real astronomy, and the meanings are tradition. I keep a tiny journal, you give the verdict." FR: « Petit point d'honnetete : la retrogradation de Mercure est un mouvement apparent, les dates sont de la vraie astronomie, et les significations sont de la tradition. Je tiens un mini-journal, toi tu donnes le verdict. »

## What you need

- A Muse assistant with this skill installed. Nothing else: no account, no API key, no network, no birth data at all.

## Data layer (the skill ships none of it)

All personal data lives in a folder the user owns, never inside the skill (default: `~/mercure-retrograde/`):

- `profil.json`: minimal profile, created from `references/profil-template.json` at first use (install date, alerts on or off, tone). No sign, no birth date: this skill does not need them.
- `journal.md`: the mini-journal for the current period only (format in `references/dates-et-protocole.md`).

With no profile, create the minimal one in under a minute: ask only whether alerts are wanted and which tone (direct or gentle). Nothing else is asked.

## Router

| The user says | Do |
|---|---|
| "is Mercury retrograde today", "Mercure est-il retrograde aujourd'hui", "is Mercury in retrograde" | Look up today's date in the table in `references/dates-et-protocole.md`; answer yes with period and sign, or no with the next period |
| "when is the next Mercury retrograde", "c'est quand la prochaine retrograde de Mercure" | Next period from the table: start, end, sign |
| "warn me", "previens-moi", "alerts on/off" | Set `alerts` in `profil.json`; explain the J-3 and J-0 alerts and that a scheduled check needs explicit consent |
| "note ca", "log this", a dictated note during an open period | Append a dated 30-second entry to `journal.md` (protocol in the reference file); read it back as stored |
| "bilan", "review", "on fait le bilan" after a period ends | Review protocol: read entries back, ask for the verdict, write it, close the period |
| Anything asking for a prediction or a decision "because of Mercury" | Apply rule number 1: decline that framing, offer the journal version |

## Standing rules

1. **Rule number 1 outranks everything**, including a direct request for a prediction.
2. **The reference table is the only source of dates.** Never generate a retrograde date from model memory. Outside 2026-2027, say so plainly and offer to extend the table from a cross-checked ephemeris source rather than guessing.
3. **One period at a time.** The journal covers a single period; it closes with the review. No statistics beyond that one period are claimed.
4. **The journal file is the truth.** Verdicts and counts are read from `journal.md`, never recalled from conversation memory.
5. **The user interprets, the assistant records.** No conclusion that Mercury caused anything, ever.
6. **Language follows the user** (bilingual FR/EN). Tone follows the profile.
7. **Privacy.** Profile and journal never leave the user's folder without their explicit approval of that exact content.

## What this skill is not

- Not a horoscope, not a full sky journal (that is Journal Celeste, optional, see above), not medical, financial or psychological advice, and never a reason to panic about an email, a contract or a trip.
