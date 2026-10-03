#!/usr/bin/env python3
"""Build the lessons site into docs/ (what GitHub Pages serves).

    python build.py              # run the demos, copy packs and renders, write the pages
    python build.py --no-demos   # only rewrite the pages (packs and renders already built)

Needs the diep-pack skill for the demos (see demos/_common.py); the page build is standard
library only. Lesson text lives in lessons/*.md: a front matter block, Markdown, and
```scene blocks holding the step-through for the lesson's demo tank.
"""
import glob
import html
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DEMOS, LESSONS, DOCS, BUILD = (os.path.join(ROOT, d) for d in ("demos", "lessons", "docs", "build"))
LAB_RENDERS = os.path.join(ROOT, "..", "output", "renders")        # the private lab's renders, when present
SITE_TITLE = "Tank lessons"
SITE_URL = os.environ.get("SITE_URL", "https://rednebulasunshine.github.io/diep-tank-lessons/")
SKILL_URL = "https://github.com/RedNebulaSunshine/diep-pack-skill"
REPO_URL = "https://github.com/RedNebulaSunshine/diep-tank-lessons"


# --- demos ------------------------------------------------------------------------------------

def run_demos():
    env = dict(os.environ, DIEP_PACK_OUT=BUILD, PYTHONIOENCODING="utf-8")
    scripts = sorted(glob.glob(os.path.join(DEMOS, "d[0-9]*.py"))) + [os.path.join(DEMOS, "all_lessons.py")]
    for s in scripts:
        print("demo:", os.path.basename(s))
        r = subprocess.run([sys.executable, s], env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode:
            sys.exit(f"{s} failed:\n{r.stdout}\n{r.stderr}")
        for line in r.stdout.splitlines():
            if re.search(r"ERROR|WARNING|HIDDEN|NOTE", line):
                print("   ", line.strip())


def copy_outputs():
    os.makedirs(os.path.join(DOCS, "packs"), exist_ok=True)
    os.makedirs(os.path.join(DOCS, "img"), exist_ok=True)
    for f in glob.glob(os.path.join(BUILD, "*.diep-pack")):
        shutil.copy2(f, os.path.join(DOCS, "packs", os.path.basename(f)))
    for f in glob.glob(os.path.join(BUILD, "renders", "*.png")):
        shutil.copy2(f, os.path.join(DOCS, "img", os.path.basename(f)))


def fetch_seen_images(names):
    """Copy 'where we used it' renders from the lab when it is beside this repo; keep what is committed."""
    missing = []
    for n in names:
        dst = os.path.join(DOCS, "img", n)
        if os.path.exists(dst):
            continue
        src = os.path.join(LAB_RENDERS, n)
        if os.path.exists(src):
            shutil.copy2(src, dst)
        else:
            missing.append(n)
    if missing:
        print("missing images (not in docs/img and no lab renders):", ", ".join(missing))


# --- markdown ---------------------------------------------------------------------------------

def parse_front(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    meta = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        text = text[m.end():]
    return meta, text


def inline(s):
    codes = []

    def keep(m):
        codes.append(html.escape(m.group(1)))
        return f"\x00{len(codes) - 1}\x00"
    s = re.sub(r"`([^`]+)`", keep, s)
    s = html.escape(s, quote=False)
    s = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"([^\"]*)\")?\)", r'<img src="\2" alt="\1">', s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", s)
    s = re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{codes[int(m.group(1))]}</code>", s)
    return s


def md_to_html(body, scene_fn):
    out, lines, i = [], body.splitlines(), 0
    para = []

    def flush():
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            flush()
            lang = line[3:].strip()
            j = i + 1
            block = []
            while j < len(lines) and not lines[j].startswith("```"):
                block.append(lines[j])
                j += 1
            text = "\n".join(block)
            if lang == "scene":
                out.append(scene_fn(text))
            else:
                out.append(f"<pre><code>{html.escape(text)}</code></pre>")
            i = j + 1
            continue
        if line.startswith("::: "):
            flush()
            cls = line[4:].strip()
            j = i + 1
            block = []
            while j < len(lines) and lines[j].strip() != ":::":
                block.append(lines[j])
                j += 1
            figs = []
            for b in block:
                m = re.match(r"!\[([^\]]*)\]\(([^)\s]+)\)", b.strip())
                if m:
                    figs.append(f'<figure><img src="{m.group(2)}" alt="{html.escape(m.group(1))}" loading="lazy"><figcaption>{inline(m.group(1))}</figcaption></figure>')
                elif b.strip():
                    figs.append("<p>" + inline(b) + "</p>")
            out.append(f'<div class="{html.escape(cls)}">' + "".join(figs) + "</div>")
            i = j + 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)", line)
        if m:
            flush()
            n = len(m.group(1))
            out.append(f"<h{n}>{inline(m.group(2))}</h{n}>")
            i += 1
            continue
        if line.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            head, body_rows = rows[0], [r for r in rows[1:] if not all(re.match(r"^:?-+:?$", c) for c in r)]
            t = "<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"
            for r in body_rows:
                t += "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
            out.append(t + "</tbody></table>")
            continue
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)", line)
        if m:
            flush()
            ordered = m.group(2)[0].isdigit()
            tag = "ol" if ordered else "ul"
            items = []
            while i < len(lines):
                m2 = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)", lines[i])
                if m2:
                    items.append(m2.group(3))
                    i += 1
                elif lines[i].startswith("  ") and items:
                    items[-1] += " " + lines[i].strip()
                    i += 1
                else:
                    break
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>")
            continue
        if line.startswith(">"):
            flush()
            q = []
            while i < len(lines) and lines[i].startswith(">"):
                q.append(lines[i][1:].strip())
                i += 1
            out.append("<blockquote><p>" + inline(" ".join(q)) + "</p></blockquote>")
            continue
        m = re.match(r"^!\[([^\]]*)\]\(([^)\s]+)\)\s*$", line)
        if m:
            flush()
            out.append(f'<figure><img src="{m.group(2)}" alt="{html.escape(m.group(1))}" loading="lazy"><figcaption>{inline(m.group(1))}</figcaption></figure>')
            i += 1
            continue
        if not line.strip():
            flush()
        else:
            para.append(line.strip())
        i += 1
    flush()
    return "\n".join(out)


# --- pages ------------------------------------------------------------------------------------

def load_pack(slug):
    path = os.path.join(DOCS, "packs", slug + ".diep-pack")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def scene_block(text, meta):
    cfg = json.loads(text)
    slug = cfg.get("pack") or meta.get("pack")
    pack = load_pack(slug)
    name = cfg.get("tank") or meta.get("tank")
    tank = next((t for t in pack["tanks"] if t["name"] == name), None)
    if tank is None:
        sys.exit(f"{meta.get('slug')}: no tank named {name!r} in {slug}")
    cfg.update(tank=tank, packFile=slug + ".diep-pack", packName=pack.get("name"), author=pack.get("author"))
    payload = json.dumps(cfg, ensure_ascii=False).replace("</", "<\\/")
    return f'<div class="scene" data-scene><script type="application/json">{payload}</script><noscript>The interactive demo needs JavaScript.</noscript></div>'


def render_image_for(meta):
    pack = meta.get("pack")
    if not pack:
        return None
    for f in sorted(glob.glob(os.path.join(DOCS, "img", pack + "-*.png"))):
        if "-proj-" not in os.path.basename(f):
            return "img/" + os.path.basename(f)
    return None


def layout(title, description, body, image=None, path=""):
    og_image = (SITE_URL + image) if image else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title) if title == SITE_TITLE else html.escape(title) + ' · ' + SITE_TITLE}</title>
<meta name="description" content="{html.escape(description)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:type" content="article">
<meta property="og:url" content="{SITE_URL}{path}">
{f'<meta property="og:image" content="{og_image}"><meta name="twitter:card" content="summary_large_image">' if og_image else '<meta name="twitter:card" content="summary">'}
<link rel="stylesheet" href="assets/style.css">
<link rel="icon" href="img/favicon.svg" type="image/svg+xml">
</head>
<body>
<header class="site-head"><a class="brand" href="index.html">☀️ {SITE_TITLE}</a><span class="crumbs">how our diep.io tanks do what they do</span></header>
<main>
{body}
</main>
<footer>Packs and lessons by Sunshine ☀️ · built with the <a href="{SKILL_URL}">diep-pack skill</a> · <a href="{REPO_URL}">source, issues and corrections</a> · MIT. Diep.io and its editor belong to the game's publisher; this site is not affiliated with them.</footer>
<script src="assets/tank.js"></script>
<script src="assets/editor.js"></script>
</body>
</html>
"""


def build_pages():
    files = sorted(f for f in glob.glob(os.path.join(LESSONS, "*.md")) if os.path.basename(f) != "index.md")
    lessons = []
    for f in files:
        with open(f, encoding="utf-8") as fh:
            meta, body = parse_front(fh.read())
        meta.setdefault("slug", os.path.splitext(os.path.basename(f))[0])
        lessons.append((meta, body))
    seen = set()
    for meta, body in lessons:
        seen.update(re.findall(r"img/(halloween-[\w-]+\.png)", body))
    fetch_seen_images(sorted(seen))
    for k, (meta, body) in enumerate(lessons):
        prev = lessons[k - 1][0] if k > 0 else None
        nxt = lessons[k + 1][0] if k + 1 < len(lessons) else None
        content = md_to_html(body, lambda text, m=meta: scene_block(text, m))
        nav = '<div class="nav-row">'
        nav += f'<a href="{prev["slug"]}.html">‹ {html.escape(prev["title"])}</a>' if prev else '<a href="index.html">‹ All lessons</a>'
        nav += '<a href="index.html">All lessons</a>'
        nav += f'<a href="{nxt["slug"]}.html">{html.escape(nxt["title"])} ›</a>' if nxt else '<a href="index.html">Back to the start ›</a>'
        nav += "</div>"
        num = meta.get("number", meta["slug"][:2])
        page = (f'<article class="card"><div class="kv">Lesson {html.escape(num)}</div><h1>{html.escape(meta["title"])}</h1>'
                f'<p class="summary">{inline(meta.get("summary", ""))}</p>{content}</article>{nav}')
        out = layout(meta["title"], meta.get("summary", ""), page, render_image_for(meta), meta["slug"] + ".html")
        with open(os.path.join(DOCS, meta["slug"] + ".html"), "w", encoding="utf-8") as fh:
            fh.write(out)
        print("page:", meta["slug"] + ".html")
    build_index(lessons)


def build_index(lessons):
    cards = ""
    for meta, _ in lessons:
        img = render_image_for(meta)
        art = f'<img src="{img}" alt="" loading="lazy">' if img else '<div class="budget-art"><b>fires too much</b><span>121 / 120 per second</span></div>'
        cards += (f'<a class="lesson-card" href="{meta["slug"]}.html"><div class="art">{art}</div>'
                  f'<div class="num">Lesson {html.escape(meta.get("number", meta["slug"][:2]))}</div><div class="name">{html.escape(meta["title"])}</div>'
                  f'<div class="sum">{inline(meta.get("summary", ""))}</div></a>')
    with open(os.path.join(LESSONS, "index.md"), encoding="utf-8") as fh:
        meta, body = parse_front(fh.read())
    intro = md_to_html(body, lambda t: "")
    page = f'<article class="card">{intro}</article><div class="grid">{cards}</div>'
    with open(os.path.join(DOCS, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(layout(meta.get("title", SITE_TITLE), meta.get("summary", ""), page, "img/lesson-08-jaws-chomper.png", ""))
    print("page: index.html")


def write_favicon():
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="-60 -60 120 120"><rect x="-10" y="-70" width="20" height="60" fill="#999" stroke="#6e6e6e" stroke-width="6"/>'
           '<circle r="40" fill="#00B2E1" stroke="#0080a2" stroke-width="6"/></svg>')
    with open(os.path.join(DOCS, "img", "favicon.svg"), "w", encoding="utf-8") as fh:
        fh.write(svg)


if __name__ == "__main__":
    if "--no-demos" not in sys.argv:
        run_demos()
    copy_outputs()
    write_favicon()
    build_pages()
