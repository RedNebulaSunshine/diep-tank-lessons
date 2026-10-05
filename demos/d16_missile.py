"""Lesson 16: a missile that steers itself: a rear engine barrel riding an auto turret on the bullet."""
from _common import C, run


def build(p):
    d = p.tank("Hornet", level=1, parents=[0])
    d.hull(0, 50)
    missile = d.missile("Seeker missile")
    d.missile_launcher(missile=missile, name="missile tube")
    return d


if __name__ == "__main__":
    run(build, "Lesson 16 Missile")
