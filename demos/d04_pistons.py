"""Lesson 04: parts that pump: a wing is a barrel that fires a harmless speck."""
from _common import C, run


def build(p):
    d = p.tank("Flapper", level=1, parents=[0])
    d.hull(0, 46)
    wing = d.rod((8, 18), (46, 150), width=30, end_width=14, color=C.white, name="wing")
    other = d.mirror(wing)
    d.animate(wing)
    d.animate(other, phase=0.5)
    d.cannon(length=85, name="cannon")
    return d


if __name__ == "__main__":
    run(build, "Lesson 04 Pistons")
