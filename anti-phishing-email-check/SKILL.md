---
name: "anti-phishing-email-check"
description: "Verify whether a scary 'action required' email is real or phishing: authenticate the sender (SPF/DKIM/DMARC), inspect every link's true destination, and compare against the official channel — before clicking anything or sharing credentials. Use on any unexpected security/alert email."
---

# Anti-Phishing Email Check

## Purpose
The emails that scare you into clicking are exactly the ones to verify
first. This is the 5-minute triage from a real case: a "developer portal
now open, complete intake" email that turned out authentic (proper
authentication, direct links, no redirectors) — and would have been
caught in 60 seconds if it hadn't been.

## Workflow
1. **Read the headers** — in Gmail: open the message → "Show original".
   Check the `Authentication-Results`: you want `spf=pass`, `dkim=pass`,
   `dmarc=pass` **all three**, with the DKIM `d=` domain matching the
   claimed sender's domain (not a lookalike).
2. **Inspect every link** — hover or copy: the *visible* text means
   nothing. The real destination is the `href`. Red flags: URL
   shorteners, redirector domains, punycode/lookalike domains
   (`rnuse.ai` vs `muse.ai`), mismatched display vs destination.
3. **Check the ask** — does it demand credentials, a password reset, a
   payment, or an "urgent" download? Legit senders rarely lead with
   urgency + a link. When in doubt, **don't use the email's link**:
   navigate to the official site yourself and check for the same notice
   in your account.
4. **Cross-check the channel** — is the same announcement on the
   company's official site, status page, or verified social? A real
   "portal is open" email has a public counterpart.
5. **Decide** — authentic: proceed, still via your own navigation.
   Suspicious: report as phishing, delete, and if you already clicked,
   rotate the exposed credential immediately.

## Output Contract
- Verdict: authentic / suspicious / inconclusive — with the evidence
  (which checks passed, which failed).
- The true destinations of the inspected links (domain-level, safe to
  quote).
- Next step: what to do (proceed safely / report / rotate).

## Operating Rules
1. **Headers before links.** Authentication results are harder to fake
   than link text.
2. A familiar logo, your name, or "we've emailed before" proves nothing.
3. Approval to *read* an email is never approval to *click* its links.
4. Never forward a suspicious email's links to someone else "to check" —
   describe it in words.
5. If you clicked before verifying: assume compromise of whatever the
   page asked for, rotate it, then investigate.

See `references/triage.md` for the 60-second version.
