"""Lesson 07: a hand that follows the cursor while you fire: a controllable turret with Range 0."""
from _common import C, TEAM, run


def build(p):
    d = p.tank("Waver", level=1, parents=[0])
    d.hull(0, 50)
    d.cannon(name="cannon")
    t = d.cursor_pivot(at=(-10, 44), angle=35, arc=70, size=8, name="arm pivot")
    d.rod((0, 0), (60, 0), width=16, color=TEAM, turret=t, name="arm")
    d.shape(0, 11, at=(64, 0), color=C.yellow, turret=t, above=True, name="hand")
    d.rod((64, 0), (146, 0), width=8, color=C.brown, turret=t, above=True, name="wand")
    d.shape(5, 14, at=(152, 0), star=True, color=C.yellow, turret=t, above=True, name="wand star")
    return d


if __name__ == "__main__":
    run(build, "Lesson 07 Hand")
