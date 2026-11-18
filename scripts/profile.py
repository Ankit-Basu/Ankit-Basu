"""
All the hand-written content, kept apart from the layout code.

Edit this file to change what the cards say. Numbers that GitHub already
knows (repos, stars, streaks, languages) are NOT here - those come from
data/stats.json via fetch_stats.py, so they can never go stale.
"""
from design import CREAM, ROSE, MINT, VIOLET

NAME = "ANKIT BASU"
ROLE = "SOFTWARE ARCHITECT  ×  AI RESEARCHER"
TAGLINE = "Full-Stack Systems · Computer Vision & Deep Learning · Cloud DevOps"
STATUS = "OPEN TO SWE / AI ENGINEERING ROLES"
LOCATION = "Jalandhar, Punjab · India"

GITHUB = "Ankit-Basu"
LINKEDIN_URL = "https://www.linkedin.com/in/ankit-basu-4a6774297/"
LINKEDIN = "Ankit Basu"
INSTAGRAM = "_ank1t._"
EMAIL = "ankitbasu935@gmail.com"

QUOTE = "If it isn't in production yet, it's still a side quest."
MOTTO = "BUILD  •  BREAK  •  FIX  •  SHIP  •  REPEAT"

HERO_CHIPS = ["JAVA", "PYTHON", "REACT", "NODE.JS", "PYTORCH", "DOCKER", "AWS"]

# ------------------------------------------------------------ credentials
# (value, label, sublabel, ring %, accent, icon)
CREDS = [
    ("9.2", "CGPA", "B.Tech CSE · ISC 95% · ICSE 97%", 92, CREAM, "cap"),
    ("400+", "DSA SOLVED", "LeetCode · GFG · Codeforces", 80, MINT, "code"),
    ("1590", "LEETCODE", "Top 25% globally", 72, ROSE, "pulse"),
    ("5+", "HACKATHON WINS", "National & university podiums", 85, VIOLET, "trophy"),
]

# ------------------------------------------------------------ arsenal
ARSENAL = [
    ("LANGUAGES", CREAM, ["Java", "Python", "C++", "JavaScript", "TypeScript", "SQL", "PHP"]),
    ("FRAMEWORKS", ROSE, ["React / Next", "Node / Express", "PyTorch", "LangChain",
                          "Flask", "Tailwind", "Three.js"]),
    ("INFRASTRUCTURE", MINT, ["Docker", "Kubernetes", "AWS", "MongoDB", "PostgreSQL",
                              "Redis", "CI/CD", "Jenkins"]),
]

# (label, %, accent)
PROFICIENCY = [
    ("Java / DSA", 94, CREAM),
    ("Full Stack (MERN)", 90, ROSE),
    ("Cloud & DevOps", 84, MINT),
    ("AI / Deep Learning", 80, VIOLET),
]

CERTS = [("NPTEL · IIT", "Privacy & Security"),
         ("CSE Pathshala", "Advanced C & DSA"),
         ("LPU", "Java Application Development")]

# ------------------------------------------------------------ projects
# Pulled from each repo's own README. rarity, icon, title, subtitle,
# body lines, tech chips, repo slug, live link label (or None)
PROJECTS = [
    dict(rarity="LEGENDARY", icon="shield", title="SheShield",
         sub="No one walks home alone",
         body=["Women's safety platform for LPU: one-tap SOS without sign-in,",
               "verified Walk-With-Us escorts, anonymous incident reports and a",
               "live campus safety map. Web app + Expo SDK 58 Android app."],
         tech=["PHP", "MySQL", "React Native", "Expo", "Leaflet"],
         repo="SheShield", live="sheshield-ab.vercel.app"),
    dict(rarity="MYTHIC", icon="bolt", title="Vyapaar",
         sub="Agent commerce on Razorpay rails",
         body=["An outside AI agent discovers the catalog, proves a human's",
               "consent and clears nine guardrails before it pays, while the",
               "merchant's own growth agent can never fake a discount."],
         tech=["FastAPI", "Next.js", "Razorpay", "JWT mandates"],
         repo="Vyapaar", live="vyapaar-web.vercel.app"),
    dict(rarity="EPIC", icon="users", title="Hirehearsal",
         sub="Rehearse the hire",
         body=["Ora, a voice-first AI interviewer, runs technical,",
               "project and HR rounds, adapts difficulty and scores",
               "substance, clarity and depth."],
         tech=["Next.js 16", "Java", "Docker"], repo="Hirehearsal", live=None),
    dict(rarity="EPIC", icon="cap", title="BookMyCampus",
         sub="Every bookable room, one platform",
         body=["Labs, halls and equipment with approval chains,",
               "QR check-in, auto-release of no-shows and a",
               "make-up class finder for faculty."],
         tech=["Django", "PostgreSQL", "React"], repo="BookMyCampus",
         live="book-my-campus-ab.vercel.app"),
    dict(rarity="RARE", icon="clock", title="TimedInk",
         sub="Fault-tolerant email scheduler",
         body=["Sends land on time through restarts, a wiped",
               "Redis and provider rate limits. MySQL is the",
               "truth; the queue rebuilds from it. 73 tests."],
         tech=["Node", "BullMQ", "Redis", "MySQL"], repo="TimedInk",
         live="timed-ink.vercel.app"),
    dict(rarity="RARE", icon="code", title="PII Redaction",
         sub="Enterprise document privacy engine",
         body=["Hybrid regex + NER engine that swaps 10 PII",
               "types for realistic fakes in .docx files while",
               "keeping every table and format intact."],
         tech=["Python", "spaCy", "python-docx"], repo="PII-Redaction-Tool", live=None),
]

# The rest of the story, shown as compact chips under the vault.
# (title, one-liner, repo slug or None)
SIDE_QUESTS = [
    ("GridSense", "3D smart-grid digital twin", "GridSense"),
    ("MindBloom", "Gemini AI wellness for kids", "MindBloom"),
    ("Pixel-Board", "8-bit multiplayer whiteboard", "Pixel-Board"),
    ("CampusWhisper", "Anonymous confessions", "CampusWhisper"),
    ("AlgoTrail", "Algorithm visual playground", "AlgoTrail"),
    ("SUDARSHAN-X", "Autonomous drone defence", None),
    ("KrishiVaani", "Multilingual farming assistant", None),
]

# ------------------------------------------------------------ story
ROLES = ["Software Architect", "AI Researcher", "Full-Stack Engineer",
         "Safety-Tech Builder"]

STORY = ["A builder from Jalandhar who turns campus problems into",
         "production systems: safety tech, AI agents and tools",
         "that real people open every day."]

# Chapter cards between sections: (numeral, kicker, title, narrator line, accent)
# Titles are narrative on purpose - the panel below each card carries the
# descriptive heading, so the two never repeat each other.
CHAPTERS = [
    ("I", "ORIGIN STORY", "It started with one commit",
     "September 2023. An empty account, a laptop, and far too many ideas.", CREAM),
    ("II", "THE ARSENAL", "Gearing up",
     "Before any boss fight, the player checks what they are carrying.", ROSE),
    ("III", "THE BUILDS", "Things that shipped",
     "Some quests ended as products that people open every single day.", MINT),
    ("IV", "BATTLE LOG", "Every commit leaves a mark",
     "GitHub keeps score. Here is what it says, refreshed every morning.", VIOLET),
    ("V", "TROPHY HALL", "Hard-won loot",
     "Not every battle was won. These ones were, and they left a mark.", CREAM),
    ("VI", "CURRENT QUEST", "The road ahead",
     "The story is not finished. You get to choose what happens next.", ROSE),
]

# Origin timeline, dated from each repo's creation date.
# (when, title, line 1, line 2, accent)
TIMELINE = [
    ("SEP 2023", "Player spawned", "Created this GitHub account.", "Level 1, no gear, big ideas.", CREAM),
    ("SEP 2024", "The grind begins", "LeetCode-Solutions and CP drills:", "400+ problems and counting.", MINT),
    ("MAR 2025", "SheShield", "A women's safety platform that", "now has 20 stars and an APK.", ROSE),
    ("JUL 2025", "Hackathon season", "AlgoTrail visualiser and the", "Adobe Hackathon PDF engine.", VIOLET),
    ("NOV 2025", "GridSense", "A 3D smart-grid digital twin", "with ML forecasting.", CREAM),
    ("FEB 2026", "Real-time arc", "Pixel-Board and CampusWhisper:", "Socket.IO, WebRTC, Groq vision.", MINT),
    ("MAY 2026", "MindBloom", "Gemini-powered wellness for", "children, parents, counsellors.", ROSE),
    ("AUG 2026", "Systems arc", "PII redaction engine, then", "Vyapaar agent commerce.", VIOLET),
    ("SEP 2026", "Production grade", "TimedInk scheduler and the", "Hirehearsal AI interviewer.", CREAM),
    ("NOV 2026", "Now playing", "BookMyCampus, Pratirodh and", "the SheShield Android app.", MINT),
]

# ------------------------------------------------------------ trophies
# icon, title, sub, value, unit, accent
TROPHIES = [
    ("medal", "Hackathon Wins", "National & university podiums", "5+", "WINS", CREAM),
    ("code", "DSA Mastery", "400+ problems · top 25%", "1590", "LC RATING", MINT),
    ("bolt", "Contest Ranking", "CF Div3 #1178 · CC #1161", "1119", "CF RATING", VIOLET),
    ("cap", "Academic Honours", "ISC 95% · ICSE 97%", "9.2", "/ 10 CGPA", ROSE),
]

# ------------------------------------------------------------ quest log
QUESTS = [
    ("Pratirodh", "Detecting AI voice-clone fraud on Indian phone calls", 18, CREAM),
    ("SheShield Mobile", "Android app: offline reports, hold-to-send SOS", 88, ROSE),
    ("Daily DSA Grind", "Contest-grade problems, every single day", 90, MINT),
    ("Cloud Native", "EKS + GitOps deployment pipeline", 58, VIOLET),
]

LEARNING = ["Speech ML", "Distributed Systems", "Rust", "MLOps", "System Design"]

# ------------------------------------------------------------ game mode
# Visitors vote for the next quest by opening an issue titled "vote: <key>".
# .github/workflows/vote.yml counts it into data/votes.json and redraws.
# (key, label, one-liner, accent)
VOTE_OPTIONS = [
    ("pratirodh", "Ship Pratirodh v1", "First working voice-clone detector", CREAM),
    ("ios", "SheShield on iOS", "Bring the safety app to iPhone", ROSE),
    ("rust", "A Rust side quest", "A fast CLI tool, written in Rust", MINT),
    ("oss", "Open-source arc", "Contribute to the tools I use daily", VIOLET),
]

# ------------------------------------------------------------ end credits
CREDITS = [
    ("DIRECTED BY", "Ankit Basu"),
    ("STARRING", "SheShield  ·  Vyapaar  ·  Hirehearsal"),
    ("ALSO STARRING", "BookMyCampus  ·  TimedInk  ·  PII Redaction"),
    ("SUPPORTING CAST", "GridSense  ·  MindBloom  ·  Pixel-Board  ·  AlgoTrail"),
    ("SIDEKICK", "BYTE, the pixel robot"),
    ("STUNT WORK", "400+ DSA problems, no doubles used"),
    ("FILMED ON LOCATION", "Jalandhar, Punjab"),
    ("SOUNDTRACK", "lo-fi, compiler warnings, 2 a.m. keyboard clicks"),
    ("SPECIAL THANKS", "everyone who starred, forked or voted"),
    ("NO BUGS WERE HARMED", "(several were, actually)"),
]

MARQUEE = ["OPEN TO SWE / AI ROLES", "SHIPPING SAFETY TECH", "AI AGENTS", "FULL-STACK SYSTEMS",
           "400+ DSA", "5x HACKATHON WINS", "BUILT IN JALANDHAR"]

# ------------------------------------------------------------ skill tree
# Branches of (skill, unlocked). Locked nodes are what's being learned now.
SKILL_TREE = [
    ("FRONTEND", CREAM, [("HTML / CSS", True), ("JavaScript", True), ("React", True),
                         ("Next.js", True), ("Three.js", True)]),
    ("BACKEND", ROSE, [("Java", True), ("Node / Express", True), ("FastAPI", True),
                       ("Django", True), ("Distributed Sys", False)]),
    ("AI / ML", MINT, [("Python", True), ("PyTorch", True), ("LangChain", True),
                       ("Speech ML", False), ("MLOps", False)]),
    ("CLOUD", VIOLET, [("Linux", True), ("Docker", True), ("Kubernetes", True),
                       ("AWS", True), ("Rust", False)]),
]
SKILL_ROOT = "DSA + C++"

# ------------------------------------------------------------ boss fight
# The current main quest, drawn as a boss. (phase, label, state) where state
# is done / now / next.
BOSS = dict(name="THE VOICE CLONE", quest="Pratirodh", repo="Pratirodh",
            lore="Fakes a family member's voice and calls asking for money.",
            weak="Weak point: the phone line leaves a fingerprint.",
            moves=[("0", "Foundation & tooling", "done"),
                   ("1", "Data engineering", "now"),
                   ("2", "Telephony simulator", "next"),
                   ("4", "Channel-aware detector", "next"),
                   ("5", "Evidence fusion", "next")])
