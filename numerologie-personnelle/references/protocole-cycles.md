# Protocole cycles — onboarding, profil calculé, journal, bilan

Mirror the user's language. Ask the onboarding questions **one or two at a time**, conversationally, never as a form dump. Save each answer to `profil.json` as it arrives; if the user stops midway, the profile is resumable where it stopped. Every computed number is written **with its steps** (see `references/calculs-et-formules.md`); a number without its calculation is never stored alone.

## Onboarding script

**Opening (always, before question 1):**
- EN: "Before anything: the math here is exact. I will show you every step of every calculation, and you can check each one by hand. What the numbers mean comes from a tradition, and I will label it as such every time. I predict nothing. You journal what you live through your cycles, and afterwards you decide whether it resonated."
- FR: « Avant tout : ici, les calculs sont exacts. Je vais te montrer chaque étape de chaque calcul, et tu pourras tout vérifier à la main. Ce que les nombres veulent dire vient d'une tradition, et je vais l'étiqueter comme telle à chaque fois. Je ne prédis rien. Tu journalises ce que tu vis pendant tes cycles, et après, c'est toi qui décides si ça a résonné. »

**Q1 — Birth date.** Date of birth (day, month, year), needed for every calculation. One line on privacy: it stays in the local profile, nothing is sent anywhere. → `birth_date`

**Q2 — Which calculations.** Base profile (life path only), base + personal year, or full cycles (year, month and day)? The user can extend later; the change is written the same turn. → `calculations[]`, `cycle_interest` (`base | yearly | monthly_daily`)

**Q3 — Expression number (optional).** "Do you also want the expression number? It needs your full birth name, used only for the letter calculation, stored only if you say so." Declining is always fine and blocks nothing else. → `birth_name` (or null), `expression_opt_in`

**Q4 — Method note (not a question, a disclosure).** State the main method in one line ("I reduce month, day and year separately, then add; if you were ever given a different number elsewhere, a variant method is the likely reason, and I can show you the difference on your date"). If the user's date is one where the variant diverges, show both and record that the main method rules.

**Q5 — What to track.** Mood, energy, work/decisions, relationships, projects, other (their words). → `tracking[]`

**Q6 — Language and tone.** → `language`, `tone` (`gentle | direct`)

**Close.** Compute the profile (below), read it back **with its steps**, name the current personal cycle numbers if chosen, and ask if they want to open their first journal entry today.

## Computed profile format (`profil.json`, numbers block)

Each number is stored as an object, never as a bare integer:

```json
{
  "life_path": {"value": 1, "steps": "mois 3, jour 15 > 6, année 1990 > 1 ; 3 + 6 + 1 = 10 > 1", "method": "principale (mois/jour/année réduits séparément)", "computed_on": "YYYY-MM-DD"}
}
```

Rules:
- Recompute from the birth date at every display; if the stored value and the fresh calculation disagree, the fresh calculation wins and the file is corrected the same turn, with the correction told to the user.
- If a master number (11, 22, 33) appears at any step, the steps say so ("arrêt, nombre maître").
- The expression number, when present, stores the per-letter breakdown in its steps.

## Journal entries by cycle (`journal.md`)

One section per personal year; entries inside it are dated and tagged with the cycle numbers **computed for that entry's date** (personal month, and personal day if the profile tracks daily cycles):

```markdown
## Année personnelle 1 — 2026 (calcul : jour 15 > 6 + mois 3 > 3 + année 2026 > 1 = 10 > 1)
### Entries
- [2026-10-10] mois personnel 11 · jour personnel 3 · [one line, user's words]
```

Entry format (30 seconds): accept free dictation. Extract only what `tracking[]` covers and one line of what happened. Read it back as stored. Never interpret an entry mid-cycle unless asked, and never attach a "because your day was a 3" explanation to anything.

## End-of-personal-year review (le bilan)

Trigger: the personal year ends (31 December, calendar convention of this skill) or the user asks.

1. Read the year's entries **from the file**, summarize in 2–3 lines without adding meaning.
2. Restate the year's number and its traditional lens, labelled tradition, in one line.
3. Ask the single verdict question: "Your verdict on this personal year: resonated, didn't resonate, or in between?" / « Ton verdict sur cette année personnelle : résonné, pas résonné, ou entre les deux ? »
4. Write verdict + a one-line summary (user's words preferred) to `journal.md` and one line to `bilans.json`: `{"personal_year": 1, "calendar_year": 2026, "verdict": "resonated|no|in_between", "summary": "one line"}`.
5. Compute and present the **next** personal year with its steps, and ask whether they want to set one thing to observe for it.

## Statistics protocol

Counts come only from `bilans.json` (verdicts per personal-year number) and `journal.md` (tracked items). Always show the denominator ("2 of your 3 personal years 9 were closed with 'resonated'"). Always end with the user's call: "That's what your journal shows; what do you make of it?" Never state causation, never extrapolate beyond the journal's years.
