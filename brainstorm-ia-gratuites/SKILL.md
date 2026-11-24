---
name: "brainstorm-ia-gratuites"
description: "Multi-AI Brainstorm asks the same question to several free AIs at once, without opening a browser. Give it a topic, and it sends the same prompt to each free voice, collects every answer, removes duplicates, keeps the ideas that come back often and the best unique ones, then gives you a short top list with the source of each idea. Wild ideas are kept apart, not thrown away.\n\nNo browser is needed for a run. Right now, by default, it goes through Pollinations, with no key and no account at all (one small model, gpt-oss-20b, about one request every 15 seconds). That is enough to test it.\n\nHow to add more voices, all free, no card. Do each one once, then it just works:\n- Pollinations with a key: make a free account at enter.pollinations.ai, get your free Seed key. It unlocks more models and goes faster, about one request every 5 seconds.\n- Gemini: open Google AI Studio with your Google account, create a free API key, no card needed.\n- Groq: make a free account on the Groq console, create a free API key, no card needed.\n- OpenRouter: make a free account, create a free API key, and use the models ending in :free.\n\nNever paste a key in the chat and never put one in a file. Tell your Muse which key you made, it opens a secure entry card, you type the key there, and it lives in the secure vault from then on.\n\nTested live, 2026-11-08, no browser: Pollinations answered in about 13 seconds with 5 name ideas. The same small model drifted off topic on a second test, which is why the skill filters and synthesises instead of copying answers raw.\n\nCaveats:\n- How it works, in plain terms: by default it goes through Pollinations, no key, no account. You can also use a free Pollinations key (free Seed account), and every other voice works with a free key, no card: Gemini (Google AI Studio), Groq, or OpenRouter :free models. See the description above for how to make each key, step by step.\n- No official free ChatGPT or Claude through an API: their free tiers are web only, so they need a browser. This skill does not pretend otherwise.\n- LLM7 anonymous access failed on 2026-11-08 (401 invalid key), and Duck.ai by direct call was blocked by an anti-bot challenge the same evening. Both are left out of the no-browser version.\n- Free tiers change often: models, limits and quotas move. Do not send sensitive or personal data to a free tier.\n- Ideas are not verified facts: a free model can invent a price, a name already taken, or a fact. Check before using an idea as a fact."
---

# Free multi-AI brainstorm, no browser needed

## The goal, in one sentence

You give a topic, the assistant asks the same question to
several free AIs through direct API calls (no browser, no
clicks, no sign-in to a chat website), then hands you back
a synthesis: the ideas that come back often, the best unique
ideas, and the wild ideas kept apart.

## What "no browser" means, honestly

With no browser, you CANNOT have the real free ChatGPT
or the real free Claude. Their official APIs have no free
tier. For those, you need the browser.

With no browser, you can have:

1. **With no key at all, right now: Pollinations.**
   Anonymous endpoint, no sign-up, no key.
   A single model when anonymous: `gpt-oss-20b`.
   Slow: about 1 request every 15 seconds.
   Quality: small model, decent but not brilliant ideas.
2. **With a free key, set up once, no browser after that:**
   - Gemini API (Google AI Studio): free key, no card.
     Flash-Lite, about 500 requests per day. Real Gemini.
   - Groq: free key, no card. About 1000 requests
     per day on `gpt-oss-120b` and other open models.
     Very fast.
   - OpenRouter, `:free` models: a single free key,
     several models behind it. About 50 requests per day,
     1000 after a one-time $10 credit purchase.
   - Pollinations with a free Seed key: unlocks more
     models (GPT, Gemini, DeepSeek, etc.), 1 request
     every 5 seconds.
3. **As a bonus, no browser needed: the PC's local LLM
   (Muscle, Qwen) if the PC is on, and Muse herself as
   the synthesis voice.** They are not AIs from the web,
   but they add different voices at no cost.

Free keys are never pasted in a thread, never in this
file, never in plain text in a script. They live in the
assistant's secure vault, and the assistant uses them
through its connector, without ever displaying them.

Never send sensitive or personal data to a free tier:
Google says it may use free-tier content to improve its
products, and anonymous relays offer no confidentiality
guarantee.

## Test verified on 2026-11-08 (no browser, from the VM)

Test topic: "5 short name ideas for a skill that makes
several free AIs brainstorm together", in French.

- **Pollinations anonymous, POST https://text.pollinations.ai/openai,
  model `gpt-oss-20b`: WORKS.**
  Answer in about 13 seconds, 453 tokens in total.
  Result: 1. Éclat IA, 2. CréaCollectif, 3. BrainSync gratuit,
  4. Fusion d'idées, 5. Conflux Cogité/Compréhensif.
  Average quality, one idea in five is vague, but the
  mechanism works.
- **LLM7 anonymous, key `unused`: DEAD, tested the same evening.**
  `401 invalid_api_key`, despite August 2026 articles saying
  it worked with no account. Do not include it.
- **Duck.ai by direct curl: BLOCKED, tested the same evening.**
  The status endpoint returns an anti-bot challenge, no
  easily usable token. It is a browser service, not a
  reliable API for this skill. Do not include it in the
  no-browser version.

Test conclusion: with no key, there is a single reliable
external voice today (Pollinations). To have 3 different
external voices with no browser, you need at least one free
key (Gemini, Groq or OpenRouter).

## Global rule — check everywhere, in every chat

Max's decision, 2026-11-08: this rule applies to ALL
chats, present and future, not just this skill. At every
brainstorm, whatever the topic, the assistant tries to
check everywhere:

1. No browser first: Pollinations with no key, then
   Gemini / Groq / OpenRouter if a free key is installed.
2. Muse herself, as synthesis and filtering voice.
3. The PC's local LLM (Muscle, Qwen) if the PC is on.
4. Browser only if Max asks for it explicitly:
   ChatGPT, Gemini web, Claude, Duck.ai.

Each source is reported with what worked or not,
never invented. A failure (401, anti-bot block, timeout)
is noted as-is, and the brainstorm goes on with the voices
that remain. Never present an invented idea as coming from
an AI that was not asked.

## How it works, step by step

### 1. The user gives the topic

The assistant asks, if it is not already clear:
- the topic, in one sentence
- the language of the answer
- how many ideas (default: 10)
- the constraints (budget, audience, tone, things to avoid)
- which AIs to use (test default: Pollinations alone;
  default with keys: Pollinations + Gemini + Groq)

If the topic is vague, the assistant restates the topic in its
own words and waits for the yes before launching the calls.
Do not launch 3 time-costly calls on a misunderstood topic.

### 2. Same prompt, everywhere

The assistant writes ONE prompt, the same for every AI,
for example:

```text
Brainstorm on: <topic>.
Give <N> short and different ideas, in <language>.
Constraints: <constraints>.
Format: numbered list, one idea per line, no long explanation.
```

Same prompt = honest comparison. If the prompt changes
between two AIs, you no longer know whether the difference
comes from the AI or from the prompt.

### 3. Calls, one by one, no browser

- Pollinations anonymous:
  `POST https://text.pollinations.ai/openai`
  `{"model": "gpt-oss-20b", "messages": [{"role": "user", "content": "<prompt>"}]}`
  Wait at least 15 seconds between two anonymous calls.
- Gemini / Groq / OpenRouter: same OpenAI-compatible
  format, with the key from the vault, never in plain text.
  Base URL depends on the provider, model depends on the key.
- Each answer is kept as-is, with its source
  (provider + model + time). Do not rewrite an answer
  before the synthesis, or you lose track of who said what.

If a call fails (401, 429, timeout), note it as-is,
do not invent it, and carry on with the others. A
2-voice brainstorm is better than an invented 3-voice one.

### 4. Synthesis

The assistant, as synthesis voice, does this:
- removes duplicates (same idea, different words = one idea)
- counts the ideas that come back across several AIs
- keeps the best unique ideas, even if only one AI
  said them
- puts wild or risky ideas apart, without throwing them away
- returns a top 5 or top 10, with the source of each idea
- proposes a single concrete next step

Default output format:
- Top ideas (with source)
- Ideas that come back everywhere (consensus)
- Unique ideas worth keeping
- Wild ideas, to keep
- Proposed next step

### 5. Second round, only if the user wants it

If the user picks 2 or 3 ideas, the assistant can
run ONE second round: same refinement prompt to
every AI, on those ideas only. No automatic second round:
each round costs time and free quota.

## Limits to tell the user, without hiding them

- Free tiers change often: model, limit,
  price. Check live before promising a number.
- Anonymous Pollinations is slow and small. It is a test,
  not production.
- Ideas are not verified: a free AI can
  invent a fact, a price, a name already taken. Check
  before using an idea as a fact.
- No official ChatGPT or Claude without a browser.
- Free quotas are per day and per account, not
  infinite. A brainstorm with 3 AIs, 2 rounds, is 6 calls.

## What this skill does not do

- It opens no browser.
- It does not sign in to any ChatGPT, Claude, Google
  or other account in the user's place.
- It does not paste any key, password or secret
  in a thread or in this file.
- It does not publish anything, on Skill Harbor or anywhere else.
- It does not promise an exact number of free messages
  per day: limits change, they are checked.

## Test checklist

- [x] Pollinations anonymous: works, 2026-11-08
- [x] LLM7 anonymous: dead (401), 2026-11-08
- [x] Duck.ai by curl: blocked (challenge), 2026-11-08
- [ ] Test with a real topic from Max, 3 voices
- [ ] Test with a free key (Gemini or Groq), if Max wants it
- [ ] Reviewed and approved by Max before any other use
