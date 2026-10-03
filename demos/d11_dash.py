"""Lesson 11: a dash on right click: an invisible backward barrel whose harmless shot has huge recoil."""
from _common import C, run


def build(p):
    d = p.tank("Pouncer", level=1, parents=[0])
    d.hull(0, 50)
    d.cannon(name="cannon")
    d.dash(power=16, name="pounce")
    return d


if __name__ == "__main__":
    run(build, "Lesson 11 Dash")
