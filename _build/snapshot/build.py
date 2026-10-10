#!/usr/bin/env python3
"""
Generates the portfolio HTML pages.
Underscore folders are ignored by GitHub Pages, so this never ships.
Run:  python3 _build/build.py
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
EMAIL = "aranytotharon@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/aron-arany-toth/"

NAV = [
    ("link",  "index.html", "Home"),
    ("group", "Experience", [
        ("airhint.html",  "AirHint"),
        ("publicis.html", "Publicis"),
        ("synetech.html", "Synetech"),
    ]),
    ("group", "Research", [
        ("research.html",         "AI and product choice"),
        ("research-booking.html", "Website nudges"),
    ]),
    ("link",  "content.html", "Content"),
    ("link",  "skills.html",  "Skills and tools"),
    ("link",  "about.html",   "About"),
]

# flat order, for the "More" links at the foot of each page
FLAT = []
for row in NAV:
    if row[0] == "link":
        FLAT.append((row[1], row[2]))
    else:
        FLAT.extend(row[2])
LABEL = dict(FLAT)

# The "Want to browse more?" buttons name the area, not the employer:
# nobody outside the industry knows what AirHint or Synetech is.
ONWARD_LABEL = dict(LABEL, **{
    "airhint.html":          "Growth marketing (AirHint)",
    "publicis.html":         "Instagram rebranding (Publicis)",
    "synetech.html":         "Content strategy (Synetech)",
    "research.html":         "AI and product choice (research)",
    "research-booking.html": "Website nudges (research)",
})


def sidebar(current):
    out = []
    for row in NAV:
        if row[0] == "link":
            _, href, label = row
            cls = ' class="active"' if href == current else ""
            out.append(f'    <a href="{href}"{cls}>{label}</a>')
        else:
            _, glabel, items = row
            out.append(f'    <p class="nav-group">{glabel}</p>')
            for href, label in items:
                cls = ' class="navsub active"' if href == current else ' class="navsub"'
                out.append(f'    <a href="{href}"{cls}>{label}</a>')
    links = "\n".join(out)
    return f"""<aside class="sidebar">
  <div class="side-top">
    <img class="signature" src="assets/signature.png" alt="">
    <div class="side-name">
      <strong>Aron Arany-Toth</strong>
      <span>Digital marketing and growth</span>
    </div>
  </div>

  <nav class="nav" aria-label="Pages">
{links}
  </nav>

  <button class="nav-connect" type="button" data-connect>Connect</button>

  <div class="side-bottom">
    <p>English · Español · Magyar</p>
    <p>Madrid</p>
  </div>
</aside>"""


def onward(current):
    order = [h for h, _ in FLAT]
    i = order.index(current) if current in order else -1
    rotated = order[i + 1:] + order[:i] if i >= 0 else order
    picked = []
    for h in rotated:
        if h == "index.html" or h == current:
            continue
        picked.append((h, ONWARD_LABEL[h]))
        if len(picked) == 3:
            break
    links = "\n".join(f'    <a href="{h}">{l}</a>' for h, l in picked)
    return f"""<nav class="onward" aria-label="More pages">
  <p class="onward-label">Want to browse more?</p>
  <div class="onward-links">
{links}
  </div>
</nav>"""


FOOT = """<footer class="pagefoot">
  <button class="foot-connect" type="button" data-connect>Connect</button>
</footer>"""

DIALOG = f"""<dialog id="connect-panel" class="connect">
  <div class="connect-inner">
    <button class="connect-close" type="button" data-connect-close aria-label="Close">&times;</button>
    <h2 class="connect-title">Connect</h2>

    <div class="c-block">
      <p class="c-label">Email</p>
      <p class="c-val">{EMAIL}</p>
      <div class="c-actions">
        <a class="btn primary" href="mailto:{EMAIL}">Compose an email</a>
        <button class="btn" type="button" data-copy="{EMAIL}">Copy address</button>
      </div>
    </div>

    <div class="c-block">
      <p class="c-label">Stay in touch</p>
      <p class="c-note">I am most responsive on LinkedIn.</p>
      <div class="c-actions">
        <a class="btn" href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>
      </div>
    </div>

    <div class="c-block">
      <p class="c-label">CV</p>
      <div class="c-actions">
        <a class="btn" href="assets/cv.pdf">Download as PDF</a>
      </div>
    </div>
  </div>
</dialog>"""


def page(filename, title, description, body):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

{sidebar(filename)}

<main id="main">
{body}

{onward(filename)}
{FOOT}
</main>

{DIALOG}
<script src="script.js"></script>
</body>
</html>
"""
    (ROOT / filename).write_text(html, encoding="utf-8")
    print("wrote", filename)



# ----------------------------------------------------------------- CHART HELPERS
def _hbar(rows, vmin, vmax, note):
    """Horizontal bars, single series. rows = [(label, value)]"""
    LW, BW, RH, GAP, PAD = 268, 322, 30, 12, 6
    H = PAD * 2 + len(rows) * RH + (len(rows) - 1) * GAP + 46
    out = [f'<svg class="chart" viewBox="0 0 640 {H}" role="img" xmlns="http://www.w3.org/2000/svg">']
    # baseline + ticks
    for t in range(vmin, vmax + 1):
        x = LW + (t - vmin) / (vmax - vmin) * BW
        out.append(f'<line x1="{x:.1f}" y1="{PAD}" x2="{x:.1f}" y2="{H-42}" class="c-grid"/>')
        out.append(f'<text x="{x:.1f}" y="{H-26}" class="c-tick" text-anchor="middle">{t}</text>')
    y = PAD
    for label, v in rows:
        w = max(2.0, (v - vmin) / (vmax - vmin) * BW)
        x0, x1, r = LW, LW + w, 4
        r = min(r, w / 2)
        out.append(
            f'<path class="c-bar" d="M{x0},{y} L{x1-r:.1f},{y} Q{x1:.1f},{y} {x1:.1f},{y+r} '
            f'L{x1:.1f},{y+RH-r} Q{x1:.1f},{y+RH} {x1-r:.1f},{y+RH} L{x0},{y+RH} Z"><title>{label}: {v}</title></path>')
        out.append(f'<text x="{LW-12}" y="{y+RH/2+4.5:.1f}" class="c-lab" text-anchor="end">{label}</text>')
        out.append(f'<text x="{x1+9:.1f}" y="{y+RH/2+4.5:.1f}" class="c-val">{v:.2f}</text>')
        y += RH + GAP
    out.append(f'<text x="{LW}" y="{H-6}" class="c-note">{note}</text>')
    out.append('</svg>')
    return "\n".join(out)


def _vbar(rows, vmin, vmax, xnote, ynote):
    """Vertical bars, single series. rows = [(xlabel, value)]"""
    L, R, T, B, W = 46, 10, 26, 46, 640
    PH = 210
    H = T + PH + B
    n = len(rows)
    slot = (W - L - R) / n
    bw = min(46.0, slot * 0.54)
    out = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" xmlns="http://www.w3.org/2000/svg">']
    for t in range(vmin, vmax + 1):
        yy = T + PH - (t - vmin) / (vmax - vmin) * PH
        out.append(f'<line x1="{L}" y1="{yy:.1f}" x2="{W-R}" y2="{yy:.1f}" class="c-grid"/>')
        out.append(f'<text x="{L-10}" y="{yy+4:.1f}" class="c-tick" text-anchor="end">{t}</text>')
    for i, (xl, v) in enumerate(rows):
        h = max(2.0, (v - vmin) / (vmax - vmin) * PH)
        x = L + slot * i + (slot - bw) / 2
        yb, yt, r = T + PH, T + PH - h, min(4.0, bw / 2)
        out.append(
            f'<path class="c-bar" d="M{x:.1f},{yb} L{x:.1f},{yt+r:.1f} Q{x:.1f},{yt:.1f} {x+r:.1f},{yt:.1f} '
            f'L{x+bw-r:.1f},{yt:.1f} Q{x+bw:.1f},{yt:.1f} {x+bw:.1f},{yt+r:.1f} L{x+bw:.1f},{yb} Z">'
            f'<title>{xl}: {v}</title></path>')
        out.append(f'<text x="{x+bw/2:.1f}" y="{yt-9:.1f}" class="c-val" text-anchor="middle">{v:.2f}</text>')
        out.append(f'<text x="{x+bw/2:.1f}" y="{yb+20:.1f}" class="c-tick" text-anchor="middle">{xl}</text>')
    out.append(f'<text x="{L}" y="{H-8}" class="c-note">{xnote}</text>')
    out.append(f'<text x="14" y="{T+PH/2:.1f}" class="c-note" text-anchor="middle" transform="rotate(-90 14 {T+PH/2:.1f})">{ynote}</text>')
    out.append('</svg>')
    return "\n".join(out)


def figure(svg, caption):
    return f'<figure class="chart-fig">{svg}<figcaption>{caption}</figcaption></figure>'


# ----------------------------------------------------------------- HOME
home = """
<section class="hero">
  <img class="hero-photo" src="assets/aron.jpg" alt="Aron Arany-Toth">
  <div class="hero-text">
    <div class="greet">
      <div class="greet-langs"><span>Hi,</span><span>Hola,</span><span>Szia,</span></div>
      <h1 class="greet-name">I'm Aron.</h1>
    </div>
    <p class="hero-head">Curious human first.<br>Growth and digital marketer second.</p>
  </div>
</section>


<section class="section curious">
  <div class="shelf">
    <div class="shelf-row">
      <svg class="plant" viewBox="0 0 82 150" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">
      <path d="M41 104 C30 84 24 62 28 40 C38 54 44 76 41 104Z"/>
      <path d="M41 104 C52 86 60 66 58 44 C47 58 39 80 41 104Z"/>
      <path d="M41 106 C28 94 16 82 13 64 C27 72 38 88 41 106Z"/>
      <path d="M41 106 C55 95 67 84 70 66 C56 74 44 89 41 106Z"/>
      <path d="M41 108 C40 92 41 70 44 52" class="thin"/>
      <path d="M14 104 L68 104 L61 144 L21 144 Z"/>
      <path d="M14 113 L68 113" class="thin"/>
      <path d="M22 122 l5 -6 5 6 5 -6 5 6 5 -6 5 6 5 -6 5 6" class="thin"/>
    </svg>
      <ul class="standing">
        <li class="book sp1" style="height:138px;animation-delay:0ms"><span>SEO</span></li>
        <li class="book sp3" style="height:124px;animation-delay:60ms"><span>CRM</span></li>
        <li class="book sp4" style="height:146px;animation-delay:120ms"><span>CRO</span></li>
        <li class="book sp2" style="height:118px;animation-delay:180ms"><span>Maths</span></li>
        <li class="book sp5" style="height:152px;animation-delay:240ms"><span>Social media</span></li>
      </ul>
      <ul class="stack">
        <li class="flat sp4" style="width:138px;animation-delay:300ms">Statistics</li>
        <li class="flat sp1" style="width:172px;animation-delay:360ms">Claude automation</li>
        <li class="flat sp5" style="width:158px;animation-delay:420ms">Website building</li>
        <li class="flat sp2" style="width:180px;animation-delay:480ms">Content marketing</li>
        <li class="flat sp1" style="width:172px;animation-delay:540ms">Media planning</li>
        <li class="flat sp3" style="width:196px;animation-delay:600ms">Growth marketing</li>
      </ul>
      <svg class="plant" viewBox="0 0 74 150" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">
      <path d="M29 106 L29 50 a8 8 0 0 1 16 0 L45 106Z"/>
      <path d="M29 84 L20 84 a6 6 0 0 1 -6 -6 L14 64 a5 5 0 0 1 10 0 L24 74 a2 2 0 0 0 2 2 L29 76Z"/>
      <path d="M45 74 L54 74 a6 6 0 0 0 6 -6 L60 52 a5 5 0 0 0 -10 0 L50 64 a2 2 0 0 1 -2 2 L45 66Z"/>
      <circle cx="37" cy="62" r="1.3" class="fill"/><circle cx="37" cy="76" r="1.3" class="fill"/>
      <circle cx="37" cy="90" r="1.3" class="fill"/><circle cx="18" cy="72" r="1.2" class="fill"/>
      <circle cx="56" cy="60" r="1.2" class="fill"/>
      <path d="M11 106 L63 106 L56 144 L18 144 Z"/>
      <path d="M11 115 L63 115" class="thin"/>
      <path d="M19 124 q5 -7 10 0 q5 -7 10 0 q5 -7 10 0" class="thin"/>
    </svg>
    </div>
    <div class="shelf-board"></div>
  </div>

  <h2 class="sec-title">About</h2>
  <p>I am interested in a lot of things. Three years at Publicis showed me how a campaign gets planned, bought and measured across five markets, and then how a strategy gets built out of the data sitting underneath it. Synetech taught me what B2B content has to do differently. AirHint is where I got to own a funnel end to end, and where I had to learn enough about statistics and experiments to trust my own results. Alongside that I taught maths on Saturdays for five years, and I build websites because I want to understand how one goes up from nothing, which is also why I keep starting projects of my own.</p>
  <p>The thing holding all of it together is curiosity. I want to understand how things work, the whole structure of them, companies, tools and products, all the way down. Then I want to use that to build better products for the people who use them, through marketing.</p>

  <h2 class="sec-title tl-title">Work experience</h2>
  <ol class="timeline">
    <li>
      <span class="tl-date">May 2026 — now</span>
      <span class="tl-role"><a href="airhint.html">Growth Marketing Manager</a></span>
      <span class="tl-org">AirHint · Madrid, remote</span>
    </li>
    <li>
      <span class="tl-date">Apr — Jul 2026</span>
      <span class="tl-role"><a href="synetech.html">Social Media &amp; Content Creator</a></span>
      <span class="tl-org">Synetech · Madrid</span>
    </li>
    <li>
      <span class="tl-date">Sep 2024 — now</span>
      <span class="tl-role">Social Media Content Strategist</span>
      <span class="tl-org">Influnter · Budapest, part time</span>
    </li>
    <li>
      <span class="tl-date">Aug 2024 — Aug 2025</span>
      <span class="tl-role"><a href="publicis.html">Junior Digital Strategist</a></span>
      <span class="tl-org">Publicis Groupe Hungary · Budapest</span>
    </li>
    <li>
      <span class="tl-date">Sep 2022 — Aug 2024</span>
      <span class="tl-role">Junior Integrated Media Planner</span>
      <span class="tl-org">Publicis Groupe Hungary · Budapest</span>
    </li>
  </ol>
</section>

<section class="section">
  <h2 class="sec-title">Work</h2>
  <div class="cards">

    <article class="card">
      <a class="thumb wide" href="airhint.html">
        <img src="assets/airhint/deals-page.jpg" alt="The AirHint deals page">
      </a>
      <div class="card-body">
        <h3><a href="airhint.html">Growth at AirHint</a></h3>
        <p class="card-meta">Growth Marketing Manager · May 2026 to now</p>
        <p>Paid search in three languages, a rebuilt deals page, experiments in GrowthBook, and the CRM build, for a product that only earns when a visit ends in a booking click.</p>
        <a href="airhint.html">Read it</a>
      </div>
    </article>

    <article class="card">
      <a class="thumb wide" href="publicis.html">
        <img src="assets/publicis/new-visuals.jpg" alt="Publicis Instagram redesign">
      </a>
      <div class="card-body">
        <h3><a href="publicis.html">Relaunching Publicis Groupe Hungary on Instagram</a></h3>
        <p class="card-meta">Junior Digital Strategist · August 2024 to August 2025</p>
        <p>A content strategy built from a coded database of the competitive set. Views per post up 57%, shares up 388%, and the highest engagement rate of the five agency accounts tracked.</p>
        <a href="publicis.html">Read it</a>
      </div>
    </article>

    <article class="card">
      <a class="thumb wide" href="research.html">
        <img src="assets/thesis-chart.jpg" alt="Thesis result chart">
      </a>
      <div class="card-body">
        <h3><a href="research.html">Does an AI recommendation change what you buy?</a></h3>
        <p class="card-meta">MSc thesis · UC3M · 2026</p>
        <p>A controlled experiment with 192 participants. The recommendation moved product choice from 30% to 47%, and changed nothing about how fast or how confidently people decided.</p>
        <a href="research.html">Read it</a>
      </div>
    </article>

    <article class="card">
      <a class="thumb wide" href="synetech.html">
        <img src="assets/synetech/linkedin-formats.jpg" alt="LinkedIn content and format benchmark">
      </a>
      <div class="card-body">
        <h3><a href="synetech.html">LinkedIn content strategy for Synetech</a></h3>
        <p class="card-meta">Social Media &amp; Content Creator · April to July 2026</p>
        <p>A competitor benchmark of websites and LinkedIn output for a B2B edtech brand, written and delivered in Spanish, with the format recommendations that came out of it.</p>
        <a href="synetech.html">Read it</a>
      </div>
    </article>

  </div>
</section>

<section class="section">
  <h2 class="sec-title">Things I built</h2>
  <p class="sec-intro">I do not write code, I build these with AI tools, and everything here is live and run by me.</p>
  <div class="cards">
    <article class="card">
      <a class="thumb wide" href="https://rokonszavak.hu" target="_blank" rel="noopener">
        <img src="assets/work/rokonszavak-game.jpg" alt="A solved Rokonszavak puzzle showing three colour-coded groups of four Hungarian words">
      </a>
      <div class="card-body">
        <h3>Rokonszavak</h3>
        <p>A daily Hungarian word grouping puzzle, in the shape of the New York Times Connections game. There was nothing like it in Hungarian. I wrote the business case, built it, and it publishes a new puzzle every day.</p>
        <a href="https://rokonszavak.hu" target="_blank" rel="noopener">rokonszavak.hu</a>
      </div>
    </article>
    <article class="card">
      <a class="thumb wide" href="https://theataron.github.io/genztrivia/" target="_blank" rel="noopener">
        <img src="assets/work/genz-trivia.jpg" alt="A Gen Z Trivia question card: food and drinks, 15 points, medium">
      </a>
      <div class="card-body">
        <h3>Gen Z Trivia</h3>
        <p>A trivia game I made so my friend group had something to argue about. Rounds, categories, points, and questions on the internet culture we grew up with.</p>
        <a href="https://theataron.github.io/genztrivia/" target="_blank" rel="noopener">Play it</a>
      </div>
    </article>
  </div>
  <p class="after-cards">This site is one of them too. So is The Lake, which I built for my partner and me while we were living in different countries: a countdown, shared lists, a rating for each day, a question of the day, song and film lists, a drawing board and a game of noughts and crosses, running on Firebase.</p>

  <div class="cv-cta">
    <p>Want a short summary of all of my experience?</p>
    <a class="btn primary" href="assets/cv.pdf">Download my CV</a>
  </div>
</section>
"""

# ----------------------------------------------------------------- AIRHINT
airhint = """
<section class="section">
  <p class="eyebrow">Case study</p>
  <h1 class="page-title">Growth at <a href="https://www.airhint.com" target="_blank" rel="noopener">AirHint</a></h1>
  <p class="case-meta">Growth Marketing Manager · May 2026 to now · Madrid, remote</p>

  <p class="lead">AirHint predicts whether a flight price is going to rise or fall and tells you when to book. It is an early stage product with an engineering founder and no marketing function before I joined, so paid search, SEO, analytics, conversion and the CRM are all mine.</p>

  <h2 class="sub">How the money works</h2>
  <p>Revenue comes from Skyscanner affiliate links and display ads, which means a visit only earns anything if it ends in a booking click and traffic volume on its own is not a useful number. That changes which searches are worth bidding on and which pages are worth fixing, and it is the first job where I have had to work backwards from what a user is actually worth rather than against a campaign KPI someone else had already set.</p>

  <h2 class="sub">Paid search</h2>
  <p>I plan and run the Google Ads search campaigns and manage budget against CPA and CPC, in three languages: English, Spanish and Portuguese. This is the only paid platform I have bought on myself. At Publicis I planned and monitored budgets on Meta and TikTok, which is a different job.</p>

  <h2 class="sub">SEO</h2>
  <p>Organic search brings in most of the site's traffic, so a good share of my week goes on reading what already works and finding what is missing. In practice that means going through page content to see which queries a page could realistically answer, looking for keywords with enough volume to justify building a page around them, and then checking in Search Console which of those pages actually earn clicks once they rank. I worked alongside the SEO team at Publicis before this, which is where I picked up most of the method, and for the terms we target AirHint currently comes out as the first result.</p>

  <h2 class="sub">Traffic analysis</h2>
  <p>I am in Google Analytics and Search Console most days, mostly to answer one question: which traffic is worth having. Since the site only earns on a booking click, a channel that sends plenty of sessions and no clicks is a cost rather than a win, so the work is breaking traffic down by source, country, device and landing page and seeing which combinations end in someone actually clicking through to the airline.</p>
  <p>The most useful thing to come out of that was an analysis of the site's AI referral traffic, which had grown into a real channel while nobody was looking at it properly. Calling it AI traffic turns out to overstate the picture, because 99.6% of it is ChatGPT and every other assistant put together sent fewer than a hundred sessions in a month, so every decision about this channel is really a decision about one assistant. It also behaves unlike anything else on the site, clicking through to book at roughly four times the site average, and the countries it arrives from barely overlap with the countries our Google traffic comes from, which makes it a second market rather than a transfer of the first.</p>
  <p>To understand why we get cited at all I went through each major competitor's robots.txt by hand, and the pattern was that Skyscanner, Kayak and Momondo block their flight pages to generic crawlers using rules written years ago against scrapers, which happen to exclude OpenAI's search crawler as well. Kayak is the clearest case, since they allow ChatGPT's live-fetch agent into their flight pages but never named the indexing crawler, so their pages cannot be retrieval candidates in the first place while ours can. Expedia is the exception and has opted in deliberately, which makes this a window rather than a moat, because any competitor could join by editing one line.</p>
  <p>The problem the analysis surfaced is that almost all of this traffic lands on a deal page, which is a static price table, and almost none of it ever reaches the prediction, which is the thing the product is actually for. That finding is where the next piece of work came from.</p>

  <h2 class="sub">Conversion and A/B testing</h2>
  <p>Rebuilding the deals page was the largest piece of it. The old flow collected one filter per page load, whereas the new one puts them all on a single page with results already on screen before anyone touches a control, and two filter rows, when and where, both defaulting to the most open option.</p>
  <figure class="fig">
    <img src="assets/airhint/deals-page.jpg" alt="The AirHint deals page: cheapest one-way flights from Madrid, with filter chips for trip type, direct only, sort order and month, over a grid of destination cards">
  </figure>
  <p>What makes it ours rather than a worse Skyscanner is that every price carries a reference point, because €41 on its own means nothing while €41, 38% below what that route normally costs in November, means something, and a price comparison site cannot write that second line since it does not hold the route history. So the default sort is by that gap rather than by lowest price, given that sorting by cheapest always surfaces the same short haul routes. One constraint shaped the whole thing: browsing has to cost nothing to compute, since a month of dates across sixty destinations would be 1,800 model runs for a single page load, so browsing only ever reads stored prices and the model runs once, after someone has picked a route and pressed see prediction.</p>
  <p>It is live, and the next step is moving it into the header so that it also picks up traffic from the search pages. The moment I care about most is straight after someone sets a price alert, because they have just given us their home airport and then been asked to wait, which is the emptiest point on the site, and a list of other cheap departures from that same airport belongs exactly there.</p>
  <p>Smaller changes get tested in GrowthBook: how a button is highlighted, how a panel is structured, where a call to action sits and how it is worded, and the interface around the point where someone decides.</p>
  <figure class="fig">
    <img src="assets/airhint/growthbook.jpg" alt="A GrowthBook experiment results screen with the test name and metric names hidden, showing a goal metric up and a guardrail metric down">
  </figure>
  <p>One of them, with the test and the metrics covered. What I have taken from running these is mostly about choosing the metric before you launch rather than after, because a variant can win on the number you set while moving the number you actually care about in the opposite direction, and you only find that out if the guardrail was picked up front.</p>

  <h2 class="sub">CRM and email</h2>
  <p>I am building the CRM and the email lifecycle in Brevo from scratch, so that one-off visitors become captured and nurtured leads rather than a single affiliate click that never comes back. This is in progress and I am not claiming results from it yet.</p>
</section>
"""

# ----------------------------------------------------------------- PUBLICIS
publicis = """
<section class="section">
  <p class="eyebrow">Case study</p>
  <h1 class="page-title">Relaunching Publicis Groupe Hungary on Instagram</h1>
  <p class="case-meta">Publicis Groupe Hungary · Junior Digital Strategist · August 2024 to August 2025</p>

  <p class="lead">The agency's own Instagram account was posting about three times a month. There was no video at all in Q4 2024, no consistent design, and the content leaned on a few repeated formats.</p>

  <h2 class="sub">Where the strategy came from</h2>
  <p>Before writing anything I built a database in Excel of every post from our four closest competitors, coded by content pillar, content type, format and posting date, and recorded the performance of each one against likes, comments, saves and shares. That gave me a view of which formats and which topics their audiences actually responded to, rather than an impression picked up from scrolling their feeds.</p>

  <h2 class="sub">Two pillars</h2>
  <p>What We Do covers the agency's work: creative output, case studies, awards, expert insight, interviews, industry data and recent campaigns. Who We Are covers the inside of the agency: the team, the culture, trends and memes, office pets, DEI. Each pillar got a fixed set of recurring formats, so there was always a next post to make rather than a blank page every week.</p>
  <figure class="fig">
    <img src="assets/publicis/pillars.jpg" alt="Content pillar framework: What We Do and Who We Are, with the content types under each">
  </figure>

  <h2 class="sub">What changed</h2>
  <p>Posting went from three a month to eight, with scheduled video every month, new content types, a unified design across posts, highlights, stickers and GIFs, and the newer Instagram features the account had not been using.</p>
  <figure class="fig">
    <img src="assets/publicis/before-after.jpg" alt="Before and after the strategy, side by side">
  </figure>
  <figure class="fig">
    <img src="assets/publicis/new-visuals.jpg" alt="New designed covers, story stickers and the new profile look">
  </figure>

  <h2 class="sub">New content types</h2>
  <p>The Last 5 is a series where an employee walks through the last five posts they saved on Instagram. Work Your World profiles people who moved abroad within the group. Expert Insights turns internal data and research into carousels. Publicis Pets is what it sounds like, and it outperformed most of the serious content.</p>
  <div class="fig-row">
    <figure class="fig"><img src="assets/publicis/content-types-1.jpg" alt="Publicis Pets and Expert Insights formats"></figure>
    <figure class="fig"><img src="assets/publicis/content-types-2.jpg" alt="Latest Campaigns and The Last 5 formats"></figure>
    <figure class="fig"><img src="assets/publicis/content-types-3.jpg" alt="Entertaining content and Work Your World formats"></figure>
  </div>

  <h2 class="sub">Results</h2>
  <div class="stat-block">
    <p class="stat-label">Per post, Q4 2024 against January to April 2025</p>
    <div class="stats">
      <div class="stat"><span class="num">+57%</span><span class="cap">average views</span></div>
      <div class="stat"><span class="num">+388%</span><span class="cap">average shares</span></div>
      <div class="stat"><span class="num">+105%</span><span class="cap">average saves</span></div>
      <div class="stat"><span class="num">+16%</span><span class="cap">average likes</span></div>
    </div>
  </div>

  <h2 class="sub">Against the competitive set</h2>
  <p>Engagement rate reached 4.31%, the highest of the five agency accounts tracked. The next closest was 3.16%.</p>
  <figure class="fig">
    <img src="assets/publicis/competitors.jpg" alt="Engagement rate, followers and average likes for the five agency accounts tracked">
  </figure>

  <p class="links"><a href="content.html">The posts themselves</a></p>
</section>
"""

# ----------------------------------------------------------------- RESEARCH
research = """
<section class="section">
  <p class="eyebrow">Research</p>
  <h1 class="page-title">Does an AI recommendation change what you buy?</h1>
  <p class="case-meta">MSc thesis · Universidad Carlos III de Madrid · 2026</p>

  <p class="lead">A while ago I typed something like "I don't know anything about vacuum cleaners, which one should I buy" into ChatGPT, and then followed the recommendation. I did not check the specs or compare anything, I went straight to the purchase page. I assumed I was not the only one, and nobody had tested what that does to how we decide, so I made it my thesis.</p>

  <figure class="fig">
    <img src="assets/thesis-chart.jpg" alt="30 percent chose the product without an AI recommendation, 47 percent chose it with one. n=192, p=.015, Cramer's V .176">
  </figure>

  <h2 class="sub">Method</h2>
  <p>A controlled between-subjects experiment with 192 participants. Everyone evaluated two pairs of wireless headphones. One group saw an AI recommendation, the other did not. I measured which product they chose, how long they took, and how confident they felt about the choice. Analysis in SPSS.</p>

  <h2 class="sub">Findings</h2>
  <p>The recommendation shifted product choice. 47% of the AI group picked the recommended product against 30% in the control group, a 17 point difference, significant at p=.015. The two products were fictional, Auro X3 and Velion S7, so there was no brand preference carried into the task.</p>
  <figure class="fig">
    <img src="assets/research/choice.jpg" alt="Product choice by condition. Control group: 70% Auro X3, 30% Velion S7. AI group: 53% and 47%.">
  </figure>
  <p>Decision time showed no significant difference either, and if anything the median ran slightly higher in the AI group rather than lower, with a wide spread in both conditions.</p>
  <figure class="fig">
    <img src="assets/research/time.jpg" alt="Box plot of decision time in seconds by condition, control against AI, with overlapping distributions">
  </figure>
  <p>Confidence showed no significant difference either, 4.46 in the control group against 4.60 with the recommendation.</p>
  <figure class="fig">
    <img src="assets/research/confidence.jpg" alt="Decision confidence by condition. Control 4.46, AI 4.60, with overlapping error bars.">
  </figure>
  <p>So people did not decide any faster and they did not feel any more certain, they simply chose differently, which on these results makes the recommendation a persuasion tool rather than a shortcut.</p>

  <h2 class="sub">Why that was not the prediction</h2>
  <p>Dual-process theory and the heuristic-systematic model suggest you offload the thinking, decide faster and feel better about it. Only the first hypothesis held. Two things probably explain the rest. The AI group was looking at a structurally larger information environment, which may have cancelled out any time saved. And people in a research setting think more deliberately than people spending their own money, where leaning on a shortcut is more natural.</p>

  <h2 class="sub">Limitations</h2>
  <p>The sample was a convenience one, 75% female and skewed young and educated, the brands were fictional and there was only a single product category, so the effect could look quite different for a higher stakes purchase or for someone less used to AI.</p>

  <h2 class="sub">Why it matters now</h2>
  <p>Amazon Rufus, Google AI Overviews and Klarna are already steering millions of purchase decisions a day. Adobe Analytics reported a 1,200% increase in retail traffic from generative AI sources between mid 2024 and early 2025. The technology is ahead of the regulation and the evidence base is still thin.</p>

  <h2 class="sub">The question I would ask next</h2>
  <p>AI shifts the decision. Whether it shifts it in a better direction is a separate question, and this experiment does not answer it. I measured what people chose and how sure they felt while choosing, not whether the product was right for them or whether they were still happy with it a month later. A recommendation that moves choice and raises satisfaction and one that moves choice and lowers it look identical in my data. Measuring satisfaction after the purchase instead of confidence during it is where I would take this next.</p>
</section>
"""

# ----------------------------------------------------------------- CONTENT
content = """
<section class="section">
  <p class="eyebrow">Publicis Groupe Hungary</p>
  <h1 class="page-title">Content</h1>
  <p class="lead">Examples of content I wrote, structured and art directed. These are my favourite ones, not all of it.</p>

  <h2 class="sub">Publicis Groupe Hungary</h2>
  <p>I ran the Instagram account from January to August 2025, so every post published in that window went through my hands. The full feed is on <a href="https://www.instagram.com/publicisgroupe_hu/" target="_blank" rel="noopener">Instagram</a>.</p>

  <div class="cards">
    <article class="card">
      <a class="thumb" href="https://www.instagram.com/p/DH-9ErWMNHf/?img_index=1" target="_blank" rel="noopener">
        <img src="assets/work/white-lotus.jpg" alt="Welcome to the White Lotus Marketing Agency cover">
      </a>
      <div class="card-body">
        <h3>The White Lotus marketing agency</h3>
        <p>Each character from the new season placed in a role at a marketing agency, with a line they would plausibly say. It went up while the season was still airing, and it was the best performing post of the period at 3,799 views.</p>
        <a href="https://www.instagram.com/p/DH-9ErWMNHf/?img_index=1" target="_blank" rel="noopener">See the post</a>
      </div>
    </article>

    <article class="card">
      <a class="thumb" href="https://www.instagram.com/p/DNnVfVWM47U/?img_index=1" target="_blank" rel="noopener">
        <img src="assets/work/connections.jpg" alt="Publicis Connections, a four by four grid of words">
      </a>
      <div class="card-body">
        <h3>Publicis Connections</h3>
        <p>The New York Times word grouping game, rebuilt with Publicis words and categories. Beanbag, Kantar, popcorn machine, Meta Ads. The answers were on the following slides.</p>
        <a href="https://www.instagram.com/p/DNnVfVWM47U/?img_index=1" target="_blank" rel="noopener">See the post</a>
      </div>
    </article>

    <article class="card">
      <a class="thumb" href="https://www.instagram.com/p/DKb6p6Msq1D/?img_index=1" target="_blank" rel="noopener">
        <img src="assets/work/acronyms.jpg" alt="Marketing Acronyms, wrong answers only">
      </a>
      <div class="card-body">
        <h3>Marketing acronyms, wrong answers only</h3>
        <p>We use a lot of acronyms. I took the common ones and gave them the wrong definitions.</p>
        <a href="https://www.instagram.com/p/DKb6p6Msq1D/?img_index=1" target="_blank" rel="noopener">See the post</a>
      </div>
    </article>

    <article class="card">
      <a class="thumb" href="https://www.instagram.com/p/DLFWijvM9B0/?img_index=1" target="_blank" rel="noopener">
        <img src="assets/work/research-carousel.jpg" alt="Meet Your Perfect Match, dating games and marketing gains">
      </a>
      <div class="card-body">
        <h3>Research, made readable</h3>
        <p>Eszter Domonkos, Brand Strategy Director, wrote the research on dating app mechanics and what marketing can take from them. I did the slide structure, the copy and the visual direction so it worked as a carousel rather than a document.</p>
        <a href="https://www.instagram.com/p/DLFWijvM9B0/?img_index=1" target="_blank" rel="noopener">See the post</a>
      </div>
    </article>
  </div>

  <p class="links">The strategy behind these is on the <a href="publicis.html">Publicis case study</a>.</p>

  <h2 class="sub">Synetech</h2>
  <p>B2B edtech in Spain, where I designed these in Illustrator to the brand book.</p>

  <div class="cards">
    <article class="card">
      <a class="thumb" href="https://www.linkedin.com/posts/synetechworld_daedadelaia-edtech-synetechworld-activity-7483410153501839361-51Ic" target="_blank" rel="noopener">
        <img src="assets/synetech/post-ia.jpg" alt="Infographic in Spanish: how Synetech AI helps in each class, with five numbered subject examples">
      </a>
      <div class="card-body">
        <h3>Synetech IA, subject by subject</h3>
        <p>The product claim is that AI helps in any classroom, which means nothing to a teacher, so this turns it into five concrete things it does, one per subject, and a maths teacher and a biology teacher each find their own case in it.</p>
        <a href="https://www.linkedin.com/posts/synetechworld_daedadelaia-edtech-synetechworld-activity-7483410153501839361-51Ic" target="_blank" rel="noopener">See the post</a>
      </div>
    </article>
    <article class="card">
      <a class="thumb" href="https://www.linkedin.com/posts/synetechworld_learntec26-learntec2026-synetech-activity-7454782709538701312-CLoA" target="_blank" rel="noopener">
        <img src="assets/synetech/post-learntec.jpg" alt="Post announcing Synetech at LearnTec in Karlsruhe, hall 2 stand M16, with Spain and Germany on a map">
      </a>
      <div class="card-body">
        <h3>LearnTec, Karlsruhe</h3>
        <p>A trade fair announcement. Spain to Germany on the map, hall and stand number large enough to read in the feed, because the only job of this post is for someone to turn up at the right place.</p>
        <a href="https://www.linkedin.com/posts/synetechworld_learntec26-learntec2026-synetech-activity-7454782709538701312-CLoA" target="_blank" rel="noopener">See the post</a>
      </div>
    </article>
  </div>

  <p class="links">The strategy behind these is on the <a href="synetech.html">Synetech case study</a>.</p>
</section>
"""

# ----------------------------------------------------------------- SKILLS
SKILLS = [
    ("Content strategy",
     "Built the competitive content database behind the Publicis Instagram relaunch and wrote the strategy out of it. I have done the same job twice since: Synetech's LinkedIn, in Spanish, and a Hungarian page supporting the LGBTQ+ community.",
     "publicis.html", "The Publicis case study"),
    ("Paid search",
     "Google Ads for AirHint, planning and running search campaigns against CPA and CPC in English, Spanish and Portuguese.",
     "airhint.html", "What that involves"),
    ("SEO",
     "I worked alongside the SEO team at Publicis. At AirHint I analyse page content and look for the keywords worth building a page around. AirHint currently comes out first on the results page for the searches we target.",
     None, None),
    ("CRO and A/B testing",
     "A rebuilt deals page at AirHint, and the A/B tests behind it in GrowthBook: button and call to action changes, page structure, interface changes around the point where someone decides.",
     "airhint.html", "The deals page and an experiment"),
    ("Traffic analysis",
     "Daily work in Google Analytics 4 and Search Console. The most useful piece so far was working out where AirHint's AI referral traffic comes from and why we get cited, which turned it into a channel we are deliberately growing.",
     "airhint.html", "What that found"),
    ("CRM and email",
     "Mailchimp at Synetech. At AirHint I am building the CRM and the email lifecycle in Brevo from the bottom up.",
     None, None),
    ("Integrated media planning",
     "Two years planning and monitoring campaigns across TV, out of home, radio, digital and partnerships in five European markets. The largest was Disney, with a yearly budget over €4M, planned and tracked in Excel. Also Disney+, National Geographic, Disney Channel, Diageo and Spin Master.",
     None, None),
    ("Quantitative research",
     "A between-subjects experiment with 192 participants for my master's thesis, analysed in SPSS. Before that, a 213-respondent survey for my bachelor's.",
     "research.html", "Both write-ups"),
    ("Social and creator campaigns",
     "Influencer and social concepts at Influnter for Nike, Costa Coffee, Madame Tussauds and ChatGPT, on Instagram and TikTok.",
     None, None),
    ("Design",
     "Brand assets, logos and icons for Synetech, drawn to their brand book in Illustrator.",
     "synetech.html", "The posts I designed"),
    ("Presenting and running teams",
     "Five years teaching the advanced maths exam to groups of forty to sixty for Studium Generale, and a year as its programme manager running five teams.",
     "about.html", "More on that"),
]

TOOLS = [
    # (name, category key, level, description)
    ("Google Ads", "paid", "daily", "AirHint. Search campaigns in English, Spanish and Portuguese for a flight price alert product."),
    ("Google Analytics 4", "analytics", "daily", "AirHint, daily. Traffic, conversion paths and which pages carry the affiliate clicks. I also set up the event tracking on my own site."),
    ("Google Search Console", "analytics", "daily", "AirHint. Which queries bring traffic and which pages are worth improving."),
    ("GrowthBook", "analytics", "daily", "AirHint. Running and reading A/B tests on the product."),
    ("Looker Studio", "analytics", "used", "Publicis. Campaign reporting dashboards."),
    ("Google Campaign Manager", "paid", "used", "Publicis. Ad serving and tracking across digital campaigns."),
    ("Meta Ads", "paid", "basic", "I know the concepts, the ad types and the invoicing side from Publicis, where I planned and monitored budgets. I have not bought on the platform myself."),
    ("Brevo", "crm", "basic", "Building AirHint's CRM and email flows from scratch. In progress, no results to show yet."),
    ("Mailchimp", "crm", "used", "Synetech. Email campaigns for a B2B audience."),
    ("Salesforce", "crm", "basic", "A ten hour course. I know what it does, I have not run one in production."),
    ("Excel", "productivity", "daily", "Publicis. Media plans, budget tracking, and the competitive content database behind the Instagram strategy."),
    ("PowerPoint", "productivity", "daily", "Publicis. Client strategy decks and monthly reporting, to agency standard."),
    ("Word", "productivity", "used", "Long form documents and the thesis."),
    ("Monday.com", "productivity", "used", "Publicis. Task management and team communication across accounts."),
    ("SAP", "productivity", "used", "Publicis. Two years handling invoicing with vendors and clients, Disney included."),
    ("Toggl", "productivity", "daily", "AirHint. Time tracking against invoiced work."),
    ("GitHub", "productivity", "used", "Hosting this site and my own projects."),
    ("YouScan", "research", "used", "Publicis. Social listening as a digital strategist."),
    ("AdReal, Gemius, Kantar, TGI", "research", "used", "Publicis. Audience research and market data behind media plans."),
    ("SPSS", "research", "used", "UC3M. Statistical analysis for the thesis."),
    ("Power BI", "analytics", "basic", "Beginner."),
    ("Illustrator", "design", "used", "Synetech. Brand assets, logos and icons built to the brand book. I draft shapes with Claude and finish them in Illustrator."),
    ("Premiere Pro", "design", "used", "Synetech. Social video editing."),
    ("Canva", "design", "daily", "Social and presentation work where a full Adobe file is overkill."),
    ("Figma", "design", "basic", "Enough to work inside a file someone else built."),
    ("Claude", "ai", "daily", "Analysis, drafting, and building the projects on this site. I completed the Claude 101 course."),
    ("ChatGPT and Perplexity", "ai", "daily", "University and thesis research, and general daily use."),
]

CATS = [
    ("all", "All"),
    ("paid", "Paid media"),
    ("analytics", "Analytics"),
    ("crm", "CRM and email"),
    ("research", "Research"),
    ("design", "Design"),
    ("ai", "AI"),
    ("productivity", "Productivity"),
    ("basic", "Still learning"),
]

LEVEL_LABEL = {"daily": "Use regularly", "used": "Used in production", "basic": "Basics"}


def skills_html():
    out = []
    for name, desc, href, label in SKILLS:
        link = f' <a href="{href}"{" target=\"_blank\" rel=\"noopener\"" if href and href.endswith(".pdf") else ""}>{label}</a>' if href else ""
        out.append(f"""    <details class="skill-card">
      <summary>{name}</summary>
      <div class="skill-body"><p>{desc}{link}</p></div>
    </details>""")
    return "\n".join(out)


def tools_html():
    chips = "\n".join(
        f'    <button type="button" class="chip{" on" if key == "all" else ""}" data-filter="{key}">{label}</button>'
        for key, label in CATS)
    items = []
    for name, cat, level, desc in TOOLS:
        items.append(f"""    <li class="tool" data-cat="{cat}" data-level="{level}">
      <div class="tool-head"><span class="tool-name">{name}</span><span class="lvl lvl-{level}">{LEVEL_LABEL[level]}</span></div>
      <p>{desc}</p>
    </li>""")
    return f"""  <div class="chips" role="group" aria-label="Filter tools">
{chips}
  </div>
  <ul class="tools">
{chr(10).join(items)}
  </ul>
  <p class="tools-empty" hidden>Nothing in that group.</p>"""


skills = f"""
<section class="section">
  <h1 class="page-title">Skills</h1>
  <p class="lead">Each one points at something you can look at. If I cannot show the proof, it is not on the list. Click to open.</p>

  <div class="skill-grid">
{skills_html()}
  </div>
</section>

<section class="section">
  <h2 class="sec-title">Tools</h2>
  <p class="sec-intro">Where I used each one and what for.</p>
{tools_html()}
</section>
"""

# ----------------------------------------------------------------- ABOUT
about = """
<section class="section">
  <h1 class="page-title">About</h1>
  <p class="lead">I grew up liking numbers. Maths was the thing I was good at and the thing I enjoyed, and for a long time that was enough on its own.</p>
  <p>Then it stopped being enough, because getting the small calculations right is satisfying for a while but I wanted to see the bigger picture and have some say in why we were doing any of it. That is what moved me from maths towards strategy, and at Publicis it is what moved me out of the media department, where I was ordering and monitoring campaigns, and into digital strategy, where I got to decide what we were doing and why.</p>
  <p>What I want from work now is to see my own contribution in the thing that comes out of it. Marketing is where the two halves of me meet. The numbers I have always liked, and the creative and strategic side I went looking for because the numbers alone were not enough.</p>
  <p>I am in Madrid, looking for a growth or digital marketing role where I own decisions rather than only execute them.</p>
</section>

<section id="volunteering" class="section">
  <h2 class="sec-title">Volunteering</h2>
  <p>For five years I taught maths on Saturdays for Studium Generale, a student-run volunteer organisation in Hungary. It prepares secondary school students for the final school-leaving exams, free, for students who would not get that preparation otherwise. I taught the advanced level maths exam, usually to a group of forty to sixty.</p>
  <figure class="fig">
    <img src="assets/teaching.jpg" alt="A full classroom of secondary school students working through maths problems at desks">
  </figure>
  <p>I also ran the week-long camps, where students do eight hours of maths a day.</p>
  <p>For one year I was programme manager, running three permanent teams and two temporary ones, and I was responsible for the events of a section of more than sixty people.</p>
  <p>I still teach maths, now one to one and online.</p>
</section>

<section class="section">
  <h2 class="sec-title">Outside work</h2>
  <p>I listen to a lot of Alex Hormozi, Chris Williamson and Andrew Huberman. For relationship advice, Esther Perel, or of course, my mother.</p>
  <p>I work best in long uninterrupted blocks. I am social, and I push myself into situations that are uncomfortable rather than avoiding them. At the moment I am working through the hundred days of rejection tasks, from Jia Jiang's project, which is built on Jason Comely's Rejection Therapy game.</p>
  <p>I go to the gym and play volleyball. I travel as often as I can.</p>
  <p>I used to act, mostly background and small parts. Halo is the one listed on my <a href="https://www.imdb.com/name/nm12520506/" target="_blank" rel="noopener">IMDb page</a>, and I am in The Witcher too. I do not do it any more.</p>
  <p>I am writing a novel in Hungarian, called Conticinium. It comes from the Spanish conticinio, the quietest part of the night. It is part adventure, part science fiction, sprinkled with a little romance. The question underneath is why people are never satisfied with what they have.</p>
  <p>Oh, and last but not least: I put the milk in before the cereal. If you disagree but are still not judging me, you are living by my fourth quote. They are all below.</p>
</section>

<section class="section">
  <h2 class="sec-title">Quotes</h2>
  <ul class="quotes">
    <li>
      <blockquote>You cannot wish for an easy life and a good character. One is the price of the other.</blockquote>
      <p class="attr">Alex Hormozi</p>
      <p class="gloss">His point is that character gets built by doing hard things, so you do not get to order both. I use it as a filter. I try to take the route that makes for a more interesting person and a more colourful life, which is almost never the comfortable one.</p>
    </li>
    <li>
      <blockquote>No one knows enough to be a pessimist.</blockquote>
      <p class="attr">Wayne Dyer</p>
      <p class="gloss">I have always been an optimist, and seeing the glass as half full is one of the things I am actually good at. This is the argument for it. You cannot know what is coming, or what you will have the chance to do. I read once that if you asked the person you were five years ago to predict where you are now, they would get almost none of it right, and that has held up every time I have checked it against myself.</p>
    </li>
    <li>
      <blockquote>Winners lose more than losers ever will.</blockquote>
      <p class="gloss">This one is about experimentation. You have to run a lot of tests and fail most of them before you find the thing that works, and you never find out if you never run them.</p>
    </li>
    <li>
      <blockquote>Be curious, not judgmental.</blockquote>
      <p class="attr">Ted Lasso, which credits Walt Whitman, who never wrote it</p>
      <p class="gloss">This applies to most of my life. When I hear something I disagree with, or something my first instinct is to judge, I try to stop and ask the person why, so I understand their position before I decide what I think of it. I still get to disagree afterwards. Being open-minded matters for a career for the same reason.</p>
    </li>
  </ul>
</section>
"""


# ----------------------------------------------------------------- SYNETECH
synetech = """
<section class="section">
  <p class="eyebrow">Case study</p>
  <h1 class="page-title">LinkedIn content strategy for Synetech</h1>
  <p class="case-meta">Synetech · Social Media &amp; Content Creator · April to July 2026 · Madrid</p>

  <p class="lead">Synetech sells interactive classroom technology in Spain, to wholesalers, distributors and integrators, and to the IT coordinators who choose it for a school. I owned social and content for the brand. The work below comes from the digital strategy I wrote for them, in Spanish.</p>

  <h2 class="sub">Benchmarking the site against four competitors</h2>
  <p>I put Synetech's website next to Newline, Smarttech, i3 Connect and Promethean and scored each one on four things: what sits above the fold, the menu and structure, the content on offer, and the E-E-A-T signals. Scoring every cell rather than writing impressions is what makes the gaps arguable instead of a matter of taste.</p>
  <figure class="fig">
    <img src="assets/synetech/web-benchmark.jpg" alt="A five column comparison table scoring Synetech against Newline, Smarttech, i3 Connect and Promethean on above the fold, menu and structure, content, and E-E-A-T">
  </figure>
  <p>The two weakest areas came out as navigation and trust. No product photos in the menu, element names written in internal language rather than the customer's, and no case studies or tutorials, where every competitor had both. Promethean categorised its menu by sector, Smarttech put photos in it, and all four led with customer stories that Synetech did not have.</p>

  <h2 class="sub">What the sector posts on LinkedIn, and what we posted</h2>
  <p>For LinkedIn I coded a sample of the sector's posts by content category and by format, then set Synetech's own mix against the sector average, so the question stopped being what we should post and became where we were over and under weight.</p>
  <figure class="fig">
    <img src="assets/synetech/linkedin-formats.jpg" alt="Two tables comparing the sector average against Synetech by content category and by post format, with the differences shaded">
  </figure>
  <p>The recommendation was to move output out of HR and events and into product and customer stories, and into the formats the sector was not using much yet, carousels and video, rather than competing on the ones it was saturating.</p>

  <h2 class="sub">The posts</h2>
  <p>Two examples, both designed in Illustrator.</p>
  <div class="cards">
    <article class="card">
      <a class="thumb" href="https://www.linkedin.com/posts/synetechworld_daedadelaia-edtech-synetechworld-activity-7483410153501839361-51Ic" target="_blank" rel="noopener">
        <img src="assets/synetech/post-ia.jpg" alt="Infographic in Spanish: how Synetech AI helps in each class, with five numbered subject examples">
      </a>
      <div class="card-body">
        <h3>Synetech IA, subject by subject</h3>
        <p>The product claim is that AI helps in any classroom, which means nothing to a teacher. This turns it into five concrete things it does, one per subject, so a maths teacher and a biology teacher each see their own case.</p>
        <a href="https://www.linkedin.com/posts/synetechworld_daedadelaia-edtech-synetechworld-activity-7483410153501839361-51Ic" target="_blank" rel="noopener">See the post</a>
      </div>
    </article>
    <article class="card">
      <a class="thumb" href="https://www.linkedin.com/posts/synetechworld_learntec26-learntec2026-synetech-activity-7454782709538701312-CLoA" target="_blank" rel="noopener">
        <img src="assets/synetech/post-learntec.jpg" alt="Post announcing Synetech at LearnTec in Karlsruhe, hall 2 stand M16, with Spain and Germany on a map">
      </a>
      <div class="card-body">
        <h3>LearnTec, Karlsruhe</h3>
        <p>A trade fair announcement. Spain to Germany on the map, hall and stand number large enough to be read in the feed, because the only job of this post is for someone to turn up at the right place.</p>
        <a href="https://www.linkedin.com/posts/synetechworld_learntec26-learntec2026-synetech-activity-7454782709538701312-CLoA" target="_blank" rel="noopener">See the post</a>
      </div>
    </article>
  </div>

  <h2 class="sub">Working in Spanish</h2>
  <p>The strategy deck, the analysis and most of the content were written in Spanish. Some posts went out in English where the audience was international, like the German trade fair. This is the clearest evidence I have that working in Spanish is not a problem for me.</p>
</section>
"""


# ----------------------------------------------------------------- BOOKING THESIS
research_booking = """
<section class="section">
  <p class="eyebrow">Research</p>
  <h1 class="page-title">How much website nudges move a booking decision</h1>
  <p class="case-meta">BSc thesis · Corvinus University of Budapest · 2023</p>

  <p class="lead">Every booking site runs the same set of mechanisms on you. Scarcity, social proof, urgency framing, loss aversion, defaults, anchoring. They are the most reliable conversion tools there are, which is why they are everywhere, and they sit closer to the legal line than most of the people deploying them realise. I wrote my bachelor thesis on how well they actually work, on whether anyone notices them, and on where regulators have drawn that line.</p>

  <h2 class="sub">The case that prompted it</h2>
  <p>In 2020 the Hungarian Competition Authority fined Booking.com 2.5 billion forint. Three violations. Free cancellation was advertised as a feature when at many properties it was only temporarily available, and those bookings cost more than the same stay without it, because the price of the option was folded into the fare. Urgency and scarcity messages appeared at every step of the search and booking flow. And information about which properties accepted the Hungarian leisure card was inconsistent. The fine was calculated against commission revenue from the affected bookings.</p>

  <h2 class="sub">The mechanisms, as they appear on the page</h2>
  <p>These are the five I tested. Scarcity of supply, a time-limited offer, live social proof, recent social proof, and a membership default framed as a loss if you skip it.</p>
  <figure class="fig narrow">
    <img src="assets/research/booking-messages.jpg" alt="Five booking site message mockups: sign in and save 10 percent or more, limited time offer, 3 people are viewing this right now, only 2 rooms left, 22 people booked here in the past week">
    <figcaption>Top to bottom: sign in and save 10% or more · limited time offer · 3 people are viewing this right now · only 2 rooms left · 22 people booked here in the past week. Two of these were live on the site at the time of the ruling.</figcaption>
  </figure>

  <h2 class="sub">How I measured them</h2>
  <p>A 24 question survey, 213 respondents, anonymous. 72.3% women, the largest group aged 18 to 25 and a second cluster aged 46 to 55. Over 99% travel at least once a year and 61.5% book their own accommodation online. Booking.com was the platform they used most.</p>
  <p>The order of the questions carried the method. Asking someone outright whether an urgency message influenced them does not work, because the influence is mostly not conscious and the question invites a no. So the early questions established what they think they look at, and only later did I name the mechanisms and show them the formats above.</p>

  <h2 class="sub">Unprompted, almost nobody names them</h2>
  <p>Asked in an open question which messages or factors had influenced their booking decisions, 9 of 213 mentioned urgency messages. Ten mentioned free cancellation. Everyone else named price, reviews, location and amenities. The practices the regulator fined a company over barely registered as things that happen.</p>

  <h2 class="sub">Shown the same messages, they rate them as persuasive</h2>
  """ + figure(_hbar([
    ("Only 2 rooms left", 3.65),
    ("Sign in to save 10% or more", 3.62),
    ("Limited time offer", 3.10),
    ("22 people booked here this week", 2.98),
    ("3 people are viewing this now", 2.56),
], 1, 6, "1 no pull at all &#183; 6 very strong pull"),
    "Rated persuasive power of each message. 213 respondents.") + """
  <p>Scarcity of the room count scored highest and live social proof lowest, which is the reverse of what I expected going in. The two strongest are both about something running out, whether that is stock or a discount, while the two weakest are both claims about other people, which also happen to be the easiest ones to disbelieve.</p>

  <h2 class="sub">People have to believe it for it to work</h2>
  <p>Asked how often these messages carry real information, on a scale of one to six, the average was 3.18. People lean towards assuming the claim is not true. And belief turns out to track persuasion almost linearly.</p>
  """ + figure(_vbar([
    ("1", 1.98), ("2", 2.97), ("3", 3.16),
    ("4", 4.02), ("5", 3.90), ("6", 4.52),
], 1, 6, "How often do these messages tell the truth? 1 never &#183; 6 always",
    "Persuasive power"),
    "Persuasive power by how much the respondent believes the claim.") + """
  <p>What makes these messages work is not really how they are worded, it is whether people believe them. If nobody believes the claim then the message is just one more thing on the page, and a false one makes the true ones next to it harder to believe as well. Which means the honest version of the tactic also happens to be the one that keeps working.</p>

  <h2 class="sub">They put it at nearly half the decision</h2>
  <div class="hero-stat">
    <span class="hero-num">46%</span>
    <p>of the booking decision, by respondents' own estimate, comes down to these messages rather than to the price, the location and the services. People who could not name a single one of them ten minutes earlier.</p>
  </div>

  <h2 class="sub">Where the two regulators differ</h2>
  <p>Comparing the Hungarian and Dutch responses to the same company is the useful part. The Dutch authority issued guidance in 2020 on online commercial practices that influence consumer decisions, but did not directly address emotional, urgency-based messaging. Foreign authorities have generally examined whether a claim is misleading and pushed for transparency. The Hungarian decision went further and treated commercial practice built on psychological pressure as harm to consumer welfare in itself, which at the time was unusual internationally.</p>

  <h2 class="sub">Conclusions</h2>
  <p>The first thing to say is what this study cannot do: it was a survey, so people were rating messages that I had shown them and asked them to think about, which is nothing like a person booking a trip with their own money. Survey conditions make people more deliberate than they are in real life, and they can only report the influence they are aware of, which the unprompted question had already shown is not much. The honest measurement of a button or a message is on a live page, with real traffic split between two versions.</p>
  <p>What the research did give me is a clear picture of the mechanisms and of where the legal line runs, which turns out to be about whether the claim is true rather than whether the technique is used at all. Only two rooms left is fine to show if two rooms are left. The enforcement in the Booking.com case did not land on urgency messaging existing. It landed on claims that were not accurate and terms that were not what they appeared to be.</p>
  <p>It also pointed me at what I do now. Writing it is what made me want to measure these things properly instead of asking people about them, and at <a href="airhint.html">AirHint</a> I get to, with A/B tests on the real page and real traffic.</p>

  <p class="links">Sources: GVH decision VJ/17-110/2018 · ACM, Guidelines on Protection of the Online Consumer, 2020</p>
</section>
"""

page("index.html", "Aron Arany-Toth — Digital marketing and growth",
     "Digital marketing and growth. Paid search, content strategy and campaign analysis. Madrid, working in English, Spanish and Hungarian.", home)
page("airhint.html", "Growth at AirHint — Aron Arany-Toth",
     "Paid search, a rebuilt deals page, experiments and CRM work for AirHint, a flight price prediction product.", airhint)
page("publicis.html", "Publicis Groupe Hungary on Instagram — Aron Arany-Toth",
     "A content strategy built from a coded database of the competitive set, and what it did to the numbers.", publicis)
page("research.html", "Does an AI recommendation change what you buy? — Aron Arany-Toth",
     "A controlled experiment with 192 participants on AI product recommendations and consumer choice.", research)
page("synetech.html", "LinkedIn content strategy for Synetech — Aron Arany-Toth",
     "A competitor benchmark of websites and LinkedIn output for a B2B edtech brand in Spain, written in Spanish.", synetech)
page("research-booking.html", "How much website nudges move a booking decision — Aron Arany-Toth",
     "A survey of 213 people on how urgency and scarcity messages affect booking decisions, against the Booking.com competition case.", research_booking)
page("content.html", "Content — Aron Arany-Toth",
     "Instagram formats written, structured and art directed at Publicis Groupe Hungary.", content)
page("skills.html", "Skills and tools — Aron Arany-Toth",
     "What I can do and where I proved it, and a filterable list of the tools I use.", skills)
page("about.html", "About — Aron Arany-Toth",
     "Teaching, acting, writing, and the things I keep coming back to.", about)
