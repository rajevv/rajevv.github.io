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
    :root {
      --ground: #eaeaea;
      --card-edge: #dcdcdc;
    }

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
        grid-template-columns: minmax(0, 728px) 284px;
        gap: 0 88px;
        justify-content: center;
        align-items: start;
        max-width: 1144px;
      }

      /* The base stylesheet caps the article at 680px; the column governs here. */
      article { grid-column: 1; grid-row: 1; max-width: none; }
      .stream { grid-column: 1; grid-row: 2; }

      .rail {
        grid-column: 2;
        grid-row: 1 / span 2;
        position: sticky;
        top: 34px;
        /* Clears the card's top padding, so the name meets the title's baseline. */
        margin-top: 45px;
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

    /* ── The feed: each post its own card on a tinted ground ── */
    body { background: var(--ground); }

    article,
    .stream-item {
      background: #ffffff;
      border: 1px solid var(--card-edge);
      border-radius: 5px;
      padding: 38px 44px 30px;
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
    }

    /* An excerpt card answers the pointer, since the whole post leads away. */
    .stream-item {
      transition: border-color 0.18s ease, box-shadow 0.18s ease;
    }

    .stream-item:hover {
      border-color: #cbcbcb;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05), 0 10px 26px rgba(0, 0, 0, 0.04);
    }

    ::selection { background: #dde3e8; }

    /* The card frames the photograph, so the photograph drops its own frame. */
    article figure img {
      border: none;
      border-radius: 4px;
    }

    /* A short centred rule instead of a full-width one. */
    article hr {
      width: 54px;
      margin: 26px auto 32px;
      border-top: 1px solid #d2d2d2;
    }

    .stream { max-width: 728px; }
    .stream-item { margin-top: 26px; }
    .stream-label { display: none; }

    article figure { margin: 26px 0 30px; }

    article figure img { width: 100%; }

    /* On a narrow screen the cards run the full width, as a feed does. */
    @media (max-width: 620px) {
      #container { padding-left: 0; padding-right: 0; }

      article,
      .stream-item {
        padding: 26px 22px 22px;
        border-left: none;
        border-right: none;
        border-radius: 0;
      }

      .stream-item { margin-top: 18px; }

      .rail { padding: 0 22px; }
    }

    .stream-item h2 {
      font-size: 1.3rem;
      font-weight: 700;
      line-height: 1.25;
      margin: 0 0 14px;
    }

    .stream-item h2 a {
      color: var(--text);
      text-decoration: none;
    }

    .stream-item h2 a:hover { text-decoration: underline; text-underline-offset: 3px; }

    .stream-lede {
      font-style: italic;
      color: var(--muted);
    }

    .stream-more {
      font-size: 0.95rem;
      text-decoration: none;
    }

    .stream-more:hover { text-decoration: underline; text-underline-offset: 3px; }

    /* ── The essay rests at reduced strength until the first scroll ── */
    /* The children dim rather than the card, so the card stays white. */
    article > * { transition: opacity 0.6s ease; }
    article.at-rest > * { opacity: 0.72; }
    article.at-rest > figure { opacity: 0.85; }

    @media (prefers-reduced-motion: reduce) {
      article > * { transition: none; }
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



VOID_TAGS = {"br", "img", "hr", "input", "meta", "link"}


def clip_html(fragment, budget):
    """Cut a paragraph's HTML at the first sentence end past `budget` words.

    Tags are tracked so the fragment closes cleanly, and a cut is never taken
    inside a $...$ math span.
    """
    out, open_tags, words, done = [], [], 0, False
    for token in re.findall(r"<[^>]+>|[^<]+", fragment):
        if done:
            break
        if token.startswith("<"):
            out.append(token)
            name = re.match(r"</?\s*([A-Za-z0-9]+)", token)
            if name:
                tag = name.group(1).lower()
                if token.startswith("</"):
                    if tag in open_tags:
                        open_tags.remove(tag)
                elif tag not in VOID_TAGS and not token.endswith("/>"):
                    open_tags.append(tag)
            continue
        piece = ""
        for chunk in re.split(r"(\s+)", token):
            piece += chunk
            if chunk.strip():
                words += 1
            if words >= budget and re.search(r"[.?!][\"\u201d\u2019)]?\s*$", piece):
                if piece.count("$") % 2 == 0:      # never stop inside math
                    done = True
                    break
        out.append(piece)
    text = "".join(out)
    if done:
        text = text.rstrip()
        # The cut lands on a full stop, which the ellipsis replaces.
        text = (text[:-1] if text.endswith(".") else text) + "&hellip;"
    for tag in reversed(open_tags):
        text += "</%s>" % tag
    return text, done


def excerpt(essay_name, date, budget=150):
    """Title, subtitle line and roughly `budget` words of an older essay."""
    html = (ROOT / "blog" / essay_name).read_text()
    title = re.search(r"<h1>(.*?)</h1>", html).group(1)

    body = html.split("</h1>", 1)[1]
    body = re.sub(r"<figure.*?</figure>", "", body, flags=re.S)
    body = re.sub(r"<blockquote.*?</blockquote>", "", body, flags=re.S)
    # Margin notes belong to the essay page, so the excerpt drops their machinery.
    body = re.sub(r'<span class="sidenote">.*?</span>', "", body, flags=re.S)
    body = re.sub(r"<label[^>]*>.*?</label>|<input[^>]*/?>", "", body, flags=re.S)

    lede, paras, words = "", [], 0
    for tag, inner in re.findall(r"<p([^>]*)>(.*?)</p>", body, re.S):
        if any(c in tag for c in ("post-meta", "author", "pdf-notice")):
            continue
        text = inner.strip()
        if not text:
            continue
        if not paras and not lede and re.fullmatch(r"<em>.*</em>", text, re.S):
            lede = text
            continue
        clipped, stop = clip_html(text, max(0, budget - words))
        words += len(re.findall(r"\S+", re.sub(r"<[^>]+>", " ", clipped)))
        paras.append(clipped)
        if stop or words >= budget:
            break

    parts = ['    <section class="stream-item">',
             '      <h2><a href="blog/%s">%s</a>'
             '<span class="post-date">%s</span></h2>' % (essay_name, title, date)]
    if lede:
        parts.append("      <p class=\"stream-lede\">%s</p>" % lede)
    parts += ["      <p>%s</p>" % t for t in paras]
    parts.append('      <p><a class="stream-more" href="blog/%s">'
                 'Continue reading &rarr;</a></p>' % essay_name)
    parts.append("    </section>")
    return "\n".join(parts)


def build(essay_name, date=None, older=()):
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

    if older:
        stream = "\n".join(excerpt(name, when) for name, when in older)
        html = html.replace("    </article>\n",
                            '    </article>\n\n    <div class="stream">\n'
                            '      <p class="stream-label">Earlier</p>\n%s\n    </div>\n'
                            % stream, 1)

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
        build(entries[0][0], entries[0][1], older=entries[1:])
