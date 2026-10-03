"""Lesson 01: a face on the hull that keeps the team colour."""
from _common import C, TEAM, arc, run


def build(p):
    d = p.tank("Face", level=1, parents=[0])
    d.hull(0, 50)                                                        # team colour: the hitbox
    d.cannon(name="cannon")
    d.shape(0, 50, color=C.yellow, above=True, name="face cover")       # same size as the body
    d.shape(0, 10, at=(14, -17), color=C.white, above=True, name="eye left")
    d.shape(0, 10, at=(14, 17), color=C.white, above=True, name="eye right")
    d.shape(0, 4, at=(16, -17), color=C.charcoal, above=True, name="pupil left")
    d.shape(0, 4, at=(16, 17), color=C.charcoal, above=True, name="pupil right")
    d.polyline(arc((0, 0), 30, 150, 210, 5), width=5, color=C.charcoal, name="smile")
    d.shape(0, 7, at=(-4, -34), color=TEAM, above=True, name="cheek left (team)")
    d.shape(0, 7, at=(-4, 34), color=TEAM, above=True, name="cheek right (team)")
    return d


if __name__ == "__main__":
    run(build, "Lesson 01 Face")
