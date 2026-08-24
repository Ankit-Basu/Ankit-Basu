"""
Pull live GitHub numbers for the profile cards.

Runs in two modes:
  * with a token (GITHUB_TOKEN in Actions) -> GraphQL, gets the full
    contribution calendar, streaks and per-language byte counts
  * without a token (local dev)            -> REST for repos/profile plus the
    public streak service for the contribution totals

Either way the result is normalised into data/stats.json, and if the network
is unreachable the previous stats.json is kept so a build never regresses to
placeholder numbers.
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone, date

USER = os.environ.get("GH_USER", "Ankit-Basu")
TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "stats.json")

UA = {"User-Agent": "profile-readme-builder", "Accept": "application/vnd.github+json"}


def get(url, data=None, headers=None, timeout=30):
    h = dict(UA)
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=data, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


# ---------------------------------------------------------------- GraphQL
GQL = """
query($login:String!) {
  user(login:$login) {
    name
    createdAt
    followers { totalCount }
    following { totalCount }
    repositories(first:100, ownerAffiliations:OWNER, isFork:false,
                 orderBy:{field:STARGAZERS, direction:DESC}) {
      totalCount
      nodes {
        name stargazerCount forkCount
        languages(first:12, orderBy:{field:SIZE, direction:DESC}) {
          edges { size node { name color } }
        }
      }
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      totalRepositoryContributions
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def via_graphql():
    body = json.dumps({"query": GQL, "variables": {"login": USER}}).encode()
    raw = get("https://api.github.com/graphql", body,
              {"Authorization": "bearer " + TOKEN,
               "Content-Type": "application/json"})
    doc = json.loads(raw)
    if "errors" in doc:
        raise RuntimeError(doc["errors"])
    u = doc["data"]["user"]
    repos = u["repositories"]["nodes"]

    langs = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            n = e["node"]["name"]
            if n not in langs:
                langs[n] = {"size": 0, "color": e["node"]["color"] or "#8fb8c9"}
            langs[n]["size"] += e["size"]

    days = []
    for wk in u["contributionsCollection"]["contributionCalendar"]["weeks"]:
        for d in wk["contributionDays"]:
            days.append((d["date"], d["contributionCount"]))

    cc = u["contributionsCollection"]
    return {
        "name": u["name"] or USER,
        "created_at": u["createdAt"],
        "followers": u["followers"]["totalCount"],
        "following": u["following"]["totalCount"],
        "repos": u["repositories"]["totalCount"],
        "stars": sum(r["stargazerCount"] for r in repos),
        "forks": sum(r["forkCount"] for r in repos),
        "commits": cc["totalCommitContributions"],
        "prs": cc["totalPullRequestContributions"],
        "issues": cc["totalIssueContributions"],
        "languages": langs,
        "calendar": days,
        "top_repos": [{"name": r["name"], "stars": r["stargazerCount"]}
                      for r in repos[:6]],
    }


# ---------------------------------------------------------------- REST
def via_rest(prev):
    u = json.loads(get("https://api.github.com/users/" + USER))
    repos = json.loads(get(
        "https://api.github.com/users/%s/repos?per_page=100&type=owner" % USER))
    repos = [r for r in repos if not r.get("fork")]

    # Per-repo /languages gives true byte counts. The cheap alternative -
    # charging a repo's whole size to its primary language - badly misreports
    # a polyglot profile, since one large JS repo swamps every Python one.
    # Unauthenticated callers only get 60 requests an hour though, so the
    # per-repo results are cached and the walk resumes where it left off;
    # a couple of runs converge on full coverage.
    cache = dict(prev.get("lang_by_repo") or {})
    names = [r["full_name"] for r in repos]
    for r in repos:
        if r["full_name"] in cache:
            continue
        try:
            cache[r["full_name"]] = {k: int(v) for k, v in json.loads(get(
                "https://api.github.com/repos/%s/languages" % r["full_name"],
                timeout=20)).items()}
        except urllib.error.HTTPError as e:
            if e.code in (403, 429):
                print("rate limited - keeping %s/%s repos cached, rerun later"
                      % (len(cache), len(repos)), file=sys.stderr)
                break
            cache[r["full_name"]] = {}
        except Exception:
            pass

    cache = {k: v for k, v in cache.items() if k in names}
    covered = len(cache)
    langs = {}
    for per in cache.values():
        for n, size in per.items():
            langs.setdefault(n, {"size": 0, "color": None})
            langs[n]["size"] += size

    if covered < max(1, len(repos) * 0.75) or not langs:
        print("language coverage only %s/%s - falling back to primary language"
              % (covered, len(repos)), file=sys.stderr)
        langs = {}
        for r in repos:
            n = r.get("language")
            if n:
                langs.setdefault(n, {"size": 0, "color": None})
                langs[n]["size"] += max(int(r.get("size") or 1), 1)
    else:
        print("languages from %s/%s repos (exact byte counts)" % (covered, len(repos)))

    repos.sort(key=lambda r: -r["stargazers_count"])
    return {
        "name": u.get("name") or USER,
        "created_at": u["created_at"],
        "followers": u["followers"],
        "following": u["following"],
        "repos": u["public_repos"],
        "stars": sum(r["stargazers_count"] for r in repos),
        "forks": sum(r["forks_count"] for r in repos),
        "commits": None,
        "prs": None,
        "issues": None,
        "languages": langs,
        "calendar": [],
        "lang_by_repo": cache,
        "top_repos": [{"name": r["name"], "stars": r["stargazers_count"]}
                      for r in repos[:6]],
    }


# ---------------------------------------------------------------- streaks
def streaks_from_calendar(days):
    """Current + longest streak, computed from the real calendar."""
    days = sorted(days)
    today = datetime.now(timezone.utc).date().isoformat()
    best = cur = run = 0
    best_end = None
    for d, n in days:
        if d > today:
            break
        if n > 0:
            run += 1
            if run > best:
                best, best_end = run, d
        else:
            run = 0
    # current streak: walk backwards, tolerating an empty "today"
    past = [(d, n) for d, n in days if d <= today]
    for i in range(len(past) - 1, -1, -1):
        d, n = past[i]
        if n > 0:
            cur += 1
        elif i == len(past) - 1:
            continue  # today may simply not have landed yet
        else:
            break
    total = sum(n for _, n in past)
    return {"current": cur, "longest": best, "longest_end": best_end,
            "total_contributions": total}


def streaks_from_service():
    """Fall back to the public streak card and read the numbers back out."""
    txt = get("https://streak-stats.demolab.com?user=" + USER, timeout=40)
    nums = [n.replace(",", "") for n in
            re.findall(r">\s*([\d,]+)\s*<", txt)]
    nums = [int(n) for n in nums if n.isdigit()]
    out = {"current": None, "longest": None, "total_contributions": None}
    if len(nums) >= 3:
        out["total_contributions"], out["current"], out["longest"] = nums[0], nums[1], nums[2]
    return out


# ---------------------------------------------------------------- main
def main():
    prev = {}
    if os.path.exists(OUT):
        try:
            prev = json.load(open(OUT, encoding="utf-8"))
        except Exception:
            prev = {}

    data = None
    if TOKEN:
        try:
            data = via_graphql()
            print("source: graphql")
        except Exception as e:
            print("graphql failed: %s" % e, file=sys.stderr)
    if data is None:
        try:
            data = via_rest(prev)
            print("source: rest")
        except Exception as e:
            print("rest failed: %s" % e, file=sys.stderr)

    if data is None:
        if prev:
            print("network unreachable - keeping previous stats.json", file=sys.stderr)
            return 0
        print("no data and no cache; aborting", file=sys.stderr)
        return 1

    if data["calendar"]:
        data.update(streaks_from_calendar(data["calendar"]))
    else:
        try:
            data.update(streaks_from_service())
            print("streaks: public service")
        except Exception as e:
            print("streak service failed: %s" % e, file=sys.stderr)
            for k in ("current", "longest", "total_contributions"):
                data[k] = prev.get(k)

    # never let a transient blank overwrite a good number
    for k in ("current", "longest", "total_contributions"):
        if not data.get(k) and prev.get(k):
            data[k] = prev[k]

    created = data["created_at"][:10]
    y, m, d = (int(v) for v in created.split("-"))
    data["years_active"] = round(
        (date.today() - date(y, m, d)).days / 365.25, 1)
    data["synced_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("repos=%s stars=%s contributions=%s longest=%s current=%s langs=%s" % (
        data["repos"], data["stars"], data.get("total_contributions"),
        data.get("longest"), data.get("current"), len(data["languages"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
