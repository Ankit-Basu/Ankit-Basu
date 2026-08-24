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
# rarity, icon, title, subtitle, body lines, tech chips, repo slug
PROJECTS = [
    dict(rarity="LEGENDARY", icon="drone", title="SUDARSHAN-X",
         sub="Autonomous Drone Defense Platform",
         body=["YOLOv8 aerial threat detection with RF spectrum analysis and",
               "Doppler tracking, driving a Reynolds-Boids 3D swarm interceptor."],
         tech=["YOLOv8", "React Three Fiber", "Node.js", "Python"], repo=None),
    dict(rarity="EPIC", icon="shield", title="SheShield",
         sub="Campus & Personal Safety Network",
         body=["ML-powered live incident heatmaps that cut response time 30%,",
               "automated escort dispatch and a 24/7 AI safety chatbot."],
         tech=["PHP", "React", "MySQL", "Tailwind"], repo="SheShield"),
    dict(rarity="RARE", icon="leaf", title="KrishiVaani",
         sub="Multilingual Smart Farming Assistant",
         body=["99.48% crop-disease diagnosis on MobileNetV2, Groq LLM",
               "reasoning, live mandi prices and full voice I/O."],
         tech=["PyTorch", "Flask", "Groq LLM"], repo=None),
    dict(rarity="RARE", icon="maze", title="AlgoTrail",
         sub="Algorithm & Maze Playground",
         body=["Pathfinding visualiser with real-time maze generation,",
               "step metrics and AI-generated step explanations."],
         tech=["JavaScript", "CSS3", "AI Assist"], repo="AlgoTrail"),
    dict(rarity="UNCOMMON", icon="bolt", title="GridSense",
         sub="Smart Energy & Power-Grid Dashboard",
         body=["IoT telemetry ingestion with anomaly detection and",
               "live consumption forecasting across sensor fleets."],
         tech=["React", "Node.js", "IoT"], repo=None),
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
    ("SUDARSHAN-X v2.0", "Multi-target Kalman fusion tracker", 72, CREAM),
    ("Swarm Visualiser", "Shipping the 3D interception view to prod", 84, ROSE),
    ("Daily DSA Grind", "Contest-grade problems, every single day", 90, MINT),
    ("Cloud Native", "EKS + GitOps deployment pipeline", 58, VIOLET),
]

LEARNING = ["Distributed Systems", "Rust", "MLOps", "System Design"]
