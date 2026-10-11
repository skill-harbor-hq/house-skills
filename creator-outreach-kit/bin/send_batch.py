#!/usr/bin/env python3
"""Send the next N outreach emails from queue.json via Gmail. Marks sent.

Usage: send_batch.py --queue queue.json --account <gmail-account-id>
                     --subject "..." --template template.txt [--batch 30]

queue.json: [{"email": ..., "creator_name": ..., "projects": "...",
              "claim_url": ..., "sent": false}]
template.txt: plain text with {creator_name}, {projects}, {claim_url}.
Appends to send-log.txt next to the queue file. Never retries failures.
"""
from __future__ import annotations
import argparse, json, os, subprocess, time

# Scraper placeholder artifacts: never send to these, even if queued.
PLACEHOLDER_LOCALS = {"name", "your", "test", "example", "email", "user",
                      "me", "nobody", "none", "placeholder", "xxx", "abc",
                      "asdf", "dnx"}
PLACEHOLDER_DOMAINS = {"example.com", "example.org", "example.net",
                       "email.com", "test.com", "fdpez.aa", "report.url.cn"}

def looks_like_placeholder(email: str) -> bool:
    local, _, domain = email.partition("@")
    if "u003e" in email or "u003c" in email:
        return True
    return local in PLACEHOLDER_LOCALS or domain in PLACEHOLDER_DOMAINS

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--queue", required=True)
    ap.add_argument("--account", required=True)
    ap.add_argument("--subject", required=True)
    ap.add_argument("--template", required=True)
    ap.add_argument("--batch", type=int, default=30)
    args = ap.parse_args()

    queue = json.load(open(args.queue))
    template = open(args.template).read()
    pending = [x for x in queue if not x.get("sent")]
    batch = pending[:args.batch]
    sent, failed = [], []
    for item in batch:
        email = item["email"]
        if looks_like_placeholder(email):
            item["skipped"] = "placeholder"
            failed.append((email, "skipped: placeholder address"))
            continue
        body = template.format(
            creator_name=item.get("creator_name", "there"),
            projects=item.get("projects", ""),
            claim_url=item.get("claim_url", ""),
        )
        try:
            r = subprocess.run(
                ["hatch_gws_cli", "gmail", "+send", "--account", args.account,
                 "--to", email, "--subject", args.subject, "--body", body],
                capture_output=True, text=True, timeout=120)
            if r.returncode == 0:
                item["sent"] = True
                item["sent_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
                sent.append(email)
            else:
                err = (r.stderr or "")[-500:].replace("\n", " ")
                failed.append((email, err))
        except Exception as ex:
            failed.append((email, str(ex)[:200]))
        time.sleep(2)

    json.dump(queue, open(args.queue, "w"), indent=1)
    remaining = sum(1 for x in queue if not x.get("sent") and not x.get("skipped"))
    print(f"sent: {len(sent)}, failed: {len(failed)}, remaining: {remaining}")
    for email, err in failed:
        print(f"FAILED {email}: {err}")
    logdir = os.path.dirname(os.path.abspath(args.queue))
    with open(os.path.join(logdir, "send-log.txt"), "a") as log:
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        for e in sent:
            log.write(f"{ts} SENT {e}\n")
        for e, err in failed:
            log.write(f"{ts} FAILED {e} :: {err}\n")

if __name__ == "__main__":
    main()
