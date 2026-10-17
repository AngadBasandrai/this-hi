"""Stamp the shared layout into every page in _pages/ and write the site to the repo root.

Run:  python _build.py
Each _pages/*.html file starts with a header block:
    <!--
    title: History
    slug: history          (output path; "index" for the home page, "404" for the error page)
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
    ("portrait", "Portraits"),
    ("in-the-world", "In the World"),
    ("download", "Download"),
    ("fan-art", "Fan Art"),
    ("guestbook", "Guestbook"),
    ("contact", "Contact"),
]

# Shown in the right-hand NEWS widget; keep in sync with _pages/news.html.
NEWS = [
    ("This Hi in Azide&rsquo;s Poster", "/this-hi-in-azides-poster/"),
    ("Was This Hi Caught on Camera?", "/was-this-hi-caught-on-camera/"),
]

ICON_X = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18.9 1.2h3.7l-8 9.2 9.4 12.4h-7.4l-5.8-7.6-6.6 7.6H.5l8.6-9.8L0 1.2h7.6l5.2 6.9 6.1-6.9zm-1.3 19.4h2L6.5 3.3H4.3l13.3 17.3z"/></svg>'
ICON_GH = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 .3a12 12 0 0 0-3.8 23.4c.6.1.8-.3.8-.6v-2c-3.3.7-4-1.6-4-1.6-.6-1.4-1.4-1.8-1.4-1.8-1-.7.1-.7.1-.7 1.2.1 1.8 1.2 1.8 1.2 1 1.8 2.8 1.3 3.5 1 0-.8.4-1.3.7-1.6-2.7-.3-5.5-1.3-5.5-6 0-1.2.5-2.3 1.3-3.1-.2-.4-.6-1.6 0-3.2 0 0 1-.3 3.4 1.2a11.5 11.5 0 0 1 6 0c2.3-1.5 3.3-1.2 3.3-1.2.6 1.6.2 2.8.1 3.2.8.8 1.3 1.9 1.3 3.2 0 4.6-2.8 5.6-5.5 5.9.5.4.9 1.1.9 2.3v3.3c0 .3.1.7.8.6A12 12 0 0 0 12 .3"/></svg>'

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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,400;0,700;0,800;1,400&display=swap">
<link rel="stylesheet" href="/assets/style.css">
</head>
<body class="{body_class}">
<a class="skip" href="#content">Skip to content</a>
<aside class="left">
  <div class="branding">
    <a href="/"><img class="portrait" src="/assets/portrait-sidebar.png" alt="Black and white sketch of the cat" width="200" height="235"></a>
    <a class="site-title" href="/">Ever dream this hi?</a>
    <p class="site-desc">Every night all over the world hundreds of people get a hi from this cat</p>
  </div>
  <nav class="left-nav" aria-label="Main">
    <input type="checkbox" id="menu" class="menu-toggle">
    <label for="menu" class="menu-btn">&#9776; Menu</label>
    <ul>
{nav}
    </ul>
  </nav>
</aside>
<div class="page">
{title_band}<div class="area" id="content">
  <main class="content">
{body}
  </main>
  <aside class="widgets">
    <section class="widget menu">
      <ul>
{nav}
      </ul>
    </section>
    <section class="widget">
      <h3><a href="/news/">News</a></h3>
      <ul>
{news}
      </ul>
    </section>
    <section class="widget plain">
      <h3>Contact</h3>
      <a href="/contact/">www.thishi.org/contact</a>
    </section>
    <section class="widget plain">
      <h3>Old website</h3>
      <a href="https://www.thisman.org/">www.thisman.org</a>
    </section>
    <section class="widget">
      <h3>Social</h3>
      <div class="social">
        <a href="https://x.com/SillyPianist67" aria-label="Hi on X">{icon_x}</a>
        <a href="{repo}" aria-label="thishi.org on GitHub">{icon_gh}</a>
      </div>
    </section>
  </aside>
</div>
<footer class="footer">
  thishi.org &copy; 2025-{year}
  <span class="parody">A parody of <a href="https://www.thisman.org/">thisman.org</a></span>
</footer>
</div>
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
    news = "\n".join(f'        <li><a href="{href}">{label}</a></li>' for label, href in NEWS)
    for path in sorted((ROOT / "_pages").glob("*.html")):
        meta, body = parse(path)
        slug = meta["slug"]
        home = slug == "index"
        nav = "\n".join(
            f'      <li><a href="/{s}/"{" aria-current=\"page\"" if s == slug else ""}>{label}</a></li>'
            for s, label in NAV
        )
        out_path = ROOT / ("index.html" if home else "404.html" if slug == "404" else f"{slug}/index.html")
        html = LAYOUT.format(
            title=meta["title"] if home else f'{meta["title"]} | Ever dream this hi?',
            description=meta.get("description", "Every night all over the world hundreds of people get a hi from this cat."),
            url=SITE + ("/" if home else f"/{slug}/"),
            site=SITE,
            repo=REPO,
            body_class="home" if home else "inner",
            title_band="" if home else f'<header class="title-band"><h1>{meta["title"]}</h1></header>\n',
            nav=nav,
            news=news,
            body=body.strip(),
            icon_x=ICON_X,
            icon_gh=ICON_GH,
            year=date.today().year,
        )
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8", newline="\n")
        print("wrote", out_path.relative_to(ROOT))


if __name__ == "__main__":
    build()
