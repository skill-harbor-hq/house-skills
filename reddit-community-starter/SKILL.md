---
name: "reddit-community-starter"
description: "Launch and moderate a new subreddit: the 10-rule starter set, AutoMod config (link policy, referral-code funnel, per-thread exemptions), pinned-thread strategy, and the human moderation habits that keep a small community alive. Use when starting or reviving a community subreddit."
---

# Reddit Community Starter

## Purpose
A new subreddit dies from two things: no clear rules and no reason to
come back. This is the full starter kit from two live communities —
rules, AutoMod, pinned threads, and the moderation habits that kept
early members posting. Everything here assumes a human moderator, not a
bot: automation handles the boring enforcement, you handle the people.

## Workflow
1. **Rules** — start with the 10-rule set in `references/rules.md`
   (on-topic, be kind, no vulgar content, no misinformation, respect
   privacy, no piracy, self-promo with context encouraged, no bare links
   or reposts, referral codes only in the pinned thread). Adapt the
   wording, keep the count low — nobody reads 25 rules.
2. **Pinned threads** — pin exactly two: the themed discussion/build
   thread (#1, the reason to return weekly) and the referral/code megathread
   (#2, the funnel that keeps codes out of the feed). Rotate or refresh the
   #1 thread on a schedule.
3. **AutoMod** — configure the three policies in `references/automod.md`:
   link policy per thread type, referral-code funnel (approve in megathread,
   remove elsewhere with a redirect message), and per-thread exemptions by
   thread id.
4. **Moderation habits** — every removal gets a short modmail naming the
   rule and where the content belongs. Never silently remove. Leave
   Reddit's own spam-filter removals alone unless they're wrong.
5. **Growth** — seed with your own posts (up to ~3/day, real content not
   filler), reply to every early commenter sincerely, cross-link with your
   other communities (Facebook group, newsletter). Never mention bans,
   removals, or bot activity publicly.

## Output Contract
- Rules published on the subreddit (sidebar + rules page).
- AutoMod wiki page configured and tested with a throwaway post.
- Two pinned threads live, in the right order.

## Operating Rules
1. **You post, the assistant drafts.** Published text is always the human's
   own words — drafts are thinking tools only, never signed.
2. Never invent anecdotes or personal experiences in drafts.
3. Referral/promo codes live ONLY in the megathread — removed on sight
   elsewhere, with a redirect modmail. No exceptions, including your own.
4. If Reddit removes something, leave it removed. Don't re-approve against
   the admins.
5. Never create alt accounts to seed activity. One honest community beats
   ten astroturfed ones.
6. Automated posting stays OFF until explicitly re-authorized — and every
   automated action must be reversible and logged.

See `references/rules.md` and `references/automod.md`.
