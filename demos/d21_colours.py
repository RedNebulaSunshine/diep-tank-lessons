"""Lesson 21: your own colours: a body in an exact hex colour, a Same-color part that still shows
the team, a half-transparent fin, and the Fallen swatch."""
from _common import C, run


def build(p):
    d = p.tank("Tangerine", level=1, parents=[0])
    d.hull(0, 50, color=C.rgb(230, 120, 40))                              # Custom color #e67828
    d.shape(4, 18, color=C.owner, above=True, name="badge (same color as the body)")
    d.shape(0, 11, at=(-28, -30), color=C.fallen, above=True, name="stud (Fallen)")
    d.shape(0, 11, at=(-28, 30), color=C.fallen, above=True, name="stud right (Fallen)")
    d.shape(3, 34, at=(-78, 0), angle=180, color=C.rgba(255, 255, 255, 0.4), name="fin (40 % opacity)")
    d.cannon(name="cannon")
    d.set(helpText="The badge is your team colour; the fin is see-through")
    return d


if __name__ == "__main__":
    run(build, "Lesson 21 Colours")
