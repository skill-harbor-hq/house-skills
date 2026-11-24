---
name: delegation-parallele
description: Delegate long work to subagents in parallel, in waves of 2 to 5 maximum, without ever blocking the main agent, with a final, instant stop.
---

# Parallel Delegation — the main agent stays available

> Status: CLEANED DRAFT, not published.
> No deployment, no production writes, no queue entries made from this draft. To approve before any other use.
> This file contains no personal data, no secrets, no personal paths, no network addresses, no real host names.

Delegate long, multi-step, self-contained work to subagents, in parallel when the tasks are independent, without ever blocking the main agent. The main agent coordinates and answers the user; it does not do the heavy work itself.

## Golden rule: keep juice to answer

- The main agent never launches the heavy computation, the heavy scan, or the heavy processing in its own turn. It delegates, then stays free to answer the user.
- If the user writes while work is running, answering the user comes first. The background work continues, except on stop.
- Never poll: do not check in a loop whether the agents are done, do not wait, do not predict a duration. Results arrive on their own via the runtime.
- A brief acknowledgement of receipt, then the work, then a message only when there is a result or a decision to make. No narration of work in progress.

## When to delegate, when not to delegate

- Delegate: long, multi-step, self-contained work, or several independent tasks to do at the same time.
- Do it yourself: a short answer, a simple read, a single quick action.
- Never delegate to a generic subagent: navigation or buying in a live browser, or creating a document, a page, or an application. Those routes have their own dedicated tools.

## Number of agents in parallel: a ceiling, not a theoretical maximum

- By default, 2 agents in parallel for heavy work. That is enough to move on two fronts without blocking the main agent.
- Absolute ceiling: 4 to 5 agents in parallel, never more.
- Lesson learned: 10 agents in parallel hit a rate limit (429 error) and 2 agents died on the way. After a rate limit, reduce the wave, do not relaunch harder.
- For dependent tasks (for example chained lots), do not parallelize: a single coordinator, sequential execution, complete validation per step, clean stop at the first failure or the first rate limit.

## Launching correctly

- One subagent per independent task, all launched in the same turn, not one at a time.
- If a task needs several subagents, launch a single coordinator and let it distribute the work itself. Nesting stops there: the coordinator's subagents do not launch their own subagents.
- Each brief is self-sufficient: the exact task, the expected deliverable, the output file, the facts already verified, the constraints and the prohibitions. The subagent does not guess what is not written.
- After launching, briefly acknowledge what went out and end the turn. Do not invent results, do not promise an end time.

## Standard brief: what it must always contain

- The concrete result expected, and where to put it (a file, not a message alone).
- What is forbidden: no publication, no deployment, no production writes, except a separate explicit go for that exact action.
- The work's guardrails: verify before asserting, sourced numbers only, failures preserved and reported (never erased), never repeat an irreversible action whose result is unknown.

## During and after: verify, then report piece by piece

- Report each piece as soon as it comes in, not only at the end. A long silent chain is forbidden.
- Verify delegated work with the same care as work done yourself: reread the evidence behind decisive claims, and re-verify it when it is missing or ambiguous. An agent's "done" report proves one step, not the result.
- If an agent is interrupted, failed, or of unknown status: inspect its results before deciding (tell the user, relaunch, or close). Never silently abandon work.
- To redirect an agent in progress: send it a follow-up instruction, knowing the send is asynchronous (sent, not applied). To stop work that has become useless: close the agent.

## Separate compute: parallelize the computation, not the decision

- If the user has a separate compute machine, it can serve heavy work (builds, tests, heavy processing, heavy scans). The brain stays the main agent.
- Delegate to that machine when it is faster, or when the main machine is out of juice (saturated, low memory or processor, heavy job already running), even if the raw speed gain is modest.
- Hard rules, unchanged by delegation: report after each job; nothing published or deployed without the user's explicit go for that action; stop = instant halt; never the user's accounts or passwords; jobs only within the hours the user authorized.
- Unreachable machine = the job waits, say so, do not hammer. Never display a private network address in the thread.
- Aim for 90%, not 100%: on the compute machine itself, a single heavy job at a time when possible, two tracks maximum in total, and always a reserve for the system and for the user's own use. Pushing to 100% bugs the whole thing instead of going faster. If a job fails or hits a rate limit, reduce, do not relaunch harder.
- A separate machine removes the compute ceiling. It removes neither the go, nor the parallel-agent ceiling, nor external delays outside our control (exploration, indexing, third-party services).

## Stop: final and instant

- When the user says stop / no, or when the system refuses an action: everything stops in the same turn. Agents closed, no new probe, no "last check".
- Confirm the halt with a verified fact (0 active agents), then stay silent.
- A refusal is never retried in another form (another tool, another wording, a workaround) without the user's new explicit go for that exact action.

## What this skill does not do

- It does not replace browser tools, nor document- and application-creation tools.
- It does not authorize publication, deployment, or production writes.
- It does not remove rate limits, nor delays from external services.

Note: this skill does not replace browser tools, nor document- and application-creation tools; it does not authorize publication, deployment, or production writes.
