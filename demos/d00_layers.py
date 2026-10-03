"""Lesson 00: how the editor draws a tank. A part under the body, a barrel, a part over the body."""
from _common import C, run


def build(p):
    d = p.tank("Layers", level=1, parents=[0])
    d.hull(0, 50)                                                        # the body: team colour
    d.shape(4, 62, at=(-6, 0), color=C.box, name="plate (under the body)")
    d.cannon(name="cannon")
    d.shape(3, 20, at=(0, 0), color=C.charcoal, above=True, name="badge (over the body)")
    return d


if __name__ == "__main__":
    run(build, "Lesson 00 Layers")
