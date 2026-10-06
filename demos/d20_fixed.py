"""Lesson 20: a part that keeps its heading: a fixed-rotation base under the body and a compass
needle over it hold still in the world while the tank turns."""
from _common import C, run


def build(p):
    d = p.tank("Navigator", level=1, parents=[0])
    d.hull(0, 50)
    d.base(sides=4, size=82, color=C.charcoal, name="base (fixed)")
    d.compass(length=64, width=10, color=C.crimson, name="needle (fixed)")
    d.cannon(name="cannon")
    d.set(helpText="Turn: the square and the needle stay put")
    return d


if __name__ == "__main__":
    run(build, "Lesson 20 Fixed")
