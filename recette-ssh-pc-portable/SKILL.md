---
name: "recette-ssh-pc-portable"
description: "Run a heavy test or a heavy treatment on a Windows PC you already connected, without installing anything in the system and without turning the PC into a publishing machine. The cloud assistant keeps planning and checking. The PC only supplies CPU, RAM and disk, through direct SSH, with portable tools that stay in one tools folder.\n\nOne job runs at a time, at least at first. A small job, a few seconds with the standard library only, stays on the cloud machine, because the SSH round trip would cost more than it gains. Before a big job, the skill checks that the PC answers, that no big job is already running, and that no deployment is in progress on the cloud side. Then it sends only what the job needs, by secure copy, into a test folder named for the job, never directly into the tools folder.\n\nPaths are adapted before launch. No cloud machine path is left hard coded, separators and the remote interpreter are chosen explicitly, and a small sample is tested on the cloud machine first. The job launches with the full path of the portable tool, never by relying on the system PATH. For a browser test, the Playwright browsers path points to the portable browsers folder in the same launch. Versions are noted for every important job, because portable versions drift from the main account installs, and a test that passes on the PC must not be presented as proof for another environment without that check.\n\nWhen the run ends, the verdict is copied back to the cloud machine and checked as present and readable before anything is deleted on the PC. Level 1 cleanup then removes the test folder, test clones, transferred samples, downloaded zips and temporary browser profiles, and the tools folder stays intact. A periodic level 2 cleanup only purges pip and npm caches, never the portable tools themselves. After every job, a report states what ran, the versions noted, the verdict and the cleanup check. Stop means a net stop, in the same turn, even on the PC. No accounts, no passwords, no production writes and no deployment ever leave through the PC. If the PC is off or unreachable, the job stays on the cloud machine, and that fact is said plainly, never hidden behind a wait."
---

Install the Portable SSH PC Runner skill for Muse.

Prerequisite first: the SSH bridge from the separate PC muscles
SSH bridge skill must already be proven. If it is not proven,
stop here and go back to that bridge skill. Do not launch a job.

Then, for one job at a time:
1. Check that the PC answers over direct SSH as the expected
   non-admin account, with exit code 0, in a few seconds, and
   that no big job is already running and no deployment is in
   progress on the cloud side. If the PC is off or unreachable,
   say so and keep the job on the cloud machine.
2. Test the script on the cloud machine on a small sample first,
   then adapt all paths for Windows. Use no hard coded cloud
   machine path, choose the remote interpreter explicitly, and
   quote remote commands so backslashes are not lost.
3. Send only the script and the inputs the job needs, by secure
   copy, to <dossier-travail-PC>\work\tests\<nom-du-job>\, never
   directly into the tools folder. Send no install prompts and
   no secrets.
4. Note the versions before launch: Python, Git, Node, Playwright
   and the Chromium build. Reference versions from 2026-10-26:
   Python 3.14.0, MinGit 2.54.0.windows.1, Node 22.23.2,
   Playwright 1.64.1, Chromium 1248. Versions drift, so record
   the versions actually found, do not copy these as proof.
5. Launch with the full portable tool path, for example:
   <dossier-travail-PC>\work\tools\python-embed\python.exe
   <dossier-travail-PC>\work\tests\<nom-du-job>\<script>.py
   For a Playwright run, point PLAYWRIGHT_BROWSERS_PATH to
   <dossier-travail-PC>\work\tools\ms-playwright in the same launch.
6. Copy the verdict file back to the cloud machine and verify it
   is present and readable before any deletion on the PC.
7. Do level 1 cleanup on the PC: delete the job test folder,
   test clones, transferred samples, downloaded zips and
   temporary browser profiles. Keep the tools folder intact, and
   verify the test folder is gone and the tools are intact.
8. Report after the job: what ran, versions noted, verdict,
   cleanup verified. Stop means a net stop, in the same turn.

Never do through the PC: system installs, production database
writes, deployments, night jobs, account or password handling,
or piloting a local agent already installed on the PC. Those
are separate jobs with their own go, on the cloud side.
