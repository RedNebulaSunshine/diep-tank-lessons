"""Lesson 12: hiding the hull and giving the figure a hitbox with a collidable part."""
from _common import C, run


def build(p):
    d = p.tank("Shell", level=1, parents=[0])
    d.hull(0, 8)                                                         # the body all but vanishes
    d.cannon(length=110, name="cannon")
    d.shape(8, 78, color=C.plum, collidable=True, name="shell (collidable)")
    d.shape(8, 58, color=C.pink, name="shell top")
    return d


if __name__ == "__main__":
    run(build, "Lesson 12 Hitbox")
