"""Lesson 03: spinning parts (Spin speed) and a pulsing light (two counter-spinning stars)."""
from _common import C, run


def build(p):
    d = p.tank("Lantern", level=1, parents=[0])
    d.hull(0, 50)
    d.cannon(name="cannon")
    d.shape(8, 28, at=(-10, -78), star=True, spin=0.05, color=C.cannon, name="gear")
    d.shape(0, 9, at=(-10, -78), color=C.charcoal, name="gear hub")
    d.rod((0, 30), (0, 92), width=8, color=C.brown, name="lantern pole")
    d.pulse(at=(0, 108), size=18, name="lantern")
    return d


if __name__ == "__main__":
    run(build, "Lesson 03 Spin and pulse")
