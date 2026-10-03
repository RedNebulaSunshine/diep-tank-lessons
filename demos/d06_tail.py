"""Lesson 06: a tail that swings: a turret with a narrow arc, facing backward, under a cover."""
from _common import C, TEAM, run


def build(p):
    d = p.tank("Swisher", level=1, parents=[0])
    d.hull(0, 50)
    d.cannon(name="cannon")
    t = d.pendulum(at=(-36, 0), angle=180, arc=20, cover_color=TEAM, name="tail pivot")
    d.rod((0, 0), (130, 0), width=26, end_width=6, color=TEAM, turret=t, name="tail")
    d.shape(0, 10, at=(136, 0), color=C.charcoal, turret=t, name="tail tuft")
    return d


if __name__ == "__main__":
    run(build, "Lesson 06 Tail")
