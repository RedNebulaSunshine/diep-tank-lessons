"""Lesson 22: a boss of your own: a boss-only tank (three collidable horns, a drone spawner, a big
cannon) wrapped in a boss record with the simple brain, Charge and ram, size 2.5."""
import math

from _common import C, run


def build(p):
    d = p.tank("Warden", level=1)                                         # no parents: a boss is out of the tree
    d.hull(0, 60, color=C.fallen)                                         # the stock Fallen bosses' grey
    d.shape(3, 40, color=C.charcoal, above=True, name="crest")
    for k, a in enumerate((60, 180, 300)):
        d.shape(3, 26, at=(math.cos(math.radians(a)) * 76, math.sin(math.radians(a)) * 76), angle=a,
                color=C.fallen, collidable=True, name=f"horn {k + 1} (collidable)")
    d.spawner(angle=180, count=4, name="spawner")
    d.cannon(length=120, width=50, name="main gun")
    d.cannon(angle=120, name="side gun left")
    d.cannon(angle=-120, name="side gun right")
    p.boss(d, name="Warden", brain="simple", behaviour="charge", idle="wander", spot_range=2000,
           size=2.5, health=6000, xp=50000, ring=(0, 0.4), weight=1,
           message="The Warden wakes!", minDamageMultiplier=4)
    return d


if __name__ == "__main__":
    run(build, "Lesson 22 Boss")
