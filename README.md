<!--
  ┌──────────────────────────────────────────────────────────────────────┐
  │  STORY MODE. This README is generated; don't hand-edit the .svg files.│
  │                                                                      │
  │    python scripts/fetch_stats.py   # pull live numbers from GitHub   │
  │    python scripts/build.py         # redraw every panel              │
  │                                                                      │
  │  Wording        scripts/profile.py   (chapters, timeline, projects)  │
  │  Story panels   scripts/story.py     (hero, chapters, city, vault)   │
│  Arcade panels  scripts/arcade.py    (companion, ticker, game mode)  │
  │  Other panels   scripts/build.py                                     │
  │  Design system  scripts/design.py    (glass + neo-brutalist blocks)  │
  │  Portrait       scripts/make_sketch.py + make_avatar.py (offline)    │
  │                                                                      │
  │  .github/workflows/stats.yml re-runs fetch + build daily.            │
  │  Bump ?v= below if GitHub's image proxy serves a stale panel.        │
  └──────────────────────────────────────────────────────────────────────┘
-->

<div align="center">

<a name="prologue"></a>
<img src="./banner.svg?v=60" width="100%" alt="Ankit Basu: Software Architect and AI Researcher. A self-drawing line portrait resolves into a photo." />

<img src="./marquee.svg?v=60" width="100%" alt="" />

**Chapter select**&nbsp;&nbsp;
[Origin](#origin) ·
[Arsenal](#arsenal) ·
[Builds](#builds) ·
[Battle&nbsp;Log](#battle-log) ·
[Trophies](#trophies) ·
[Current&nbsp;Quest](#quest) ·
[Epilogue](#epilogue)

<!-- ── CHAPTER I · ORIGIN ───────────────────────────────────────────── -->
<a name="origin"></a>
<img src="./chapter1.svg?v=60" width="100%" alt="Chapter I: Origin story" />
<img src="./timeline.svg?v=60" width="100%" alt="Timeline from joining GitHub in 2023 to the projects in progress now" />

<!-- ── CHAPTER II · ARSENAL ─────────────────────────────────────────── -->
<a name="arsenal"></a>
<img src="./chapter2.svg?v=60" width="100%" alt="Chapter II: The arsenal" />
<img src="./loadout.svg?v=60" width="100%" alt="Skills, credentials and tech arsenal" />

<!-- ── CHAPTER III · BUILDS ─────────────────────────────────────────── -->
<a name="builds"></a>
<img src="./chapter3.svg?v=60" width="100%" alt="Chapter III: The builds" />
<img src="./projects.svg?v=60" width="100%" alt="Featured projects: SheShield, Vyapaar, Hirehearsal, BookMyCampus, TimedInk, PII Redaction" />

**Enter the build →**
[SheShield](https://github.com/Ankit-Basu/SheShield) ·
[Vyapaar](https://github.com/Ankit-Basu/Vyapaar) ·
[Hirehearsal](https://github.com/Ankit-Basu/Hirehearsal) ·
[BookMyCampus](https://github.com/Ankit-Basu/BookMyCampus) ·
[TimedInk](https://github.com/Ankit-Basu/TimedInk) ·
[PII Redaction](https://github.com/Ankit-Basu/PII-Redaction-Tool)

</div>

<details>
<summary><b>Open the codex</b> &nbsp;·&nbsp; every build, its stack, and where to play it</summary>

<br/>

| Build | What it is | Stack | Play it |
|---|---|---|---|
| [**SheShield**](https://github.com/Ankit-Basu/SheShield) | Women's safety platform for LPU: one-tap SOS without sign-in, verified Walk-With-Us escorts, anonymous incident reports, live campus safety map, and an Android app | PHP · MySQL · React Native · Expo SDK 58 · Leaflet | [web](https://sheshield-ab.vercel.app) · [APK](https://github.com/Ankit-Basu/SheShield/releases) |
| [**Vyapaar**](https://github.com/Ankit-Basu/Vyapaar) | Agent-commerce layer for a Razorpay merchant: an outside AI agent proves human consent and clears nine guardrails before it pays; the merchant's growth agent can't fake a discount | FastAPI · Next.js · Razorpay (test mode) · JWT mandates | [control room](https://vyapaar-web.vercel.app/dashboard) |
| [**Hirehearsal**](https://github.com/Ankit-Basu/Hirehearsal) | AI mock-interview platform. Ora runs technical, project and HR rounds out loud, adapts difficulty and hands back a scorecard | Next.js 16 · React 19 · Java · Docker | — |
| [**BookMyCampus**](https://github.com/Ankit-Basu/BookMyCampus) | One booking system for every room, lab and instrument on campus, with approval chains, QR check-in, no-show release and a make-up class finder | Django · PostgreSQL · React | [demo](https://book-my-campus-ab.vercel.app) |
| [**TimedInk**](https://github.com/Ankit-Basu/TimedInk) | Fault-tolerant, rate-paced email scheduler that survives restarts and a wiped Redis; 73 hermetic tests | Node · BullMQ · Redis · MySQL | [app](https://timed-ink.vercel.app) |
| [**PII Redaction Engine**](https://github.com/Ankit-Basu/PII-Redaction-Tool) | Detects 10 PII types in .docx with hybrid regex + NER and swaps in realistic fakes, keeping formatting intact; benchmarked on a 1,006-paragraph prospectus | Python · spaCy · python-docx | — |
| [**Pratirodh**](https://github.com/Ankit-Basu/Pratirodh) | *In progress.* Channel-conditioned detection of AI voice-clone fraud on Indian phone calls | Python · FastAPI · Next.js 15 · MLflow | — |
| [**GridSense**](https://github.com/Ankit-Basu/GridSense) | Cyber-physical smart-grid digital twin with 3D asset inspection and ML forecasting | React Three Fiber · Flask · scikit-learn | — |
| [**MindBloom**](https://github.com/Ankit-Basu/MindBloom) | AI emotional-wellness platform connecting children, parents and counsellors | Laravel · Gemini | — |
| [**Pixel-Board**](https://github.com/Ankit-Basu/Pixel-Board) | 8-bit real-time collaborative whiteboard with an AI vision maths solver and an arcade | MERN · Socket.IO · WebRTC · Groq | — |
| [**CampusWhisper**](https://github.com/Ankit-Basu/CampusWhisper) | Anonymous campus confessions with live chat, video calls and a confession map | React 19 · Express 5 · Socket.IO · Firebase | — |
| [**AlgoTrail**](https://github.com/Ankit-Basu/AlgoTrail) | Algorithm playground: pathfinding, maze generation and puzzles with an AI explainer | JavaScript · CSS | — |
| [**Adobe Hackathon**](https://github.com/Ankit-Basu/Adobe_hackathon) | Offline PDF outline extractor (title + H1–H3) in under 10 s on CPU | Python · PyMuPDF · Docker | — |

</details>

<div align="center">

<!-- ── CHAPTER IV · BATTLE LOG: rebuilt daily from the GitHub API ───── -->
<a name="battle-log"></a>
<img src="./chapter4.svg?v=60" width="100%" alt="Chapter IV: Battle log" />
<img src="./stats.svg?v=60" width="100%" alt="Live GitHub activity and reach" />
<img src="./city.svg?v=60" width="100%" alt="The last 52 weeks of contributions drawn as an isometric city, one tower per day" />
<img src="./companion.svg?v=60" width="49%" alt="BYTE, a pixel robot companion whose mood follows my commit streak" /> <img src="./ticker.svg?v=60" width="49%" alt="$ANKIT: weekly contributions drawn as trading candles" />

<!-- Contribution snake (generated by .github/workflows/snake.yml) -->
<picture>
  <source media="(prefers-color-scheme: dark)"
          srcset="https://raw.githubusercontent.com/Ankit-Basu/Ankit-Basu/output/github-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)"
          srcset="https://raw.githubusercontent.com/Ankit-Basu/Ankit-Basu/output/github-snake.svg" />
  <img width="100%" alt="Contribution snake eating my commit graph"
       src="https://raw.githubusercontent.com/Ankit-Basu/Ankit-Basu/output/github-snake.svg" />
</picture>

<!-- ── CHAPTER V · TROPHIES ─────────────────────────────────────────── -->
<a name="trophies"></a>
<img src="./chapter5.svg?v=60" width="100%" alt="Chapter V: Trophy hall" />
<img src="./trophies.svg?v=60" width="100%" alt="Achievements and milestones" />

<!-- ── CHAPTER VI · CURRENT QUEST ───────────────────────────────────── -->
<a name="quest"></a>
<img src="./chapter6.svg?v=60" width="100%" alt="Chapter VI: Current quest" />
<img src="./questlog.svg?v=60" width="100%" alt="What I'm building right now" />

<!-- GAME MODE: each link opens a prefilled issue; .github/workflows/vote.yml counts it -->
<img src="./votes.svg?v=60" width="100%" alt="Game Mode: vote for my next quest" />

**Cast your vote →**
[**Pratirodh v1**](https://github.com/Ankit-Basu/Ankit-Basu/issues/new?body=Just+press+Submit.+A+bot+counts+your+vote+and+closes+this+issue.&title=vote%3A+pratirodh) ·
[**SheShield on iOS**](https://github.com/Ankit-Basu/Ankit-Basu/issues/new?body=Just+press+Submit.+A+bot+counts+your+vote+and+closes+this+issue.&title=vote%3A+ios) ·
[**Rust side quest**](https://github.com/Ankit-Basu/Ankit-Basu/issues/new?body=Just+press+Submit.+A+bot+counts+your+vote+and+closes+this+issue.&title=vote%3A+rust) ·
[**Open-source arc**](https://github.com/Ankit-Basu/Ankit-Basu/issues/new?body=Just+press+Submit.+A+bot+counts+your+vote+and+closes+this+issue.&title=vote%3A+oss)

</div>

<details>
<summary><b>Behind the scenes</b> &nbsp;·&nbsp; how this profile is built</summary>

<br/>

Every panel above is an SVG generated by Python in [`scripts/`](scripts/). No third-party stats services, so nothing can rate-limit it into a broken image. A GitHub Action refreshes the numbers every day.

- **The portrait** is traced from my photo with OpenCV: GrabCut separates me from the background, Canny finds the edges, and each edge becomes a Bézier path that draws itself with `stroke-dashoffset` before the photo resolves through a mask.
- **The city** is my last 52 weeks of contributions in isometric 3D: one tower per day, one street per week.
- **The look** mixes four styles on one flat GitHub-dark canvas: synthwave for the hero (striped sun, scrolling grid floor), frosted glass for content, neo-brutalism for the story layer (chapter stamps, stickers, ribbons, vote cards), and JRPG dialogue boxes for the narrator.
- **Smooth by design:** these panels load as `<img>`, so the browser repaints the whole image on every animation frame. There are no blur or drop-shadow filters anywhere; glows and shadows are gradients and offset shapes, and the motion is plain transforms and opacity.
- **BYTE** reads my current streak every day: 3+ days and it's hyped, 1-2 it's on it, 0 and it falls asleep.
- **Game Mode** is a real vote: each link opens an issue, and [a workflow](.github/workflows/vote.yml) validates it, counts one vote per player, redraws the panel and closes the issue.
- **No blank panels:** every animation's resting state is the finished frame, so a renderer that never plays it still shows a complete panel. `scripts/verify.py` checks this before each commit.

</details>

<div align="center">

<!-- ── EPILOGUE ─────────────────────────────────────────────────────── -->
<a name="epilogue"></a>
<img src="./marquee2.svg?v=60" width="100%" alt="" />
<img src="./credits.svg?v=60" width="100%" alt="The End: end credits starring my projects" />
<img src="./footer.svg?v=60" width="100%" alt="Epilogue: connect with Ankit Basu" />

<!-- Links live out here, not inside the SVG: GitHub renders these panels
     through <img>, and anchors inside an <img>-loaded SVG are never clickable. -->
**Join the party →**
[**GitHub**](https://github.com/Ankit-Basu) ·
[**LinkedIn**](https://www.linkedin.com/in/ankit-basu-4a6774297/) ·
[**Portfolio**](https://ankitbasu.vercel.app/) ·
[**Instagram**](https://instagram.com/_ank1t._) ·
[**Email**](mailto:ankitbasu935@gmail.com)

<br/>

<img src="https://komarev.com/ghpvc/?username=Ankit-Basu&style=for-the-badge&color=fbe2a7&label=PLAYERS+WHO+VISITED"
     alt="Profile views" />

</div>
