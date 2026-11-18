"""
Count one Game Mode vote. Run by .github/workflows/vote.yml when someone
opens an issue titled "vote: <key>".

    ISSUE_TITLE="vote: rust" ISSUE_USER=octocat python scripts/vote.py

The issue title and author are untrusted input. They only ever arrive through
environment variables, the key must match one of profile.VOTE_OPTIONS
exactly, and nothing from the title is echoed back except a known key.

Writes the reply for the bot's issue comment to $GITHUB_OUTPUT as `reply`,
and `changed=true|false` so the workflow knows whether to rebuild.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import profile as P  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "data", "votes.json")


def out(**kw):
    dest = os.environ.get("GITHUB_OUTPUT")
    lines = "".join("%s=%s\n" % (k, v) for k, v in kw.items())
    if dest:
        with open(dest, "a", encoding="utf-8") as f:
            f.write(lines)
    print(lines, end="")


def main():
    title = os.environ.get("ISSUE_TITLE", "")
    user = os.environ.get("ISSUE_USER", "").lower()
    m = re.match(r"\s*vote\s*:\s*([a-z0-9-]+)\s*$", title, re.I)
    options = {k: label for k, label, *_ in P.VOTE_OPTIONS}
    key = m.group(1).lower() if m else None
    if key not in options or not re.fullmatch(r"[a-z0-9-]{1,39}", user or ""):
        out(changed="false", reply="Unknown quest. Valid votes: " + ", ".join(
            "`vote: %s`" % k for k in options) + ". Nothing was counted.")
        return 0

    data = json.load(open(PATH, encoding="utf-8")) if os.path.exists(PATH) else {}
    entry = data.setdefault(key, {"votes": 0, "voters": []})
    if user in entry["voters"]:
        out(changed="false", reply="You have already voted for **%s**. One vote per player per quest!"
            % options[key])
        return 0
    entry["voters"].append(user)
    entry["votes"] = len(entry["voters"])
    for k in options:
        data.setdefault(k, {"votes": 0, "voters": []})
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
    out(changed="true", reply="Vote counted for **%s** (now %d). Thanks for playing! "
        "The profile redraws in a minute." % (options[key], entry["votes"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
