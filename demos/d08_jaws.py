"""Lesson 08: jaws that bite: two cursor pivots and invisible contact-damage barrels."""
from _common import C, run


def build(p):
    d = p.tank("Chomper", level=1, parents=[0])
    d.hull(0, 50)
    d.jaws()
    d.eye(at=(8, -30), size=13, pupil=6, look=5, name="eye left")
    d.eye(at=(8, 30), size=13, pupil=6, look=5, name="eye right")
    return d


if __name__ == "__main__":
    run(build, "Lesson 08 Jaws")
