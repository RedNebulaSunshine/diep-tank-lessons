"""Lesson 15: staying under the lobby's budget: two pumping wings and a trail, affordable because
the tank's Reload stat is capped at 0, so every barrel fires at its slowest."""
from _common import C, run


def build(p):
    d = p.tank("Thrifty", level=1, parents=[0])
    d.hull(0, 46)
    wing = d.rod((8, 18), (46, 150), width=30, end_width=14, color=C.white, name="wing")
    other = d.mirror(wing)
    d.animate(wing)
    d.animate(other, phase=0.5)
    d.trail(seconds=1.5, size=1.2, sides=6, name="trail dropper")
    d.cannon(length=85, name="cannon")
    d.set(statsMaxLevel=[7, 0, 7, 7, 7, 7, 7, 7], helpText="Reload capped at 0: the cheapest way to move")
    return d


if __name__ == "__main__":
    run(build, "Lesson 15 Budget")
