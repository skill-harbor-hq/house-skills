# Creator Outreach Kit — pipeline reference

## targets.json
```json
[
  {"seller_id": "acme-widget", "github_login": "janedoe", "seller_name": "Jane Doe"}
]
```
One row per creator. `seller_id` is your internal key; `github_login` is the
GitHub username whose public profile you read.

## Collect (GitHub profiles)
`GET https://api.github.com/users/{login}` with headers
`Accept: application/vnd.github+json`, `X-GitHub-Api-Version: 2022-11-28`,
and a browser-like `User-Agent`. Authenticate (token with `read:user`) —
unauthenticated rate limits (60 req/h) die fast on any real list; authed
gets 5,000 req/h. Keep only `email` when the profile exposes one publicly.
Resume-safe: persist per-login results and skip done logins on rerun.

Save as `profiles.json`:
```json
{"acme-widget": {"github_login": "janedoe", "seller_name": "Jane Doe", "email": "jane@doe.dev"}}
```

## Verify
`bin/verify_emails.py profiles.json --out emails-verified.json`.
Free: syntax regex + `dig MX` (fallback `dig A`). Cache per domain.

## Queue
Build `queue.json` — one entry per **email** (dedupe!), not per project:
```json
[{"email": "jane@doe.dev", "creator_name": "janedoe",
  "projects": "Your project Acme Widget is listed here:\nhttps://example.com/p/acme-widget",
  "claim_url": "https://example.com/claim?token=...",
  "sent": false}]
```
Sort hottest-first if you track demand. Reject placeholder artifacts at
build time (the `looks_like_placeholder` guard): `name@`, `your@`,
`test@`, `u003e…` unicode escapes, `example.com`/`email.com` style domains.

## Claim links (optional)
HMAC-SHA256 over `claim.{email}|{expiry}`, hex digest as token:
`https://example.com/claim?token={token}`. Server recomputes and checks
expiry (30 days is plenty). Lets a creator take over their page with zero
account friction. Keep the signing secret in a vault, never in the repo.

## Send
`bin/send_batch.py --queue queue.json --account <id> --subject "…" --template template.txt --batch 30`.
Sequential, ~2s apart, marks `sent` + `sent_at`, appends `send-log.txt`.
Failures are logged, never retried in a loop — fix the address, not the loop.

## template.txt (example)
```
Hi {creator_name},

I'm {your_name}, founder of Example (example.com) — a directory of AI builds.

{projects}

Here's your personal link to claim the listing. You can edit the
description, add links, and manage the page yourself:
{claim_url}

It's free. If you'd rather not be listed, just reply and I'll remove it.

— {your_name}

To opt out of future emails, reply with "remove".
```

## Next-day bounce triage
Gmail bounces arrive asynchronously from Mail Delivery Subsystem. The day
after a batch, search for them, classify (nonexistent address / blocked /
mailbox full / delayed), and prune dead addresses from future queues.
A `200 OK` on send is not proof of delivery.
