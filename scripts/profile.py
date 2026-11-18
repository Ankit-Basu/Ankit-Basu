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

QUOTE = "Turning ambitious engineering ideas into scalable, production reality."
MOTTO = "INNOVATE  •  SCALE  •  ARCHITECT  •  SHIP"

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
    ("CampusWhisper", "Anonymous campus confessions", "CampusWhisper"),
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

# Chapter cards between sections: (numeral, kicker, title, subtitle, accent)
CHAPTERS = [
    ("I", "ORIGIN STORY", "How the player got here", "Three years, thirty-odd repos, one habit: ship it", CREAM),
    ("II", "THE ARSENAL", "Skills, credentials & gear", "Everything equipped for the next boss fight", ROSE),
    ("III", "THE BUILDS", "Systems shipped to production", "Pulled straight from the repos that hold them", MINT),
    ("IV", "BATTLE LOG", "Live telemetry from GitHub", "Rebuilt every day by GitHub Actions", VIOLET),
    ("V", "TROPHY HALL", "Achievements unlocked", "Podiums, ratings and the grind behind them", CREAM),
    ("VI", "CURRENT QUEST", "What's on the bench right now", "Active missions, live progress", ROSE),
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
