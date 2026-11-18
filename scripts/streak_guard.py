"""
Streak guard: a nudge, never a commit.

Run by .github/workflows/streak-guard.yml in the evening (IST). It reads
today's count from the public contribution calendar and:

  * count > 0  -> closes any open guard issue ("streak safe")
  * count == 0 -> opens one issue that @-mentions the owner, so the GitHub
                  app pushes a notification while there is still time to
                  ship something real; a later run the same evening adds a
                  last-call comment instead of opening a second issue
  * guard issues left over from an earlier day are closed as stale

It never writes to the repository and never makes a contribution itself.

    GITHUB_TOKEN=... GH_USER=Ankit-Basu GITHUB_REPOSITORY=Ankit-Basu/Ankit-Basu \\
        python scripts/streak_guard.py

Testing: DRY_RUN=1 prints what it would do; FORCE_COUNT=0 pretends today
is empty so the alert path can be exercised.
"""
import datetime as dt
import json
import os
import sys
import urllib.request

TOKEN = os.environ.get("GITHUB_TOKEN", "")
USER = os.environ.get("GH_USER", "Ankit-Basu")
REPO = os.environ.get("GITHUB_REPOSITORY", "%s/%s" % (USER, USER))
DRY = bool(os.environ.get("DRY_RUN"))
TZ = dt.timezone(dt.timedelta(hours=5, minutes=30))  # IST - the calendar dates commits in local time
LABEL = "streak-guard"
API = "https://api.github.com"


def call(method, path, body=None):
    url = path if path.startswith("http") else API + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": "bearer " + TOKEN,
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "User-Agent": "profile-streak-guard",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()
    return json.loads(raw) if raw else None


def today_count(today):
    q = ("query($login:String!){user(login:$login){contributionsCollection{"
         "contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}")
    res = call("POST", "/graphql", {"query": q, "variables": {"login": USER}})
    weeks = res["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    days = {d["date"]: d["contributionCount"] for w in weeks for d in w["contributionDays"]}
    return days.get(today, 0), days


COUNTED = {"PushEvent", "PullRequestEvent", "IssuesEvent", "PullRequestReviewEvent", "CreateEvent"}


def events_today(midnight):
    """Contribution-type events since local midnight, from the public feed.

    The calendar alone can't answer "today": GitHub buckets it in the
    viewer's timezone, and the Actions token has none, so it gets UTC days -
    commits made before 05:30 IST land on "yesterday". Event timestamps are
    exact, so counting from IST midnight is right whatever token runs this.
    """
    n = 0
    for page in (1, 2, 3):
        evs = call("GET", "/users/%s/events/public?per_page=100&page=%d" % (USER, page)) or []
        for e in evs:
            when = dt.datetime.fromisoformat(e["created_at"].replace("Z", "+00:00"))
            if when < midnight:
                return n
            if e["type"] in COUNTED:
                n += 1
        if len(evs) < 100:
            break
    return n


def streak_before(today, days):
    """Length of the streak that ends yesterday - what is at stake tonight."""
    n, d = 0, dt.date.fromisoformat(today) - dt.timedelta(days=1)
    while days.get(d.isoformat(), 0) > 0:
        n += 1
        d -= dt.timedelta(days=1)
    return n


def act(desc, fn):
    print(("[dry-run] " if DRY else "") + desc)
    if not DRY:
        return fn()


def main():
    if not TOKEN:
        print("GITHUB_TOKEN is not set", file=sys.stderr)
        return 1
    now = dt.datetime.now(TZ)
    today = now.date().isoformat()
    cal_count, days = today_count(today)
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    ev_count = events_today(midnight)
    # either source seeing activity is enough; only both at zero raises an alert
    count = max(cal_count, ev_count)
    print("calendar says %d, activity feed says %d since midnight IST" % (cal_count, ev_count))
    if os.environ.get("FORCE_COUNT") is not None:
        count = int(os.environ["FORCE_COUNT"])
    at_stake = streak_before(today, days)
    hours_left = 24 - now.hour - (1 if now.minute else 0)
    print("%s IST: %d contributions today, %d-day streak at stake, ~%dh left"
          % (now.strftime("%Y-%m-%d %H:%M"), count, at_stake, hours_left))

    open_issues = call("GET", "/repos/%s/issues?state=open&labels=%s&per_page=20" % (REPO, LABEL)) or []
    title_today = "Streak guard: no contributions yet on %s" % today

    for iss in open_issues:
        if iss["title"] != title_today:
            act("close stale #%d" % iss["number"], lambda i=iss: (
                call("POST", "/repos/%s/issues/%d/comments" % (REPO, i["number"]),
                     {"body": "That day is over, closing this one."}),
                call("PATCH", "/repos/%s/issues/%d" % (REPO, i["number"]), {"state": "closed"})))

    mine = [i for i in open_issues if i["title"] == title_today]
    if count > 0:
        for iss in mine:
            act("close #%d, streak safe" % iss["number"], lambda i=iss: (
                call("POST", "/repos/%s/issues/%d/comments" % (REPO, i["number"]),
                     {"body": "Streak safe: %d contribution%s today. BYTE is back to work."
                      % (count, "" if count == 1 else "s")}),
                call("PATCH", "/repos/%s/issues/%d" % (REPO, i["number"]), {"state": "closed"})))
        if not mine:
            print("nothing to do")
        return 0

    stake = ("your **%d-day streak** ends at midnight IST" % at_stake) if at_stake else \
        "today's square is still empty"
    if mine:
        act("last-call comment on #%d" % mine[0]["number"], lambda: call(
            "POST", "/repos/%s/issues/%d/comments" % (REPO, mine[0]["number"]),
            {"body": "@%s last call: about %d hour%s left and %s." % (
                USER, hours_left, "" if hours_left == 1 else "s", stake)}))
        return 0

    body = ("@%s BYTE is falling asleep: no contributions yet today, and %s "
            "(about %d hours left).\n\n"
            "Anything real counts: a commit to any repo's default branch, a pull request, "
            "an issue, or a review.\n\n"
            "<sub>Opened by `.github/workflows/streak-guard.yml`. It closes itself once "
            "today has a contribution. It never commits for you.</sub>"
            % (USER, stake, hours_left))
    act("open guard issue for %s" % today, lambda: (
        call("POST", "/repos/%s/labels" % REPO, {"name": LABEL, "color": "ff4fa0"})
        if not any(l["name"] == LABEL for l in call("GET", "/repos/%s/labels?per_page=100" % REPO))
        else None,
        call("POST", "/repos/%s/issues" % REPO, {"title": title_today, "body": body, "labels": [LABEL]})))
    return 0


if __name__ == "__main__":
    sys.exit(main())
