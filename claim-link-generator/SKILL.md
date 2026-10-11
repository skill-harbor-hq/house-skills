---
name: "claim-link-generator"
description: "Let someone claim, edit, or take over their page with a magic link — no account, no password. HMAC-signed tokens binding email + expiry, verified server-side. Use when onboarding creators/sellers onto a directory or marketplace with zero friction."
---

# Claim-Link Generator

## Purpose
"Here's your personal link to claim the listing" beats "create an account"
every time. One signed URL per recipient lets them take over their page —
edit the description, add links, manage it — with no signup flow. Proven
across 255 creators: free, frictionless, revocable by expiry.

## Workflow
1. **Sign** — token = `HMAC-SHA256(secret, "claim." + email + "|" + expiry)`,
   hex-encoded. URL: `https://your-site.com/claim?token={token}`.
   Embed the expiry (unix timestamp, e.g. +30 days) in the signed payload
   so the server can check it without a database lookup.
2. **Send** — include the link in the outreach/pitch email, personalized:
   "Here's your personal link to claim the listing… It's free. If you'd
   rather not be listed, just reply and I'll remove it."
3. **Verify** — on `GET /claim?token=…`: recompute the HMAC over the
   presented `email|expiry`, compare in constant time, reject expired
   tokens. On success, bind the session to that email (set a cookie or
   mark the listing claimed).
4. **Scope** — one token claims everything tied to that email (all their
   listings), not one token per item. Fewer emails, fewer lost links.

## Output Contract
- Token URL safe in email clients (hex only, no `+`/`/`/`=`).
- Verification needs no DB read for the signature check itself (only to
  load the claimant's listings afterward).
- Expired or tampered tokens show a plain "link expired" page with a
  "resend" option — never a stack trace.

## Operating Rules
1. **Secret lives in a vault**, never in the repo or the client bundle.
   Rotating it invalidates all outstanding links — acceptable; reissue on
   demand.
2. Tokens are bearer credentials: don't log them, don't put them in
   analytics URLs, don't forward them.
3. 30-day TTL is plenty. Shorter for sensitive actions.
4. The claim page must work with zero JavaScript — email recipients open
   links everywhere.
5. Always offer the inverse: "rather not be listed? reply and I'll remove
   it." Claim links build trust only when removal is one reply away.

See `references/signing.md` for the exact sign/verify code.
