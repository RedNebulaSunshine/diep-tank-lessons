"""Lesson 13: shots that are pictures: parts on a projectile."""
from _common import C, run


def build(p):
    d = p.tank("Thrower", level=1, parents=[0])
    d.hull(0, 50)
    star = d.projectile("Spiky star", base="bullet", sides=5, star=True, spin=0.15,
                        parts=[d.part(0, 16, at=(0, 0), color=C.white, above=True, name="eye"),
                               d.part(0, 7, at=(6, 0), color=C.charcoal, above=True, name="pupil")])
    d.cannon(projectile=star, name="star cannon")
    return d


if __name__ == "__main__":
    run(build, "Lesson 13 Shots")
