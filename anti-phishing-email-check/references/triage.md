# Anti-Phishing Email Check — 60-second triage

Do these in order. Stop at the first hard fail.

## 0:00–0:15 — Who really sent it
- Gmail → message → ⋮ → "Show original".
- Find `Authentication-Results`. Need all three:
  - `spf=pass`
  - `dkim=pass` with `d=` = the sender's real domain
  - `dmarc=pass`
- Any `fail` or `none` → treat as suspicious until proven otherwise.
- `From` says `support@yourbank.com` but DKIM `d=` is `random-mailer.net`?
  That's a fail.

## 0:15–0:35 — Where do the links really go
- Copy each link address (don't click). Read the *domain*:
  - ✅ `muse.ai/platform/…` — direct, matches the claimed sender.
  - 🚩 `bit.ly/…`, `t.co/…`, any shortener in a "security" email.
  - 🚩 Lookalikes: `rnuse.ai`, `meta-support.com`, extra subdomains
    like `secure-login.yourbank.evil.com`.
- Display text ≠ destination. Always read the href.

## 0:35–0:50 — What does it want
- Credentials / password reset / payment / "verify within 24h" → high
  alert. Real companies put the notice in your account dashboard too —
  go there yourself (type the URL, don't click).
- Attachments you didn't ask for (`.html`, `.zip`, Office macros) →
  don't open, verify via another channel first.

## 0:50–1:00 — Verdict
- **Authentic**: all three auth checks pass, links are direct and match
  the sender, the ask is ordinary. Proceed — still via your own
  navigation, not the email link.
- **Suspicious**: any hard fail. Report phishing in Gmail, delete.
- **Inconclusive**: mixed signals → treat as suspicious. Contact the
  company through a known-good channel and ask.

## If you already clicked
1. Don't enter anything else. Close the tab.
2. Rotate whatever it asked for (password, API key, token) from the
   *real* site, typed by hand.
3. Check account activity for sessions you don't recognize.
