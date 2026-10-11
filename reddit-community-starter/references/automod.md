# Reddit Community Starter — AutoMod config

Edit via new.reddit.com → Mod Tools → AutoModerator (wiki page
`config/automoderator`). Test every rule with a throwaway post before
announcing.

## 1. Link policy per thread type
Allow links in effort threads (builds, showcases, tutorials); hold
link-only posts elsewhere for review:

```yaml
# Links are fine in effort threads
type: submission
flair_text (includes): ["Build", "Showcase", "Tutorial"]
action: approve

# Bare link posts elsewhere → filter for mod review
type: submission
is_self: false
~flair_text (includes): ["Build", "Showcase", "Tutorial"]
action: filter
action_reason: "bare link, needs context (Rule 7)"
```

## 2. Referral-code funnel
Codes are welcome ONLY in the pinned megathread. Anywhere else: remove
with a redirect message.

```yaml
# Auto-approve referral comments inside the megathread
type: comment
parent_submission:
  id: ["MEGATHREAD_POST_ID"]
action: approve

# Remove referral-looking comments elsewhere
type: comment
body (regex): ['(?i)(referral|promo|discount).{0,40}(code|link)|use my (code|link)']
~parent_submission:
  id: ["MEGATHREAD_POST_ID"]
action: remove
comment: |
  Thanks for sharing! Referral codes belong in our pinned referral
  megathread so the feed stays clean — please repost yours there. (Rule 9)
```

Replace `MEGATHREAD_POST_ID` with the base-36 id from the thread URL.
Note: Reddit's own spam filter sometimes eats legit megathread comments —
leave those alone unless the poster asks.

## 3. Per-thread exemptions by id
When a special thread needs different rules (e.g. the #1 build thread
allows links that would otherwise be filtered), exempt by thread id:

```yaml
type: submission
id: ["BUILDTHREAD_POST_ID"]
action: approve
```

Keep a note of every exempted thread id and why — exemptions rot when
threads are replaced.

## 4. Habits, not just config
- Every AutoMod removal that a human would question gets a manual modmail
  follow-up naming the rule.
- Review the mod queue daily for the first month; weekly after.
- Revisit the rules quarterly: dead rules get cut, new abuse patterns get
  one new rule max.
