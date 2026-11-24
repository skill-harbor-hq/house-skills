---
name: "perfume-advisor"
description: "Perfume Advisor is a perfume helper for Muse. It starts with your profile, not with a bestseller list: what you wear now, what you loved or hated before, whether you prefer eau de toilette or eau de parfum, whether the bottle matters to you, and which scents to avoid because someone close already wears them.\n\nThen it gives you three clear paths: buy the exact same scent again, try a similar scent in the same family, or upgrade to a richer, more mature scent from another house. Age is a guide, not a rule, and an eau de toilette is never presented as the same as an eau de parfum.\n\nBefore you spend anything, it checks real prices: in stock or sold out, boxed or tester, in your country and currency, including shipping, taxes and duties for cross-border shops. A catalogue price is never presented as an in-stock price.\n\nFinally, it helps you try before you buy: stores near you that carry the scent, a call to confirm the tester is actually there, clean skin with no perfume on, one scent per wrist, and a wait for the dry-down before deciding. If no store has a tester, it checks for small hand-filled decants, and warns you that an \"inspired by\" product is not the original."
---

## When to use this skill

When the user asks, in their own words:
- to find the best place / price to order a perfume;
- to replace a nearly empty bottle;
- to move on from their current perfume (a similar one, or an upgrade);
- whether they are "too old / too young" for a perfume;
- whether they can try a perfume near them, or buy a small cheap
  sample / decant before deciding.

Do not use this skill to push one specific perfume at all costs, or
to push a purchase. The final decision always belongs to the user,
after a try on their skin when possible.

## Principle 0 — Everything adapts to the user's place

Nothing is fixed to one country, city, currency, or merchant.

Before any price or store research, establish:
- the user's `[COUNTRY]` and `[CITY / REGION]`;
- `[CURRENCY]`;
- the local merchants to check, in this order:
  1. verified local discounters (authentic, no third-party sellers
     with no history);
  2. local official retailers / department stores;
  3. local loyalty programs (points, multiplier events);
  4. foreign merchants, only if the total delivered price
     (conversion + shipping + taxes / duties) is still truly lower.

Never present a merchant from another country as the default
reference, and never convert a price without saying so.

## Step 1 — Build the profile (before any recommendation)

Ask the questions, one at a time if the user dictates or answers
short, and guess nothing. Note the answers as given:

- Current perfume: `[BRAND + NAME + CONCENTRATION + SIZE]`
  (e.g.: eau de parfum 100 ml — concentration matters as much as
  the name).
- Current bottle: nearly empty? still half full?
- History, in order: `[PREVIOUS PERFUMES]` — what the person wore
  young, then later, then now.
- What they like: families / notes that work well on their skin
  (e.g.: fresh, citrus, woody, floral).
- What does not work for them: notes or families that smell
  "strange" on them, even if the perfume smells good on paper or on
  someone else (e.g.: smoky, leathery, very sweet).
- Preferred concentration: eau de toilette (EDT, usually 5-7 h) or
  eau de parfum (EDP, usually 7-9 h) — and why.
- Bottle looks: are the bottles displayed at home? An ugly bottle
  can rule out a perfume, even a good one.
- Perfumes to avoid by duplication: does someone close already wear
  a perfume the user likes? If so, exclude it, even if it is the
  favourite — say so clearly, without insisting.
- Budget: `[MAX BUDGET]` and tolerance (full price accepted?
  sale only? loyalty points accepted as a real discount?).
- Use: daily, work, outings, evenings, or all.

Rule: an EDT is never presented as equivalent to an EDP of the same
name. If the user wants "the same", it is the same concentration.

## Step 2 — Recommend: three paths, not one

Always present the three paths, in this order:

### A. Rebuy the exact one
The same perfume, same concentration, same size. This is the
default path if the bottle is nearly empty and the user loves it.

### B. A similar one
Same scent family, another house or another name, to vary without
changing style. Name how it resembles (shared notes) and how it
differs.

### C. An upgrade
Move away from the current house after years, toward a perfume:
- from the same base family, but richer / more mature / more
  elegant (stronger woody base, less "fresh shower");
- from another house, to mark the change;
- with a beautiful bottle, if looks matter.

Do not propose a perfume from the same house as an "upgrade" if the
user precisely wants to change houses.

### Age, a guide — not a rule
- A perfume has no age limit. Marketing often targets an age
  group, but the smell on the skin matters more than the ad.
- Distinguish: a lighter EDT version can feel younger than a
  woodier / rounder EDP version of the same name.
- Perfumes that truly feel "too young" in adulthood are usually
  sweet going-out scents (club, candy), not clean / woody / fresh
  ones.
- If the user feels too young / too old for a perfume, propose one
  notch more mature in the same family, without telling them they
  "must" change.

## Step 3 — Check prices, in stock, for real

For each perfume kept, check separately:

- Merchant, country, currency, exact size (e.g.: 100 ml, men's, EDP).
- Boxed or tester: a tester is the same juice, but often without
  a nice box and sometimes without a decorative cap — flag it when
  bottles are displayed. A tester is not a defect, it is a
  price / presentation trade-off.
- In stock or sold out, at the time of checking (date + time).
  A catalogue price is never an in-stock price.
- Listed price vs total price: taxes, shipping, conversion, duties.
  A foreign price that looks "cheaper" but beats the local price
  after conversion + shipping + duties is not a deal — say so with
  the numbers.
- Loyalty program: if a retailer offers multiplier points (e.g.:
  20x the points), compute the effective price in points and compare
  it to the discounter price, without inflating the value of points.
- Merchants to avoid: third-party sellers with no history,
  "inspired by" imitations presented as the original.

Present the result as a short table: perfume, best verified
in-stock price, merchant, boxed / tester, and what is still
unverified.

Presentation rules:
- Never claim "guaranteed in stock" for a specific store without
  having checked that store.
- Never claim a tester is on the shelf in a specific store without
  having checked it or proposing a confirmation call.
- If a check fails (store selector not loading, blocked site,
  etc.), say so as is, and propose the alternative (call the store,
  mobile app, another branch).

## Step 4 — Try before you buy

In order, cheapest first:

### 1. Free in-store try (first choice)
- Find stores that sell the perfume near `[CITY]`: local
  perfumeries first, then big beauty retailers.
- Give address, today's hours, and phone number if available —
  without inventing any address or hours.
- Propose calling before going: "Do you have the tester of
  `[PERFUME]` in store today?" — 30 seconds that avoid a wasted trip.
- In-store try plan:
  - one perfume per wrist, at most two on the skin;
  - the others on paper strips only;
  - do not rub the wrists together after spraying;
  - ask for free samples to take home if the store gives any.

### 2. Clean skin, dry-down first
- After a shower: no perfume, no scented cream, no strong
  aftershave on the test areas (wrists, inside of elbows, neck).
  Deodorant under the arms is acceptable, it is far from the test
  areas.
- Wait at least 20-30 minutes, ideally 1-2 hours (for example
  during a meal): the dry-down decides, not the first minute.
- A perfume that smells good on paper can smell different on the
  skin, and vice versa. The verdict is made on the skin, after
  drying.

### 3. Decants (small hand-filled sizes)
- If no nearby store has the tester, or to test for several days
  at your own pace: 2 ml, 5 ml, or 10 ml decants, hand-filled from
  the real bottle.
- Check, perfume by perfume and site by site, whether an authentic
  decant exists — many perfumes have none from local decanters.
- Warning: a "hybrid" or "inspired by" product is not the original,
  even if the name looks similar. Never present it as a decant of
  the real perfume.
- Rough size guide (to check, not to state): a 5 ml decant is
  enough for 4-5 real tests over several days.

### 4. Smallest official size
- If neither tester nor decant exists: the smallest official boxed
  size (e.g.: 50-60 ml) may be the cheapest test, to compare with
  the 100 ml.

## Step 5 — Decide, then only buy

Summarize in one sentence per option, with the verified price:
- Exact rebuy: `[PERFUME]` — `[VERIFIED PRICE]` at `[MERCHANT]`.
- Similar: `[PERFUME]` — `[VERIFIED PRICE]` at `[MERCHANT]`.
- Upgrade: `[PERFUME]` — `[VERIFIED PRICE]` at `[MERCHANT]`.

Add nothing to a cart, buy nothing, without the user's explicit yes
for that exact purchase, that exact merchant, that exact price.

If the user tried in store, ask for their verdict on the dry-down
(after drying), not on the first impression, before ordering.

## Pitfalls to avoid (lessons of the method)

- Presenting a catalogue price as an in-stock price.
- Presenting an EDT as "the same" as an EDP.
- Guaranteeing a tester in store without checking that store.
- Recommending a sweet / gourmand perfume to someone whose profile
  is fresh / clean, just because it is popular.
- Ignoring the bottle when the user displays their bottles.
- Ignoring a duplication with someone close ("someone close
  already wears it") in the name of the "best perfume".
- Presenting a foreign price without conversion, shipping, and duties.
- Presenting an "inspired by" imitation as the original.
- Pushing an in-store purchase at full price when the same perfume
  is verified much cheaper online — unless the user wants to leave
  with it right away and accepts it knowingly.

## Profile template (to copy at the start of the conversation)

```
Current perfume: [BRAND + NAME + CONCENTRATION + SIZE]
Bottle: [nearly empty / half / full]
History: [young] → [later] → [now]
Likes: [notes / families]
Dislikes on their skin: [notes / families]
Preferred concentration: [EDT / EDP + why]
Bottles displayed? [yes / no]
To avoid (someone close wears it): [PERFUME]
Budget: [MAX + tolerance]
Use: [daily / work / outings / evening]
Country / city: [COUNTRY] / [CITY]
Currency: [CURRENCY]
```

## What this skill does not do

- It sells nothing, puts nothing in a cart, pays nothing.
- It does not replace a try on the skin.
- It does not guarantee stock, a tester, or a future price: every
  price is dated, and must be rechecked before buying.
- It keeps no personal user data inside the skill itself: the
  profile lives in the conversation, not in this file.
