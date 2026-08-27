#!/usr/bin/env python3
"""Render the newest essay as the site homepage.

    python3 tools/build-home.py            # newest essay listed in about.html
    python3 tools/build-home.py on-reason.html   # a specific one

The newest essay is the first entry of the Essays list in about.html that
carries a date label and points into blog/, so adding an essay is two steps:
write blog/<essay>.html, add its line to that list, then run this script.

The homepage is the essay page with three changes: the back-to-blog nav becomes
the panel on the right, the byline under the title goes (the panel carries the
name), and the article loads dimmed until the first scroll.
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ABOUT = ROOT / "about.html"
OUT = ROOT / "index.html"
SITE = "https://rajevv.github.io/"

RAIL = '''    <aside class="rail" aria-label="Elsewhere on this site">
      <p class="rail-name">Rajeev Verma</p>
      <p class="rail-role">PhD Candidate in Machine Learning, University of Amsterdam</p>
      <nav class="rail-nav" aria-label="Site sections">
        <a href="about.html#top">About me</a>
        <a href="about.html#publications">Selected Publications</a>
        <a href="about.html#blog">Essays</a>
        <a href="about.html#service">Service</a>
        <a href="assets/pdf/CV_updated.pdf">CV</a>
        <a href="https://scholar.google.com/citations?hl=en&amp;user=xSgjaZYAAAAJ&amp;view_op=list_works&amp;sortby=pubdate" target="_blank" rel="noopener noreferrer">Scholar</a>
      </nav>
    </aside>
'''

CSS = '''
    /* ── Right-hand panel ── */
    article h1 { font-size: 1.45rem; margin-bottom: 14px; }

    .post-date {
      font-size: 0.62em;
      font-weight: 400;
      color: var(--muted);
      white-space: nowrap;
      margin-left: 0.55em;
    }

    /* Line box and offset are tuned so this baseline meets the essay title's. */
    .rail-name {
      font-size: 1.75rem;
      font-weight: 700;
      letter-spacing: -0.01em;
      line-height: 1.18;
      margin: -10px 0 7px;
    }

    .rail-role {
      font-size: 0.97rem;
      line-height: 1.5;
      color: var(--muted);
      margin: 0 0 22px;
    }

    .rail-nav {
      display: flex;
      flex-direction: column;
      gap: 13px;
      padding-top: 20px;
      border-top: 1px solid var(--rule);
    }

    .rail-nav a {
      font-size: 1.07rem;
      text-decoration: none;
    }

    .rail-nav a:hover {
      color: var(--link-hover);
      text-decoration: underline;
      text-underline-offset: 2px;
    }

    @media (min-width: 1081px) {
      #container {
        display: grid;
        grid-template-columns: minmax(0, 680px) 284px;
        gap: 0 88px;
        justify-content: center;
        align-items: start;
        max-width: 1096px;
      }

      article { grid-column: 1; grid-row: 1; }

      .rail {
        grid-column: 2;
        grid-row: 1;
        position: sticky;
        top: 34px;
      }

      /* The panel occupies the gutter, so margin notes run inline instead. */
      .sidenote {
        float: none;
        clear: none;
        width: auto;
        margin: 1rem 0 1.4rem;
        padding: 10px 14px;
        background: #f7f7f5;
        border-left: 3px solid var(--rule);
        border-radius: 0 6px 6px 0;
        display: none;
      }

      .margin-toggle:checked + .sidenote { display: block; }
    }

    /* ── The essay rests at reduced strength until the first scroll ── */
    article { transition: opacity 0.6s ease; }
    article.at-rest { opacity: 0.72; }

    @media (prefers-reduced-motion: reduce) {
      article { transition: none; }
    }

    @media (max-width: 1080px) {
      .rail {
        padding-bottom: 16px;
        margin-bottom: 34px;
        border-bottom: 1px solid var(--rule);
      }

      .rail-role { margin-bottom: 14px; }

      .rail-nav {
        flex-direction: row;
        flex-wrap: wrap;
        gap: 7px 18px;
        padding-top: 14px;
      }
    }
'''

SCRIPT = '''
  <script>
    // The article loads dimmed and comes up to full strength on the first
    // scroll. Adding the class from script keeps the page readable with no JS.
    (function () {
      var article = document.querySelector('article');
      if (!article || window.scrollY > 0) return;
      article.classList.add('at-rest');
      function wake() { article.classList.remove('at-rest'); }
      ['scroll', 'wheel', 'touchmove', 'keydown', 'pointerdown'].forEach(function (name) {
        window.addEventListener(name, wake, { once: true, passive: true });
      });
    })();
  </script>
'''


MONTHS = {"Jan": "January", "Feb": "February", "Mar": "March", "Apr": "April",
          "May": "May", "Jun": "June", "Jul": "July", "Aug": "August",
          "Sep": "September", "Oct": "October", "Nov": "November", "Dec": "December"}


def essay_entries():
    """The Essays list in about.html, newest first, as (filename, date) pairs."""
    about = ABOUT.read_text()
    section = re.search(r'<ul class="plain-list">(.*?)</ul>', about, re.S)
    if not section:
        sys.exit("no Essays list found in about.html")
    entries = []
    for item in re.findall(r"<li>(.*?)</li>", section.group(1), re.S):
        href = re.search(r'href="blog/([^"#]+\.html)"', item)
        date = re.search(r'<span class="essay-date">\[([A-Za-z]{3}) (\d{4})\]</span>', item)
        if href and date:
            entries.append((href.group(1), "%s %s" % (MONTHS.get(date.group(1), date.group(1)),
                                                      date.group(2))))
    if not entries:
        sys.exit("no dated essay entry found in the Essays list")
    return entries


def build(essay_name, date=None):
    essay = ROOT / "blog" / essay_name
    html = essay.read_text()
    stem = essay.stem

    title = re.search(r"<h1>(.*?)</h1>", html).group(1)
    if date:
        html = html.replace("<h1>%s</h1>" % title,
                            '<h1>%s <span class="post-date">%s</span></h1>' % (title, date), 1)
    description = re.search(r'<meta name="description" content="(.*?)"', html)
    description = description.group(1) if description else title

    # Figures sit next to the essay; the homepage is one level above them.
    html = html.replace('src="%s_figs/' % stem, 'src="blog/%s_figs/' % stem)

    header_image = re.search(r'<img src="(blog/[^"]+)"', html)
    header_image = SITE + header_image.group(1) if header_image else SITE + "assets/prof_pic.jpg"

    html = re.sub(r"<title>.*?</title>",
                  "<title>Rajeev Verma &mdash; %s</title>" % title, html, count=1)
    html = re.sub(r'<link rel="canonical"[^>]*/>',
                  '<link rel="canonical" href="%s" />\n'
                  '  <meta property="og:type" content="article" />\n'
                  '  <meta property="og:title" content="%s &mdash; Rajeev Verma" />\n'
                  '  <meta property="og:description" content="%s" />\n'
                  '  <meta property="og:url" content="%s" />\n'
                  '  <meta property="og:image" content="%s" />\n'
                  '  <meta name="twitter:card" content="summary_large_image" />'
                  % (SITE, title, description, SITE, header_image), html, count=1)

    # The panel replaces the back-to-blog nav.
    html = re.sub(r'    <nav class="site-nav".*?</nav>\n', RAIL, html, count=1, flags=re.S)

    # The panel already carries the name, so the byline goes.
    html = re.sub(r'\s*<p class="post-meta">.*?</p>\n', "\n", html, count=1, flags=re.S)

    # The panel carries every link the footer used to repeat.
    html = re.sub(r"\s*<footer>.*?</footer>\n", "\n", html, count=1, flags=re.S)

    # Whatever else the essay links relative to blog/ is one level up from here.
    html = html.replace('"../', '"')

    html = html.replace("  </style>", CSS + "  </style>", 1)
    html = html.replace("</body>", SCRIPT + "</body>", 1)

    OUT.write_text(html)
    print("homepage built from blog/%s (%s)" % (essay_name, title))


if __name__ == "__main__":
    entries = essay_entries()
    if len(sys.argv) > 1:
        wanted = sys.argv[1]
        date = dict(entries).get(wanted)
        build(wanted, date)
    else:
        build(*entries[0])
