"""Lesson 10: a body that trails behind: an invisible always-firing rear barrel dropping stationary shots."""
from _common import C, run


def build(p):
    d = p.tank("Slither", level=1, parents=[0])
    d.hull(0, 40)
    d.eye(at=(12, -18), size=12, pupil=5, look=4, name="eye left")
    d.eye(at=(12, 18), size=12, pupil=5, look=4, name="eye right")
    d.rod((40, 0), (62, 0), width=6, color=C.crimson, above=True, name="tongue")
    d.trail(seconds=2.0, size=1.4, sides=6, taper=(1.0, 0.75), name="trail dropper")
    return d


if __name__ == "__main__":
    run(build, "Lesson 10 Trail")
