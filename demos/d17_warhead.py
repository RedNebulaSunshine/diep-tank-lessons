"""Lesson 17: a missile that bursts: a warhead barrel that fires when the missile dies, then a
proximity fuse: the same warhead as an auto gun on a second, short-range turret."""
from _common import C, run


def build(p):
    a = p.tank("Grenadier", level=1, parents=[0])
    a.hull(0, 50)
    a.set(helpText="Right click to set off your missiles")
    a.missile_launcher(missile=a.missile("Exploding missile", warhead=10), name="missile tube")

    b = p.tank("Flak", level=1, parents=[0])
    b.hull(0, 50)
    b.missile_launcher(missile=b.missile("Flak missile", warhead=10, proximity=True, right_click_burst=False),
                       name="missile tube")
    return [a, b]


if __name__ == "__main__":
    run(build, "Lesson 17 Warhead")
