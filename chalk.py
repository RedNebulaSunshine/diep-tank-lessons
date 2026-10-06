#!/usr/bin/env python3
"""Chalkboard diagrams for the lessons: each lesson's demo tank drawn in white chalk on a green
board, with yellow labels and arrows naming the parts that do the trick ("thrust", "pivot").

    python chalk.py            # writes docs/img/chalk/<id>.svg for every diagram below

A lesson shows one with a line of its own:  !chalk(16-engine)
build.py inlines the SVG there, floated beside the text, so the page's handwriting font applies.
The tanks are read from docs/packs/, so a diagram always matches the demo tank it labels.
Standard library only. MIT, Sunshine.
"""
import html
import json
import math
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
PACKS = os.path.join(ROOT, "docs", "packs")
OUT = os.path.join(ROOT, "docs", "img", "chalk")

BOARD, FRAME = "#2c4a3a", "#6b4a2e"
CHALK, YELLOW, PINK, BLUE = "#efeee6", "#f6e27a", "#f4a7b9", "#a8dcef"
PART_FILL, HULL_FILL = "#36584a", "#3a6670"
FONT = "Caveat, 'Segoe Print', 'Comic Sans MS', cursive"


def rot(p, a):
    c, s = math.cos(a), math.sin(a)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


def add(p, q):
    return (p[0] + q[0], p[1] + q[1])


def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def pts(ps):
    return " ".join(f"{f(x)},{f(y)}" for x, y in ps)


def poly(sides, r, star=False):
    if star:
        return [rot(((r if k % 2 else 0.4 * r), 0), k * math.pi / sides) for k in range(2 * sides)]
    start = math.pi / 4 if sides == 4 else 0
    return [rot((r, 0), start + 2 * math.pi * k / sides) for k in range(sides)]


def load(pack, tank=None, projectile=None):
    with open(os.path.join(PACKS, pack + ".diep-pack"), encoding="utf-8") as fh:
        p = json.load(fh)
    t = next(x for x in p["tanks"] if tank is None or x["name"] == tank)
    if projectile is None:
        return t
    q = next(x for x in t["projectiles"] if x["name"] == projectile)
    sides = q.get("sides", -1)
    return {"body": {"sides": sides if sides >= 3 else 0, "size": 50, "star": q.get("star", False)},
            "bodyShapes": q.get("parts", []), "barrels": q.get("barrels", []), "turrets": q.get("turrets", [])}


# --- a tank as chalk lines ----------------------------------------------------------------------

class Figure:
    """A tank (or a projectile drawn as one) placed on the board: `at` its centre in board
    units, `scale` board units per tank unit, `heading` in degrees (-90 = nose up)."""

    def __init__(self, tank, at, scale=1.0, heading=-90, hide=(), ghost=(), alpha=1.0, team=True):
        self.t, self.at, self.s, self.h = tank, at, scale, math.radians(heading)
        self.hide, self.ghost, self.alpha, self.team = set(hide), set(ghost), alpha, team
        self.geo = {}            # name -> ("poly", points) | ("circle", centre, r), in tank units
        self.overlay = []        # dashed outlines (invisible barrels, hidden turrets), drawn on top

    def P(self, p):
        return add(self.at, tuple(v * self.s for v in rot(p, self.h)))

    def anchor(self, name, where="mid"):
        """A point on a named part, in board units: mid, tip (muzzle end), base, rim, or a
        tank-frame point given as a tuple."""
        if isinstance(name, tuple):
            return self.P(name)
        g = self.geo[name]
        if g[0] == "circle":
            c, r = g[1], g[2]
            if where == "rim":
                return self.P(add(c, rot((r, 0), math.radians(-35))))
            if where == "top":
                return self.P(add(c, (r, 0)))
            return self.P(c)
        p = g[1]
        if where == "tip":
            return self.P(((p[1][0] + p[2][0]) / 2, (p[1][1] + p[2][1]) / 2))
        if where == "base":
            return self.P(((p[0][0] + p[3][0]) / 2, (p[0][1] + p[3][1]) / 2))
        if where == "rim":
            return self.P(p[0])
        return self.P((sum(x for x, _ in p) / len(p), sum(y for _, y in p) / len(p)))

    def draw(self):
        t = self.t
        bars, shapes, turs = t.get("barrels", []), t.get("bodyShapes", []), t.get("turrets", [])
        name = lambda d, k, i: (d.get("editor") or {}).get("name") or f"{k} {i}"
        out = []

        def barrel(i, origin=(0, 0), ang=0.0):
            b = bars[i]
            x0 = b.get("startDistance", 0)
            x1 = x0 + min(b.get("distance", 95), 500)
            off = b.get("offset", 0)
            hw0 = 21 * b.get("heightMultiplier", 1)
            hw1 = hw0 * b.get("muzzleScale", 1)
            a = b.get("angle", 0)
            local = [(x0, off + hw0), (x1, off + hw1), (x1, off - hw1), (x0, off - hw0)]
            ps = [add(origin, rot(rot(p, a), ang)) for p in local]
            n = name(b, "barrel", i)
            self.geo[n] = ("poly", ps)
            if n in self.hide:
                return
            mid = add(origin, rot(rot(((x0 + x1) / 2, off), a), ang))
            for j, m in enumerate(bars):
                if m.get("mount") == i and "mountTurret" not in m:
                    barrel(j, mid, ang + a)
            dashed = b.get("invisible") or n in self.ghost
            fill = "none" if dashed else (HULL_FILL if b.get("color") == 27 and self.team else PART_FILL)
            out.append(self._poly(ps, fill, dashed))

        def rides(d):
            """A part or barrel riding a body shape (mountPart; mount and mountTurret win over it)."""
            return d.get("mountPart", -1) >= 0 and "mount" not in d and "mountTurret" not in d

        def shape(s, i, origin=(0, 0), ang=0.0):
            c = add(origin, rot((s.get("xOffset", 0), s.get("yOffset", 0)), ang))
            n = name(s, "shape", i)
            size, sides = s.get("size", 25), s.get("sides", 0)
            fill = HULL_FILL if s.get("color") == 27 and self.team else PART_FILL
            col = s.get("color")
            if col == 19 or (isinstance(col, str) and col[:7].lower() == "#ffffff"):
                fill = "#7d9488"
            a = s.get("angle", 0)
            if s.get("fixedRotation"):
                a -= self.h + math.pi / 2          # a fixed part keeps its world angle, whatever the figure's heading
            own = ang + a
            riders = [(j, "b") for j, m in enumerate(bars) if rides(m) and m["mountPart"] == i]
            riders += [(j, "s") for j, r in enumerate(shapes) if rides(r) and r["mountPart"] == i]
            above = lambda j, k: (bars[j].get("flags") or {}).get("aboveBody") if k == "b" else shapes[j].get("aboveBody")
            for j, k in riders:                    # riders draw under their carrier unless aboveBody
                if not above(j, k):
                    barrel(j, c, own) if k == "b" else shape(shapes[j], j, c, own)
            if sides <= 2:
                self.geo[n] = ("circle", c, size)
                if n not in self.hide:
                    out.append(self._circle(c, size, fill, n in self.ghost))
            else:
                ps = [add(c, rot(p, own)) for p in poly(sides, size, s.get("star"))]
                self.geo[n] = ("poly", ps)
                if n not in self.hide:
                    out.append(self._poly(ps, fill, n in self.ghost))
            for j, k in riders:
                if above(j, k):
                    barrel(j, c, own) if k == "b" else shape(shapes[j], j, c, own)

        def turret(u, i):
            o, a = (u.get("xOffset", 0), u.get("yOffset", 0)), u.get("angle", 0)
            items = [(b.get("order", 0), 1, j, "b") for j, b in enumerate(bars) if b.get("mountTurret") == i]
            items += [(s.get("order", 0), 0, j, "s") for j, s in enumerate(shapes) if s.get("mountTurret") == i]
            items.sort()
            above = lambda k, j: (bars[j].get("flags") or {}).get("aboveBody") if k == "b" else shapes[j].get("aboveBody")
            for _, _, j, k in items:
                if not above(k, j):
                    barrel(j, o, a) if k == "b" else shape(shapes[j], j, o, a)
            n = name(u, "turret", i)
            r = u.get("baseSize", 25)
            self.geo[n] = ("circle", o, r)
            if n not in self.hide:
                hidden = u.get("aboveBody") is False and self.t.get("_projectile")
                out.append(self._circle(o, r, PART_FILL, n in self.ghost or hidden))
            for _, _, j, k in items:
                if above(k, j):
                    barrel(j, o, a) if k == "b" else shape(shapes[j], j, o, a)

        under, over = [], []
        for i, b in enumerate(bars):
            if "mountTurret" not in b and "mount" not in b and not rides(b):
                ((over if (b.get("flags") or {}).get("aboveBody") else under)).append((b.get("order", 0), 0, i, "b"))
        for i, s in enumerate(shapes):
            if "mountTurret" not in s and "mount" not in s and not rides(s):
                (over if s.get("aboveBody") else under).append((s.get("order", 0), 1, i, "s"))
        for i, u in enumerate(turs):
            (over if u.get("aboveBody", True) else under).append((u.get("order", 0), 2, i, "t"))
        run = {"b": lambda i: barrel(i), "s": lambda i: shape(shapes[i], i), "t": lambda i: turret(turs[i], i)}
        for *_, i, k in sorted(under):
            run[k](i)
        body = t.get("body", {})
        size, sides = body.get("size", 50), body.get("sides", 0)
        if sides <= 2:
            self.geo["body"] = ("circle", (0, 0), size)
            if "body" not in self.hide:
                out.append(self._circle((0, 0), size, HULL_FILL if self.team else PART_FILL, "body" in self.ghost))
        else:
            ps = poly(sides, size * 1.3, body.get("star"))
            self.geo["body"] = ("poly", ps)
            if "body" not in self.hide:
                out.append(self._poly(ps, HULL_FILL if self.team else PART_FILL, "body" in self.ghost))
        for *_, i, k in sorted(over):
            run[k](i)
        a = f' opacity="{f(self.alpha)}"' if self.alpha < 1 else ""
        return f'<g class="fig"{a}>' + "".join(out) + "".join(self.overlay) + "</g>"

    def _poly(self, ps, fill, dashed=False):
        if dashed:
            self.overlay.append(f'<polygon points="{pts([self.P(p) for p in ps])}" fill="none" stroke="{CHALK}" stroke-width="3" stroke-dasharray="7 6"/>')
            return ""
        return f'<polygon points="{pts([self.P(p) for p in ps])}" fill="{fill}" stroke="{CHALK}" stroke-width="3"/>'

    def _circle(self, c, r, fill, dashed=False):
        x, y = self.P(c)
        if dashed:
            self.overlay.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r * self.s)}" fill="none" stroke="{CHALK}" stroke-width="3" stroke-dasharray="7 6"/>')
            return ""
        return f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r * self.s)}" fill="{fill}" stroke="{CHALK}" stroke-width="3"/>'


# --- the board ------------------------------------------------------------------------------------

class Board:
    def __init__(self, ident, w=600, h=420, title=""):
        self.id, self.w, self.h, self.title = ident, w, h, title
        self.layers, self.figs, self.words = [], [], []

    def fig(self, tank, **kw):
        g = Figure(tank, **kw)
        g.drawn = g.draw()               # draws now, so its parts can be pointed at
        self.layers.append(g)
        return g

    def raw(self, s):
        self.layers.append(s)

    # chalk primitives, board units
    def circle(self, c, r, color=CHALK, fill="none", dash=False, width=3, opacity=1):
        d = ' stroke-dasharray="7 6"' if dash else ""
        o = f' opacity="{opacity}"' if opacity != 1 else ""
        self.raw(f'<circle cx="{f(c[0])}" cy="{f(c[1])}" r="{f(r)}" fill="{fill}" stroke="{color}" stroke-width="{width}"{d}{o}/>')

    def square(self, c, r, color=PINK, angle=15):
        ps = [add(c, rot(p, math.radians(angle))) for p in poly(4, r)]
        self.raw(f'<polygon points="{pts(ps)}" fill="#55524a" stroke="{color}" stroke-width="3"/>')

    def line(self, a, b, color=CHALK, dash=False, width=3):
        d = ' stroke-dasharray="7 6"' if dash else ""
        self.raw(f'<line x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(b[0])}" y2="{f(b[1])}" stroke="{color}" stroke-width="{width}" stroke-linecap="round"{d}/>')

    def arrow(self, a, b, color=YELLOW, bend=0.0, width=3.5, head=13, dash=False):
        """A chalk arrow from a to b, bowed sideways by `bend` (a fraction of its length)."""
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        dx, dy = b[0] - a[0], b[1] - a[1]
        c = (mx - dy * bend, my + dx * bend)
        ang = math.atan2(b[1] - c[1], b[0] - c[0])
        h1 = add(b, rot((-head, -head * 0.55), ang))
        h2 = add(b, rot((-head, head * 0.55), ang))
        d = ' stroke-dasharray="8 7"' if dash else ""
        self.raw(f'<path d="M{f(a[0])},{f(a[1])} Q{f(c[0])},{f(c[1])} {f(b[0])},{f(b[1])}" fill="none" stroke="{color}" '
                 f'stroke-width="{width}" stroke-linecap="round"{d}/>'
                 f'<path d="M{f(h1[0])},{f(h1[1])} L{f(b[0])},{f(b[1])} L{f(h2[0])},{f(h2[1])}" fill="none" '
                 f'stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')

    def arc(self, c, r, a0, a1, color=YELLOW, both=False, width=3.5, dash=False):
        """An arc arrow round c from a0 to a1 degrees (clockwise on screen when a1 > a0)."""
        n = 24
        ps = [add(c, rot((r, 0), math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]
        d = ' stroke-dasharray="8 7"' if dash else ""
        self.raw(f'<polyline points="{pts(ps)}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round"{d}/>')

        def head(p, q):
            ang = math.atan2(p[1] - q[1], p[0] - q[0])
            h1, h2 = add(p, rot((-12, -7), ang)), add(p, rot((-12, 7), ang))
            self.raw(f'<path d="M{f(h1[0])},{f(h1[1])} L{f(p[0])},{f(p[1])} L{f(h2[0])},{f(h2[1])}" fill="none" '
                     f'stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')
        head(ps[-1], ps[-3])
        if both:
            head(ps[0], ps[2])

    def text(self, xy, s, size=33, color=YELLOW, anchor="middle", weight=700):
        lines = s.split("\n")
        y0 = xy[1] - (len(lines) - 1) * size * 0.95 / 2
        spans = "".join(f'<tspan x="{f(xy[0])}" y="{f(y0 + k * size * 0.95)}">{html.escape(t)}</tspan>'
                        for k, t in enumerate(lines))
        self.words.append(f'<text filter="url(#ch-{self.id}-t)" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{color}" '
                 f'text-anchor="{anchor}" dominant-baseline="middle">{spans}</text>')
        w = max(len(t) for t in lines) * size * 0.4
        h = len(lines) * size * 0.95
        x0 = xy[0] - (w / 2 if anchor == "middle" else (w if anchor == "end" else 0))
        return (x0 - 4, xy[1] - h / 2 - 2, x0 + w + 4, xy[1] + h / 2 + 2)

    def label(self, xy, s, to, size=33, anchor="middle", bend=0.15, color=YELLOW, gap=5):
        """Text at xy with an arrow from the edge of its box to the point `to`."""
        x0, y0, x1, y1 = self.text(xy, s, size, color, anchor)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        dx, dy = to[0] - cx, to[1] - cy
        tx = (x1 - cx) / abs(dx) if dx else 1e9
        ty = (y1 - cy) / abs(dy) if dy else 1e9
        k = min(tx, ty)
        start = (cx + dx * k, cy + dy * k)
        L = math.hypot(to[0] - start[0], to[1] - start[1])
        if L < 12:
            return
        end = (to[0] - (to[0] - start[0]) / L * gap, to[1] - (to[1] - start[1]) / L * gap)
        self.arrow(start, end, color=color, bend=bend)

    def svg(self):
        p = "ch-" + self.id
        body = "".join(x.drawn if isinstance(x, Figure) else x for x in self.layers)
        smudge = "".join(f'<ellipse cx="{f(self.w * a)}" cy="{f(self.h * b)}" rx="{f(self.w * c)}" ry="{f(self.h * c * 0.6)}" '
                         f'fill="#ffffff" opacity="0.035"/>' for a, b, c in ((0.25, 0.3, 0.22), (0.75, 0.7, 0.3), (0.6, 0.15, 0.15)))
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" role="img" '
                f'aria-label="{html.escape(self.title)}" class="chalkboard">'
                f'<title>{html.escape(self.title)}</title>'
                f'<defs><filter id="{p}-c" x="-5%" y="-5%" width="110%" height="110%">'
                f'<feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="2" seed="7" result="n"/>'
                f'<feDisplacementMap in="SourceGraphic" in2="n" scale="2.6" xChannelSelector="R" yChannelSelector="G" result="d"/>'
                f'<feTurbulence type="fractalNoise" baseFrequency="1.6" numOctaves="1" seed="3" result="g"/>'
                f'<feColorMatrix in="g" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2.2 1.75" result="m"/>'
                f'<feComposite in="d" in2="m" operator="in"/></filter>'
                f'<filter id="{p}-t"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="1" seed="5" result="n"/>'
                f'<feDisplacementMap in="SourceGraphic" in2="n" scale="1.3" xChannelSelector="R" yChannelSelector="G"/></filter></defs>'
                f'<rect x="3" y="3" width="{self.w - 6}" height="{self.h - 6}" rx="10" fill="{BOARD}" stroke="{FRAME}" stroke-width="6"/>'
                f'{smudge}<g filter="url(#{p}-c)">{body}</g>{"".join(self.words)}</svg>')


# --- the diagrams ---------------------------------------------------------------------------------

def d00():
    b = Board("00-layers", 600, 400, "The plate is drawn under the body, the badge over it")
    g = b.fig(load("lesson-00-layers"), at=(300, 230), scale=1.55)
    b.label((110, 300), "plate:\nunder the body", g.anchor((-6 - 38, -38)), bend=0.1)
    b.label((495, 330), "badge:\nover the body", g.anchor("badge (over the body)"), bend=-0.15)
    b.label((480, 120), "body:\nSize 50", g.anchor("body", "rim"), bend=-0.2)
    b.label((120, 80), "cannon", g.anchor("cannon", "tip"), bend=0.1)
    b.text((300, 375), "drawn in order: under  >  body  >  over", size=28, color=CHALK)
    return b


def d01():
    b = Board("01-face", 600, 400, "A face drawn on a cover over the body; the cheeks keep the team colour")
    g = b.fig(load("lesson-01-face"), at=(300, 235), scale=1.85)
    b.label((105, 90), "eyes: circles\nover the body", g.anchor("eye left"))
    b.label((500, 80), "face cover:\nhides the body", g.anchor("face cover", "rim"), bend=-0.15)
    b.label((105, 345), "smile: 4 thin\nbarrels", g.anchor("smile 2", "mid"))
    b.label((500, 340), "cheeks: team\ncolour shows", g.anchor("cheek right (team)"), bend=-0.15)
    return b


def d02():
    b = Board("02-line-art", 600, 420, "Barrels used as pen strokes: brows, a scar, a tapered horn, a fanned tail")
    g = b.fig(load("lesson-02-line-art"), at=(300, 245), scale=1.25)
    b.label((115, 75), "horn: tip\n0.02 wide", g.anchor("horn (tip 0.02 wide)", "tip"))
    b.label((480, 70), "brow: a hair-thin\nbarrel", g.anchor("brow right", "mid"), bend=-0.15)
    b.label((450, 378), "scar: Gap -70,\nstarts behind centre", g.anchor("scar (Gap -70)", "base"), bend=0.15)
    b.label((115, 385), "fan tail:\ntip 1.1 wide", g.anchor("fan tail (tip 1.1 wide)", "tip"), bend=-0.15)
    return b


def d03():
    b = Board("03-spin-pulse", 600, 400, "A spinning gear and a lantern of two shapes turning opposite ways")
    g = b.fig(load("lesson-03-spin-and-pulse"), at=(300, 230), scale=1.3)
    gear = g.anchor("gear")
    b.arc(gear, 52, 200, 330)
    b.label((120, 90), "Spin speed:\nturns forever", (gear[0] - 20, gear[1] - 50), bend=0.15)
    lan = g.anchor("lantern front")
    b.arc(lan, 40, -70, 10, color=YELLOW)
    b.arc(lan, 40, 190, 110, color=YELLOW)
    b.label((480, 85), "two shapes spin\nopposite ways:\nit pulses", (lan[0], lan[1] - 44), bend=-0.1)
    return b


def d04():
    b = Board("04-pistons", 600, 400, "Each wing is a barrel that fires a tiny speck, so it slides back and forth")
    g = b.fig(load("lesson-04-pistons"), at=(300, 250), scale=1.1)
    tipL, baseL = g.anchor("wing left", "tip"), g.anchor("wing left", "base")
    tipR = g.anchor("wing right", "tip")
    for t in (tipL, tipR):
        b.circle((t[0] + (t[0] - 300) * 0.12, t[1] - 10), 5, CHALK, CHALK)
    ux, uy = (baseL[0] - tipL[0]), (baseL[1] - tipL[1])
    n = math.hypot(ux, uy)
    mid = ((tipL[0] + baseL[0]) / 2, (tipL[1] + baseL[1]) / 2 - 38)
    b.arrow((mid[0] - ux / n * 30, mid[1] - uy / n * 30), (mid[0] + ux / n * 40, mid[1] + uy / n * 40), bend=0)
    b.text((120, 75), "fires a tiny speck...", size=33)
    b.label((470, 75), "...and kicks back:\na flap", tipR, bend=-0.15)
    b.text((300, 380), "wings are barrels: every shot slides them back", size=28, color=CHALK)
    return b


def d05():
    b = Board("05-eyes", 600, 400, "Each eye is an auto turret that turns to the nearest enemy; the pupil rides it")
    g = b.fig(load("lesson-05-eyes"), at=(240, 250), scale=1.6)
    sq = (520, 95)
    b.square(sq, 30)
    for e in ("eye left", "eye right"):
        b.line(g.anchor(e), sq, YELLOW, dash=True, width=2)
    b.text((520, 150), "enemy", size=28, color=PINK)
    b.label((110, 75), "eye: an auto\nturret", g.anchor("eye left", "rim"))
    b.label((470, 330), "pupil: rides the turret,\nlooks where it looks", g.anchor("eye right pupil"), bend=-0.15)
    return b


def d06():
    b = Board("06-tail", 600, 420, "The tail rides a pivot that may only swing 20 degrees each way, so it lags turns")
    g = b.fig(load("lesson-06-tail"), at=(300, 150), scale=1.0)
    piv = g.anchor("tail pivot")
    tip = g.anchor("tail tuft")
    r = math.hypot(tip[0] - piv[0], tip[1] - piv[1])
    for a in (70, 110):
        b.line(piv, add(piv, rot((r + 20, 0), math.radians(a))), YELLOW, dash=True, width=2)
    b.arc(piv, r + 8, 72, 108, both=True)
    b.label((120, 330), "pivot: an auto\nturret, Arc 20", g.anchor("tail pivot cover", "rim"), bend=0.2)
    b.label((480, 365), "swings 20 each\nway, lags turns", (piv[0] + 28, piv[1] + r + 6), bend=-0.2)
    return b


def d07():
    b = Board("07-hand", 600, 400, "Hold fire and the arm swings to the cursor; let go and it drops back")
    g = b.fig(load("lesson-07-hand"), at=(250, 260), scale=1.15)
    cur = (520, 70)
    b.raw(f'<path d="M{cur[0]},{cur[1]} l0,34 l9,-9 l8,16 l7,-3 l-8,-16 l12,0 z" fill="{CHALK}" stroke="{CHALK}" stroke-width="2"/>')
    star = g.anchor("wand star")
    b.arc(g.anchor("arm pivot"), 125, 25, -40)
    b.text((520, 135), "cursor", size=28, color=CHALK)
    b.label((115, 80), "pivot: Range 0,\nfollows the cursor\nwhile you fire", g.anchor("arm pivot", "rim"))
    b.label((470, 350), "let go: back\nto rest", star, bend=-0.15)
    return b


def d08():
    b = Board("08-jaws", 600, 420, "Two cursor pivots swing the jaws shut while fire is held; bite points hurt what is between")
    g = b.fig(load("lesson-08-jaws"), at=(300, 290), scale=1.05)
    rt, lt = g.anchor("jaw right fang"), g.anchor("jaw left fang")
    b.arrow(rt, (rt[0] - 70, rt[1] - 25), bend=0.25)
    b.arrow(lt, (lt[0] + 70, lt[1] - 25), bend=-0.25)
    b.text((300, 45), "hold fire: SNAP", size=34)
    b.label((440, 390), "bite points: invisible,\nhurt what's caught", g.anchor("jaw right bite 2"), bend=-0.1)
    b.label((110, 390), "jaw pivot", g.anchor("jaw pivot left", "rim"), bend=0.1)
    return b


def d09():
    b = Board("09-limbs", 600, 400, "Each leg rides a living-limb turret: it twitches toward enemies and toward the cursor while firing")
    g = b.fig(load("lesson-09-limbs"), at=(240, 245), scale=1.45)
    sq = (530, 300)
    b.square(sq, 26)
    b.text((530, 352), "enemy", size=28, color=PINK)
    knee = g.anchor("knee 2 right")
    b.arrow((knee[0] + 22, knee[1] + 8), (sq[0] - 40, sq[1] - 4), bend=-0.2, dash=True)
    b.label((440, 45), "living limb: twitches\ntoward enemies", g.anchor("leg 1 right pivot", "rim"), bend=-0.1)
    b.label((105, 350), "and to the cursor\nwhile you fire", g.anchor("shin 2 left", "tip"), bend=0.15)
    return b


def d10():
    b = Board("10-trail", 600, 430, "An invisible dropper leaves stationary segments behind, so the body follows the path")
    g = b.fig(load("lesson-10-trail"), at=(330, 80), scale=1.0, heading=-60)
    path = [(330 - 8 * k * math.sin(k / 3.0) - 6 * k, 80 + 30 * k) for k in range(1, 12)]
    for k, p in enumerate(path):
        b.circle(p, 30 - k * 1.2, CHALK, PART_FILL, opacity=round(1 - k * 0.07, 2))
    b.raw("")
    b.layers.append(b.layers.pop(0))          # the tank over its trail
    b.label((520, 120), "dropper:\ninvisible, at\nthe back", g.anchor("trail dropper", "tip"), bend=-0.2)
    b.label((450, 330), "each piece: speed 0,\nstays where dropped", path[5], bend=-0.1)
    b.label((115, 395), "gone after\nits Lifetime", path[-1], bend=0.15)
    return b


def d11():
    b = Board("11-dash", 600, 420, "An invisible barrel facing backward fires a harmless shot; the recoil throws the tank forward")
    g = b.fig(load("lesson-11-dash"), at=(300, 215), scale=1.45)
    back = g.anchor("pounce", "mid")
    shot = g.anchor((-80, 0))
    b.circle(shot, 9, CHALK, CHALK)
    b.arrow((shot[0], shot[1] + 16), (shot[0], shot[1] + 55), color=CHALK, width=3, head=10)
    b.arrow((300, 140), (300, 32), width=6, head=18)
    b.text((410, 65), "THRUST:\nthe lunge", size=34)
    b.label((150, 330), "invisible barrel,\nAngle 180, Recoil 16", back, bend=0.2)
    b.label((470, 330), "harmless shot\nfired backward", (shot[0] + 12, shot[1]), bend=-0.15)
    return b


def d12():
    b = Board("12-hitbox", 600, 400, "A tiny body hides under a collidable shell, and the shell is what gets hit")
    g = b.fig(load("lesson-12-hitbox"), at=(300, 230), scale=1.6, hide=["shell top"])
    b.raw("")
    b.label((110, 90), "the real body:\nSize 8", g.anchor("body"), bend=0.1)
    b.label((445, 350), "shell: Collidable,\nthis is what gets hit", g.anchor("shell (collidable)", "rim"), bend=-0.15)
    b.arrow((560, 120), (g.anchor((40, 75))[0] + 18, g.anchor((40, 75))[1] - 8), color=PINK, bend=0.1)
    b.text((540, 90), "bonk", size=30, color=PINK)
    return b


def d13():
    b = Board("13-shots", 600, 400, "A projectile has its own layers: a star shape that spins, with an eye drawn on it")
    t = b.fig(load("lesson-13-shots"), at=(110, 330), scale=0.6)
    s = b.fig(load("lesson-13-shots", projectile="Spiky star"), at=(370, 190), scale=1.7)
    b.arrow((110, 255), (285, 205), bend=-0.2, dash=True)
    b.arc((370, 190), 112, -150, -60)
    b.label((140, 60), "the shot: Sides 5,\ndrawn as a star", s.anchor("body", "rim"), bend=0.1)
    b.label((520, 350), "eye: a part\non the shot", s.anchor("eye"), bend=-0.15)
    b.text((510, 70), "Spin: turns\nin flight", size=34)
    return b


def d14():
    b = Board("14-ghost", 600, 360, "Standing still the tank fades away; moving or firing brings it back")
    for k, a in enumerate((1.0, 0.45, 0.12)):
        g = b.fig(load("lesson-14-ghost"), at=(110 + 190 * k, 190), scale=0.95, alpha=a)
        if k == 2:
            last = g
    for k in range(2):
        b.arrow((175 + 190 * k, 300), (235 + 190 * k, 300), bend=0)
    b.text((300, 335), "standing still: fades", size=34)
    b.label((470, 55), "eyes: Visible while\ninvisible", last.anchor("eye right (visible while invisible)"), bend=-0.15)
    b.text((120, 50), "move or fire:\nshows again", size=34)
    return b


def d15():
    b = Board("15-budget", 600, 380, "Every shot counts one plus every part it carries, and the lobby allows 120 a second")
    b.circle((110, 150), 34, CHALK, PART_FILL)
    b.text((110, 225), "a plain shot\ncosts 1", size=34)
    b.circle((310, 150), 34, CHALK, PART_FILL)
    for a in (0, 120, 240):
        p = add((310, 150), rot((44, 0), math.radians(a - 90)))
        b.raw(f'<polygon points="{pts([add(p, q) for q in poly(5, 14, True)])}" fill="{PART_FILL}" stroke="{CHALK}" stroke-width="3"/>')
    b.text((310, 225), "carrying 3 parts\ncosts 1 + 3 = 4", size=34)
    b.text((490, 120), "120\na second", size=40)
    b.text((490, 225), "the lobby's\nlimit", size=34)
    b.text((300, 325), "Reload cap 0: every barrel at its slowest, the cheapest tank", size=28, color=CHALK)
    return b


def d16_engine():
    b = Board("16-engine", 600, 470, "The missile: a bullet whose backward engine barrel rides a hidden seeker turret")
    g = b.fig(dict(load("lesson-16-missile", "Hornet", "Seeker missile"), _projectile=True), at=(300, 150), scale=0.85)
    tip = g.anchor("engine", "tip")
    for k in range(3):
        b.circle((tip[0] + (k - 1) * 7, tip[1] + 22 + k * 22), 8 - k * 1.5, CHALK, CHALK, opacity=1 - k * 0.3)
    b.arrow((300, 92), (300, 18), width=6, head=18)
    b.text((420, 45), "THRUST", size=34)
    b.label((115, 130), "seeker turret:\nhidden under,\naims at targets", g.anchor("seeker", "rim"), bend=0.15)
    b.label((490, 250), "engine:\nAlways fire,\nRecoil 5", g.anchor("engine", "mid"), bend=-0.15)
    b.label((140, 400), "exhaust: a speck\nthat does nothing", (tip[0] - 8, tip[1] + 40), bend=0.1)
    return b


def d16_arc():
    b = Board("16-arc", 600, 440, "The seeker's 25-degree wedge is centred on the launch direction, so a target outside it is safe")
    b.fig(load("lesson-16-missile", "Hornet"), at=(300, 385), scale=0.45)
    o = (300, 350)
    b.line(o, (300, 40), CHALK, dash=True, width=2)
    for a in (-25, 25):
        b.line(o, add(o, rot((330, 0), math.radians(-90 + a))), YELLOW, dash=False, width=2.5)
    b.arc(o, 120, -115, -65, both=True)
    b.text((300, 205), "Arc 25\neach way", size=29)
    b.square((350, 110), 18)
    b.label((480, 175), "inside the wedge:\nchased", (370, 118), bend=-0.15)
    b.square((90, 130), 18)
    b.label((120, 255), "outside it:\nsafe", (95, 152), bend=0.1, color=PINK)
    b.text((300, 25), "measured from where you FIRED", size=30, color=CHALK)
    return b


def d17_warhead():
    b = Board("17-warhead", 600, 440, "A short warhead barrel fires ten bullets in a fan when the missile bursts")
    g = b.fig(dict(load("lesson-17-warhead", "Grenadier", "Exploding missile"), _projectile=True),
              at=(300, 210), scale=0.8, hide=["engine"])
    tip = g.anchor("warhead", "tip")
    for k in range(10):
        a = math.radians(-90 + (k - 4.5) * 9)
        p = add(tip, rot((70 + 18 * (k % 3), 0), a))
        b.line(add(tip, rot((22, 0), a)), add(tip, rot((58, 0), a)), YELLOW, width=2)
        b.circle(p, 6, CHALK, CHALK)
    b.label((110, 300), "warhead: Fires\nwhen it bursts", g.anchor("warhead", "mid"), bend=0.2)
    b.text((470, 45), "10 bullets,\nSpread 10", size=33)
    b.text((300, 395), "bursts on: a hit  .  time out  .  right click", size=30, color=CHALK)
    return b


def d17_fuse():
    b = Board("17-fuse", 600, 440, "The fuse turret sees only 400 ahead; a target inside sets the warhead off")
    g = b.fig(dict(load("lesson-17-warhead", "Flak", "Flak missile"), _projectile=True),
              at=(300, 340), scale=0.35, hide=["engine"])
    o = (300, 330)
    R = 260
    ps = [o] + [add(o, rot((R, 0), math.radians(-90 + a))) for a in range(-80, 81, 8)]
    b.raw(f'<polygon points="{pts(ps)}" fill="{YELLOW}" fill-opacity="0.07" stroke="{YELLOW}" stroke-width="2.5" stroke-dasharray="8 7"/>')
    sq = (390, 150)
    b.square(sq, 22)
    for k in range(8):
        a = math.radians(k * 45 + 10)
        b.line(add(sq, rot((30, 0), a)), add(sq, rot((52, 0), a)), YELLOW, width=3)
    b.text((420, 100), "BOOM", size=30, color=YELLOW)
    b.label((110, 120), "fuse: Range 400,\nArc 80", (220, 190), bend=0.1)
    b.label((480, 330), "its gun: Reload 20,\nonce per missile", g.anchor("fuse", "rim"), bend=-0.1)
    return b


def d18():
    b = Board("18-cluster", 600, 460, "Six missiles leave as one bundle; a sideways kick fans them out; each bursts")
    b.fig(load("lesson-18-cluster"), at=(300, 410), scale=0.5)
    for k in range(6):
        b.circle((288 + (k % 3) * 12, 330 - (k // 3) * 14), 7, CHALK, PART_FILL)
    b.label((115, 345), "tube: 6 at once,\nSpread 0", (290, 335), bend=0.1)
    src = (300, 285)
    ends = []
    for k in range(6):
        a = math.radians(-90 + (k - 2.5) * 22)
        e = add(src, rot((190, 0), a))
        ends.append(e)
        b.arrow(add(src, rot((25, 0), a)), add(src, rot((150, 0), a)), color=YELLOW if k in (0, 5) else CHALK, width=2.5, bend=0)
    for e in ends:
        b.circle(e, 7, CHALK, PART_FILL)
        for j in range(4):
            a = math.radians(j * 90 + 45)
            b.line(add(e, rot((11, 0), a)), add(e, rot((22, 0), a)), YELLOW, width=2)
    b.label((470, 345), "splitter: Recoil 20\nkicks it sideways", add(src, rot((110, 0), math.radians(-90 + 2.5 * 22))), bend=-0.15)
    b.text((130, 40), "hold fire!", size=34)
    b.label((470, 40), "each bursts\ninto 4", (ends[4][0] + 16, ends[4][1] - 10), bend=-0.2)
    return b


def d19():
    b = Board("19-rider", 600, 440, "Moons ride a spinning planet and go round it; guns ride a spinning plate and fire")
    g = b.fig(load("lesson-19-rider"), at=(300, 150), scale=1.0)
    planet = g.anchor("planet")
    b.arc(planet, 60, 200, 340)
    b.arc(planet, 60, 20, 160)
    b.label((110, 300), "moons: Rides on\nplanet; the planet\nspins, they orbit", g.anchor("moon 2"), bend=0.15)
    b.label((490, 320), "ring guns: ride the\nplate, turn with it,\nstill fire", g.anchor("ring gun 2", "tip"), bend=-0.15)
    b.label((440, 60), "plate: Rotation Spins", g.anchor("plate", "rim"), bend=-0.15)
    b.text((300, 415), "spin the carrier and everything riding it goes round", size=28, color=CHALK)
    return b


def d20():
    b = Board("20-fixed", 600, 420, "The tank turns 50 degrees; the fixed base and the compass needle keep their heading")
    g1 = b.fig(load("lesson-20-fixed"), at=(165, 200), scale=1.1, heading=-90)
    g2 = b.fig(load("lesson-20-fixed"), at=(445, 200), scale=1.1, heading=-40)
    b.arrow((265, 200), (335, 200), bend=0)
    b.text((300, 165), "turn", size=30)
    b.label((110, 50), "base: Rotation Fixed", g1.anchor("base (fixed)", "rim"), bend=0.1)
    b.label((480, 50), "the cannon turned...", g2.anchor("cannon", "tip"), bend=-0.1)
    b.label((455, 385), "...the base and needle\ndid not", g2.anchor("needle (fixed)"), bend=-0.1)
    return b


def d21():
    b = Board("21-colours", 600, 420, "A body in an exact hex colour; its Same-color badge still shows the team; a see-through fin")
    g = b.fig(load("lesson-21-colours"), at=(300, 200), scale=1.5)
    b.label((115, 70), "body: Custom color\n#e67828", g.anchor("body", "rim"), bend=0.15)
    b.label((470, 80), "badge: Same color as\nthe body = the TEAM\ncolour, not orange", g.anchor("badge (same color as the body)"), bend=-0.15)
    b.label((480, 350), "fin: Opacity 40 %,\nsee-through", g.anchor("fin (40 % opacity)"), bend=-0.15)
    b.label((110, 330), "studs: Fallen,\nthe new swatch", g.anchor("stud (Fallen)"), bend=0.15)
    return b


def d22():
    b = Board("22-boss", 600, 460, "A boss record wraps the tank: the same tank at Size 2.5, with its own health, brain and spawn rule")
    small = b.fig(load("lesson-22-boss"), at=(110, 130), scale=0.45)
    big = b.fig(load("lesson-22-boss"), at=(380, 250), scale=1.1)
    b.arrow((165, 150), (240, 200), bend=-0.1)
    b.text((110, 215), "the tank", size=30, color=CHALK)
    b.label((110, 320), "Size 2.5: the whole\ntank scales", big.anchor("horn 2 (collidable)", "rim"), bend=0.15)
    b.text((470, 62), "Boss: Warden\nHealth 6000\nBrain: Simple\nCharge and ram", size=28)
    sq = (540, 400)
    b.square(sq, 18)
    b.text((540, 440), "a player", size=24, color=PINK)
    b.arrow((sq[0] - 30, sq[1] - 20), big.anchor("main gun", "base"), color=PINK, bend=0.15, dash=True)
    b.label((130, 405), "Spot range 2000:\nit fights what\ncomes close", (sq[0] - 40, sq[1] - 10), bend=0.2, size=28)
    return b


DIAGRAMS = [d00, d01, d02, d03, d04, d05, d06, d07, d08, d09, d10, d11, d12, d13, d14, d15,
            d16_engine, d16_arc, d17_warhead, d17_fuse, d18, d19, d20, d21, d22]


def build_all():
    os.makedirs(OUT, exist_ok=True)
    made = []
    for fn in DIAGRAMS:
        b = fn()
        with open(os.path.join(OUT, b.id + ".svg"), "w", encoding="utf-8") as fh:
            fh.write(b.svg())
        made.append(b.id)
    return made


if __name__ == "__main__":
    print("chalk:", ", ".join(build_all()))
