---
name: "creator-outreach-kit"
description: "Cold-outreach pipeline for open-source creators: collect public GitHub emails, verify them (syntax + MX, placeholder rejection), build a deduped send queue, and send personalized batches with per-recipient claim links. Use when someone wants to contact project maintainers at scale without spamming."
---

# Creator Outreach Kit

## Purpose
Run a respectful, high-deliverability cold-email campaign to open-source
creators: find their **public** contact emails, verify them, queue one
personalized message per creator, and send in daily batches with an
opt-out line. Built from a real campaign (255 creators, ~4% bounce rate
after verification).

## Workflow
1. **Targets** — write `targets.json`: `[{"seller_id": "...", "github_login": "...", "seller_name": "..."}]`.
2. **Collect** — fetch public GitHub profiles; keep the email only when the
   user listed it publicly on their profile. Never scrape or guess private
   addresses. (See `references/pipeline.md` for the profile-fetch pattern.)
3. **Verify** — `bin/verify_emails.py profiles.json --out emails-verified.json`:
   syntax check + MX/A DNS lookup (free, via `dig`). Marks each `valid`.
4. **Queue** — one entry per creator (dedupe by email), newest/ hottest
   first. Reject placeholder artifacts (`name@email.com`, `your@email.com`,
   `u003e...` unicode escapes, fake domains) — the bundled guard does this
   automatically.
5. **Send** — `bin/send_batch.py --queue queue.json --account <gmail-account-id>
   --subject "..." --template template.txt [--batch 30]`. Sends sequentially,
   marks `sent` with timestamp, appends to `send-log.txt`. Failed sends are
   logged, never retried in a loop.
6. **Claim links (optional)** — if your product has per-creator pages,
   generate signed, expiring claim URLs (HMAC-SHA256, `email|expiry`) so a
   creator can take over their listing without creating an account.

## Tooling
- `bin/verify_emails.py` — stdin: GitHub profiles JSON; stdout: verification
  results with `syntax_ok`, `mx_ok`, `valid`. Needs `dig` on PATH.
- `bin/send_batch.py` — sends the next N unsent queue entries via
  `hatch_gws_cli gmail +send`. Template uses `{creator_name}`, `{projects}`,
  `{claim_url}` placeholders. Skips placeholder addresses even if one
  slipped into the queue.
- `references/pipeline.md` — targets schema, GitHub API pattern (auth,
  rate limits), queue schema, log format.

## Auth
- GitHub: a token with `read:user` scope (public profiles only). Passed via
  the standard credential helper; never hardcode it.
- Gmail: the sender account must be connected; pass its account id to
  `--account`. Sending from the wrong default account is the classic
  mistake — always pass it explicitly.

## Operating Rules
1. **Public emails only.** If the address is not on the public GitHub
   profile, do not email. No guessing `firstname.lastname@` patterns.
2. **One email per creator**, even for multiple projects. Dedupe by address.
3. **Every message carries an opt-out** ("reply and I'll remove you" /
   "reply with \"remove\""). Honor removals immediately.
4. **No tracking pixels.** Developers notice; reputation beats open stats.
5. **Batch, don't blast.** ~30/day from a warmed-up mailbox. Space sends
   ~2s apart. Stop on repeated Gmail rate-limit errors; resume next day.
6. **Verify before asserting.** A `200 OK` from the send command is not
   proof of delivery — bounces arrive asynchronously via Mail Delivery
   Subsystem. Check them the next day and prune dead addresses.
7. Show the exact subject + body to the user and get an explicit go before
   the first batch. A go covers that batch only.
