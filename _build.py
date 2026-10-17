"""Stamp the shared layout into every page in _pages/ and write the site to the repo root.

Run:  python _build.py
Each _pages/*.html file starts with a header block:
    <!--
    title: History
    slug: history          (output path; "index" for the home page)
    description: ...       (optional)
    -->
"""
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
REPO = "https://github.com/AngadBasandrai/this-hi"
SITE = "https://thishi.org"

NAV = [
    ("news", "News"),
    ("history", "History"),
    ("theories", "Theories"),
    ("dreams", "Dreams"),
    ("portraits", "Portraits"),
    ("in-the-world", "In the World"),
    ("download", "Download"),
    ("fan-art", "Fan Art"),
    ("guestbook", "Guestbook"),
    ("contact", "Contact"),
]

ICON_X = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18.9 1.2h3.7l-8 9.2 9.4 12.4h-7.4l-5.8-7.6-6.6 7.6H.5l8.6-9.8L0 1.2h7.6l5.2 6.9 6.1-6.9zm-1.3 19.4h2L6.5 3.3H4.3l13.3 17.3z"/></svg>'
ICON_GH = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 .3a12 12 0 0 0-3.8 23.4c.6.1.8-.3.8-.6v-2c-3.3.7-4-1.6-4-1.6-.6-1.4-1.4-1.8-1.4-1.8-1-.7.1-.7.1-.7 1.2.1 1.8 1.2 1.8 1.2 1 1.8 2.8 1.3 3.5 1 0-.8.4-1.3.7-1.6-2.7-.3-5.5-1.3-5.5-6 0-1.2.5-2.3 1.3-3.1-.2-.4-.6-1.6 0-3.2 0 0 1-.3 3.4 1.2a11.5 11.5 0 0 1 6 0c2.3-1.5 3.3-1.2 3.3-1.2.6 1.6.2 2.8.1 3.2.8.8 1.3 1.9 1.3 3.2 0 4.6-2.8 5.6-5.5 5.9.5.4.9 1.1.9 2.3v3.3c0 .3.1.7.8.6A12 12 0 0 0 12 .3"/></svg>'
ICON_MAIL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 4h20a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1zm1 3.2V18h18V7.2l-9 6.3-9-6.3zM4.4 6l7.6 5.3L19.6 6H4.4z"/></svg>'

LAYOUT = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{site}/assets/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="/assets/favicon.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Arvo:wght@700&display=swap">
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<header class="site-header wrap">
  <a class="brand" href="/"><img src="/assets/hi-thumb.png" alt="" width="44" height="44">thishi.org</a>
  <{htag} class="headline{hclass}">Ever dream<br> this hi?</{htag}>
</header>
<nav class="site-nav" aria-label="Main">
  <input type="checkbox" id="menu" class="menu-toggle">
  <label for="menu" class="menu-btn">&#9776; Menu</label>
  <ul>
{nav}
  </ul>
</nav>
<main id="content" class="wrap">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="social">
      <a href="https://x.com/SillyPianist67" aria-label="Hi on X">{icon_x}</a>
      <a href="{repo}" aria-label="Source on GitHub">{icon_gh}</a>
      <a href="/contact/" aria-label="Contact">{icon_mail}</a>
    </div>
    <div>&copy; {year} thishi.org &middot; <a href="/contact/">Contact</a> &middot; <a href="{repo}">Source</a></div>
    <div class="parody">A fan-made parody of <a href="https://thisman.org/">thisman.org</a>. No cats were harmed. Several were said hi to.</div>
  </div>
</footer>
<script src="/assets/site.js" defer></script>
</body>
</html>
"""


def parse(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"\s*<!--(.*?)-->\s*", text, re.S)
    meta = dict(
        (k.strip(), v.strip())
        for k, v in (line.split(":", 1) for line in m.group(1).strip().splitlines() if ":" in line)
    )
    return meta, text[m.end():]


def build():
    pages = sorted((ROOT / "_pages").glob("*.html"))
    for path in pages:
        meta, body = parse(path)
        slug = meta["slug"]
        home = slug == "index"
        nav = "\n".join(
            f'    <li><a href="/{s}/"{" aria-current=\"page\"" if s == slug else ""}>{label}</a></li>'
            for s, label in NAV
        )
        out_path = ROOT / ("index.html" if home else "404.html" if slug == "404" else f"{slug}/index.html")
        url = SITE + ("/" if home else f"/{slug}/")
        html = LAYOUT.format(
            title=meta["title"] if home else f'{meta["title"]} | Ever dream this hi?',
            description=meta.get("description", "Every night, all over the world, people dream of this cat. It says hi. Have you seen it?"),
            url=url,
            site=SITE,
            repo=REPO,
            htag="h1" if home else "p",
            hclass="" if home else " small",
            nav=nav,
            body=body.strip(),
            icon_x=ICON_X,
            icon_gh=ICON_GH,
            icon_mail=ICON_MAIL,
            year=date.today().year,
        )
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8", newline="\n")
        print("wrote", out_path.relative_to(ROOT))


if __name__ == "__main__":
    build()
