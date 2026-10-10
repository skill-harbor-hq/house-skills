# Catalog QA Auditor — check list

All checks are SELECT-only. Adapt table/column names to your schema.

## A. Install prompts
- Empty or whitespace-only prompt text.
- Corrupted prompts (e.g. literal placeholder code blocks like ` ``` `).
- **Duplicated prompts**: same prompt text on 2+ listings = pasted onto the
  wrong listing. Compare normalized text, not ids.

## B. Template residue
- `{{`, `}}`, `TODO`, `lorem`, `[insérer`, `[insert`, `XXX` in any
  user-facing text field (descriptions, prompts, taglines).

## C. Translations
- EN present but FR empty (or vice versa) for description, prompt, tagline.

## D. Dates
- `created_at` null, empty, or unparsable — breaks "New" sections and
  date sorting.

## E. Duplicates
- Same normalized `repo_url` on 2+ live listings. Normalize first: strip
  `/blob/<branch>/...` suffixes; also derive `owner/repo` pairs from slugs
  for listings whose URL is just the repo root.
- Same `description` text on 2+ listings.

## F. Price consistency
- `is_free=0` but no price; `is_free=1` with a price label; label says
  "Free" on a paid product.

## G. Secrets & PII in texts
- Regex sweep for `sk-`, `ghp_`, `AKIA`, `xoxb-`, `xoxp-`, and email
  addresses inside descriptions/prompts. A pasted key is invisible to the
  naked eye.

## H. Referential integrity
- Orphaned sellers (no listings) / listings pointing at missing sellers.
- Suspicious slugs: double dashes, uppercase, trailing dash.
- Leftover test rows in analytics tables (rule: always clean up after a test).

## I. Infra & build (a few curls)
- Health endpoints still respond (if they break silently, nobody notices).
- Sitemap product-URL count matches live-listing count — a gap means an
  incomplete build.

## J. Link health (quarterly, background)
- Every `repo_url` resolves (follow redirects; note 404s).
- Paid-product `checkout_url` responds.
- `image_url` optional — broken images get a fallback, low impact.

## Post-insert validation (the incident that created this skill)
After every bulk insert, **before** building: validate against the DB that
the critical fields are actually present and non-empty. Truthiness checks
lie — a prompt containing literally ` ``` ` passes `if prompt:`. Check
real content, not presence.
