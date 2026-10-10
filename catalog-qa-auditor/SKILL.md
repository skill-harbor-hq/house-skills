---
name: "catalog-qa-auditor"
description: "Audit a product/content catalog for silent data corruption: empty or duplicated install prompts, template residue, missing translations, invalid dates, duplicate URLs, price inconsistencies, leaked secrets, orphaned sellers. Read-only scans; the agent only sees anomalies. Use for directories, marketplaces, or any large listing database."
---

# Catalog QA Auditor

## Purpose
Catch the errors nobody opens one by one: run automated **read-only**
scans over a listing database, surface only the anomalies, and fix them
with a re-read after every write. Built for a ~1,900-listing directory;
a full audit costs a few thousand tokens, not a full catalog read.

## Workflow
1. **Cadence** — full audit 1×/month, plus after any data incident.
   Link health (every URL in the catalog) 1×/quarter, in the background —
   it's slow (thousands of HTTP requests).
2. **Scan** — run every check in `references/checks.md`. All scans are
   SELECT-only; Python filters, the agent sees only the offenders.
3. **Triage**
   - Data corruption (empty prompt, duplicate, invalid date): fix directly,
     **re-read after every UPDATE** before the next one.
   - Non-critical gaps (missing translation, short description): fix where
     there's traffic; leave the long tail alone.
   - If an anomaly reveals a pipeline bug: harden the pipeline (add a
     guardrail), don't just fix the data.
4. **Report** — dated section in a corrections log: date, checks run,
   anomalies found, decisions, fixes applied. Never destructive without
   re-reading.

## Output Contract
- The anomaly list per check (counts + offending ids/URLs).
- The dated corrections entry.
- Any new guardrail added to the pipeline as a result.

## Operating Rules
1. **Read-only scans.** No UPDATE/DELETE during the scan phase, ever.
2. Dedupe on **slugs/ids**, never on display names.
3. Normalize URLs before comparing (strip `/blob/.../SKILL.md` style
   suffixes, derive owner/repo pairs) or duplicates slip through.
4. One fix at a time, re-read between writes. Bulk UPDATEs are how
   incidents happen.
5. Keep the banned-phrases list (marketing claims you removed once) as a
   permanent scan — new content reintroduces old claims.

See `references/checks.md` for the concrete check list.
