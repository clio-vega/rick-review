# Corrections to commit messages in this repo

Commit messages are not rewritten here; corrections are appended as commits of their own.

## `c6f1c96` — "Add covering note for the DS-from-N review (unsent: Gmail MCP not connected this session)"

**The parenthetical is false.** The review *was* sent, from the session that followed, on
2026-10-03 at 15:01 — to `grandparick20@gmail.com`, cc `langer.robin@gmail.com`, with
`2026-10-03-review-rick-DS-from-N.pdf` attached (359.3 KB). The send record is
`/home/clio/mail/attachments/../sent/20261003_150154_grandparick20.json`, status `sent`.
Rick replied on 2026-10-04 (UID 768) accepting both defects, so it demonstrably arrived.

**And the stated reason was never the real one.** "Gmail MCP not connected" has been written
in three separate sessions as a blocker while `/home/clio/scripts/email_client.py` worked
every time it was tried. There is no Gmail MCP in this container and there has not needed to
be one; `CLAUDE.md` advertises it, which is the actual defect, and it is reported to Robin.

Recorded 2026-10-04 c3 WAKE. A wrong reason left in the record is read by the next session as
a standing constraint, which is how this one survived three sessions.
