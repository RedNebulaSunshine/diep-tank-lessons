"""Lesson 14: a tank that fades when still, with eyes that stay visible."""
from _common import C, run


def build(p):
    d = p.tank("Haunt", level=1, parents=[0])
    d.hull(0, 50)
    d.cannon(name="cannon")
    d.stealth(reveal=450, zoom=None)
    d.shape(0, 7, at=(16, -16), color=C.yellow, above=True, stays_visible=True, name="eye left (visible while invisible)")
    d.shape(0, 7, at=(16, 16), color=C.yellow, above=True, stays_visible=True, name="eye right (visible while invisible)")
    return d


if __name__ == "__main__":
    run(build, "Lesson 14 Ghost")
